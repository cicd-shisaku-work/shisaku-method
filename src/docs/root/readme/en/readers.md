---
id: readers
---
# Who reads how far

This repository assumes three kinds of readers. Because the range each needs to read differs, what each surface alone lets you do is stated separately.

| Reader | Surface | What that surface alone lets you do |
| :-- | :-- | :-- |
| **General reader** | The canonical texts (`concepts/`) | **Read the theory from the canon alone.** Definitions, scope and references are traceable within the text, without looking at the machinery |
| **Repository reviewer** | ＋ The machinery documents (`src/engine/`, `CONTRIBUTING.md`, `terminology-policy.md`), and the modules and index of documents carried by the document build | **The construction is legible.** Why this structure, what is checked, and where the source of truth sits |
| **Author** | Everything | — |

**Scope of application.** The first surface exists for every document. Of the second, the machinery documents apply repository-wide, but **per-document modules and indexes exist only for documents carried by the document build** — those are the documents that hold an index under `src/docs/`. For the others, the published text is itself the source of truth, and the reviewer's surface is the same as the general reader's.

**What this classification decides.** What appears on which surface follows from it. The first surface holds when definitions, scope and references live **in the text itself**. Descriptions written for the machinery do not appear in the first surface's reading experience.
