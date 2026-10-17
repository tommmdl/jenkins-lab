#!/usr/bin/env python3
"""Run success/failure drills against the local authenticated Jenkins."""
import base64
import http.cookiejar
import json
from pathlib import Path
import time
import urllib.parse
import urllib.request

BASE = 'http://127.0.0.1:8080/'
ROOT = Path(__file__).resolve().parent.parent
password = (ROOT / '.local/admin-password').read_text().strip()
auth = base64.b64encode(('admin:' + password).encode()).decode()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
opener.addheaders = [('Authorization', 'Basic ' + auth)]

def request(path, data=None, headers=None):
    return opener.open(urllib.request.Request(BASE + path, data=data, headers=headers or {}), timeout=20)

def get(path):
    with request(path) as response:
        return json.load(response)

for attempt in range(120):
    try:
        crumb = get('crumbIssuer/api/json')
        break
    except Exception:
        time.sleep(2)
else:
    raise SystemExit('Jenkins did not become ready within four minutes')
headers = {crumb['crumbRequestField']: crumb['crumb']}
out = ROOT / '.local/evidence'
out.mkdir(parents=True, exist_ok=True)
results = []
for failure, expected in [(False, 'SUCCESS'), (True, 'FAILURE')]:
    # First run defines parameters; subsequent runs use the parameterized endpoint.
    job = get('job/jenkins-lab/api/json')
    endpoint = 'buildWithParameters' if job['builds'] else 'build'
    data = urllib.parse.urlencode({'SIMULATE_FAILURE': str(failure).lower()}).encode()
    with request('job/jenkins-lab/' + endpoint, data=data, headers=headers) as response:
        queue_path = urllib.parse.urlsplit(response.headers['Location']).path.lstrip('/')
    deadline = time.monotonic() + 360
    while time.monotonic() < deadline:
        queued = get(queue_path + 'api/json')
        if queued.get('cancelled'):
            raise SystemExit('Build cancelled')
        if 'executable' in queued:
            number = queued['executable']['number']
            break
        time.sleep(2)
    else:
        raise SystemExit('Queue timeout')
    path = f'job/jenkins-lab/{number}/'
    while time.monotonic() < deadline:
        result = get(path + 'api/json')
        if not result['building']:
            break
        time.sleep(2)
    else:
        raise SystemExit('Build timeout')
    with request(path + 'consoleText') as response:
        (out / f'build-{number}.log').write_bytes(response.read())
    assert result['result'] == expected, (number, result['result'], expected)
    assert any(a['relativePath'] == 'artifacts/report.txt' for a in result['artifacts'])
    with request(path + 'artifact/artifacts/report.txt') as response:
        (out / f'build-{number}-report.txt').write_bytes(response.read())
    summary = {key: result[key] for key in ['number', 'result', 'duration', 'timestamp', 'artifacts']}
    results.append(summary)
    print(json.dumps(summary), flush=True)
(out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
