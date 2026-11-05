# Heroscape Database

Version: **1.0.2**

Snapshot of [Heroscape DB - Updated Nov '26](https://docs.google.com/spreadsheets/d/1eBKKa80J6z-1_J1iERKhIBYUVUJr_ZyWNH6rsONJ4aM/edit), captured November 5, 2026: 366 units, 367 sheet rows including the header, and 31 columns.

## Files

- `units.json`: unit records.
- `units.csv`: the same records as CSV.
- `heroscape.sqlite`: unit data and source-cell archive.
- `schema.json` / `schema.sql`: field mappings and table definitions.
- `source/`: Sheet metadata, values, notes, and links.
- `scripts/regenerate.py`: export builder and validator.
- `validation.json`: integrity and consistency results.
- `manifest.sha256`: file checksums.
- `VERSION`: release number.

CSV source fields are JSON scalars; decode them after parsing CSV. `source_row` is an integer identifying the original Sheet row. Nulls, empty strings, duplicates, and separate ability names/descriptions are preserved. Source captures omit formatting, validation, comments, and revision history.

The repository LICENSE is retained.
