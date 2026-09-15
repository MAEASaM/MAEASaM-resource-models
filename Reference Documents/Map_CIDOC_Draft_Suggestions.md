# Map — CIDOC CRM Node Class suggestions (drafted by Orhun)

Drafted 2026-09-14 by Orhun, based on field name + Definition (En) + Data Type, following the
CIDOC CRM classes already established elsewhere in the project (Grid/Actor/Info/RS) wherever a
clear precedent existed. **Applied to both `Map_MetadataTemplate.csv` and `Map.json` on
2026-09-14** — but these are still just Orhun's draft picks, not yet confirmed by Package 2.
Renier and Anton (and anyone else on the team) should check them against the CIDOC CRM ontology
before treating them as final, same process as Task_List #14's other CIDOC gaps. The
"Medium"-confidence rows below are the ones most worth a second look.

**Update 2026-09-14 (same day):** a real Arches import attempt on `Map.json` surfaced that 6 of
the "Medium"-confidence picks below were actually CIDOC-invalid (not just debatable) — the
domain/range didn't validate against Arches' real ontology. Those 6 (`Geographical Identifier`,
`Map Dimensions`, `Physical File Place`, `Is Digitised?`, `Is Georeferenced?`, `Is Clipped?`) were
reverted to their original, valid classes and are marked **REVERTED** below. `Map Name` and `Grid`
were kept since they weren't the cause of any failure. See Task_List #86 and the new
`Scripts/validate_cidoc_edges.py`, which checks a class/property pairing against the real Arches
ontology files before you commit to it — worth running before proposing further changes here.

Confidence legend: **High** = matches an established project pattern closely, low risk of being
wrong. **Medium** = reasonable CIDOC fit but a defensible alternative exists, or the field is a
genuinely new type of concept not seen elsewhere in the project yet.

## Identifiers

| Field | Data Type | Suggested CIDOC | Confidence | Reasoning |
|---|---|---|---|---|
| Local ID | String | E42 Identifier | High | Same pattern as MAEASaM ID/SASES ID/Zotero Key — a catalogue/inventory number. |
| Geographical Identifier | Concept-list | ~~E44 Place Appellation~~ → **E55 Type** | REVERTED | E44 Place Appellation is invalid here: `P2_has_type`, the property already connecting this field, requires range E55 Type specifically — confirmed by a real Arches import failure 2026-09-14, reverted same day. |

## Map Details

| Field | Data Type | Suggested CIDOC | Confidence | Reasoning |
|---|---|---|---|---|
| Map Name | String | **E35 Title** | High | CSV already had this value (JSON's auto-generated placeholder had the more generic E41 Appellation instead) — keeping the CSV's more specific existing choice; JSON needs to be corrected to match. |
| Sheet Code | String | E42 Identifier | High | "A code used to identify a specific map sheet" — textbook identifier. |
| Series | String | E62 String | Medium | Free-text label naming the map series. Alternative: E41 Appellation (if "series" is treated as a name rather than a plain description). |
| Edition | String | E62 String | Medium | Same reasoning as Series. Alternative: E41 Appellation. |
| Scale | String | E62 String | High | Formatted ratio text (e.g. "1:50,000"), not a plain count — matches the project's generic-text convention. |
| Map Material | String | E62 String | High | Generic descriptive attribute text. |
| Map Dimensions | String | ~~E54 Dimension~~ → **E62 String** | REVERTED | E54 Dimension is invalid here: its connecting property (`P3_has_note`) only validates against primitive-datatype nodes when the class stays a plain literal type — confirmed by a real Arches import failure 2026-09-14, reverted same day. |
| Map Type | Concept-list | E55 Type | High | Matches Licence/Access level — a type classification chosen from a controlled vocabulary. |
| Map Condition | Concept-list | E55 Type | Medium | Matches the Map Type/Licence/Access level pattern (a vocabulary-driven classification). CIDOC also has a purpose-built **E3 Condition State** class for physical condition assessments specifically — worth Renier/Anton weighing in on which fits the project's intent better. |
| Description | String | E62 String | High | Free-text catch-all, same as Comment/Rights Notes elsewhere. |

## File Location

| Field | Data Type | Suggested CIDOC | Confidence | Reasoning |
|---|---|---|---|---|
| Digital File Name | String | E42 Identifier | Medium | Functions as an identifier for the digital surrogate. Alternative: E41 Appellation (if treated as a name rather than an identifier). |
| Digital File Path | String | E62 String | High | A path string — plain text. |
| Physical File Place | String | ~~E53 Place~~ → **E62 String** | REVERTED | E53 Place is invalid here for the same reason as Map Dimensions — confirmed by a real Arches import failure 2026-09-14, reverted same day. |

## Publication Information

| Field | Data Type | Suggested CIDOC | Confidence | Reasoning |
|---|---|---|---|---|
| Publisher | String | E82 Actor Appellation | High | Matches the Uploader/Recorder-adjacent pattern for a person/org name held as plain text. |
| Publication Year | EDTF | E50 Date | High | Matches every other date field in the project. |
| Sheet History | String | E62 String | High | Free-text provenance/history note. |

## Cartographic Information

All fields below are short technical CRS-parameter text values ("generally written on the map"),
structurally identical — suggesting the same class for consistency:

| Field | Data Type | Suggested CIDOC | Confidence | Reasoning |
|---|---|---|---|---|
| Grid | Resource-Instance-List | **E53 Place** | Medium | Links to a Grid record; Grid's own Geometry node uses E53 Place, and Grid.json's own "Related sites" field (a comparable resource link) also uses E53 Place. Alternative: E1 CRM Entity (generic, no assumption). |
| Projection | String | E62 String | High | |
| Spheroid | String | E62 String | High | |
| Unit of | String | E62 String | High | |
| Meridian of | String | E62 String | High | |
| Latitude of | String | E62 String | High | |
| Scale Factor | String | E62 String | High | |
| False Co-ords | String | E62 String | High | |
| False Co-ords of Origin | String | E62 String | High | |
| Datum | String | E62 String | High | |
| Annotation | String | E62 String | High | Text/labels/symbols shown on the original map. |

## Digitisation Status

| Field | Data Type | Suggested CIDOC | Confidence | Reasoning |
|---|---|---|---|---|
| Is Digitised? | Boolean | ~~E55 Type~~ → **E62 String** | REVERTED | E55 Type is invalid here (same `P3_has_note` reason as Map Dimensions) — confirmed by a real Arches import failure 2026-09-14, reverted same day. |
| Digitisation Person | String | E82 Actor Appellation | High | Same pattern as Publisher. |
| Digitisation Date | EDTF | E50 Date | High | |
| Is Georeferenced? | Boolean | ~~E55 Type~~ → **E62 String** | REVERTED | Same as Is Digitised? — reverted 2026-09-14. |
| Georeference Person | String | E82 Actor Appellation | High | |
| Georeference Date | EDTF | E50 Date | High | |
| Is Clipped? | Boolean | ~~E55 Type~~ → **E62 String** | REVERTED | Same as Is Digitised? — reverted 2026-09-14. |
| Clipping Person | String | E82 Actor Appellation | High | |
| Clipping Date | EDTF | E50 Date | High | |
| Digitisation Method | Concept-list | E55 Type | Medium | Matches Map Type pattern. Alternative: E29 Design or Procedure (if "method" is treated as a technique/procedure rather than a type value). |

## Digital Transformation Details

| Field | Data Type | Suggested CIDOC | Confidence | Reasoning |
|---|---|---|---|---|
| Digitisation Tool | String | E62 String | Medium | Free text naming the equipment. Alternative: E22 Human-Made Object (if the specific physical instrument is meant to be modeled as an object, likely overkill for a free-text field). |
| Color Detail | String | E62 String | High | |
| File Resolution | String | E62 String | High | |

## Already applied (2026-09-14, not part of this draft)

MAEASaM ID, Recorder, Uploader, Licence, Access level, Rights holder, Rights Notes, Preferred
Citation, Comment, Created at, Uploaded at, Last modified at — all copied from the already-agreed
values used identically across Actor/Admin/Chronology/Grid/Info/RS (see Task_List #82).

## Next step

Send this file to Renier and Anton for review/correction, same as the outstanding Task_List #14
CIDOC gaps for RS/Chronology/Info. If they want a different class for any field, update both
`Map_MetadataTemplate.csv` (CIDOC CRM Node Class row) and `Map.json` (`ontologyclass` on the
matching node) together.
