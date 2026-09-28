# Thesaurus - CV Instructions and Protocols

Naming/formatting rules for MAEASaM controlled vocabularies (CVs) - both the vocab's own name and the terms inside it. Companion to `README.md` (what the subfolders are for), `CV_Reference_Schema.csv` (the per-term column schema), and `CV_Task_List.md` (open items and decision history - each rule below links back to the task that decided it).

## Rule 1: Vocab (CV) names use sentence case

Capitalize only the first word of a vocab's name, plus any real proper noun or acronym. Do not Title Case every word.

- Correct: `Actor type`, `Name type`, `Resource type`, `Nature of association`, `Chronology name value`, `Map types`, `Document conditions`, `Digitisation methods`, `Access levels`
- Incorrect: `Actor Type`, `Map Types`, `Document Conditions`, `Digitisation Methods`, `Access Levels`

**Why this and not Title Case:** it's the existing de-facto standard, not an arbitrary pick. All 56 collection names actually live in Arches (`Thesaurus/xml/`) and all 51 sheet names in the xlsx master workbook (`Thesaurus/xlsx/`) were already overwhelmingly sentence case, with only 3 outliers (see "2026-09-15: the 3 legacy outliers" below) - this rule has no exceptions now, it's the standard for every vocab, old or new.

**Applies to:** the vocab name everywhere it's written - the CSV filename in `Thesaurus/csv/`, the `"Name (cv)"` value in a Metadata Template's `Collection` row, and any `"Name" controlled vocabulary` phrasing inside a Resource Model JSON's field `description`. All of these must read identically (case included), since a Metadata Template instruction like `Please write the term exactly as recorded in the "Access levels" controlled vocabulary` is a literal lookup key, not just prose.

**2026-09-15 cleanup:** 4 vocab CSVs were found in Title Case (`Map Types`, `Document Conditions`, `Digitisation Methods`, `Access Levels`) and renamed to sentence case. All 4 turned out to have no matching xlsx sheet or xml collection at all - they were created fresh (most likely while building the newer Map/Admin/Info Metadata Templates) rather than sourced from the tracked 51-vocab xlsx/xml universe, which is why they never inherited the existing convention. See `CV_Task_List.md` CV-13 for the full before/after and the files touched.

## Rule 2: Terms inside a vocab also use sentence case

Same rule, applied to each `Term (En)` value: capitalize only the first word (plus real proper nouns/acronyms).

- Correct: `Topographic map`, `Open access`, `External researcher`, `Born digital`, `National heritage body`
- Incorrect: `Topographic Map`, `Open Access`, `External Researcher`

This one was already being followed consistently everywhere it was checked (`CV_Reference_Schema.csv`'s own worked example uses `Radiocarbon dating`, not `Radiocarbon Dating`) - this section formalizes it as a rule rather than an unwritten habit, so it survives being copied into new vocabs.

## Rule 3: Vocab (CV) names are plural (decided 2026-09-24)

A vocab's name is written in the plural, since it names the list of allowed values: `Site types`, `Measurement units`, `Access levels`, `Licences`, `Threat probabilities`. Same "applies everywhere" scope as Rule 1 - xlsx sheet name, csv filename, the `Name (cv)` value in a Metadata Template's `Collection` row, and any vocab name quoted in a Resource Model JSON description must read identically.

- **Decided by the user 2026-09-24** while mapping the Site template's Collection names to the Thesaurus. At that point the repo was mixed: ~8 newer vocabs (created for Map/Admin/Info) were already plural (`Access levels`, `Countries`, `Languages`, `Licences`, `Map types`, `Digitisation methods`, `Document conditions`), while the older xlsx/Arches vocabs were mostly singular. The plural form was chosen as the standard going forward; the remaining singular vocabs are a tracked rollout (`CV_Task_List.md` CV-21), not yet renamed.
- **Excel's 31-character sheet-name limit:** a vocab name must fit in 31 characters so the xlsx sheet tab can carry it exactly. If the natural plural is longer, pick a shorter name rather than letting the tab silently truncate (e.g. `Probability of threat affecting site` -> `Threat probabilities`, 2026-09-24).
- **`/` in a vocab name:** Excel forbids `/` in sheet names, so a vocab like `Material/object types` has the tab `Materialobject types` (slash dropped, no space) - the one permitted difference between the sheet tab and the vocab name. Everywhere else (Metadata Template `Collection`, Input Instructions, the sheet's own vocab-name header cell, csv filename where the OS allows) the name keeps its `/`.
- **How renames are applied to the xlsx master:** edit the sheet `name` attribute in `xl/workbook.xml` (and the vocab-name header cell's shared string in `xl/sharedStrings.xml`, only if that string is used by that one sheet) directly inside the zip - never open-and-save in Excel. Same method as the 2026-09-15 casing fix below.

## 2026-09-15: the 3 legacy outliers are fixed too - no more exceptions

`Coordinate System`, `Ownership Type`, `Survey Type` were the only 3 sheet names in the xlsx master workbook that broke Rule 1. Fixed the same day: `xl/workbook.xml` inside `Thesaurus/xlsx/20260317_Thesaurus_AllSites_CURRENT.xlsx` was edited directly (sheet-tab `name` attribute only, via a small script - not opened in Excel, so none of this machine's Excel/CSV-export corruption risk applies) to `Coordinate system`, `Ownership type`, `Survey type`. No Metadata Template or Resource Model JSON referenced these 3 by name, so nothing else needed updating there.

**Still outstanding - not something this repo can do:** these 3 are already-uploaded, live Arches collections (`Thesaurus/xml/MAEASaM Demo V2_collections.xml`, still showing the old Title Case names). `xml/` is treated as read-only here (see `README.md`) - it's a mirror of whatever is actually live in the running Arches instance, so the rename has to happen there directly (by whoever administers Arches), after which a fresh xml export will reflect it. Until that happens, the xlsx master and the live Arches instance disagree on these 3 names - flag this as a to-do for whoever next touches Arches, don't silently re-export xml to "fix" it here.

One more Title Case name is known to exist live in Arches - `Resource To Resource Relationship Types` (per `CV_Task_List.md` CV-6) - but it has no xlsx sheet or csv file at all to fix here; same "needs a real Arches rename" caveat applies whenever someone gets to it. Aside from that single live-Arches-only case, there is no longer a documented exception to Rule 1 - every vocab and term name in `Thesaurus/csv/` and `Thesaurus/xlsx/`, old or new, is sentence case.

## Where this doesn't apply

- Acronyms and initialisms stay fully capitalized: `LULC`, `EPSG`, `CC BY`, `ISO 3166-1`.
- Proper nouns keep their own capitalization: country names (`Cote d'Ivoire`), language names (`English`, `French`), organization/standard names in a `Source (En)` citation.
- The `"(cv)"` / `"(rm)"` suffix notation itself (lowercase, in parentheses) is a separate, already-documented rule - see `Reference Documents/metadata_rules.json`'s `collection_notation_rules`. This file only governs the vocab/term name that comes before that suffix.
