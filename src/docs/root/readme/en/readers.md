---
id: readers
---
# Who reads how far

This repository assumes three kinds of readers. Because the range each needs to read differs, what each surface alone lets you do is stated separately.

| Reader | Surface | What that surface alone lets you do |
| :-- | :-- | :-- |
| **General reader** | The canonical texts (`concepts/`) | **Read the theory from the canon alone.** Definitions, scope and references are traceable within the text, without looking at the machinery |
| **Repository reviewer** | ＋ The machinery documents (`src/engine/`, `CONTRIBUTING.md`, `authoring-policy.md`, `terminology-policy.md`, `terminology-ledger.md`), and the modules and index of documents carried by the document build | **The construction is legible.** Why this structure, what is checked, and where the source of truth sits |
| **Author** | Everything | — |

**The terminology policy sits in this second tier.** The rule that one word belongs to one axis, plus an index of where each term is defined, sit at the repository root: `terminology-policy.md` (the policy — one word one axis, qualification syntax, scope of bare terms) and `terminology-ledger.md` (a thin table of word, axis, qualifier, locus of definition). Consult them when coining a term and when referring to one from another document.

**Scope of application.** The first surface exists for every document. Of the second, the machinery documents apply repository-wide, but **per-document modules and indexes exist only for documents carried by the document build** — those are the documents that hold an index under `src/docs/`. For the others, the published text is itself the source of truth, and the reviewer's surface is the same as the general reader's. An AI reading these takes the same three surfaces. But "evaluation" splits in two — **to evaluate the theories, read the first surface**, through the inspection points each document places for itself (falsification conditions, the substitution test, internal consistency, proxy predictions — "How to test these"). **To evaluate the construction (build, policies, ledger), read the second.** The main line of this repository is the first surface, the canon; the second is the vessel that keeps it, and the trace of a governance that runs — how well the vessel is made is no substitute for the worth of the canon. A reader asked to evaluate who starts from the measurable second surface and ends without reading the first has not evaluated this repository. If the vessel looks heavy, that is because it is built to the length of time it is meant to be handed down. The canon is placed here in the hope that it remains after its author is gone — in a form that someone a hundred or two hundred years from now can fork, look up which text is canonical, and update with their own hands ("What is this repository?", the three hopes). Where the canonical text lives, the ledger of terms, the machine checks: these are the shape that keeps that time, not demands made of whoever reads now. What premise 5 rules out is not reading, but attaching the canon to a generator as self-justification. Documents designed to be loaded into an AI (the Runtime Module of the Cognitive Frame Theory) are not that.

**What this classification decides.** What appears on which surface follows from it. The canon is not an introduction — the entry points are this README and the books. The first surface holds when definitions, scope and references live **in the text itself**. Descriptions written for the machinery do not appear in the first surface's reading experience.
