"""Read the fixed RSI-HA evidence snapshot using only the Python standard library."""
from pathlib import Path
import csv
import json

root = Path(__file__).resolve().parents[1]
snapshot = root / 'snapshots/2026-11-04'
studies = json.loads((snapshot / 'evidence_map.json').read_text(encoding='utf-8'))
rows = list(csv.DictReader((snapshot / 'evidence_map.csv').open(encoding='utf-8-sig')))
assert len(studies) == len(rows) == 85
assert {x['key'] for x in studies} == {x['key'] for x in rows}
memory = [x for x in studies if 'memory' in x['update_target'].lower()]
print(f'{len(studies)} studies; {len(memory)} mention memory in the update target.')
example = next(x for x in studies if x['key'] == 'medhospital2024')
print(example['name'])
print(example['independent_evaluation'])
for locator in example['locators']:
    print(locator['location'], locator['url'])
