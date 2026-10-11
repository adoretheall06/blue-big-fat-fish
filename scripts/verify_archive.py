"""Verify archived production files against the recorded SHA-256 manifest."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    manifest = json.loads((ROOT / 'artifact-manifest.json').read_text(encoding='utf-8'))
    failures = []
    for record in manifest['artifacts']:
        path = ROOT / record['path']
        if not path.is_file():
            failures.append(f'Missing: {record["path"]}')
            continue
        data = path.read_bytes()
        if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
            failures.append(f'Changed: {record["path"]}')
    if failures:
        raise SystemExit('\n'.join(failures))
    print(f'All {len(manifest["artifacts"])} archived production files verified.')

if __name__ == '__main__':
    main()
