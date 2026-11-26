"""Stage exact GitHub connector bytes locally; never certify or execute a runtime.

Input is JSON, one complete record or a list of records. Records may be split
into numbered base64 chunks (split the base64 text, not the decoded bytes).
No network access, cloud storage, or credentials are required by this helper.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re


def stage(records, directory):
    if isinstance(records, dict):
        records = [records]
    if not isinstance(records, list) or not records:
        raise ValueError('NONEMPTY_RECORD_LIST_REQUIRED')
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    results = []
    for row in records:
        sha = row['sha']
        if not isinstance(sha, str) or not re.fullmatch(r'[0-9a-f]{40}', sha):
            raise ValueError('GIT_SHA1_REQUIRED')
        if row['encoding'] != 'base64':
            raise ValueError('BASE64_REQUIRED')
        data = row['content']
        if not isinstance(data, str):
            raise ValueError('BASE64_TEXT_REQUIRED')
        data = ''.join(data.split())
        index, total = row.get('index', 0), row.get('total', 1)
        if type(index) is not int or type(total) is not int or not 0 <= index < total <= 10000:
            raise ValueError('CHUNK_INDEX_INVALID')
        parts = root / (sha + '.parts')
        parts.mkdir(exist_ok=True)
        marker = parts / 'total'
        if marker.exists() and marker.read_text() != str(total):
            raise ValueError('CHUNK_TOTAL_CONFLICT')
        marker.write_text(str(total))
        chunk = parts / str(index)
        if chunk.exists() and chunk.read_text() != data:
            raise ValueError('CHUNK_CONTENT_CONFLICT')
        chunk.write_text(data)
        if not all((parts / str(i)).is_file() for i in range(total)):
            results.append({'sha': sha, 'status': 'PARTIAL', 'received_index': index})
            continue
        payload = base64.b64decode(''.join((parts / str(i)).read_text() for i in range(total)), validate=True)
        actual = hashlib.sha1(b'blob ' + str(len(payload)).encode() + b'\0' + payload).hexdigest()
        if actual != sha:
            raise ValueError('GIT_BLOB_HASH_MISMATCH:' + sha)
        dest = root / sha
        if dest.exists() and dest.read_bytes() != payload:
            raise ValueError('EXISTING_BLOB_CONFLICT:' + sha)
        dest.write_bytes(payload)
        results.append({'sha': sha, 'status': 'BLOB_VERIFIED', 'bytes': len(payload)})
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records', type=Path)
    parser.add_argument('blob_directory', type=Path)
    args = parser.parse_args()
    print(json.dumps(stage(json.loads(args.records.read_text(encoding='utf-8')), args.blob_directory)))
