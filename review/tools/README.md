# Reproduce the dataset review

Use Node.js 18 or newer and Python 3.10 or newer. Supply these inputs locally.

- CrochetPARADE's `parse64.js` at revision `06e987b13ccfc94cfdfcebc1fe4664d37d2c6687`.
- The `train.json`, `val.json`, and `test.json` files from the [public CrochetBench release](https://huggingface.co/datasets/peiyugeorgia/CrochetBench/tree/81e4b2e25b49c67ac4170ae239ff6b7908d2f219), stored together. CrochetBench is by Peiyu Li and colleagues. The original crochet instructions are from Yarnspirations. For custom inputs, supply one plain-text file of instructions at `<image_id>/input.txt` for each available pattern.

From the dataset checkout, set `parser_source` to the path to `parse64.js`, and `english_source` to the directory of source files. Run the parser setup and dataset check there.

```sh
python3 review/tools/make_parser.py "$parser_source" review/tools/parser.mjs
python3 review/tools/report.py dsl_patterns.json /path/to/final-flags.json
```

For a single DSL pattern saved as a plain-text file, run `python3 review/tools/check.py /path/to/pattern.cp`.

## Rebuild the review files

Run the following from the dataset checkout. The first two dataset commits supply the intermediate versions used to label the changes.

```sh
base=5ee0179347d79d42b70c9a73cd74656e7db372fd
scratch=$(mktemp -d)
git rev-list --reverse "$base"..HEAD -- dsl_patterns.json > "$scratch/commits"
a=$(sed -n '1p' "$scratch/commits")
b=$(sed -n '2p' "$scratch/commits")
git show "$base:dsl_patterns.json" > "$scratch/before.json"
git show "$a:dsl_patterns.json" > "$scratch/mechanical.json"
git show "$b:dsl_patterns.json" > "$scratch/even.json"

python3 review/tools/build_review.py \
  --before "$scratch/before.json" \
  --mechanical "$scratch/mechanical.json" \
  --even "$scratch/even.json" \
  --final dsl_patterns.json \
  --notes review/reviewer_notes.json \
  --english "$english_source" \
  --revision 5ee0179 \
  --output "$scratch/review"
```

The output contains the review report, both Markdown tables, and the unified DSL diffs included in the branch. To generate the additional exact diffs marked “Generate locally” in the changes table, run the same command with `--include-source-matches`. These local diffs can contain longer passages from the source. The English files stay at the path you supply.

- `rows.mjs` runs the parser and records the attachments for each row.
- `cplib.py` checks round closure and stitch counts stated in DSL comments.
- `engalign.py` compares counts stated in the English with compiled row counts.
- `normalize.py`, `normalize2.py`, and `fix_even.py` reproduce the automatic repair passes. The review lists the plain-round changes excluded after inspection.

`make_parser.py` builds a local Node module and limits expression evaluation to arithmetic. The generated module is derived from CrochetPARADE (GPLv3) and stays local.

The [MIT license](LICENSE) covers the review tools only. Its scope excludes the dataset, the source English, and the generated parser.
