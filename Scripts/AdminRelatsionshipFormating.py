import csv
import json
from shapely.wkt import loads
import unicodedata
import warnings
warnings.filterwarnings('ignore')


# Set a higher field size limit for large CSV files
csv.field_size_limit(1024 * 1024 * 50)  # 50 MB


input_csv_file = r"E:\MAEASaM\Arches\Arches_demo_v2_tdb2\Resource_models\Admin\Admin_With_UUID_expanded.csv"
output_csv_file = r"E:\MAEASaM\Arches\Arches_demo_v2_tdb2\Resource_models\Admin\Admin_Relationships_Output.csv"

# Prompt user for metadata to add to all rows
upload_date = input("Enter Upload date (e.g., 2026-08-26): ").strip()
uploader_name = input("Enter Uploader name: ").strip()

if not upload_date or not uploader_name:
    print("Error: Both Upload date and Uploader name are required.")
    exit(1)


def fix_geometries(rows, geom_column_name):
    """
    Fix invalid WKT geometries by using Shapely's buffer(0) trick.

    Args:
        rows (list): List of row dictionaries
        geom_column_name (str): Name of the geometry column

    Returns:
        list: Rows with fixed geometries
    """
    print(f"Fixing geometries in '{geom_column_name}' column...")
    fixed_count = 0
    error_count = 0

    for idx, row in enumerate(rows):
        geom_wkt = row.get(geom_column_name, "")

        if not geom_wkt or (isinstance(geom_wkt, str) and geom_wkt.strip() == ""):
            continue  # Skip empty geometries

        try:
            geom = loads(str(geom_wkt))
            if not geom.is_valid:
                geom = geom.buffer(0)  # Fix invalid geometry
                row[geom_column_name] = geom.wkt
                fixed_count += 1
        except Exception as e:
            error_count += 1
            if error_count <= 5:  # Print first 5 errors
                print(f"  Row {idx}: Could not fix geometry - {str(e)[:50]}")

        if (idx + 1) % 500 == 0:
            print(f"  Processed {idx + 1} rows...")

    print(f"✓ Fixed {fixed_count} geometries ({error_count} errors)")
    return rows


def format_relationship(source_uuid, target_uuid, ontology_property, inverse_property):
    """
    Formats a relationship for Arches resource-instance-list field.
    Uses the official Arches format with resourceXresourceId as empty string.

    Args:
        source_uuid (str): Current resource identifier (not used in target format)
        target_uuid (str): Related resource identifier (parent UUID)
        ontology_property (str): Directional CRM property
        inverse_property (str): Reverse directional CRM property

    Returns:
        str: Relationship JSON string in official Arches format
    """
    if not target_uuid:
        return ""

    # Official Arches format: resourceId, ontologyProperty, resourceXresourceId (empty), inverseOntologyProperty
    return f'[{{"resourceId":"{target_uuid}","ontologyProperty":"{ontology_property}","resourceXresourceId":"","inverseOntologyProperty":"{inverse_property}"}}]'


def parse_level(level_str):
    """Extract numeric level from 'Level X' format."""
    level_str = level_str.strip()
    try:
        if level_str.startswith("Level "):
            return int(level_str.replace("Level ", "").strip())
        else:
            return int(level_str)
    except (ValueError, AttributeError):
        return -1


def process_row(row, lookup_map):
    """
    Processes a single row, updating relationships using embedded UUIDs.
    Searches for parent entries by name, hierarchical level, and country.

    Args:
        row (dict): CSV row data
        lookup_map (dict): Pre-built map of (name, level, country) -> uuid

    Returns:
        dict: Modified row with relationship strings
    """
    current_level = parse_level(row.get("Administrative level", ""))
    source_uuid = row.get("uuid", "")
    country = row.get("Country", "").strip()

    # Process 'Related to' relationship
    if row.get("Related to"):
        related_to_uuid = row.get("uuid", "")
        row["Related to"] = format_relationship(
            source_uuid,
            related_to_uuid,
            "http://www.cidoc-crm.org/cidoc-crm/P106_is_composed_of",
            "http://www.cidoc-crm.org/cidoc-crm/P106_forms_part_of"
        )

    # Process 'Part of' relationship
    if row.get("Part of"):
        part_of_value = row.get("Part of", "").strip()
        if part_of_value:
            part_of_lower = strip_accents(part_of_value).lower()
            # Find parent with same name but one level higher
            # Search within the same country, except "Africa" is searched globally
            part_of_uuid = find_parent_by_name_and_level(
                part_of_lower, current_level, lookup_map, country
            )
            if part_of_uuid:
                row["Part of"] = format_relationship(
                    source_uuid,
                    part_of_uuid,
                    "http://www.cidoc-crm.org/cidoc-crm/P106_is_composed_of",
                    "http://www.cidoc-crm.org/cidoc-crm/P106i_forms_part_of"
                )
            else:
                row["_unmatched_part_of"] = part_of_value

    return row


def strip_accents(text):
    """Remove accents from characters for matching (e.g., Sédhiou -> Sedhiou)."""
    if not text:
        return text
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(text))
        if unicodedata.category(c) != 'Mn'
    )


def build_parent_lookup_map(all_rows):
    """
    Build a map of (name_normalized, level, country) -> uuid for fast parent lookup.
    Allows O(1) lookup while accounting for country-specific admin areas.
    Special case: "Africa" is stored with empty country string for cross-country matching.
    """
    lookup = {}
    for row in all_rows:
        admin_name = row.get("Administrative area name", "").strip()
        admin_level = parse_level(row.get("Administrative level", ""))
        admin_uuid = row.get("uuid", "")
        country = row.get("Country", "").strip()

        if admin_name and admin_uuid:
            name_normalized = strip_accents(admin_name).lower()
            # For "Africa", store with empty country so it's accessible from all countries
            if name_normalized == "africa":
                key = (name_normalized, admin_level, "")
            else:
                key = (name_normalized, admin_level, country)
            lookup[key] = admin_uuid

    return lookup


def find_parent_by_name_and_level(name_lower, current_level, lookup_map, country):
    """
    Find a parent entry using pre-built lookup map, filtered by country.
    Search by name and country, skipping entries at the same level (prevents self-linking).
    Special case: "Africa" is searched globally (uses empty country string).

    Args:
        name_lower (str): Name to search for (normalized)
        current_level (int): Current level (used to prevent self-linking)
        lookup_map (dict): Pre-built map of (name, level, country) -> uuid
        country (str): Country to restrict search to (empty for "Africa")

    Returns:
        str: UUID of matching entry, or empty string if not found
    """
    name_normalized = strip_accents(name_lower).lower()

    # Try to find a parent at a different level with the same name
    # Start from highest levels (geopolitical, Level 0) and go down
    for level in [-1, 0, 1, 2, 3, 4, 5]:  # -1 for Geopolitical/custom levels
        if level != current_level:
            # For "Africa", search with empty country (stored globally)
            if name_normalized == "africa":
                key = (name_normalized, level, "")
            else:
                # For country-specific areas, search within the same country
                key = (name_normalized, level, country)

            if key in lookup_map:
                return lookup_map[key]

    return ""


def sort_rows_by_hierarchy(rows):
    """
    Sort rows by Administrative level so parents are imported BEFORE children.
    Order: Geopolitical/Custom → Level 0 → Level 1 → Level 2 → ...

    Args:
        rows (list): List of processed row dictionaries

    Returns:
        list: Rows sorted by Administrative level (parents first)
    """
    def get_level_sort_key(row):
        level_str = row.get("Administrative level", "").strip()
        try:
            if level_str.startswith("Level "):
                return int(level_str.replace("Level ", "").strip())
            else:
                # Try to parse as int
                return int(level_str)
        except (ValueError, AttributeError):
            # Geopolitical/custom levels come FIRST (lowest key)
            return -1

    # Sort by level (ascending), then by name for consistency
    # Lower numbers = higher in hierarchy (imported first)
    sorted_rows = sorted(
        rows,
        key=lambda r: (
            get_level_sort_key(r),
            r.get("Administrative area name", "").strip()
        )
    )

    return sorted_rows


def build_uuid_lookup_map(all_rows):
    """
    Build a reverse lookup map: UUID -> (name, country, level) for validation.

    Args:
        all_rows (list): List of all row dictionaries

    Returns:
        dict: Map of UUID -> {'name': str, 'country': str, 'level': int}
    """
    uuid_map = {}
    for row in all_rows:
        uuid = row.get("uuid", "").strip()
        if uuid:
            uuid_map[uuid] = {
                'name': row.get("Administrative area name", "").strip(),
                'country': row.get("Country", "").strip(),
                'level': parse_level(row.get("Administrative level", ""))
            }
    return uuid_map


def validate_relationships(rows, all_rows):
    """
    Validate relationships: check for self-links, country matching, and level hierarchy.

    Args:
        rows (list): List of processed row dictionaries
        all_rows (list): List of all original rows for UUID lookup

    Returns:
        tuple: (is_valid, validation_errors) where validation_errors is a list of dicts
    """
    uuid_map = build_uuid_lookup_map(all_rows)
    validation_errors = []

    for row in rows:
        resource_id = row.get("ResourceID", row.get("uuid", ""))
        source_country = row.get("Country", "").strip()
        source_level = parse_level(row.get("Administrative level", ""))
        source_name = row.get("Administrative area name", "N/A")

        # Check 'Related to' relationships
        if row.get("Related to", "").startswith("[{"):
            try:
                relationships = json.loads(row["Related to"])
                for rel in relationships:
                    target_uuid = rel.get("resourceId", "").strip()

                    # Check for self-link
                    if target_uuid == resource_id:
                        validation_errors.append({
                            "type": "self_link",
                            "source_name": source_name,
                            "source_level": row.get("Administrative level", "N/A"),
                            "source_country": source_country,
                            "field": "Related to",
                            "message": f"Self-linked relationship detected"
                        })
                        continue

                    # Validate target UUID exists and check country/level
                    if target_uuid in uuid_map:
                        target_info = uuid_map[target_uuid]
                        target_country = target_info['country']
                        target_level = target_info['level']
                        target_name = target_info['name']

                        # For non-Africa entries, country must match
                        if target_name.lower() != "africa" and target_country != source_country:
                            validation_errors.append({
                                "type": "country_mismatch",
                                "source_name": source_name,
                                "source_country": source_country,
                                "target_name": target_name,
                                "target_country": target_country,
                                "field": "Related to",
                                "message": f"Country mismatch: {source_country} -> {target_country}"
                            })
                    else:
                        validation_errors.append({
                            "type": "missing_uuid",
                            "source_name": source_name,
                            "field": "Related to",
                            "target_uuid": target_uuid,
                            "message": f"Target UUID not found in data"
                        })
            except json.JSONDecodeError:
                pass

        # Check 'Part of' relationships
        if row.get("Part of", "").startswith("[{"):
            try:
                relationships = json.loads(row["Part of"])
                for rel in relationships:
                    target_uuid = rel.get("resourceId", "").strip()

                    # Check for self-link
                    if target_uuid == resource_id:
                        validation_errors.append({
                            "type": "self_link",
                            "source_name": source_name,
                            "source_level": row.get("Administrative level", "N/A"),
                            "source_country": source_country,
                            "field": "Part of",
                            "message": f"Self-linked relationship detected"
                        })
                        continue

                    # Validate target UUID exists and check country/level
                    if target_uuid in uuid_map:
                        target_info = uuid_map[target_uuid]
                        target_country = target_info['country']
                        target_level = target_info['level']
                        target_name = target_info['name']

                        # For non-Africa entries, country must match
                        if target_name.lower() != "africa" and target_country != source_country:
                            validation_errors.append({
                                "type": "country_mismatch",
                                "source_name": source_name,
                                "source_country": source_country,
                                "target_name": target_name,
                                "target_country": target_country,
                                "field": "Part of",
                                "message": f"Country mismatch: {source_country} -> {target_country}"
                            })

                        # Target level should be higher (lower number) in hierarchy
                        if target_level >= source_level and target_name.lower() != "africa":
                            validation_errors.append({
                                "type": "level_hierarchy",
                                "source_name": source_name,
                                "source_level": source_level,
                                "target_name": target_name,
                                "target_level": target_level,
                                "field": "Part of",
                                "message": f"Hierarchy violation: source level {source_level} should be under target level {target_level}"
                            })
                    else:
                        validation_errors.append({
                            "type": "missing_uuid",
                            "source_name": source_name,
                            "field": "Part of",
                            "target_uuid": target_uuid,
                            "message": f"Target UUID not found in data"
                        })
            except json.JSONDecodeError:
                pass

    return len(validation_errors) == 0, validation_errors
    """
    Add comment to entries with modified geometries.

    Args:
        rows (list): List of processed row dictionaries

    Returns:
        list: Rows with updated comments for geometry-modified entries
    """
    maeasam_ids_with_geometry_mods = {
        "ADMN-SEN-000000002",
        "ADMN-SEN-000000016",
        "ADMN-SEN-000000014",
        "ADMN-KEN-000000132"
    }

    geometry_mod_comment = "Geometry modified for Arches compatibility using the Shapely Python library."

    for row in rows:
        maeasam_id = row.get("MAEASaM ID", "").strip()
        if maeasam_id in maeasam_ids_with_geometry_mods:
            existing_comment = row.get("Comment", "").strip()
            if existing_comment:
                # Append to existing comment
                if geometry_mod_comment not in existing_comment:
                    row["Comment"] = f"{existing_comment} {geometry_mod_comment}"
            else:
                # Add new comment
                row["Comment"] = geometry_mod_comment

    return rows
    """
    Validate relationships: check for self-links, country matching, and level hierarchy.

    Args:
        rows (list): List of processed row dictionaries
        all_rows (list): List of all original rows for UUID lookup

    Returns:
        tuple: (is_valid, validation_errors) where validation_errors is a list of dicts
    """
    uuid_map = build_uuid_lookup_map(all_rows)
    validation_errors = []

    for row in rows:
        resource_id = row.get("ResourceID", row.get("uuid", ""))
        source_country = row.get("Country", "").strip()
        source_level = parse_level(row.get("Administrative level", ""))
        source_name = row.get("Administrative area name", "N/A")

        # Check 'Related to' relationships
        if row.get("Related to", "").startswith("[{"):
            try:
                relationships = json.loads(row["Related to"])
                for rel in relationships:
                    target_uuid = rel.get("resourceId", "").strip()

                    # Check for self-link
                    if target_uuid == resource_id:
                        validation_errors.append({
                            "type": "self_link",
                            "source_name": source_name,
                            "source_level": row.get("Administrative level", "N/A"),
                            "source_country": source_country,
                            "field": "Related to",
                            "message": f"Self-linked relationship detected"
                        })
                        continue

                    # Validate target UUID exists and check country/level
                    if target_uuid in uuid_map:
                        target_info = uuid_map[target_uuid]
                        target_country = target_info['country']
                        target_level = target_info['level']
                        target_name = target_info['name']

                        # For non-Africa entries, country must match
                        if target_name.lower() != "africa" and target_country != source_country:
                            validation_errors.append({
                                "type": "country_mismatch",
                                "source_name": source_name,
                                "source_country": source_country,
                                "target_name": target_name,
                                "target_country": target_country,
                                "field": "Related to",
                                "message": f"Country mismatch: {source_country} -> {target_country}"
                            })
                    else:
                        validation_errors.append({
                            "type": "missing_uuid",
                            "source_name": source_name,
                            "field": "Related to",
                            "target_uuid": target_uuid,
                            "message": f"Target UUID not found in data"
                        })
            except json.JSONDecodeError:
                pass

        # Check 'Part of' relationships
        if row.get("Part of", "").startswith("[{"):
            try:
                relationships = json.loads(row["Part of"])
                for rel in relationships:
                    target_uuid = rel.get("resourceId", "").strip()

                    # Check for self-link
                    if target_uuid == resource_id:
                        validation_errors.append({
                            "type": "self_link",
                            "source_name": source_name,
                            "source_level": row.get("Administrative level", "N/A"),
                            "source_country": source_country,
                            "field": "Part of",
                            "message": f"Self-linked relationship detected"
                        })
                        continue

                    # Validate target UUID exists and check country/level
                    if target_uuid in uuid_map:
                        target_info = uuid_map[target_uuid]
                        target_country = target_info['country']
                        target_level = target_info['level']
                        target_name = target_info['name']

                        # For non-Africa entries, country must match
                        if target_name.lower() != "africa" and target_country != source_country:
                            validation_errors.append({
                                "type": "country_mismatch",
                                "source_name": source_name,
                                "source_country": source_country,
                                "target_name": target_name,
                                "target_country": target_country,
                                "field": "Part of",
                                "message": f"Country mismatch: {source_country} -> {target_country}"
                            })

                        # Target level should be higher (lower number) in hierarchy
                        if target_level >= source_level and target_name.lower() != "africa":
                            validation_errors.append({
                                "type": "level_hierarchy",
                                "source_name": source_name,
                                "source_level": source_level,
                                "target_name": target_name,
                                "target_level": target_level,
                                "field": "Part of",
                                "message": f"Hierarchy violation: source level {source_level} should be under target level {target_level}"
                            })
                    else:
                        validation_errors.append({
                            "type": "missing_uuid",
                            "source_name": source_name,
                            "field": "Part of",
                            "target_uuid": target_uuid,
                            "message": f"Target UUID not found in data"
                        })
            except json.JSONDecodeError:
                pass

    return len(validation_errors) == 0, validation_errors


if __name__ == "__main__":
    # Read CSV file with all data first to support lookups
    try:
        with open(input_csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            all_data = list(reader)
            fieldnames = reader.fieldnames

    except FileNotFoundError:
        print(f"Error: File not found - {input_csv_file}")
        exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        exit(1)

    if not all_data:
        print("Error: Input CSV is empty or contains no data rows")
        exit(1)

    # Validate required columns
    required_columns = ["Administrative area name", "Part of", "uuid"]
    missing_columns = [col for col in required_columns if col not in fieldnames]
    if missing_columns:
        print(f"Error: Missing required columns in CSV: {missing_columns}")
        print(f"Available columns: {list(fieldnames)}")
        exit(1)

    # Fix geometries (find the WKT/Geometry column - typically first column)
    geom_column = None
    for col in fieldnames:
        if 'geometry' in col.lower() or col.upper() == 'WKT':
            geom_column = col
            break

    if geom_column:
        print(f"\nStep 1: Fixing invalid geometries...")
        all_data = fix_geometries(all_data, geom_column)
    else:
        print("Warning: No geometry column found (WKT or 'Geometry')")

    print(f"\nStep 2: Processing {len(all_data)} rows...")
    print(f"Building parent lookup map for fast searches...")
    parent_lookup = build_parent_lookup_map(all_data)
    print(f"  Map built: {len(parent_lookup)} (name, level) combinations found")

    print(f"Processing relationships...")

    # Process each row (using pre-built lookup map for fast parent searches)
    processed_rows = [process_row(row, parent_lookup) for row in all_data]

    # Validate that relationships were created
    relationship_count = sum(1 for row in processed_rows if row.get("Part of", "").startswith("[{"))
    unmatched_count = sum(1 for row in processed_rows if "_unmatched_part_of" in row)

    if relationship_count == 0:
        print("Error: No relationships were created!")
        if unmatched_count > 0:
            print(f"  {unmatched_count} rows have 'Part of' values that couldn't be matched to 'Administrative area name'")
            unmatched_values = set(row["_unmatched_part_of"] for row in processed_rows if "_unmatched_part_of" in row)
            print(f"  Unmatched values (first 10): {list(unmatched_values)[:10]}")
        exit(1)
    else:
        print(f"Created relationships for {relationship_count} rows")
        if unmatched_count > 0:
            print(f"Warning: {unmatched_count} rows have 'Part of' values that couldn't be matched")

    # Write output file, removing temporary helper columns
    try:
        # Remove rows where 'Part of' equals 'Africa' and remove unwanted columns
        filtered_rows = []
        africa_removed_count = 0
        for row in processed_rows:
            # Clear "Part of" value if it's "Africa", but keep the row
            if row.get("Part of", "").strip() == "Africa":
                row["Part of"] = ""
                africa_removed_count += 1
            filtered_rows.append(row)

        if africa_removed_count > 0:
            print(f"Removed 'Africa' value from {africa_removed_count} rows")

        print(f"Total rows in filtered data: {len(filtered_rows)}")

        # Sort rows by hierarchy (parents before children)
        print("Sorting rows by parent-child hierarchy...")
        filtered_rows = sort_rows_by_hierarchy(filtered_rows)

        # Debug: count levels after sorting
        level_0_after = sum(1 for r in filtered_rows if r.get("Administrative level", "").strip().startswith("Level 0"))
        level_1_after = sum(1 for r in filtered_rows if r.get("Administrative level", "").strip().startswith("Level 1"))
        level_2_after = sum(1 for r in filtered_rows if r.get("Administrative level", "").strip().startswith("Level 2"))
        print(f"After sorting - Level 0: {level_0_after}, Level 1: {level_1_after}, Level 2: {level_2_after}")

        # Validate relationships
        print("Validating relationships for self-links, country matching, and level hierarchy...")
        is_valid, validation_errors = validate_relationships(filtered_rows, all_data)
        if not is_valid:
            print(f"❌ ERROR: Found {len(validation_errors)} validation errors:")
            error_types = {}
            for error in validation_errors:
                error_type = error.get('type', 'unknown')
                if error_type not in error_types:
                    error_types[error_type] = []
                error_types[error_type].append(error)

            # Print errors grouped by type
            for error_type, errors in sorted(error_types.items()):
                print(f"\n  {error_type.upper()} ({len(errors)} errors):")
                for error in errors[:5]:  # Show first 5 of each type
                    print(f"    - {error.get('source_name', 'N/A')}: {error.get('message', 'Unknown error')}")
                if len(errors) > 5:
                    print(f"    ... and {len(errors) - 5} more")
            exit(1)
        else:
            print("✓ All relationships validated successfully")
            print(f"  ✓ No self-linked relationships")
            print(f"  ✓ All country assignments match")
            print(f"  ✓ All level hierarchies are valid")

        # Prepare fieldnames for output in correct order for Arches import
        columns_to_remove = {'fid', 'valid_on', 'valid_to', 'version', 'Official division', 'Administrative area name alternative'}

        # Define the desired column order for Arches import
        # Only include columns that are in the mapping
        desired_order = [
            'ResourceID',
            'MAEASaM ID',
            'Administrative area name',
            'Name type',
            'Part of',
            'Administrative level',
            'Country',
            'Description',
            'Comment',
            'Geometry (WKT)',
            'Upload date',
            'Uploader name'
        ]

        # Build output fieldnames in the desired order
        output_fieldnames = [col for col in desired_order if col in [
            'Seq', 'ResourceID', 'MAEASaM ID', 'Administrative area name', 'Name type',
            'Part of', 'Administrative level', 'Country', 'Description', 'Comment',
            'Geometry (WKT)', 'Upload date', 'Uploader name'
        ]]

        # Rename columns in all rows and add metadata
        columns_to_remove = {'fid', 'valid_on', 'valid_to', 'version', 'Official division', 'Administrative area name alternative'}

        for row in filtered_rows:
            # Rename uuid to ResourceID
            if "uuid" in row:
                row["ResourceID"] = row.pop("uuid")

            # Rename WKT to Geometry (WKT)
            if "WKT" in row:
                row["Geometry (WKT)"] = row.pop("WKT")

            # Clear empty/invalid geometries (e.g., "MULTIPOLYGON EMPTY")
            geom_value = row.get("Geometry (WKT)", "").strip()
            if not geom_value or "EMPTY" in geom_value.upper():
                row["Geometry (WKT)"] = ""

            # Remove unwanted columns
            for col in list(row.keys()):
                if col in columns_to_remove:
                    row.pop(col, None)

            # Remove temporary helper columns
            row.pop("_unmatched_part_of", None)

            # Add metadata to each row
            row["Upload date"] = upload_date
            row["Uploader name"] = uploader_name

            # Add geometry modification comments to specific entries
            maeasam_id = row.get("MAEASaM ID", "").strip()
            geometry_mod_comment = "Geometry modified for Arches compatibility using the Shapely Python library."
            if maeasam_id in {"ADMN-SEN-000000002", "ADMN-SEN-000000016", "ADMN-SEN-000000014", "ADMN-KEN-000000132"}:
                existing_comment = row.get("Comment", "").strip()
                if existing_comment:
                    if geometry_mod_comment not in existing_comment:
                        row["Comment"] = f"{existing_comment} {geometry_mod_comment}"
                else:
                    row["Comment"] = geometry_mod_comment

        with open(output_csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=output_fieldnames, extrasaction='ignore')
            writer.writeheader()

            # Rebuild each row in the correct column order
            for row in filtered_rows:
                ordered_row = {}
                for fieldname in output_fieldnames:
                    ordered_row[fieldname] = row.get(fieldname, '')
                writer.writerow(ordered_row)

        print(f"Successfully processed {len(filtered_rows)} rows!")
        print(f"Output saved to: {output_csv_file}")

    except Exception as e:
        print(f"Error writing file: {e}")
        exit(1)
