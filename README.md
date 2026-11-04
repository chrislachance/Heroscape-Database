# Heroscape-Database

Free community-available Heroscape Unit database, up-to-date with upcoming figures in 2027.

Source: [Heroscape DB – Google Sheet](https://docs.google.com/spreadsheets/d/1eBKKa80J6z-1_J1iERKhIBYUVUJr_ZyWNH6rsONJ4aM/edit?gid=2046690831#gid=2046690831).

Captured through the connected Google Drive/Sheets integration on November 4, 2026. Workbook title: `Heroscape DB - Updated Nov '26`; source locale `en_US`, time zone `America/Los_Angeles`. This is a snapshot; the online source can change. Source modification time before and after capture: `2026-11-04T12:45:07.877Z`.

## Contents

- `units.csv`: UTF-8, RFC 4180 quoting, one header row, 366 source records. **Source fields contain JSON scalar literals inside CSV fields**: decode with `json.loads` after CSV parsing. This preserves null, empty strings, numbers, booleans, Unicode, and literal text without ambiguous sentinel values. `source_row` is an ordinary integer. Spreadsheet programs may show the JSON string quotes; this is intentional. Formula-like source text remains quoted JSON text.
- `units.json`: array of objects with JSON scalar values, using the same field names and order as CSV.
- `heroscape.sqlite`: portable SQLite 3 database with `units`, `source_sheets`, and `source_cells` tables. Example: `SELECT unit_name, cost FROM units ORDER BY cost;`.
- `schema.json`: exact source header-to-field mappings, column coordinates, observed types, and primary key documentation. `schema.sql`: executable DDL.
- `source/metadata.json` and `source/cells_*.json`: complete connector CellData responses for all 997 rows × 27 columns, including header, blank rows, formatting, hyperlinks, and any other properties returned by the connector. These are the archival source of truth; no cell properties were deliberately discarded.
- `scripts/regenerate.py`: dependency-free Python 3 converter and validator.
- `validation.json`: counts and integrity results. `manifest.sha256`: checksums of all project files except itself.

## Schema and preservation

The workbook exposes exactly one tab, `Units` (sheet ID `2046690831`); all tabs were included. The first row supplies 26 named columns. The unnamed 27th column is retained as `column_27`. Header names are normalized to lower-case underscores; mappings retain original spelling and position. No descriptions, unit identities, relationships, or missing values were guessed.

`source_row` is the original one-based sheet row and is the primary key for this snapshot. It is not a permanent unit identifier across sheet edits. Duplicate names and duplicate records are permitted and preserved. Source data columns have no SQLite type affinity, preventing unwanted text-to-number conversion. No unsupported uniqueness or foreign-key assumptions are imposed on game data. Archival cells reference `source_sheets` with an enforced foreign key and a composite coordinate primary key.

There are 366 populated data rows and 630 blank data rows. Blank rows are omitted only from the convenience `units` exports; their positions, formatting and full grid dimensions remain in `source/` and the archival SQLite tables. Missing cell values become JSON null / SQL NULL; explicit empty strings remain empty strings. Values are not trimmed, corrected, split, deduplicated, or inferred. Embedded line breaks and URLs are preserved. SQLite `source_cells.cell_json` preserves each nonempty CellData object, including formatting-only cells; absent trailing cells are represented by grid dimensions and the full raw response.

The converter uses effective values when supplied, otherwise entered values. If a future snapshot contains formulas without effective values, their literal formula text is exported rather than evaluated or guessed. Formula text and original cell metadata remain in the archive. This snapshot has zero formulas and zero reported error cells. Error objects, if supplied in future captures, are serialized as JSON text in the convenience exports and preserved structurally in archival cells. Display formatting is retained in archival CellData rather than imposed on typed values. JSON numbers follow the numeric precision delivered by Google Sheets; no original pre-import numeric precision is claimed.

The archive preserves everything returned by these bounded CellData reads, not a complete Google Drive backup: file comments, revision history, permissions, and workbook features outside the returned metadata/CellData are not included.

## Regeneration

From the project directory, run:

```sh
python3 scripts/regenerate.py
```

This rebuilds CSV, JSON, SQLite, schema, validation, and checksums from the saved snapshot using only Python's standard library. Generated files are replaced; keep edits in a separate location. It verifies full grid row coverage, source row identities, exact CSV/JSON/SQLite scalar round trips, SQLite integrity and foreign keys. Check the manifest on macOS with `shasum -a 256 -c manifest.sha256`.

To refresh from the live source, use the connected Google Drive/Sheets integration: read workbook metadata first, then read every tab with `get_spreadsheet_cells` using exact metadata-derived names and bounded ranges. For this snapshot the reads were `'Units'!A1:AA100`, then 100-row chunks through `'Units'!A901:AA997`. Save the metadata structured response in `source/metadata.json`. Save each cells structured response as `{"requestedRange":"<exact A1 range>","response":<structured response>}` in `source/cells_0001.json`, etc. Remove obsolete chunk files, include hidden tabs when metadata exposes them, and use new grid dimensions rather than assuming current bounds. Read source modification metadata before and after the capture and retry if it changed. Then run the converter. Fresh authentication and integration access are required only for refreshing the online snapshot, not for rebuilding these exports. Update this README's snapshot date, modification time, and counts when refreshing.

The existing repository LICENSE is retained; this export makes no additional claim about rights to source content.
