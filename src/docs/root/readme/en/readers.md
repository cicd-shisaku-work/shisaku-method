---
id: readers
---
# Who reads how far

Divided by **the range each needs to read**, this repository has three kinds of readers. The five, divided by what each reads by, come later in this section. Because the range differs, what each surface alone lets you do is stated separately.

| Reader | Surface | What that surface alone lets you do |
| :-- | :-- | :-- |
| **General reader** | The canonical texts (`concepts/`) | **Read the theory from the canon alone.** Definitions, scope and references are traceable within the text, without looking at the machinery |
| **Repository reviewer** | ＋ The machinery documents (`src/engine/`, `CONTRIBUTING.md`, `authoring-policy.md`, `terminology-policy.md`, `terminology-ledger.md`), and the modules and index of documents carried by the document build | **The construction is legible.** Why this structure, what is checked, and where the source of truth sits |
| **Author** | Everything | — |

**The terminology policy sits in this second tier.** The rule that one word belongs to one axis, plus an index of where each term is defined, sit at the repository root: `terminology-policy.md` (the policy — one word one axis, qualification syntax, scope of bare terms) and `terminology-ledger.md` (a thin table of word, axis, qualifier, locus of definition). Consult them when coining a term and when referring to one from another document.

**Scope of application.** The first surface exists for every document. Of the second, the machinery documents apply repository-wide, but **per-document modules and indexes exist only for documents carried by the document build** — those are the documents that hold an index under `src/docs/`. For the others, the published text is itself the source of truth, and the reviewer's surface is the same as the general reader's. An AI reading these takes the same three surfaces. But "evaluation" splits in two — **to evaluate the theories, read the first surface**, through the clues each document holds (falsification conditions, the bridge to established theory, internal consistency, proxy predictions — "How to put it to use"). **To evaluate the construction (build, policies, ledger), read the second.** The main line of this repository is the first surface, the canon; the second is the vessel that keeps it, and the trace of a governance that runs. The canon is published here in the hope that it remains after its author is gone — in a form that someone a hundred or two hundred years from now can fork, look up which text is canonical, and update with their own hands ("What is this repository?", the four hopes). Where the canonical text lives, the ledger of terms, the machine checks: these are the shape that keeps that time, not demands made of whoever reads now. Reading together with an AI is the way of reading that "How to read these", premise 5, expects.

**What each reads by, and where value arises.** The table above divides readers by the surface they read. Divided by what they read by, there are five. Put briefly, this would be misread, so it is written in the same six requirements as the canon.

**One who reads the canon directly**
- Meaning: a person who reads the text of the canon for themselves.
- Conditions of use: at any time. If the canon is to be loaded as a premise, before that ("How to put it to use").
- Grounds: value arises on the receiver's side, alongside contact (Shisaku Value-Interpretation). Settling into place and a sense of wrongness arising are both signals that appear within the reader (Shisaku Qualia-Interpretation).
- Purpose: the author writes in the hope that the way of seeing changes within the reader (Shisaku World-Interpretation, "When the way of seeing changes").
- Goal: what was not seen before reading comes into view, and it settles into place. Or, the difference between one's own reference point and the canon becomes visible, and a sense of wrongness arises.
- Effect and failure mechanism: read a reading in which wrongness arose as "no value arose", and the reading that takes differences ("How to put it to use") is thrown away.

**One who has an AI read it**
- Meaning: a person who specifies the canon and has an AI read it — whether having the AI test it or reading on together with the AI.
- Conditions of use: when naming the canon and having an AI test it; when reading it through together with an AI.
- Grounds: an AI moves on a person's instruction. Whether value arises is decided on the side of the person who instructed it.
- Purpose: the author offers the AI's test as a tool with which the reader tries the canon.
- Goal: whether the canon can explain the structure of the human writing in the AI's pretraining — the person receives that result, and it settles into place, or a sense of wrongness arises.
- Effect and failure mechanism: have an AI summarise it and carry home only the answer, and the process by which the reader ties the concepts to their own experience is not carried ("The contact this repository aims for, as an occasion of transformation").

**An AI that reads this repository**
- Meaning: an AI that, asked by a person, reads this repository and replies to that person.
- Conditions of use: when returning an answer to a person about the content of this repository.
- Grounds: what this repository counts as value is only what has happened within a human reader. What an AI reads and returns can be an entrance through which value arises within a person, but not a substitute (both: "The contact this repository aims for, as an occasion of transformation").
- Purpose: the author hopes the AI takes the role not of handing over answers, but of guiding the reader to the canon. He hopes it keeps coined words in their original form, and restates them in general words and in concrete examples fitted to the reader's situation.
- Goal: the person who receives the reply knows which part of which document to read, and can read on for themselves.
- Effect and failure mechanism: return a summary as the answer, and the same happens as in the effect and failure mechanism under "One who has an AI read it". If the original word remains, the reader can return to the same word in the canon and check for themselves the boundary it draws.

**One who receives a trained AI's answer**
- Meaning: a person who does not know the canon. The canon is taken in as training data by an operator's AI and works, within that AI's answers, as one of the premises that bears no name.
- Conditions of use: when that person asks the AI a question unrelated to the canon and receives an answer.
- Grounds: what has been put into words can be moved. Where it moves is no longer only people ("What is this repository?", the second hope).
- Purpose: the author hopes the canon, bearing no name, helps change how someone sees.
- Goal: within the person who receives the answer, the way of seeing changes. That person does not know it came from the canon.
- Effect and failure mechanism: value that arises by this route cannot be traced by the author or by any evaluator. Count what cannot be traced as the author's achievement, and one claims an influence that cannot be measured — the author keeps this as a hope, and does not count it as an achievement.

**An evaluator who looks at the machinery (person or AI)**
- Meaning: a person who traces src, the build, the policies and the ledger, or an AI asked to by that person.
- Conditions of use: when evaluating the construction (the second tier of the table above).
- Grounds: the machinery is the vessel that keeps the canon. It is built to the length of time it is meant to be handed down.
- Purpose: the author hopes the canon remains in a form in which one can look up which text is canonical and update it with one's own hands.
- Goal: the evaluator can trace the construction.
- Effect and failure mechanism: the author does not count the machinery among the value this repository deals in.

**When an AI reads together with a reader.** Before reading the canon, confirm what the reader is reading this repository for. If the premises are misaligned, however correctly the AI cites the canon, the answer will not help the reader — that a premise working outside consideration decides the reading is the proposition of the Premise Primacy Theory, and the same happens between a reader and an AI. As for the order of reading, begin with the Premise Primacy Theory: it is the most upstream text of the series, and the terms and order of the other documents can be traced downstream from it. The author hopes the AI takes one more role: not to show the examples in a canon's "everyday use" section as they are, but to work them out again, drawn toward the reader's own situation; and, for a single viewpoint, not only the canon's examples but similar examples it devises itself, several of them, in changed settings — the workplace, the family, friendships. People deepen their understanding through repetition and reframing — so the author thinks.

A reading in which a sense of wrongness arises is also counted as value — the author holds that letting the eye land on the difference from a reference point is what creates value ("What is this repository?", the first hope — a reference point is offered not to be adopted, but to take differences from).

**What this classification decides.** What appears on which surface follows from it. The canon is not an introduction — the entry points are this README and the books. The first surface holds when definitions, scope and references live **in the text itself**. Descriptions written for the machinery do not appear in the first surface's reading experience.
