# Model-by-Model Update Log

A changelog of the metadata standardization work, reorganized by Resource Model
instead of chronologically. Source: `Task_List.md`'s Solved section plus this
session's work (branch `OU_csvXjson_match`, 2026-09-08/09). For full detail on
any item, see `Task_List.md` (task numbers referenced below) and
`Template_Progress_Log.md` (gitignored, local-only).

Local-only file (gitignored) — not pushed to the shared repo.

---

## Actor

- CSV/JSON mismatch fixed: "Contact information", "Uploader name", "Upload date" added to `Actor.json` (task #1).
- Operational Info: "Uploader name"/"Upload date"/"Resource last modified at" changed from `N/A` to `Auto-Populated`; Input Instructions regenerated to match (2026-09-06, task #3).
- Operational Info casing fixed: `Primary key`→`Primary Key`, `Foreign key`→`Foreign Key` (2026-09-02, task #40).
- Dublin Core Equivalent filled 0/17 → 17/17 (2026-09-02, task #41).
- Cardinality validated — fully clean (2026-09-02, task #25).
- Data Type vocabulary validated (fixed directly by the user, 2026-09-01/02, task #19).
- **2026-09-09:** "Start date"/"End date" — Arches datatype `string`→`edtf`, CSV `Data Type` `Date`→`EDTF`, Input Instructions updated (config block copied from Map's working `edtf` nodes; no widget entry existed before or after, still needs a widget assigned in Arches Designer — see the JSON checklist below).
- **Current state:** 17/17 fields match between CSV and JSON (names, groups, data types) — fully clean.

## Admin

- Dublin Core Equivalent filled (2026-09-01, task #17).
- `N/A` Operational Info type added; Primary/Foreign Key rule violations fixed (2026-09-02, task #20).
- **Still open:** "Geometry (WKT)" Necessity value is a literal placeholder, `(Still to be decided if it will be added)` (task #8).
- **Still open:** no real dataset exists to validate the template/Resource Model against (task #49).
- **Current state:** 12/12 fields fully clean (no CSV/JSON mismatches at all).

## Chronology

- Fully-empty Operational Info rows filled (2026-09-02, task #21).
- "Nodes modified" Necessity typo fixed (2026-09-02, task #24).
- Last Definition (En) gap ("Comment") filled (2026-09-02, task #43).
- **2026-09-09:** "Start date"/"End date" — `string`→`edtf`, CSV `Date`→`EDTF`, Input Instructions updated. No widget entry existed before or after (same caveat as Actor).
- **2026-09-09:** "Digital provenance" had blank Input Instructions — `URL` Data Type had no rule in `metadata_rules.json` at all; rule drafted, applied, user-approved same day (task #53).
- **Still open:** Group mismatch "Time span" (CSV) vs "Time Span" (JSON) on 6 fields — casing only.
- **Still open:** 5 fields present in CSV but missing from JSON — Access level, Licence, Preferred Citation, Rights Notes, Rights holder.
- **Still open:** 2 Data Type mismatches unrelated to dates — "Name of recorder"/"Region" are `Resource-Instance-List` in CSV but `string` in JSON.

## Grid

- `N/A` Operational Info + key-rule fixes applied (2026-09-02, task #20).
- "Resource created at"-type fields → `Auto-Populated` rule applied (2026-09-02, task #27).
- **Current state:** near-clean — only 1 mismatch: "Number of maps" exists in CSV but has no matching JSON node.

## Information

- 10 missing Definition (En) values drafted (2026-09-02, draft, task #34).
- Example 1/Example 2 filled from a real dataset record (2026-09-02, task #42).
- Remaining Definition (En) gaps closed as a side effect of RS's rights-fields merge (2026-09-02, task #43).
- **2026-09-09:** "Year of publication" — `string`→`edtf`, CSV `Date`→`EDTF`, Input Instructions updated, widget switched from the generic text widget to the edtf widget (this field *did* have an explicit widget entry, unlike Actor/Chronology).
- **2026-09-09:** "URL" had blank Input Instructions — same `URL` Data Type rule gap as Chronology's "Digital provenance"; fixed, approved (task #53).
- **2026-09-09:** Found and fixed a second orphaned column (distinct from the one in task #10): `APA_Reference` had only Data Type/Collection/Necessity/Cardinality set, nothing else. Renamed to "APA Reference", Dublin Core Equivalent set to `bibliographicCitation` (reusing the term already established for Map's "Preferred Citation"), Operational Info set to `N/A`, Definition (En) and Input Instructions (En) drafted (task #54). Fr/Ar/Pt name/translations still blank (part of task #13).
- **Still open:** task #10's original orphaned column (between "Copyright" and "Comment") is still unresolved — needs a decision: name/define it, or delete it.
- **Current state:** 21/21 named fields matched with JSON, clean on names/groups/data types otherwise.

## Map

- `Resource Models/Map.json` generated (`Scripts/generate_map_resource_model.py`), merged to `main` via PR #11 on 2026-09-08 (task #6). CIDOC CRM classes/properties in it are still placeholders pending review.
- Field naming hand-crafted by the user; used as the naming-standard reference for RS's Copyright/Access section (2026-09-02, task #30, #38).
- Missing "Copyright/Access" group label fixed for 5 fields (2026-09-02, task #35).
- 46 blank Operational Info cells filled with `N/A` (2026-09-02, task #36).
- Two separate Excel-encoding corruption incidents on Map specifically, both recovered from git history with all known transformations reapplied explicitly (2026-09-02, tasks #33, #37) — the second one lost the user's own recent hand-edits to Map, which had to be redone.
- French translations added for Licence/Access level/Rights holder; a stray group-name value sitting in a CIDOC CRM Scope note cell was cleared (2026-09-02, task #38).
- **2026-09-08/09:** Confirmed Map is the *reference* model for EDTF — "Clipping Date", "Digitisation Date", "Georeference Date", "Publication Year" were already Arches datatype `edtf` (unlike every other model, which had `string`). Their `edtf` node config (`fuzzy_*_padding`, `multiplier_if_*`) and widget (`widget_id adfd15ce-dbab-11e7-86d1-0fcf08612b27`) were used as the template for converting the other 5 models. CSV `Data Type` `Date`→`EDTF` applied, Input Instructions updated.
- **Current state:** 54/54 fields match between CSV and JSON — fully clean.

## Remote Sensing (RS)

- "Copyright info"/"Reference institution" renamed to "Rights Notes"/"Preferred Citation" (matching Map); Licence/Access level converted to `Concept-list` (new "Licences (cv)"/"Access Levels (cv)" vocabularies); Rights holder converted to `Resource-Instance-List` (2026-09-02, task #38).
- 5 blank Operational Info cells filled with `N/A` (2026-09-02, task #36).
- Recovered from a severe Excel corruption incident (row count inflated 58→250) by rebuilding from git HEAD (2026-09-02, task #37).
- Remaining 5 Definition (En) gaps closed as part of the rights-fields merge (2026-09-02, task #43).
- Copyright/Access section aligned to Map's field naming (2026-09-02, task #30/#38 — rest of RS still not aligned).
- **2026-09-09:** "Activity date", "Survey date", "Assessment date", "Threat assessment date", and both "Date of image used" columns — `date`→`edtf` (these were already the strict Arches `date` type, not `string`, so this widened rather than fixed them), CSV `Date`→`EDTF`, Input Instructions updated, widgets switched to the edtf widget.
- **2026-09-09, corrected same day:** the two identical "Date of image used" CSV columns were initially flagged as a copy-paste duplicate (only one matching JSON node existed). The user clarified they are **two different concepts** — column #33 is the Condition-assessment image date, column #45 is the Threat-assessment image date — that ended up with the identical name because the `Group` label was never set at column #43 where the "Threat assessment date" subsection actually starts (columns #43–45 silently inherit the forward-filled "Condition assessment" group instead of their own). **Marked High importance in Task_List (#51) — needs testing in Arches to confirm which node is which before renaming/regrouping.**
- **Still open, unresolved:** 15 CSV-only / 14 JSON-only field names — many look like naming-drift pairs rather than true gaps (e.g. "Administrative area name" ↔ "Administration area name", "Ground truthing" ↔ "Ground truthed", "Measurement value" ↔ "Measurment value" — JSON-side typo) but none have been confirmed/merged yet. A per-field decision log was started (`RS_CSVvsJSON_Match_Decisions.md`, gitignored) but paused in favor of checking directly in Arches. See the JSON checklist below.
- **Still open:** "Threat type"/"Threat severity" both reference the same vocabulary, `Disturbance cause (cv)` — possible copy-paste slip, needs a human call (task #7).
- **Still open:** 3 Data Type mismatches unrelated to dates — Access level (`Concept-list` vs `string`), Grid level 2 (`Resource-Instance-List` vs `string`), Spatial resolution m (`Number` vs `string`).

## Site

- **No Metadata Template and no Guideline exist at all** (task #5) — the single biggest remaining gap: 158 JSON nodes, 136 of them fillable, none documented. Not started.

---

## Cross-cutting: rules and tooling (`metadata_rules.json`, `Scripts/`)

- Row label terminology normalized to one canonical vocabulary across all 7 templates (2026-09-01, task #16).
- Collection column normalized to `Name (cv)` / `Name (rm)` / `N/A` notation (2026-09-01, task #18).
- `data_type_values` defined and every model validated against it (2026-09-01/02, task #19).
- Dublin Core basic 15 elements + in-use terms added as reference vocabulary (2026-09-02, task #22).
- Necessity vocabulary expanded with real-use values (`Mandatory if applicable`, `If applicable`) (2026-09-02, task #23).
- Input Instructions (En) row added to all 7 templates, generated from a Data Type + Operational Info rule (2026-09-02, task #26).
- Sequential field numbering added to every template's header row (2026-09-02, task #28).
- `input_instructions` keys renamed to match `data_type_values` naming exactly (2026-09-02, task #31).
- Input Instructions drafted for `GeoJSON-feature-collection` and `Number` (2026-09-02, draft, task #32).
- **2026-09-08:** `EDTF` split out of `Date` as its own Data Type vocabulary value (`Date` = strict ISO, `EDTF` = supports `?`/`~` qualifiers); `input_instructions` updated accordingly.
- **2026-09-08:** `known_issues` array added — documents the Arches EDTF `%` (combined uncertain+approximate) bug found via live testing (Arches 8.1.4): the qualifier is silently dropped on save. Root cause traced to `EDTFDataType.transform_value_for_tile()` re-serializing through the third-party `edtf` Python library. Not filed upstream — worked around internally instead. `?` and `~` alone confirmed working.
- **2026-09-09:** `input_instructions_csv` added — shorter, cell-ready overrides for entries whose full text is too long for an actual spreadsheet cell (currently just `EDTF`).
- **2026-09-09:** `URL` Data Type's missing Input Instructions rule drafted and approved.
- **New scripts this session:** `Scripts/check_csv_json_match.py` (compares every CSV's node names/groups/data types against its Resource Model JSON — this is what surfaced most of the "Still open" items above) and `Scripts/check_input_instructions.py` (cross-checks every field's Input Instructions text against the Data Type/Operational Info rule).
- Task_List.md gained an `Importance` column (currently only populated where a priority was already stated in the task text, plus the new RS duplicate-field item marked High).

---

## JSON checklist for the other PC (things to verify/fix directly in Arches)

1. **Data-loss risk check, before anything else:** if Actor's "Start date"/"End date" or Chronology's "Start date"/"End date" already have real (non-test) data entered as plain strings, check whether that data is valid EDTF. The datatype was changed `string`→`edtf` by hand-editing the JSON (not through Arches Designer), so any already-saved non-EDTF value could fail validation the next time that tile is opened/saved. Same check for RS's 5 converted fields, though those were already the strict `date` type (ISO-formatted), so they're lower risk — EDTF is a superset of plain ISO dates.
2. **Widget setup needed:** Actor's "Start date"/"End date" and Chronology's "Start date"/"End date" have **no widget entry at all** in `cards_x_nodes_x_widgets` (this was already true before today's change — they were `string` nodes with no widget either). They likely need the EDTF widget added via Designer so they're actually editable on the resource card, the same way Information's "Year of publication" and RS's 5 date fields already have one (those got their widget switched to edtf as part of today's change since they already had one).
3. **RS "Date of image used" duplicate columns (Task_List #51, High):** confirm which of the two identical-name CSV columns is the Condition-assessment image date and which is the Threat-assessment one, then rename them to disambiguate and fix the missing `Group` label at CSV column #43 (currently silently inherits "Condition assessment" instead of switching to "Threats"/its own subsection where "Threat assessment date" actually starts).
4. **RS's 15 CSV-only / 14 JSON-only field names:** now that you'll have RS open in Arches, this is a good time to resolve the pending renames flagged earlier — check node names directly (e.g. "Administrative area name" vs "Administration area name", "Ground truthing" vs "Ground truthed", "Measurement value" vs "Measurment value" — likely a JSON-side typo, "Date of image" vs "Date of imagery"/"Image used date"). A per-field decision log was started at `RS_CSVvsJSON_Match_Decisions.md` (gitignored) but paused — resume there once you've checked.
5. **General sanity check:** since Actor.json, Chronology.json, Information.json, and Remote Sensing.json were all hand-edited (datatype/config/widget_id changes only, not through Designer), confirm each graph still imports/publishes cleanly in Arches with no errors before relying on them further.

---

## Branch/merge activity relevant to this log

- `map-json` → merged to `main` via PR #11 (2026-09-08).
- `necessity` → merged to `main` via PR #13 (2026-09-08).
- `RH_Arches_resource_models` (a colleague's branch adding Actor/Administrative Model/Chronology/Grid/Information JSON files) → merged to `main` via PR #12 (2026-09-08).
- All of today's work (EDTF conversion, Input Instructions fixes, Task_List updates) is on branch `OU_csvXjson_match`, not yet merged.
