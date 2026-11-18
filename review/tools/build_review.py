#!/usr/bin/env python3
"""Regenerate review tables and per-entry diffs using locally supplied English."""
import argparse
from collections import Counter
import difflib
import json
import re
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from cplib import analyze_one, parse_all
from engalign import coverage

TOOLS = Path(__file__).resolve().parent
REVERTED = {
    'BRC0334-37912M': 'Fold-flat closing row works through both layers.',
    'RHC0334-028530M': 'Fold-flat closing row works through both layers.',
    'SCC0334-009502M': 'The round picks up stitches evenly around an edge.',
}
KINDS = {
    'fenced': 'Removed Markdown fence',
    'prose_preamble': 'Removed prose preamble',
    'dropped_truncated_last_line': 'Dropped truncated last line',
    'comment_brackets': 'Balanced brackets in comments',
    'even': 'Corrected plain-round counts',
    'english': 'Checked against the English',
}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def measurements(entries, tag):
    parsed = parse_all(entries, tag)
    return {key: analyze_one(parsed[key], entry['dsl']) for key, entry in entries.items()}


def summarize(result):
    if 'error' in result:
        return {'compiles': False, 'error': result['error'][:200]}
    count_flags = sum(flag['sev'] == 'count' for flag in result['flags'])
    return {
        'compiles': True, 'rows': result['nrows'], 'rows_checked': result['checked'],
        'count_flags': count_flags, 'info_flags': len(result['flags']) - count_flags,
        'stated_ok': result['stated_ok'], 'stated_bad': result['stated_bad'],
    }


def load_english(path):
    release_files = [path / f'{split}.json' for split in ('train', 'val', 'test')]
    if all(file.is_file() for file in release_files):
        return {row['id']: row['instructions'] for file in release_files for row in read(file)
                if isinstance(row.get('id'), str) and isinstance(row.get('instructions'), str)}
    inputs = sorted(path.glob('*/input.txt'))
    if not inputs:
        raise ValueError('Supply the CrochetBench JSON splits or a directory of image-ID/input.txt files')
    return {file.parent.name: file.read_text(encoding='utf-8') for file in inputs}


def english_alignment(english, result):
    if english is None:
        return None
    if 'error' in result:
        return {'ratio': None}
    counts = coverage(english,
                      [row['made'] for row in result['rowinfo'].values()])
    if not counts or counts['english_counts'] < 5:
        return {'english_counts': counts['english_counts'] if counts else 0, 'ratio': None}
    return dict(counts, ratio=round(counts['matched_in_order'] / counts['english_counts'], 2))


def grade_entry(key, record, note):
    status = note.get('status')
    ratio = (record['english_alignment'] or {}).get('ratio')
    after = record['after']
    if not after['compiles'] or status == 'unfixable' or (ratio is not None and ratio < .3):
        return 'D'
    if after['count_flags'] and key not in REVERTED and status not in ('fixed', 'no_change'):
        return 'C'
    if ratio is not None and ratio < .6:
        return 'C'
    if ratio is not None and ratio >= .85:
        return 'A'
    if status == 'fixed' and (note.get('suggested_confidence') or 0) >= 4 and record['english_available']:
        return 'A'
    return 'B'


def original_line_count(normalized, final):
    matcher = difflib.SequenceMatcher(None, normalized.rstrip().split('\n'),
                                     final.rstrip().split('\n'), autojunk=False)
    return sum(max(i2 - i1, j2 - j1)
               for tag, i1, i2, j1, j2 in matcher.get_opcodes() if tag != 'equal')


def unified_diff(key, before, after):
    # Split on LF to preserve other characters and match git/patch line handling.
    def lines(value):
        chunks = value.split('\n')
        return [line + '\n' for line in chunks[:-1]] + ([chunks[-1]] if chunks[-1] else [])

    patch = list(difflib.unified_diff(lines(before), lines(after), f'a/{key}.cp', f'b/{key}.cp'))
    added = sum(line.startswith('+') for line in patch[2:])
    removed = sum(line.startswith('-') for line in patch[2:])
    text = ''.join(line if line.endswith('\n') else line + '\n\\ No newline at end of file\n'
                   for line in patch)
    return text, added, removed


def word_sequences(text, size=8):
    words = re.findall(r'[a-z0-9]+', text.lower())
    return {tuple(words[i:i + size]) for i in range(len(words) - size + 1)}


def diff_needs_local_generation(patch, english):
    source = word_sequences(english) if english is not None else None
    for line in patch.split('\n')[2:]:
        if not line or line[0] not in ' +-':
            continue
        candidate = word_sequences(line[1:])
        if (source is None and candidate) or (source is not None and candidate & source):
            return True
    return False


def has_source_reference(before, after):
    old_comments = set(re.findall(r'# See source .+', before))
    return any(comment not in old_comments for comment in re.findall(r'# See source .+', after))


def load_mechanical_facts(base_path):
    with TemporaryDirectory() as directory:
        normalized = Path(directory, 'normalized.json')
        mechanical = Path(directory, 'mechanical.json')
        subprocess.run([sys.executable, str(TOOLS / 'normalize.py'), str(base_path),
                        str(normalized)], check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, str(TOOLS / 'normalize2.py'), str(normalized),
                        str(mechanical)], check=True, stdout=subprocess.DEVNULL)
        return read(normalized), read(normalized.with_suffix('.json.flags')), read(mechanical.with_suffix('.json.log'))


def build(args):
    base, mechanical, even, final, notes = map(
        read, (args.before, args.mechanical, args.even, args.final, args.notes)
    )
    if any(list(stage) != list(base) for stage in (mechanical, even, final)):
        raise ValueError('Dataset image IDs or their order changed')
    english = load_english(args.english)
    normalized, normalization_flags, repair_log = load_mechanical_facts(args.before)
    before_results = measurements(base, 'review_before')
    after_results = measurements(final, 'review_after')
    entries = {}
    changes = []
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    (output / 'diffs').mkdir(exist_ok=True)
    for key, entry in base.items():
        if entry['image_id'] != key:
            raise ValueError(f'Image ID does not match its key: {key}')
        versions = [stage[key]['dsl'] for stage in (base, mechanical, even, final)]
        commits = [letter for letter, old, new in zip('abc', versions, versions[1:]) if old != new]
        kinds = []
        if 'a' in commits:
            kinds.extend(flag for flag in normalization_flags[key] if flag in KINDS)
            kinds.extend(dict.fromkeys(kind for kind, _ in repair_log.get(key, [])))
        if 'b' in commits:
            kinds.append('even')
        if 'c' in commits:
            kinds.append('english')
        note = notes.get(key, {})
        alignment = english_alignment(english.get(key), after_results[key])
        record = {
            'creator_confidence': entry['confidence'],
            'before': summarize(before_results[key]),
            'after': summarize(after_results[key]),
            'commits': commits,
            'changes': kinds,
            'code_lines_changed': original_line_count(normalized[key]['dsl'], versions[-1]),
            'english_available': alignment is not None,
            'english_alignment': alignment,
        }
        if key in REVERTED:
            record['accepted_flags'] = REVERTED[key]
        if note:
            record['review_status'] = note['status']
            record['reviewer_change_count'] = len(note.get('changes') or [])
        record['grade'] = grade_entry(key, record, note)
        source_handling = []
        if 'c' in commits and has_source_reference(versions[2], versions[3]):
            source_handling.append('DSL comment cites source')
        if note.get('source_quote_paraphrased'):
            source_handling.append('Reviewer note paraphrased')
        record['source_handling'] = source_handling
        entries[key] = record
        if versions[0] != versions[-1]:
            patch, added, removed = unified_diff(key, versions[0], versions[-1])
            local_diff = diff_needs_local_generation(patch, english.get(key))
            if local_diff:
                source_handling.append('Exact diff generated locally')
            diff_path = output / 'diffs' / f'{key}.diff'
            if not local_diff or args.include_source_matches:
                diff_path.write_bytes(patch.encode('utf-8'))
            elif diff_path.exists():
                diff_path.unlink()
            changes.append((key, record, added, removed))

    (output / 'review_report.json').write_text(
        json.dumps(entries, ensure_ascii=False, indent=1) + '\n', encoding='utf-8'
    )
    write_changes(output, changes)
    write_review(output, entries, len(changes), args.revision)


def markdown_table(headers, rows):
    def row(values):
        return '| ' + ' | '.join(map(str, values)) + ' |'
    return '\n'.join([row(headers), row(['---'] * len(headers)), *(row(r) for r in rows)])


def write_changes(output, changes):
    counts = Counter(letter for _, record, _, _ in changes for letter in record['commits'])
    summary = ', '.join(f'{letter} ({counts[letter]})' for letter in 'abc')
    def artifact_link(key, record):
        if 'Exact diff generated locally' in record['source_handling']:
            return '[Generate locally](tools/README.md#rebuild-the-review-files)'
        return f'[Diff](diffs/{key}.diff)'

    affected = sum(bool(record['source_handling']) for _, record, _, _ in changes)
    rows = ((key, ', '.join(record['commits']), ', '.join(KINDS[k] for k in record['changes']),
             f'+{added} / −{removed}', record['grade'], ', '.join(record['source_handling']) or '–',
             artifact_link(key, record)) for key, record, added, removed in changes)
    table = markdown_table(
        ('Image ID', 'Commit', 'Changes', 'Lines added / removed', 'Grade', 'Source handling', 'Diff'),
        rows,
    )
    (output / 'CHANGES.md').write_text(
        f'# Changes by pattern\n\n{len(changes)} entries changed. Entries can appear in more '
        f'than one of the three correction commits. Entry counts per commit are {summary}. '
        'Line counts compare the final DSL with the upstream DSL.\n\n'
        f'Source handling is marked for {affected} changed entries. Exact diffs that would repeat '
        'a longer source passage, or contain longer text without a paired source to check, are generated locally.\n\n'
        + table + '\n',
        encoding='utf-8',
    )


def write_review(output, entries, changed, revision):
    total = len(entries)
    english = sum(r['english_available'] for r in entries.values())
    kinds = Counter(kind for r in entries.values() for kind in r['changes'])
    statuses = Counter(r.get('review_status') for r in entries.values() if 'review_status' in r)
    nonmechanical = sum(r['code_lines_changed'] > 0 for r in entries.values())
    compile_counts = {stage: sum(r[stage]['compiles'] for r in entries.values()) for stage in ('before', 'after')}
    close_counts = {stage: sum(r[stage].get('count_flags') == 0 for r in entries.values()) for stage in ('before', 'after')}
    failed = [key for key, r in entries.items() if not r['after']['compiles']]
    reverted = ', '.join(f'`{key}`' for key in REVERTED)
    grade_counts = Counter((confidence(r), r['grade']) for r in entries.values())
    all_grades = Counter(r['grade'] for r in entries.values())
    align_counts = Counter((confidence(r), alignment_bucket(r)) for r in entries.values() if r['english_available'])
    confs = ('5', '4', '3', '2', '1', 'unrated')
    bands = ('0.85 or more', '0.60 to <0.85', '0.30 to <0.60', 'Under 0.30', 'n/a')

    results = markdown_table(('', 'Before', 'After'), [
        ('Entries that compile', f"{compile_counts['before']} of {total}", f"{compile_counts['after']} of {total}"),
        ('Entries with no round-closure or stated-count errors flagged', close_counts['before'], close_counts['after']),
    ])
    kind_table = markdown_table(('Change', 'Entries'), [(label, kinds[key]) for key, label in KINDS.items()])
    alignment_table = markdown_table(('Creator confidence', *bands),
        [(c, *(align_counts[c, i] for i in range(len(bands)))) for c in confs])
    grades_table = markdown_table(('Creator confidence', *'ABCD'),
        [(c, *(grade_counts[c, g] for g in 'ABCD')) for c in confs]
        + [('**All**', *(all_grades[g] for g in 'ABCD'))])
    per_entry = markdown_table(
        ('Image ID', 'Creator confidence', 'Grade', 'Compiles before → after', 'Flags before → after',
         'Alignment', 'Review', 'Lines changed after fence and preamble removal'),
        [(key, confidence(r), r['grade'], transition(r, 'compiles'), transition(r, 'count_flags'),
          (r['english_alignment'] or {}).get('ratio') if (r['english_alignment'] or {}).get('ratio') is not None else '–',
          r.get('review_status', 'Automatic checks only').replace('_', ' '), r['code_lines_changed'])
         for key, r in entries.items()],
    )
    failed_ids = ', '.join(f'`{key}`' for key in failed)
    text = f"""# Review of the LLM-generated CrochetPARADE dataset

We checked all {total} entries at revision `{revision}` with the CrochetPARADE parser and compared stated counts with the paired CrochetBench English where available ({english} entries). The author's confidence rating is preserved. The review grade is in `review_report.json`, keyed by image ID. It can be added as a dataset field if you want it.

## Results

{results}

{changed} entries changed in total. In {nonmechanical} entries, changes went beyond removing fences and preamble. The corrections are listed in [Changes by pattern](CHANGES.md). Only the `dsl` values changed in the dataset.

## Main findings

- Markdown fences prevented {kinds['fenced']} entries from compiling. Of those, {kinds['prose_preamble']} also began with prose and {kinds['dropped_truncated_last_line']} ended mid-line.
- The parser accepts some rounds that leave stitches unworked or work past the previous round. The round-closure check catches these cases.
- The review against the English found {statuses['unfixable']} entries whose DSL was unrelated to the paired English or was a placeholder. They received grade D. Some received mechanical repairs. The reviewer notes describe invented body shapes or pieces and comments that do not track the paired instructions. Those entries need a new conversion.
- Some entries with the highest creator confidence diverge from the paired English despite compiling. The comparison assumes the pattern with the same image ID is the relevant source.
- The paired English sometimes gives a stitch count that conflicts with the written instructions. The reviewer notes record these cases.
- Recurring conversion errors include incorrect repeats, groups worked across multiple stitches instead of in one stitch, foundation-chain ovals written as magic rings, missing duplicate pieces, invented closing gathers, collapsed plain rounds, and undefined post stitches.

## What changed

{kind_table}

Claude (an AI model) made the edits in commit c with the CrochetPARADE parser in the loop. The edits were rechecked mechanically, and a sample was read by hand. The 78 edits were made against the earlier 234-entry English set, and the grades were recomputed against the 319 entries matched in the public CrochetBench release.

The review against the English covered {sum(statuses.values())} entries. The outcome was {statuses['fixed']} fixed, {statuses['partly_fixed']} partly fixed, {statuses['no_change']} requiring no change, and {statuses['unfixable']} unrelated to the paired English or placeholders.

The {len(REVERTED)} plain-round corrections excluded after review were {reverted}. The original counts fit a fold-flat closing row or a round picked up around an edge.

## How accuracy was measured

- Compile status comes from the CrochetPARADE parser.
- The round-closure check flags unworked stitches, wraparound, and mismatches with counts stated in comments. Partial turned rows, explicit attachments, and closing gathers can be classified as informational.
- English alignment measures the share of stated stitch counts found in order among the compiled row counts. The tool reports a ratio for patterns with at least five extractable counts.

The table groups entries with paired English by creator confidence and alignment.

{alignment_table}

## Review grade

- A means strong alignment (at least 0.85) or a fix against the English with reviewer confidence of at least 4.
- B means the DSL compiles and was assigned neither a high-confidence grade nor a lower grade by the checks and the review against the English.
- C means unresolved count flags outside the reviewed exceptions or English alignment from 0.30 to below 0.60.
- D means compilation failed, the reviewer marked the entry unfixable, or alignment was below 0.30.

{grades_table}

## Limits

- Grade B alone cannot establish fidelity to the English.
- Stitch counts alone cannot establish that the pattern uses the right stitch types or includes every round and piece.
- The tools checked {total - english} entries without paired English.
- The patterns were checked computationally. They were never crocheted or rendered as part of this review.
- {len(failed)} entries still fail to compile. Their IDs are {failed_ids}.

## Files

- [Changes by pattern](CHANGES.md) links to the plain-text DSL diffs.
- [Review report](review_report.json) contains the measures and grades by image ID.
- [Reviewer notes](reviewer_notes.json) record the reasons for individual edits and remaining concerns.
- [Tool instructions](tools/README.md) show how to reproduce the review.

## Per-entry table

The line count uses the original review's convention. A replacement counts the longer side of each changed block after fences and preamble are removed.

{per_entry}
"""
    (output / 'REVIEW.md').write_text(text, encoding='utf-8')
    print(f"Compile counts: {compile_counts['before']} → {compile_counts['after']}")
    print(f"Entries with no count flags: {close_counts['before']} → {close_counts['after']}")
    print(f"Changed entries: {changed}; beyond fences and preamble: {nonmechanical}")
    print(f"Grades: {dict(sorted(all_grades.items()))}")


def confidence(record):
    value = record['creator_confidence']
    return 'unrated' if value is None else str(value)


def alignment_bucket(record):
    ratio = (record['english_alignment'] or {}).get('ratio')
    if ratio is None:
        return 4
    return sum(ratio < cutoff for cutoff in (.85, .60, .30))


def transition(record, field):
    def display(stage):
        value = record[stage].get(field, '–')
        return ('yes' if value else 'no') if isinstance(value, bool) else str(value)
    return f"{display('before')} → {display('after')}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ('before', 'mechanical', 'even', 'final', 'notes', 'english', 'output'):
        parser.add_argument(f'--{option}', type=Path, required=True)
    parser.add_argument('--include-source-matches', action='store_true',
                        help='Write local diffs that may repeat passages from the English source')
    parser.add_argument('--revision', required=True, help='Dataset revision used for --before')
    build(parser.parse_args())
