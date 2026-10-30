# Arches patches and setup notes

Some MAEASaM datasets do not load into a stock Arches install because of bugs in Arches itself (not in
our data). Until these are fixed upstream, apply the patches below to the installed Arches package
before ingesting the datasets.

- **Tested with:** Arches 8.1.5 (`pip install arches==8.1.5`). The patched code is identical in 8.1.4.
- **Where:** the files are in your Python environment, under `site-packages/arches/`, e.g.
  `ENV\Lib\site-packages\arches\` on Windows or `ENV/lib/python3.12/site-packages/arches/` on Linux.
- **They are lost on every `pip install` / upgrade of Arches.** Re-apply them afterwards.
- After patching, restart `runserver` **and** the Celery worker, so both load the new code.

| # | Patch | Needed for | Symptom without it |
|---|---|---|---|
| 1 | csv field size limit | Administrative dataset (very large `Geometry (WKT)` cells) | Upload fails with "Invalid csv file" / 500 on `/etl-manager` |
| 2 | `split_geom` vertex count | Administrative dataset (large MultiPolygons) | Load ends as "loaded but unindexed"; `arches.log` shows `lwgeom_subdivide_prec: cannot subdivide to fewer than 5 vertices per output` |

## 1. csv field size limit

**Why:** Python's `csv` module refuses fields longer than 131072 characters. Some Administrative
boundaries are several million characters of WKT (Tanzania is ~9.1M). Arches catches the resulting
`_csv.Error` and reports it as "Invalid csv file".

**Fix:** raise the limit, in two files (the second one runs inside the Celery worker).

`arches/app/utils/file_validator.py` - add after the imports (after `from openpyxl.utils.exceptions import InvalidFileException`):
```python
# Python's csv module defaults to a 131072-char field size limit, which large
# geometry (WKT) fields routinely exceed. Raised process-wide here so both this
# validator and import_single_csv.py's own csv.reader calls (same process) are covered.
csv.field_size_limit(100_000_000)
```

`arches/app/etl_modules/import_single_csv.py` - add after the imports (after `from arches.app.etl_modules.save import save_to_tiles`):
```python
# Same fix as file_validator.py: raise Python's csv field size limit for large WKT fields.
csv.field_size_limit(100_000_000)
```

**Check:** both files contain `csv.field_size_limit(100_000_000)`.

## 2. `split_geom` vertex count (MultiPolygon)

**Why:** to index a geometry larger than ~32 KB in Elasticsearch, Arches splits it with PostGIS
`ST_Subdivide(geom, max_points)`. It estimates the vertex count as `len(coordinates[0])`. For a
`Polygon` that is the outer ring's vertex count, but for a `MultiPolygon` it is the number of rings of
the first polygon (usually 1). So `max_points` becomes 0, PostGIS requires at least 5, and indexing
stops. Every Administrative geometry is a MultiPolygon; about 860 of 2841 are large enough to hit this.
The data itself is saved correctly; only the search/map index is missing.

**Fix:** in `arches/app/datatypes/core/geojson_feature_collection.py`:

(a) In `split_geom()`, replace
```python
        coordinates = (
            geom["coordinates"]
            if geom["type"] == "LineString"
            else geom["coordinates"][0]
        )
        num_points = len(coordinates)
        num_chunks = self._feature_length_in_bytes(feature) / max_feature_in_bytes
        max_points = int(num_points / num_chunks)
```
with
```python
        num_points = self._count_vertices(geom["coordinates"])
        num_chunks = self._feature_length_in_bytes(feature) / max_feature_in_bytes
        max_points = max(5, int(num_points / num_chunks))
```

(b) Add this method to the same class, e.g. right after `_feature_length_in_bytes()`:
```python
    def _count_vertices(self, coordinates):
        # number of positions in any GeoJSON coordinates array
        if coordinates and isinstance(coordinates[0], (int, float)):
            return 1
        return sum(self._count_vertices(c) for c in coordinates)
```

**Check:** the file contains `_count_vertices`. Tested 2026-10-30 on Arches 8.1.5: all 2836
Administrative geometries index without error (858 of them are split).

**If Administrative was already loaded without this patch** (status "loaded but unindexed"), there is
no need to load it again. Patch, then re-index only that model:
```
python manage.py es index_resources_by_type -rt <Administrative graphid>
```
The graphid is the `graphid` value in `Resource Models/Administrative.json`.

## Setup notes (not patches)

- **Ontology and thesaurus come from this repo:** ontology `Ontologies/crm62`
  (`manage.py load_ontology --source ...`), then thesaurus `Thesaurus/xml`, thesauri file first,
  then collections (`manage.py packages -o import_reference_data -s ...`). Then import the resource models.
- **Celery is needed for `/etl-manager` imports:** any csv over 500 bytes is handed to Celery.
  Without a running worker, the page stays on "validating". Start one with
  `celery -A <project> worker --loglevel=info --pool=solo` (`--pool=solo` on Windows).
  With the `filesystem://` broker, create the broker folders (`celery_broker/out`,
  `celery_broker/processed` under the project) before the first start.
- **Restart the Celery worker after loading or reloading the thesaurus.** The worker caches each
  collection's terms the first time it uses them. If it ran before the thesaurus was loaded, every
  concept value fails with "This is an invalid concept prefLabel, or an incomplete UUID" until it is restarted.
