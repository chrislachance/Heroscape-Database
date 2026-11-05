# Heroscape Database

Version: **1.0.1**

A portable snapshot of the community Heroscape unit database, captured November 5, 2026 from [Heroscape DB - Updated Nov '26](https://docs.google.com/spreadsheets/d/1eBKKa80J6z-1_J1iERKhIBYUVUJr_ZyWNH6rsONJ4aM/edit).

## Files

- `units.csv`: one record per populated source row, with original row numbers. Source fields contain JSON scalar literals inside RFC 4180 CSV fields, preserving numbers, strings, nulls, and explicit empty strings. The `source_row` field is an ordinary integer.
- `units.json`: the same records as JSON objects, preserving source values and column order.
- `heroscape.sqlite`: SQLite database containing the convenience `units` table and archival `source_sheets` and `source_cells` tables.
- `schema.json`: original headers, normalized field names, source column positions, observed types, and primary key documentation. Its numeric `version` denotes the schema format, independently of the release version.
- `schema.sql`: executable table definitions for the SQLite database.
- `source/metadata.json`: workbook and tab metadata, including grid dimensions.
- `source/cells_*.json`: bounded source captures containing entered values, effective values, notes, hyperlinks, and text format runs returned by the connector. Existing archived formatting and validation are retained from the prior snapshot; value fields were refreshed November 5. Comments, permissions, and revision history are not included.
- `scripts/regenerate.py`: dependency-free Python converter and validator for the saved snapshot. It produces the convenience exports, schema, validation report, and checksums.
- `validation.json`: source coverage, record counts, round-trip checks, SQLite integrity, and foreign-key results.
- `manifest.sha256`: SHA-256 checksums of package files except the manifest itself.
- `VERSION`: package release version.

## Data representation

The source contains one `Units` tab, 997 rows including the header, and 31 columns. Blank data rows remain represented in source captures but are omitted from convenience exports. Original row numbers are snapshot identifiers, not permanent unit identifiers. Duplicate records are preserved. Unnamed columns retain positional names. Values are not trimmed, deduplicated, or inferred.

Ability names and descriptions use separate `Ability name 1` / `Ability description 1` columns through ability 4, matching the live Sheet. Type `Hero` and Uniqueness `Unique` jointly represent a Unique Hero. Missing values become JSON null and SQL NULL; explicit empty strings remain empty strings. Source columns have no SQLite type affinity, preserving scalar storage types. Effective formula results are used when available; otherwise literal formula text is preserved.

## Release 1.0.1

Taega the Kyrie Warrior and Cupid were checked against the user-supplied master card images. Taega's class is corrected to Profiteer & Warrior. Cupid's Arrow Of Love 16 and Lovesickness descriptions now include the full card text. Ability names, including Flying, retain title case. All requested statistics were verified against the cards. Flying is listed without an added description because neither card prints one.

This snapshot uses the corrected source workbook, Heroscape DB - Updated Nov '26. Other live Sheet data is preserved as captured. The repository LICENSE is retained; this export makes no additional claim about rights to source content.
