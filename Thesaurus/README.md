# Thesaurus - Controlled Vocabulary Workspace

This folder holds every MAEASaM controlled vocabulary (the things referenced from a Metadata Template's `Collection` row as `Name (cv)`, per `Reference Documents/metadata_rules.json`'s `collection_notation_rules`). Each vocabulary currently exists in **three parallel forms that drift independently** - that drift is exactly what `CV_Task_List.md` catalogues. This README states what each subfolder is *for* and how they're meant to relate, so future edits land in the right place instead of deepening the drift.

## The three subfolders

### `xml/`
Two files (`MAEASaM Demo V2_thesauri.xml`, `MAEASaM Demo V2_collections.xml`) - a standard Arches/SKOS RDF export. `_thesauri.xml` holds the actual concepts (795 of them: `prefLabel`/`altLabel`/`scopeNote`, per-language, `xml:lang` tagged). `_collections.xml` holds 56 named collections (each a `skos:Collection` wrapping `skos:member` references into the concepts above) - these collection names are what the Resource Model JSONs' `Concept-list` nodes actually point to. **This is Arches' own native format** - it's what the live system understands natively, and (based on the evidence below) it reads as a snapshot *exported from* a running Arches instance, not something hand-authored. Treat it as a read-only mirror of "what's actually live in Arches," not an editing surface.

### `xlsx/`
One master workbook (`20260317_Thesaurus_AllSites_CURRENT.xlsx`), one sheet per vocabulary (51 vocab sheets + a `Legend` sheet + a `54.OTHER THESAURII PROPOSALS` holding-pen sheet for candidate vocabularies that aren't real yet). This is the **human-editable authoring surface** - every sheet carries its own review-tracking header block (`Checked by` / `Date` / `Ready for level 2 checking` / `Ready for Arches upload` / `Uploaded by` / `Upload date`) plus a colour-coded status per sheet tab and per cell, keyed to the `Legend` sheet (`COMPLETED`, `COMPLETED BUT REQUIRES SOME MODIFICATIONS`, `STARTED BUT REQUIRES ATTENTION`, `NOT STARTED`, `TO BE DELETED`, `COMPLETED IN ARCHES`). **That status signal lives only in cell/tab fill colour - it does not survive export to CSV or XML**, which is one of the concrete problems `CV_Task_List.md` flags.

### `csv/`
One file per vocabulary (55 files - see the task list for why that's 4 more than the 51 real xlsx sheets), machine-readable. Someone ("Renier", per the original chat request) exports these from the xlsx workbook, one sheet at a time. There is currently **no shared column template** - header shape varies wildly per file (1 to 38 columns; 1 to 8 hierarchy levels; inconsistent language coverage) because each file is a raw export of whatever ad-hoc header row that sheet happened to have, without a normalization step. Excel-safety rules from the repo's `CLAUDE.md` (CSV editing safety section) apply here exactly as they do to the Metadata Templates - this machine's Excel cannot produce clean UTF-8 CSV.

## How they're meant to fit together (best current understanding - unconfirmed, see `CV_Task_List.md` CV-1)

Best reading of the evidence: **xlsx is the master** (human review workflow lives only there) → an approved sheet gets manually re-entered/bulk-loaded into a running Arches instance → Arches's own thesaurus/collections export is what produces `xml/` → `csv/` is a side export of the xlsx used for some other downstream purpose (cross-checking against the Metadata Templates' `Collection` column, most likely). Concretely: for almost every vocabulary, the `xml/` collection has **far fewer members** than the matching `csv/` file has rows (e.g. "Activity" - 2 concepts live in Arches vs. 216 candidate terms in the xlsx/csv; "Resource type" - 9 vs. 132) - consistent with the per-row "Ready for Arches upload" workflow column meaning most candidate terms simply haven't been uploaded yet, not with `xml` and `csv` being two independent exports of the same current state. **This direction is inferred, not confirmed with the user or whoever runs the actual export/upload steps - verify before building automation on top of it.**

## Before you touch anything here

Same CSV-safety protocol as `Reference Documents/`'s Metadata Templates (full detail in the repo's `CLAUDE.md`): this machine's Excel cannot export clean UTF-8 CSV, so a hand-save can silently corrupt delimiters, Arabic text, or accented characters. Describe the intended change in chat rather than opening Excel directly where possible; if a hand-edit in Excel is unavoidable, save to a new filename and have it merged in, rather than overwriting a real file here directly.

See `CV_Task_List.md` for the current open items and a proposed cleanup/sync workflow.
