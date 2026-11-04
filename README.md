# Heroscape-Database

Heroscape unit data from the [source Google Sheet](https://docs.google.com/spreadsheets/d/1eBKKa80J6z-1_J1iERKhIBYUVUJr_ZyWNH6rsONJ4aM/edit?gid=2046690831#gid=2046690831), captured November 4, 2026.

Some 2027 promotional figures, such as Cupid, may have inaccurate text due to the low quality of available reference images.

## Files and usage

- `units.json`: typed records, including `ability_name_1` / `ability_description_1` through pair 4.
- `units.csv`: UTF-8 CSV. Each source field contains a JSON scalar; parse CSV first, then use `json.loads` on each field except `source_row`.
- `heroscape.sqlite`: `units`, `source_sheets`, and `source_cells` tables. Example: `SELECT unit_name, cost FROM units ORDER BY cost;`
- `schema.json` / `schema.sql`: header mappings, observed types, and database DDL.
- `source/`: workbook metadata and full returned cell data, including formatting and blank rows.
- `validation.json` / `manifest.sha256`: validation results and file checksums.

The snapshot contains 366 records across 31 source columns. `source_row` is the original sheet row, not a permanent unit ID. Headers become lowercase underscore names; the unnamed column is retained as `column_31`. Values, duplicates, nulls, empty strings, and line breaks are preserved. Blank rows remain in the archive but are omitted from unit exports. SQLite source columns have no type affinity to avoid coercion.

## Rebuild

Run `python scripts/regenerate.py` with Python 3 (standard library only). It rebuilds exports from the saved snapshot and checks CSV/JSON/SQLite round trips, full row coverage, database integrity, and foreign keys.

To refresh the snapshot, read current Sheet metadata and bounded CellData ranges through the Sheets integration. Save metadata to `source/metadata.json` and each range as `{"requestedRange":"...","response":...}` in `source/cells_*.json`, replacing obsolete chunks. Capture every grid row and column, check that the source modification time stayed unchanged, then rebuild. These archives contain returned Sheet metadata/cells, not comments or revision history.

The repository LICENSE is retained; this export makes no additional claim about rights to source content.
