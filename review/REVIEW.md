# Review of the LLM-generated CrochetPARADE dataset

We checked all 323 entries at revision `5ee0179` with the CrochetPARADE parser and compared stated counts with the paired CrochetBench English where available (319 entries). The author's confidence rating is preserved. The review grade is in `review_report.json`, keyed by image ID. It can be added as a dataset field if you want it.

## Results

|  | Before | After |
| --- | --- | --- |
| Entries that compile | 89 of 323 | 319 of 323 |
| Entries with no round-closure or stated-count errors flagged | 40 | 250 |

277 entries changed in total. In 102 entries, changes went beyond removing fences and preamble. The corrections are listed in [Changes by pattern](CHANGES.md). Only the `dsl` values changed in the dataset.

## Main findings

- Markdown fences prevented 224 entries from compiling. Of those, 4 also began with prose and 19 ended mid-line.
- The parser accepts some rounds that leave stitches unworked or work past the previous round. The round-closure check catches these cases.
- The manual review found 48 entries whose DSL was unrelated to the paired English or was a placeholder. They received grade D. Some received mechanical repairs. The manual notes describe invented body shapes or pieces and comments that do not track the paired instructions. Those entries need a new conversion.
- Some entries with the highest creator confidence diverge from the paired English despite compiling. The comparison assumes the pattern with the same image ID is the relevant source.
- The paired English sometimes gives a stitch count that conflicts with the written instructions. The reviewer notes record these cases.
- Recurring conversion errors include incorrect repeats, groups worked across multiple stitches instead of in one stitch, foundation-chain ovals written as magic rings, missing duplicate pieces, invented closing gathers, collapsed plain rounds, and undefined post stitches.

## What changed

| Change | Entries |
| --- | --- |
| Removed Markdown fence | 224 |
| Removed prose preamble | 4 |
| Dropped truncated last line | 19 |
| Balanced brackets in comments | 4 |
| Corrected plain-round counts | 13 |
| Checked against the English | 78 |

The manual review covered 128 entries. The outcome was 63 fixed, 15 partly fixed, 2 requiring no change, and 48 unrelated to the paired English or placeholders.

The 3 plain-round corrections excluded after review were `BRC0334-37912M`, `RHC0334-028530M`, `SCC0334-009502M`. The original counts fit a fold-flat closing row or a round picked up around an edge.

## How accuracy was measured

- Compile status comes from the CrochetPARADE parser.
- The round-closure check flags unworked stitches, wraparound, and mismatches with counts stated in comments. Partial turned rows, explicit attachments, and closing gathers can be classified as informational.
- English alignment measures the share of stated stitch counts found in order among the compiled row counts. The tool reports a ratio for patterns with at least five extractable counts.

The table groups entries with paired English by creator confidence and alignment.

| Creator confidence | 0.85 or more | 0.60 to <0.85 | 0.30 to <0.60 | Under 0.30 | n/a |
| --- | --- | --- | --- | --- | --- |
| 5 | 17 | 3 | 3 | 0 | 3 |
| 4 | 17 | 2 | 0 | 0 | 3 |
| 3 | 15 | 2 | 0 | 0 | 1 |
| 2 | 10 | 1 | 1 | 0 | 0 |
| 1 | 9 | 2 | 1 | 1 | 3 |
| unrated | 15 | 73 | 83 | 28 | 26 |

## Review grade

- A means strong alignment (at least 0.85) or a fix against the English with reviewer confidence of at least 4.
- B means the DSL compiles and was assigned neither a high-confidence grade nor a lower grade by the checks and manual review.
- C means unresolved count flags outside the reviewed exceptions or English alignment from 0.30 to below 0.60.
- D means compilation failed, the reviewer marked the entry unfixable, or alignment was below 0.30.

| Creator confidence | A | B | C | D |
| --- | --- | --- | --- | --- |
| 5 | 17 | 7 | 1 | 2 |
| 4 | 18 | 5 | 0 | 0 |
| 3 | 16 | 2 | 0 | 0 |
| 2 | 9 | 1 | 2 | 0 |
| 1 | 12 | 1 | 2 | 1 |
| unrated | 15 | 83 | 61 | 68 |
| **All** | 87 | 99 | 66 | 71 |

## Limits

- Grade B alone cannot establish fidelity to the English.
- Stitch counts alone cannot establish that the pattern uses the right stitch types or includes every round and piece.
- The tools checked 4 entries without paired English.
- The patterns were checked computationally. They were never crocheted or rendered as part of this review.
- 4 entries still fail to compile. Their IDs are `BRC0534-034496M`, `RHC0334-022428M`, `RHC0334-028528M`, `RHC0502-022909M`.

## Files

- [Changes by pattern](CHANGES.md) links to the plain-text DSL diffs.
- [Review report](review_report.json) contains the measures and grades by image ID.
- [Reviewer notes](reviewer_notes.json) record the reasons for individual edits and remaining concerns.
- [Tool instructions](tools/README.md) show how to reproduce the review.

## Per-entry table

The line count uses the original review's convention. A replacement counts the longer side of each changed block after fences and preamble are removed.

| Image ID | Creator confidence | Grade | Compiles before → after | Flags before → after | Alignment | Review | Lines changed after fence and preamble removal |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ALC0234-035173M | 4 | A | yes → yes | 2 → 0 | 1.0 | Automatic checks only | 15 |
| ALC0234-035175M | 4 | A | yes → yes | 2 → 0 | 1.0 | fixed | 1 |
| ALC0334-025131M | 5 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| ALC0334-025237M | 3 | A | yes → yes | 7 → 0 | 1.0 | fixed | 7 |
| ALC0334-033866M | 4 | B | yes → yes | 0 → 0 | 0.82 | Automatic checks only | 0 |
| ALC0334-033995M | 5 | B | yes → yes | 0 → 0 | – | Automatic checks only | 0 |
| ALC0334-033997M | 5 | B | yes → yes | 0 → 0 | – | Automatic checks only | 0 |
| ALC0334-033999M | 4 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| ALC0334-034001M | 4 | B | yes → yes | 0 → 0 | – | Automatic checks only | 0 |
| BRC0234-002364M | 3 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| BRC0234-003805M | 2 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| BRC0234-005423M | 4 | A | yes → yes | 1 → 0 | 1.0 | fixed | 28 |
| BRC0234-010053M | 2 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| BRC0234-012724M | 1 | A | no → yes | – → 1 | 0.85 | fixed | 186 |
| BRC0234-012728M | 3 | A | yes → yes | 3 → 3 | 1.0 | no change | 0 |
| BRC0234-026964M | 1 | A | no → yes | – → 0 | 1.0 | fixed | 32 |
| BRC0234-029172M | 1 | A | yes → yes | 1 → 0 | 0.98 | fixed | 126 |
| BRC0234-029174M | 2 | A | yes → yes | 6 → 0 | 0.97 | fixed | 36 |
| BRC0234-030779M | 3 | A | yes → yes | 1 → 0 | 1.0 | fixed | 3 |
| BRC0234-032612M | 1 | A | yes → yes | 11 → 3 | 1.0 | fixed | 25 |
| BRC0234-032636M | 1 | A | yes → yes | 48 → 0 | – | fixed | 51 |
| BRC0234-033201M | 5 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| BRC0234-033203M | 3 | A | yes → yes | 1 → 0 | 1.0 | fixed | 1 |
| BRC0234-034461M | 2 | A | yes → yes | 3 → 0 | 0.94 | fixed | 23 |
| BRC0234-034483M | 4 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| BRC0234-036377M | 5 | A | yes → yes | 1 → 0 | 1.0 | fixed | 7 |
| BRC0234-37712M | 1 | A | yes → yes | 1 → 0 | 0.87 | fixed | 53 |
| BRC0320-000079M | 4 | B | yes → yes | 2 → 0 | 0.63 | partly fixed | 2 |
| BRC0320-000084M | 3 | A | yes → yes | 3 → 1 | 1.0 | fixed | 14 |
| BRC0320-003842M | 4 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| BRC0320-011713M | 1 | D | yes → yes | 4 → 1 | 0.0 | fixed | 26 |
| BRC0334-012696M | 4 | A | yes → yes | 0 → 0 | 0.91 | Automatic checks only | 0 |
| BRC0334-027952M | 3 | A | yes → yes | 0 → 0 | 0.96 | Automatic checks only | 0 |
| BRC0334-028479M | 4 | A | yes → yes | 6 → 0 | 1.0 | fixed | 16 |
| BRC0334-028939M | 3 | A | yes → yes | 11 → 0 | 1.0 | fixed | 90 |
| BRC0334-028941M | 5 | C | yes → yes | 0 → 0 | 0.38 | Automatic checks only | 0 |
| BRC0334-030330M | 5 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| BRC0334-030550M | 4 | A | yes → yes | 1 → 0 | 0.97 | fixed | 67 |
| BRC0334-031169M | 2 | A | yes → yes | 21 → 15 | 1.0 | fixed | 72 |
| BRC0334-031873M | 5 | A | yes → yes | 2 → 0 | 0.91 | fixed | 49 |
| BRC0334-031875M | unrated | B | no → yes | – → 0 | 0.61 | Automatic checks only | 0 |
| BRC0334-032095M | unrated | C | no → yes | – → 0 | 0.4 | Automatic checks only | 0 |
| BRC0334-032283M | 1 | B | yes → yes | 0 → 0 | 0.79 | Automatic checks only | 0 |
| BRC0334-034973M-1 | unrated | A | no → yes | – → 0 | 0.87 | Automatic checks only | 0 |
| BRC0334-035196M | 2 | A | yes → yes | 6 → 2 | 1.0 | fixed | 33 |
| BRC0334-035451M | unrated | B | no → yes | – → 0 | – | fixed | 93 |
| BRC0334-036172M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| BRC0334-036248M | unrated | D | no → yes | – → 0 | 0.13 | Automatic checks only | 0 |
| BRC0334-036684M | 3 | B | yes → yes | 0 → 0 | 0.83 | Automatic checks only | 0 |
| BRC0334-36837M | unrated | D | no → yes | – → 4 | 0.57 | unfixable | 0 |
| BRC0334-37351M | unrated | B | no → yes | – → 0 | 0.82 | Automatic checks only | 0 |
| BRC0334-37355M | 4 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| BRC0334-37359M | 1 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| BRC0334-37363M | 2 | A | yes → yes | 3 → 0 | 1.0 | fixed | 40 |
| BRC0334-37367M | 5 | A | yes → yes | 2 → 0 | 1.0 | fixed | 16 |
| BRC0334-37912M | unrated | C | no → yes | – → 2 | 0.38 | Automatic checks only | 0 |
| BRC0504-002277M | unrated | D | no → yes | – → 0 | 0.29 | Automatic checks only | 0 |
| BRC0504-025906M | unrated | B | no → yes | – → 0 | 0.83 | partly fixed | 5 |
| BRC0517-005618M | unrated | A | no → yes | – → 0 | 1.0 | Automatic checks only | 0 |
| BRC0517-005625M | unrated | D | no → yes | – → 0 | 0.27 | Automatic checks only | 0 |
| BRC0518-034918M | unrated | C | no → yes | – → 0 | 0.5 | Automatic checks only | 0 |
| BRC0518-036242M | 5 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| BRC0518-37124M | unrated | B | no → yes | – → 0 | – | fixed | 18 |
| BRC0520-002418M | 5 | A | yes → yes | 1 → 0 | 1.0 | fixed | 1 |
| BRC0520-009810M | unrated | B | no → yes | – → 0 | – | fixed | 4 |
| BRC0520-030523M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| BRC0520-032279M | unrated | C | no → yes | – → 0 | 0.49 | Automatic checks only | 2 |
| BRC0520-034507M | unrated | D | no → yes | – → 0 | 0.12 | Automatic checks only | 0 |
| BRC0520-37694M | 5 | B | no → yes | – → 0 | – | fixed | 9 |
| BRC0521-37161M | 5 | A | yes → yes | 1 → 0 | 1.0 | fixed | 2 |
| BRC0534-029092M | unrated | C | no → yes | – → 0 | 0.43 | Automatic checks only | 0 |
| BRC0534-034494M | unrated | C | no → yes | – → 0 | 0.44 | Automatic checks only | 0 |
| BRC0534-034496M | unrated | D | no → no | – → – | – | unfixable | 0 |
| BRC0534-034498M | unrated | B | no → yes | – → 0 | 0.64 | Automatic checks only | 0 |
| BRC0534-034501M | unrated | C | no → yes | – → 0 | 0.53 | Automatic checks only | 0 |
| BRC0534-034503M | unrated | D | no → yes | – → 0 | 0.07 | Automatic checks only | 0 |
| BRC0534-034505M | 4 | A | yes → yes | 14 → 6 | 1.0 | fixed | 76 |
| BRC0534-034510M | unrated | D | no → yes | – → 1 | 0.18 | unfixable | 0 |
| BRC0534-036536M | unrated | D | no → yes | – → 1 | 0.54 | unfixable | 0 |
| BRC0534-036538M | unrated | D | no → yes | – → 7 | 0.81 | unfixable | 0 |
| BRC0534-036542M | unrated | D | no → yes | – → 2 | 0.37 | unfixable | 0 |
| BRC0534-036546M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| CAC0201-033162M | unrated | C | no → yes | – → 0 | 0.5 | fixed | 3 |
| CAC0234-004177M | unrated | D | no → yes | – → 0 | 0.22 | Automatic checks only | 0 |
| CAC0234-011729M | unrated | D | no → yes | – → 0 | 0.15 | Automatic checks only | 7 |
| CAC0334-000707M | 4 | A | yes → yes | 2 → 0 | 1.0 | fixed | 3 |
| CAC0334-000734M | unrated | C | no → yes | – → 0 | 0.41 | Automatic checks only | 1 |
| CAC0334-000736M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 40 |
| CAC0334-000744M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| CAC0334-001738M | unrated | B | no → yes | – → 0 | 0.62 | Automatic checks only | 0 |
| CAC0334-004126M | unrated | D | no → yes | – → 0 | 0.21 | Automatic checks only | 0 |
| CAC0334-007667M | unrated | B | no → yes | – → 0 | 0.64 | Automatic checks only | 0 |
| CAC0334-029379M | unrated | A | no → yes | – → 0 | 0.91 | Automatic checks only | 0 |
| CAC0517-002668M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| CAC0517-004166M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| CAC0534-007294M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| PAC0334-001199M | unrated | D | no → yes | – → 0 | 0.26 | Automatic checks only | 1 |
| PAC0334-003436M | unrated | B | no → yes | – → 0 | 0.77 | Automatic checks only | 0 |
| PAC0334-005211M | unrated | C | no → yes | – → 0 | 0.59 | Automatic checks only | 0 |
| RHC0234-013945M | unrated | D | no → yes | – → 0 | 0.28 | Automatic checks only | 1 |
| RHC0234-014013M | unrated | C | no → yes | – → 0 | 0.46 | Automatic checks only | 0 |
| RHC0234-015136M | unrated | D | no → yes | – → 0 | 0.16 | Automatic checks only | 0 |
| RHC0234-019257M | unrated | C | no → yes | – → 0 | 0.42 | Automatic checks only | 0 |
| RHC0234-021038M | unrated | B | no → yes | – → 0 | 0.69 | Automatic checks only | 0 |
| RHC0234-022084M | unrated | B | no → yes | – → 0 | 0.68 | Automatic checks only | 0 |
| RHC0234-023128M | unrated | D | no → yes | – → 4 | 0.61 | unfixable | 0 |
| RHC0234-023194M | unrated | B | no → yes | – → 2 | – | fixed | 4 |
| RHC0234-024333M | unrated | D | no → yes | – → 1 | 0.33 | unfixable | 0 |
| RHC0234-026933M | unrated | D | no → yes | – → 0 | 0.21 | Automatic checks only | 0 |
| RHC0234-033232M | unrated | C | no → yes | – → 0 | 0.39 | Automatic checks only | 0 |
| RHC0234-033289M | unrated | D | no → yes | – → 0 | 0.07 | Automatic checks only | 0 |
| RHC0234-035753M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| RHC0334-013897M | unrated | C | no → yes | – → 0 | 0.38 | Automatic checks only | 0 |
| RHC0334-014011M | 2 | A | yes → yes | 1 → 0 | 0.97 | fixed | 2 |
| RHC0334-014286M | unrated | D | no → yes | – → 1 | 0.76 | unfixable | 0 |
| RHC0334-014497M | unrated | D | no → yes | – → 1 | 0.36 | unfixable | 0 |
| RHC0334-014670M | unrated | B | no → yes | – → 0 | 0.67 | Automatic checks only | 0 |
| RHC0334-014672M | unrated | C | no → yes | – → 0 | 0.52 | Automatic checks only | 0 |
| RHC0334-014674M | unrated | B | no → yes | – → 0 | 0.65 | Automatic checks only | 0 |
| RHC0334-014676M | 4 | A | yes → yes | 4 → 0 | 1.0 | fixed | 6 |
| RHC0334-015047M | unrated | B | no → yes | – → 0 | 0.6 | Automatic checks only | 0 |
| RHC0334-015988M | 5 | B | yes → yes | 0 → 0 | – | Automatic checks only | 0 |
| RHC0334-016621M | unrated | D | no → yes | – → 6 | 0.44 | unfixable | 0 |
| RHC0334-016805M | unrated | D | no → yes | – → 4 | 0.84 | unfixable | 0 |
| RHC0334-017235M | unrated | B | no → yes | – → 0 | 0.84 | Automatic checks only | 0 |
| RHC0334-017483M | unrated | C | no → yes | – → 0 | 0.44 | Automatic checks only | 16 |
| RHC0334-019017M | unrated | C | no → yes | – → 0 | 0.54 | Automatic checks only | 0 |
| RHC0334-019290M | 2 | B | yes → yes | 0 → 0 | 0.77 | Automatic checks only | 0 |
| RHC0334-019366M | unrated | D | no → yes | – → 2 | 0.83 | unfixable | 0 |
| RHC0334-019373M | unrated | A | no → yes | – → 0 | 1.0 | fixed | 130 |
| RHC0334-019387M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| RHC0334-019389M | unrated | D | no → yes | – → 2 | 0.91 | unfixable | 0 |
| RHC0334-019401M | unrated | C | no → yes | – → 0 | 0.5 | Automatic checks only | 0 |
| RHC0334-019492M | unrated | D | no → yes | – → 2 | 0.46 | unfixable | 1 |
| RHC0334-019501M | unrated | B | no → yes | – → 0 | 0.83 | Automatic checks only | 0 |
| RHC0334-019749M | unrated | B | no → yes | – → 0 | 0.65 | Automatic checks only | 0 |
| RHC0334-019827M | 2 | C | yes → yes | 18 → 8 | 0.48 | fixed | 35 |
| RHC0334-020085M | 3 | B | yes → yes | 0 → 0 | 0.75 | Automatic checks only | 0 |
| RHC0334-020243M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| RHC0334-020305M | unrated | D | no → yes | – → 16 | 0.56 | unfixable | 1 |
| RHC0334-020454M | unrated | D | no → yes | – → 3 | 0.46 | unfixable | 1 |
| RHC0334-020500M | unrated | C | no → yes | – → 0 | 0.5 | Automatic checks only | 0 |
| RHC0334-020509M | unrated | D | no → yes | – → 1 | 0.45 | unfixable | 0 |
| RHC0334-020567M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| RHC0334-021014M | unrated | A | no → yes | – → 0 | 1.0 | Automatic checks only | 0 |
| RHC0334-021108M | unrated | B | no → yes | – → 0 | 0.67 | Automatic checks only | 0 |
| RHC0334-021112M | unrated | C | no → yes | – → 0 | 0.58 | Automatic checks only | 0 |
| RHC0334-021389M | unrated | B | no → yes | – → 0 | – | fixed | 3 |
| RHC0334-021393M | unrated | D | no → yes | – → 0 | 0.24 | Automatic checks only | 0 |
| RHC0334-021395M | unrated | B | no → yes | – → 0 | 0.67 | Automatic checks only | 0 |
| RHC0334-021564M | unrated | B | no → yes | – → 0 | 0.72 | Automatic checks only | 0 |
| RHC0334-021640M | unrated | B | no → yes | – → 0 | 0.71 | Automatic checks only | 0 |
| RHC0334-022072M | unrated | B | no → yes | – → 0 | 0.81 | Automatic checks only | 0 |
| RHC0334-022185M | unrated | D | no → yes | – → 8 | 0.41 | unfixable | 1 |
| RHC0334-022187M | unrated | D | no → yes | – → 6 | 0.47 | unfixable | 20 |
| RHC0334-022189M | unrated | C | no → yes | – → 0 | 0.52 | fixed | 2 |
| RHC0334-022285M | unrated | B | no → yes | – → 0 | 0.65 | Automatic checks only | 0 |
| RHC0334-022428M | unrated | D | no → no | – → – | – | unfixable | 1 |
| RHC0334-022512M | unrated | D | no → yes | – → 5 | 0.53 | unfixable | 0 |
| RHC0334-022743M | unrated | B | no → yes | – → 0 | 0.63 | Automatic checks only | 0 |
| RHC0334-023118M | unrated | D | no → yes | – → 5 | 0.4 | unfixable | 0 |
| RHC0334-023355M | unrated | C | no → yes | – → 0 | 0.5 | Automatic checks only | 0 |
| RHC0334-023577M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| RHC0334-023991M | unrated | B | no → yes | – → 0 | 0.83 | Automatic checks only | 0 |
| RHC0334-023995M | unrated | C | no → yes | – → 0 | 0.52 | Automatic checks only | 0 |
| RHC0334-023999M | unrated | B | no → yes | – → 0 | 0.61 | Automatic checks only | 0 |
| RHC0334-024001M | unrated | C | no → yes | – → 0 | 0.36 | Automatic checks only | 0 |
| RHC0334-024005M | 5 | A | yes → yes | 1 → 1 | 1.0 | no change | 0 |
| RHC0334-024009M | unrated | D | no → yes | – → 4 | 0.66 | unfixable | 0 |
| RHC0334-024011M | unrated | C | no → yes | – → 0 | 0.36 | Automatic checks only | 0 |
| RHC0334-024013M | unrated | C | no → yes | – → 0 | 0.54 | Automatic checks only | 0 |
| RHC0334-024017M | unrated | B | no → yes | – → 0 | 0.82 | Automatic checks only | 0 |
| RHC0334-024019M | unrated | B | no → yes | – → 0 | 0.61 | Automatic checks only | 0 |
| RHC0334-024031M | unrated | D | no → yes | – → 1 | 0.59 | unfixable | 0 |
| RHC0334-024172M | unrated | B | no → yes | – → 0 | 0.68 | fixed | 3 |
| RHC0334-025632M | unrated | C | no → yes | – → 0 | 0.33 | Automatic checks only | 0 |
| RHC0334-025728M | unrated | B | no → yes | – → 0 | 0.75 | Automatic checks only | 0 |
| RHC0334-025731M | unrated | D | no → yes | – → 0 | 0.28 | Automatic checks only | 0 |
| RHC0334-025735M | unrated | B | no → yes | – → 0 | 0.61 | Automatic checks only | 0 |
| RHC0334-025742M | 1 | A | yes → yes | 1 → 0 | 1.0 | fixed | 76 |
| RHC0334-027897M | unrated | D | no → yes | – → 1 | 0.71 | unfixable | 0 |
| RHC0334-027899M | unrated | C | no → yes | – → 0 | 0.38 | Automatic checks only | 0 |
| RHC0334-027901M | unrated | C | no → yes | – → 0 | 0.57 | Automatic checks only | 0 |
| RHC0334-028528M | unrated | D | no → no | – → – | – | unfixable | 0 |
| RHC0334-028530M | unrated | A | no → yes | – → 2 | 0.86 | Automatic checks only | 0 |
| RHC0334-028534M | unrated | B | no → yes | – → 0 | 0.67 | Automatic checks only | 0 |
| RHC0334-028538M | 4 | B | yes → yes | 0 → 0 | – | Automatic checks only | 0 |
| RHC0334-028542M | unrated | B | no → yes | – → 0 | 0.73 | Automatic checks only | 0 |
| RHC0334-028550M | unrated | A | no → yes | – → 0 | 0.95 | Automatic checks only | 0 |
| RHC0334-028552M | unrated | B | no → yes | – → 0 | 0.75 | Automatic checks only | 0 |
| RHC0334-030089M | unrated | C | no → yes | – → 0 | 0.44 | Automatic checks only | 0 |
| RHC0334-030695M | unrated | B | no → yes | – → 0 | 0.79 | Automatic checks only | 0 |
| RHC0334-030781M | unrated | D | no → yes | – → 1 | 0.64 | unfixable | 0 |
| RHC0334-030783M | unrated | B | no → yes | – → 0 | 0.64 | Automatic checks only | 0 |
| RHC0334-030785M | unrated | D | no → yes | – → 5 | 0.63 | unfixable | 0 |
| RHC0334-030787M | unrated | D | no → yes | – → 3 | 0.45 | unfixable | 0 |
| RHC0334-030789M | unrated | D | yes → yes | 0 → 0 | 0.25 | Automatic checks only | 0 |
| RHC0334-030791M | unrated | D | no → yes | – → 3 | 0.41 | unfixable | 0 |
| RHC0334-030793M | unrated | C | no → yes | – → 0 | 0.59 | Automatic checks only | 0 |
| RHC0334-030795M | unrated | D | no → yes | – → 1 | 0.5 | unfixable | 0 |
| RHC0334-031165M | unrated | C | no → yes | – → 0 | 0.4 | Automatic checks only | 0 |
| RHC0334-031379M | unrated | B | yes → yes | 0 → 0 | 0.68 | Automatic checks only | 0 |
| RHC0334-031915M | unrated | D | no → yes | – → 6 | 0.83 | unfixable | 9 |
| RHC0334-033775M | 5 | A | yes → yes | 0 → 0 | 0.91 | Automatic checks only | 0 |
| RHC0334-033777M | 5 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| RHC0334-033779M | 5 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| RHC0334-033900M | unrated | C | no → yes | – → 0 | 0.33 | Automatic checks only | 0 |
| RHC0334-033984M | unrated | C | no → yes | – → 0 | 0.41 | Automatic checks only | 0 |
| RHC0334-034104M | unrated | B | no → yes | – → 0 | 0.63 | Automatic checks only | 1 |
| RHC0334-034277M | unrated | B | no → yes | – → 0 | 0.67 | Automatic checks only | 0 |
| RHC0334-034287M | unrated | A | no → yes | – → 0 | 1.0 | Automatic checks only | 0 |
| RHC0334-035534M | unrated | A | no → yes | – → 0 | 1.0 | Automatic checks only | 0 |
| RHC0334-036744M | unrated | A | no → yes | – → 0 | 0.9 | Automatic checks only | 0 |
| RHC0334-37335M | unrated | C | no → yes | – → 0 | 0.5 | Automatic checks only | 0 |
| RHC0334-37340M | 5 | B | yes → yes | 0 → 0 | 0.65 | Automatic checks only | 0 |
| RHC0334-37342M | 5 | B | yes → yes | 0 → 0 | 0.65 | Automatic checks only | 0 |
| RHC0334-37344M | unrated | C | no → yes | – → 0 | 0.58 | Automatic checks only | 0 |
| RHC0502-022909M | unrated | D | no → no | – → – | – | unfixable | 0 |
| RHC0517-025657M | unrated | C | no → yes | – → 0 | 0.46 | partly fixed | 1 |
| RHC0517-025661M | unrated | D | no → yes | – → 0 | 0.26 | Automatic checks only | 0 |
| RHC0517-025669M | unrated | A | no → yes | – → 0 | 0.79 | fixed | 1 |
| RHC0517-025739M | unrated | C | no → yes | – → 0 | 0.33 | Automatic checks only | 0 |
| RHC0517-027380M | unrated | B | no → yes | – → 0 | 0.65 | Automatic checks only | 0 |
| RHC0517-033715M | 1 | C | yes → yes | 49 → 44 | 0.75 | partly fixed | 7 |
| RHC0518-014126M | unrated | C | no → yes | – → 0 | 0.55 | Automatic checks only | 1 |
| RHC0518-014158M | unrated | C | no → yes | – → 0 | 0.35 | Automatic checks only | 0 |
| RHC0518-014404M | unrated | B | no → yes | – → 0 | 0.82 | Automatic checks only | 0 |
| RHC0518-014834M | unrated | C | no → yes | – → 0 | 0.43 | partly fixed | 2 |
| RHC0518-015128M | unrated | B | no → yes | – → 0 | 0.71 | Automatic checks only | 0 |
| RHC0518-015435M | unrated | C | no → yes | – → 0 | 0.57 | partly fixed | 5 |
| RHC0518-016290M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| RHC0518-016367M | 5 | A | yes → yes | 1 → 0 | 1.0 | fixed | 3 |
| RHC0518-016373M | unrated | B | no → yes | – → 0 | 0.6 | fixed | 4 |
| RHC0518-016375M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| RHC0518-016379M | unrated | C | no → yes | – → 0 | 0.57 | Automatic checks only | 0 |
| RHC0518-016428M | unrated | C | no → yes | – → 0 | 0.56 | Automatic checks only | 0 |
| RHC0518-016430M | unrated | C | no → yes | – → 0 | 0.5 | Automatic checks only | 0 |
| RHC0518-016432M | unrated | A | no → yes | – → 0 | 0.9 | Automatic checks only | 0 |
| RHC0518-016434M | unrated | D | no → yes | – → 0 | 0.14 | fixed | 6 |
| RHC0518-016436M | unrated | A | no → yes | – → 0 | 0.86 | Automatic checks only | 0 |
| RHC0518-017144M | unrated | B | no → yes | – → 0 | 0.62 | Automatic checks only | 0 |
| RHC0518-017146M | unrated | C | no → yes | – → 0 | 0.58 | Automatic checks only | 0 |
| RHC0518-017148M | unrated | B | no → yes | – → 0 | 0.67 | Automatic checks only | 0 |
| RHC0518-018060M | unrated | C | no → yes | – → 0 | 0.56 | Automatic checks only | 0 |
| RHC0518-018062M | unrated | C | no → yes | – → 0 | 0.57 | Automatic checks only | 0 |
| RHC0518-018204M | unrated | C | no → yes | – → 2 | 0.38 | fixed | 7 |
| RHC0518-019359M | unrated | C | no → yes | – → 0 | 0.43 | Automatic checks only | 0 |
| RHC0518-020159M | unrated | B | no → yes | – → 0 | 0.73 | Automatic checks only | 0 |
| RHC0518-020161M | unrated | B | no → yes | – → 0 | 0.68 | Automatic checks only | 0 |
| RHC0518-020163M | unrated | B | no → yes | – → 0 | 0.72 | fixed | 2 |
| RHC0518-020165M | unrated | B | no → yes | – → 0 | 0.76 | Automatic checks only | 1 |
| RHC0518-020167M | unrated | B | no → yes | – → 0 | 0.62 | Automatic checks only | 0 |
| RHC0518-021114M | unrated | C | no → yes | – → 1 | 0.7 | partly fixed | 3 |
| RHC0518-021145M | unrated | B | no → yes | – → 0 | 0.62 | Automatic checks only | 0 |
| RHC0518-021253M | unrated | C | no → yes | – → 2 | 0.67 | partly fixed | 17 |
| RHC0518-022216M | unrated | C | no → yes | – → 0 | 0.3 | Automatic checks only | 0 |
| RHC0518-022279M | unrated | C | no → yes | – → 0 | 0.54 | Automatic checks only | 0 |
| RHC0518-022283M | 5 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| RHC0518-022293M | unrated | B | no → yes | – → 0 | – | partly fixed | 2 |
| RHC0518-022295M | unrated | C | no → yes | – → 0 | 0.57 | Automatic checks only | 0 |
| RHC0518-023168M | unrated | B | no → yes | – → 0 | 0.71 | Automatic checks only | 0 |
| RHC0518-023170M | unrated | B | no → yes | – → 0 | 0.76 | Automatic checks only | 0 |
| RHC0518-023172M | unrated | B | no → yes | – → 0 | 0.68 | Automatic checks only | 0 |
| RHC0518-023198M | unrated | C | no → yes | – → 0 | 0.44 | Automatic checks only | 0 |
| RHC0518-023208M | unrated | B | no → yes | – → 0 | 0.73 | partly fixed | 2 |
| RHC0518-023210M | unrated | B | no → yes | – → 0 | 0.75 | Automatic checks only | 0 |
| RHC0518-023212M | unrated | C | no → yes | – → 0 | 0.42 | partly fixed | 15 |
| RHC0518-023214M | 1 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| RHC0534-016443M | unrated | B | no → yes | – → 0 | 0.66 | Automatic checks only | 0 |
| RHC0534-018113M | unrated | B | no → yes | – → 0 | 0.69 | Automatic checks only | 0 |
| RHC0534-023989M | unrated | A | no → yes | – → 0 | 0.88 | fixed | 3 |
| RHC0534-029042M | unrated | D | no → yes | – → 2 | 0.27 | unfixable | 0 |
| RHC0534-38073M | unrated | B | no → yes | – → 0 | 0.69 | Automatic checks only | 0 |
| RHC0534-38076M | unrated | A | no → yes | – → 0 | 0.94 | fixed | 103 |
| RHC0552-37268M | unrated | B | no → yes | – → 0 | 0.6 | Automatic checks only | 0 |
| RHC0552-37717M | unrated | C | no → yes | – → 0 | 0.43 | partly fixed | 4 |
| RHC0552-37719M | unrated | C | no → yes | – → 0 | 0.33 | Automatic checks only | 0 |
| RHC0552-37721M | unrated | D | no → yes | – → 0 | 0.29 | Automatic checks only | 0 |
| RHC0552-37723M | unrated | B | no → yes | – → 0 | – | fixed | 1 |
| RHC0552-37725M | unrated | D | no → yes | – → 0 | 0.29 | Automatic checks only | 0 |
| SCC0103-033263M | 5 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| SCC0117-005401M | 5 | A | yes → yes | 1 → 1 | 1.0 | fixed | 3 |
| SCC0234-005405M | unrated | C | no → yes | – → 0 | 0.43 | Automatic checks only | 0 |
| SCC0234-005411M | unrated | B | no → yes | – → 0 | 0.75 | Automatic checks only | 0 |
| SCC0234-005435M | unrated | D | no → yes | – → 2 | 0.64 | unfixable | 0 |
| SCC0234-005485M | unrated | D | no → yes | – → 4 | 0.38 | unfixable | 0 |
| SCC0234-005766M | unrated | D | no → yes | – → 6 | 0.33 | unfixable | 1 |
| SCC0234-033255M | 3 | A | yes → yes | 1 → 0 | 0.92 | fixed | 18 |
| SCC0334-003573M | 4 | B | yes → yes | 0 → 0 | – | Automatic checks only | 0 |
| SCC0334-003582M | 5 | D | yes → yes | 4 → 4 | 0.38 | unfixable | 0 |
| SCC0334-003586M | 5 | D | yes → yes | 4 → 4 | 0.44 | unfixable | 0 |
| SCC0334-003615M | unrated | D | no → yes | – → 0 | 0.12 | Automatic checks only | 0 |
| SCC0334-003625M | unrated | D | no → yes | – → 0 | 0.12 | Automatic checks only | 0 |
| SCC0334-003631M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| SCC0334-003652M | unrated | B | no → yes | – → 0 | – | Automatic checks only | 0 |
| SCC0334-003656M | 4 | A | yes → yes | 1 → 0 | – | fixed | 7 |
| SCC0334-003679M | 1 | A | no → yes | – → 0 | – | fixed | 27 |
| SCC0334-004365M | 1 | A | no → yes | – → 0 | – | fixed | 65 |
| SCC0334-004372M | 3 | A | yes → yes | 1 → 0 | – | fixed | 8 |
| SCC0334-004378M | unrated | C | no → yes | – → 0 | 0.41 | Automatic checks only | 0 |
| SCC0334-004442M | 3 | A | yes → yes | 0 → 0 | 0.86 | Automatic checks only | 0 |
| SCC0334-004467M | unrated | D | no → yes | – → 4 | 0.26 | unfixable | 1 |
| SCC0334-004469M | unrated | D | no → yes | – → 2 | 0.27 | unfixable | 2 |
| SCC0334-004471M | unrated | D | no → yes | – → 4 | 0.32 | unfixable | 1 |
| SCC0334-004473M | unrated | D | no → yes | – → 2 | 0.29 | unfixable | 0 |
| SCC0334-005462M | unrated | D | no → yes | – → 8 | 0.35 | unfixable | 16 |
| SCC0334-005471M | unrated | D | no → yes | – → 2 | 0.45 | unfixable | 0 |
| SCC0334-005483M | 3 | A | yes → yes | 2 → 0 | 0.95 | fixed | 158 |
| SCC0334-005570M | unrated | D | no → yes | – → 2 | 0.19 | unfixable | 0 |
| SCC0334-005572M | unrated | D | no → yes | – → 2 | 0.35 | unfixable | 0 |
| SCC0334-006891M | 4 | A | yes → yes | 3 → 1 | 1.0 | fixed | 4 |
| SCC0334-009380M | 2 | C | no → yes | – → 1 | 0.95 | partly fixed | 56 |
| SCC0334-009502M | 4 | A | yes → yes | 2 → 2 | 1.0 | Automatic checks only | 0 |
| SCC0334-026025M | 2 | A | no → yes | – → 1 | 1.0 | fixed | 44 |
| SCC0334-026037M | 3 | A | yes → yes | 8 → 2 | 1.0 | fixed | 44 |
| SCC0334-030366M | 5 | B | yes → yes | 0 → 0 | 0.71 | Automatic checks only | 0 |
| SCC0334-036678M | 3 | A | no → yes | – → 1 | 1.0 | fixed | 100 |
| SCC0501-002123M | 3 | A | yes → yes | 6 → 0 | 1.0 | fixed | 6 |
| SCC0518-005324M | 1 | A | yes → yes | 8 → 0 | 1.0 | partly fixed | 21 |
| SCC0534-005399M | 4 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| SCC0534-007746M | 3 | A | yes → yes | 0 → 0 | 1.0 | Automatic checks only | 0 |
| SCC0534-035767M | 1 | C | yes → yes | 18 → 1 | 0.38 | partly fixed | 122 |
| SCC0537-004479M | 4 | A | no → yes | – → 0 | 1.0 | Automatic checks only | 1 |
