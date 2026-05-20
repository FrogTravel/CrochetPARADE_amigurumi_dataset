# WIP amigutumi dataset written with CrochetPARADE
Every item can have confidence level 1 - Low, 5 - High. Every item that has high confidence level was prooved manually by me and fixed if necessary. If there is no confidence level - the item is generated through few-shot + RAG example, and is not yet checked. If the item has low confidence level, there are major problems with the code. For example: 
- One of the components (arm, leg, head...) is missing in the code
- It is a word (code) salad
- It looks nothing like the goal item


I am building an English → DSL system for CrochetPARADE, and the first step of course is the dataset.

There is no dataset that pairs natural language instructions with DSL code. From a set of 5000 crochet instructions written in English I took ~300 amigurumi patterns and manually wrote DSL for a few of them, then built a few-shot prompt for Claude Opus to generate the rest. It works well when the new pattern is similar enough to what is in the prompt, but falls apart on anything outside that distribution.

So naturally I tried to add a RAG layer. But naive similarity-based retrieval alone doesn't do a good job here, because it retrieves whole patterns by overall similarity. If I am generating DSL for a bear, it pulls other DSL for bears. But if the bear has a crown, the retrieved examples have nothing useful about crowns, and the model fails on that part.

So I combined both: my original hand-picked few-shot prompt as a stable base, plus a few RAG-retrieved examples on top for whatever the target pattern looks like.

With this I generated the remaining 240 amigurumi patterns. It cost $60, but saved an enormous amount of time on dataset creation.

The problem is that I still have to traverse and fix every DSL file manually. The code compiles, but a lot of translations are imprecise. To handle this, every item in the dataset has a confidence level from 1 to 5, where 1 is "Low" and 5 is "High". This way I can use the high-confidence items immediately and fix the rest gradually in the background. The high-confidence items are the ones I have already checked and that are very close to the English instruction input.

The best results overall come from passing a full few-shot prompt alongside a small portion of a new pattern, like only an arm instruction or only a leg instruction. Opus generates highly reliable output this way, but the cost of generating the full dataset would inflate proportionally.

My next step is to reorganize the dataset into component-level smaller English → DSL examples, since smaller and more focused prompts tend to give more reliable results, and to downgrade from Claude Opus to something smaller and cheaper — for me as a solo developer, generating a dataset with Opus is prohibitively expensive. The ultimate goal of the project is a system that generates CrochetPARADE DSL from a natural-language prompt, not from a full crochet instruction.

I am quite new to this area, so please share your thoughts and ideas!
