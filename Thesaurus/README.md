# Thesaurus - Controlled Vocabulary Workspace

This folder holds every MAEASaM controlled vocabulary (the things referenced from a Metadata Template's `Collection` row as `Name (cv)`, per `Reference Documents/metadata_rules.json`'s `collection_notation_rules`). Each vocabulary currently exists in **three parallel forms that drift independently** - that drift is exactly what `CV_Task_List.md` catalogues. This README states what each subfolder is *for* and how they're meant to relate, so future edits land in the right place instead of deepening the drift.

## The three subfolders

### `xml/`
Two files (`MAEASaM Demo V2_thesauri.xml`, `MAEASaM Demo V2_collections.xml`) - a standard Arches/SKOS RDF export. `_thesauri.xml` holds the actual concepts (795 of them: `prefLabel`/`altLabel`/`scopeNote`, per-language, `xml:lang` tagged). `_collections.xml` holds 56 named collections (each a `skos:Collection` wrapping `skos:member` references into the concepts above) - these collection names are what the Resource Model JSONs' `Concept-list` nodes actually point to. **This is Arches' own native format** - it's what the live system understands natively, and (based on the evidence below) it reads as a snapshot *exported from* a running Arches instance, not something hand-authored. Treat it as a read-only mirror of "what's actually live in Arches," not an editing surface.

### `xlsx/`
One master workbook (`20260317_Thesaurus_AllSites_CURRENT.xlsx`), one sheet per vocabulary (51 vocab sheets + a `Legend` sheet + a `54.OTHER THESAURII PROPOSALS` holding-pen sheet for candidate vocabularies that aren't real yet). This is the **human-editable authoring surface** - every sheet carries its own review-tracking header block (`Checked by` / `Date` / `Ready for level 2 checking` / `Ready for Arches upload` / `Uploaded by` / `Upload date`) plus a colour-coded status per sheet tab and per cell, keyed to the `Legend` sheet (`COMPLETED`, `COMPLETED BUT REQUIRES SOME MODIFICATIONS`, `STARTED BUT REQUIRES ATTENTION`, `NOT STARTED`, `TO BE DELETED`, `COMPLETED IN ARCHES`). **That status signal lives only in cell/tab fill colour - it does not survive export to CSV or XML**, which is one of the concrete problems `CV_Task_List.md` flags.

### `csv/`
The cleaned, machine-readable working copy of each vocabulary, in the shared `CV_Reference_Schema.csv` layout (Term ID = Arches UUID, Parent Term ID, Term/Definition En-Fr-Ar-Pt, Alt Label(s), Source, Status), maintained by OU (see "How they fit together" below). Only the vocabularies already migrated to that layout live directly in `csv/` (12 files as of 2026-10-28); `csv/Versions/` keeps the older raw per-sheet exports (wide `Hierarchy N` columns, made earlier from the xlsx, originally by Renier) until each one is migrated (`CV_Task_List.md` CV-11). Excel-safety rules from the repo's `CLAUDE.md` (CSV editing safety section) apply here exactly as they do to the Metadata Templates - this machine's Excel cannot produce clean UTF-8 CSV.

## How they fit together (confirmed by the user 2026-10-28, closes `CV_Task_List.md` CV-1)

The project is still in its set-up / workflow-building phase; this is the agreed workflow. The person responsible for all vocab sources is Orhun Ugur (OU).

1. **`xlsx/` master workbook = the team's reference.** Everyone on the team uses it today. It is not machine-readable and still contains small errors, so nothing is loaded into Arches from it directly.
2. **Team members propose new or changed terms in `CV_TermUpdate_Tracker.xlsx`** (not in the master workbook and not in Arches).
3. **`csv/` = the cleaned, machine-readable working copy.** Each vocab csv is built from the xlsx master, corrected, and extended with the new terms from the tracker when needed (`CV_Reference_Schema.csv` layout). In the end the csv versions must be clean.
4. **Arches.** OU enters terms into Arches - by hand in the RDM during set-up, or by asking Claude to prepare them. Long term, entering everything in Arches is the preferred route.
5. **`xml/` = an Arches export,** made by OU when needed. It mirrors what is in Arches; read both files together (see `CV_Instructions_and_Protocols.md`, "Comparison protocol").
6. **Publishing back to the team.** The clean csv versions are merged into an xlsx like the master and shared with the team every 3 months, or after a large change. The master is updated in batches, together with the tracker - not term by term.

**Term IDs (decided 2026-10-28):** a csv's `Term ID` is the Arches concept UUID - no separate local code. After any change in Arches, refresh the csv Term IDs from the new xml export. Move vocabularies between Arches instances by importing the xml, never by re-creating terms by hand - a re-created term gets a new UUID, and the csv and datasets no longer match (this is what happened to `Resource type.csv`, CV-22).

## Before you touch anything here

Same CSV-safety protocol as `Reference Documents/`'s Metadata Templates (full detail in the repo's `CLAUDE.md`): this machine's Excel cannot export clean UTF-8 CSV, so a hand-save can silently corrupt delimiters, Arabic text, or accented characters. Describe the intended change in chat rather than opening Excel directly where possible; if a hand-edit in Excel is unavoidable, save to a new filename and have it merged in, rather than overwriting a real file here directly.

See `CV_Task_List.md` for the current open items and a proposed cleanup/sync workflow, and `CV_Instructions_and_Protocols.md` for naming/formatting rules (e.g. vocab and term name casing) to follow when adding or editing a vocab.
