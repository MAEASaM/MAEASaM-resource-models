# Metadata Templates - Instructions and Protocols

Human-readable companion to `metadata_rules.json` (the machine-readable rules `Scripts/` actually read) - for anyone editing a `*_MetadataTemplate.csv` by hand or through the Excel round-trip (`Scripts/templates_excel_sync.py`). Mirrors `Thesaurus/CV_Instructions_and_Protocols.md`'s role on the vocab side.

Supersedes `template_instructions.csv` (see note at the end) - every rule below already lives in `metadata_rules.json`, this file just writes it out in prose so it doesn't need to be reverse-engineered from JSON.

## Spreadsheet formatting rules

1. Font: Calibri, 12pt, for all characters.
2. Bold only for the row-label columns (A-C: Arches terminology / Universal terminology / User form) - everything else normal weight.
3. Wrap text on for every cell.
4. All Borders on every cell.
5. **Colour-coding (corrected 2026-09-15):** the Metadata (En/Fr/Ar/Pt) rows are coloured per-field using `data_type_colors`, keyed by that field's own Data Type. The two CIDOC CRM ontology-class rows (`CIDOC CRM Semantic Node Class` / `CIDOC CRM Node Class`) get a fixed colour from `cidoc_class_row_colors`, regardless of Data Type. The `Data Type` and `Collection` rows themselves, and every row below `Collection`, are **not** coloured. (This replaces an earlier, less precise version of the rule that said to colour "until Collection row, inclusive" - confirmed wrong against the real reference workbook.)

## Collection row notation

- Concept-list (controlled vocabulary) field: `"Name of Vocab (cv)"`, e.g. `Resource type (cv)`.
- Resource-Instance-List (linked resource model) field: `"Name of Model (rm)"`, e.g. `Actor (rm)`.
- Anything else: `N/A`, not blank.

## Input Instructions - common phrases

The authoritative per-Data-Type text lives in `metadata_rules.json`'s `input_instructions` (11 entries: String, Concept-list, Resource-Instance-List, Date, EDTF, Boolean, Auto-Populated, Derived, GeoJSON-feature-collection, Number, URL) - `input_instructions_csv` holds shorter cell-ready overrides where the full text is too long for a spreadsheet cell (currently just EDTF).

Do not hand-copy these phrases elsewhere - a stale copy is exactly what caused `Scripts/generate_template_skeleton.py`'s `KeyError` bug (it referenced `template_instructions.csv`'s old key names, `"Concept list"` / `"Resource instance model"`, which were renamed to `"Concept-list"` / `"Resource-Instance-List"` on 2026-09-02 to match `data_type_values` - the script was never updated to match).

## Operational Info rules

- Data Type `Resource-Instance-List` → usually `Foreign Key`, unless the value is derived from the linked resource, then `Derived`.
- Metadata name `MAEASaM ID` → `Primary Key`.
- Metadata name `Resource created at` / `Resource last modified at` / `Uploader name` / `Upload date` / `Nodes modified` → `Auto-Populated`.

## About `template_instructions.csv`

`Reference Documents/template_instructions.csv` predates `metadata_rules.json` and is now fully superseded and stale - every rule it has is above, in corrected form. Two concrete things it still gets wrong if read directly: the old `"Concept list"` / `"Resource instance model"` key names (see above), and the old, less precise colour rule. Left in place for now rather than deleted (2026-09-16 - flagged, not acted on).
