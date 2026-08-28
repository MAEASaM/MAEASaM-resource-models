# MAEASaM Resource Models

This repository contains the resources required to set up and populate the MAEASaM (Mapping Africa's Endangered Archaeological Sites and Monuments) Arches instance. It includes:

- **Templates** - CSV schemas for data entry
- **Guidelines** - written documentation and PDF guidance on how to complete the schemas
- **Thesaurus** - JSON files containing thesauri and collections
- **JSON Resource Models** - ready-to-ingest JSON structures for each resource model
- **Datasets** - default and initial setup datasets for each resource model

These resources define the core data structures used to represent archaeological sites, actors, chronology, information, maps, grids, remote sensing data, and administrative boundaries within the MAEASaM Arches instance.

## How to Set Up

The datasets and resource models must be ingested into Arches in a specific order. It is important to follow the setup sequence because some resource models and datasets are interdependent and rely on resources created during earlier steps.

Follow the setup instructions in the order provided to ensure that all dependencies are correctly established before ingesting the related datasets.

### Importing Resource Models into Arches

1. **Download the Models:**
   - Clone this repository or download the individual JSON files you need.

2. **Access Arches Management Console:**
   - Log in to your Arches instance with admin privileges.

3. **Import Models:**
   - Navigate to the *Resource Models* section.
   - Use the "Import" function to upload each JSON file (e.g., `Actor.json`, `Site.json`, etc.).
   - Follow the prompts to complete the import process for each model.

4. **Verify Models:**
   - After importing, check that each model appears in the list and is correctly configured.

## Files

- `Actor.json` — Defines actors and organizations.
- `Administrative Model.json` — Administrative boundaries and regions.
- `Chronology.json` — Chronological periods and events.
- `Information.json` — Information resources and documentation.
- `MAEASaM Grid.json` — Grid reference system for spatial data.
- `Remote sensing.json` — Remote sensing data and metadata.
- `Site.json` — Archaeological site definitions.

## Contributing

Contributions and suggestions are welcome. Please open an issue or submit a pull request for improvements or new models.

## License

See the repository for license information.
