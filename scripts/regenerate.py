#!/usr/bin/env python3
"""Rebuild portable exports from the immutable connected-Sheets snapshot (stdlib only)."""
import collections, csv, hashlib, json, pathlib, re, sqlite3

ROOT = pathlib.Path(__file__).resolve().parents[1]
def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def scalar(cell):
    v = cell.get('effectiveValue', cell.get('userEnteredValue', {}))
    for key in ('stringValue', 'numberValue', 'boolValue', 'formulaValue'):
        if key in v: return v[key]
    if 'errorValue' in v: return json.dumps(v['errorValue'], ensure_ascii=False, sort_keys=True)
    return None
def main():
    metadata = json.loads((ROOT/'source/metadata.json').read_text())
    grids = {}
    for sheet in metadata['sheets']:
        p = sheet['properties']; grids[p['sheetId']] = (p, {})
    for path in sorted((ROOT/'source').glob('cells_*.json')):
        capture = json.loads(path.read_text())
        for sheet in capture['response']['sheets']:
            p, rows = grids[sheet['properties']['sheetId']]
            for block in sheet.get('data', []):
                for offset, row in enumerate(block.get('rowData', [])):
                    rn = block.get('startRow', 0) + offset + 1
                    assert rn not in rows, 'Overlapping capture'
                    rows[rn] = row.get('values', [])
    dbpath = ROOT/'heroscape.sqlite'
    if dbpath.exists(): dbpath.unlink()
    db = sqlite3.connect(dbpath)
    db.execute('PRAGMA foreign_keys=ON')
    db.executescript('CREATE TABLE source_sheets(sheet_id INTEGER PRIMARY KEY,title TEXT NOT NULL,row_count INTEGER NOT NULL,column_count INTEGER NOT NULL); CREATE TABLE source_cells(sheet_id INTEGER NOT NULL REFERENCES source_sheets(sheet_id),source_row INTEGER NOT NULL CHECK(source_row>0),source_column INTEGER NOT NULL CHECK(source_column>0),cell_json TEXT NOT NULL,PRIMARY KEY(sheet_id,source_row,source_column));')
    schema = {'version': 1, 'tables': []}; reports = []
    for sid, (p, rows) in grids.items():
        height = p['gridProperties']['rowCount']; width = p['gridProperties']['columnCount']
        assert set(rows) == set(range(1, height+1)), 'Incomplete grid capture'
        db.execute('INSERT INTO source_sheets VALUES(?,?,?,?)', (sid,p['title'],height,width))
        headers = [scalar(c) for c in rows[1]]
        headers += [None]*(width-len(headers))
        names = []; used = {'source_row'}
        for i,h in enumerate(headers):
            base = re.sub(r'[^a-z0-9]+','_',str(h or '').lower()).strip('_') or f'column_{i+1}'
            name = base; n = 2
            while name in used: name = f'{base}_{n}'; n += 1
            used.add(name); names.append(name)
        table = re.sub(r'[^a-z0-9]+','_',p['title'].lower()).strip('_') + ('' if len(grids)==1 else f'_{sid}')
        # No declared affinity on source columns: SQLite preserves each scalar storage type.
        db.execute(f'CREATE TABLE "{table}" (source_row INTEGER PRIMARY KEY CHECK(source_row>1),'+','.join('"'+n+'"' for n in names)+')')
        records = []; formulas = 0; errors = 0; types = [collections.Counter() for _ in names]
        for rn, cells in sorted(rows.items()):
            for ci,cell in enumerate(cells,1):
                if cell:
                    db.execute('INSERT INTO source_cells VALUES(?,?,?,?)',(sid,rn,ci,json.dumps(cell,ensure_ascii=False)))
                formulas += int('formulaValue' in cell.get('userEnteredValue',{}))
                errors += int('errorValue' in cell.get('effectiveValue',{}))
            if rn == 1 or not any(any(k in c for k in ('userEnteredValue','effectiveValue','note','hyperlink','textFormatRuns')) for c in cells): continue
            values = [scalar(c) for c in cells] + [None]*(width-len(cells))
            assert len(values)==width
            record = dict(zip(['source_row']+names,[rn]+values)); records.append(record)
            for i,v in enumerate(values): types[i][type(v).__name__] += 1
            db.execute(f'INSERT INTO "{table}" VALUES('+','.join('?' for _ in record)+')',list(record.values()))
        dump(ROOT/f'{table}.json', records)
        with (ROOT/f'{table}.csv').open('w',newline='',encoding='utf-8') as f:
            writer=csv.writer(f); writer.writerow(['source_row']+names)
            # Each source field is a JSON scalar, preserving null vs empty string and types.
            writer.writerows([[r['source_row']]+[json.dumps(r[n],ensure_ascii=False) for n in names] for r in records])
        reread=json.loads((ROOT/f'{table}.json').read_text()); assert reread==records
        with (ROOT/f'{table}.csv').open(newline='',encoding='utf-8') as f:
            parsed=[{'source_row':int(r['source_row']),**{n:json.loads(r[n]) for n in names}} for r in csv.DictReader(f)]
        assert parsed==records
        loaded=[dict(zip(['source_row']+names,r)) for r in db.execute(f'SELECT * FROM "{table}" ORDER BY source_row')]
        assert loaded==records
        schema['tables'].append({'name':table,'source_sheet_id':sid,'source_sheet_title':p['title'],'primary_key':'source_row','columns':[{'name':n,'source_column':i+1,'source_header':headers[i],'observed_types':dict(types[i]),'sqlite_affinity':'NONE'} for i,n in enumerate(names)]})
        reports.append({'sheet':p['title'],'captured_rows_including_header_and_blanks':height,'columns':width,'exported_records':len(records),'omitted_blank_data_rows':height-1-len(records),'formulas':formulas,'error_cells':errors,'csv_json_sqlite_roundtrip':'passed'})
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert not db.execute('PRAGMA foreign_key_check').fetchall()
    db.commit()
    (ROOT/'schema.sql').write_text('\n'.join(row[0]+';' for row in db.execute("SELECT sql FROM sqlite_master WHERE type='table' ORDER BY name"))+'\n')
    db.close(); dump(ROOT/'schema.json',schema); dump(ROOT/'validation.json',{'sqlite_integrity':'ok','foreign_keys':'ok','sheets':reports})
    files = sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name!='manifest.sha256' and '__pycache__' not in p.parts)
    (ROOT/'manifest.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(ROOT))+'\n' for p in files))
    print(json.dumps(reports,indent=2))
if __name__=='__main__': main()
