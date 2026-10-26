# Thesaurus - CV Change Log

Every change made to a controlled-vocabulary source (`xml/`, `csv/`, `xlsx/`, or the running Arches) - one row per change, newest first. Open differences that were found but not fixed belong in `CV_Task_List.md`; how sources are compared is in `CV_Instructions_and_Protocols.md` ("Comparison protocol").

| Date | Source / file | Change | Why | Decided by |
|---|---|---|---|---|
| 2026-10-26 | `csv/Resource type.csv` | Added row `Thesis` - Term ID `762d5545-163a-4edc-a1d2-3d5cc8d7f82e`, Parent Term ID `6db0b215-ae7b-40c5-bdbd-3e5135ff6030` (Publication), both taken from the current Arches export (`xml/`); other columns empty. Inserted after `Book`. | Term exists in Arches (added by OU 2026-09-11 per `CV_TermUpdate_Tracker.xlsx`) and is used by 22 records in `Datasets/20260910_InfoDefault.csv`, but was missing from the csv. | User |
| 2026-10-26 | `xml/` (both files) | Replaced with a fresh export from the running Arches (concept UUIDs changed, collection ids unchanged). | Before the planned fresh rebuild. | User (exported) |
