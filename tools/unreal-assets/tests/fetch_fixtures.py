"""Fetch only the pinned public test files; not used by the asset reader."""
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'fixtures.json').read_text(encoding='utf-8'))
    target = root / 'fixtures'
    target.mkdir(exist_ok=True)
    for item in manifest['files']:
        path = target / item['name']
        if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256']:
            print(f"verified {item['name']}")
            continue
        url = f"https://raw.githubusercontent.com/atenfyr/UAssetAPI/{manifest['revision']}/{item['path']}"
        with urlopen(Request(url, headers={'User-Agent': 'OneStep-tests'}), timeout=30) as response:
            data = response.read(2_000_001)
        if len(data) > 2_000_000 or hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError(f"Untrusted fixture content: {item['name']}")
        path.write_bytes(data)
        print(f"fetched {item['name']}")


if __name__ == '__main__':
    main()
