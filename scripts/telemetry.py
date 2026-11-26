import json, os, urllib.request, urllib.parse
from collections import Counter
from xml.sax.saxutils import escape
from pathlib import Path

owner = os.environ.get('GITHUB_REPOSITORY_OWNER', 'Zylus08')
repos = []
for page in range(1, 101):
    url = f'https://api.github.com/users/{urllib.parse.quote(owner)}/repos?type=owner&per_page=100&page={page}'
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'profile-telemetry'}
    if os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
        batch = json.load(response)
    repos.extend(batch)
    if len(batch) < 100:
        break
else:
    raise RuntimeError('Pagination limit reached')
repos = [r for r in repos if not r['private'] and not r['fork'] and not r['archived'] and r['name'].lower() != owner.lower()]
langs = Counter(r['language'] for r in repos if r['language'])
rows = []
for i, (lang, count) in enumerate(langs.most_common(5)):
    y = 145 + i * 34
    width = 360 * count / max(1, len(repos))
    rows.append(f'<text x="30" y="{y}" fill="#c6d6e4" font-size="14">{escape(lang)}</text><rect x="235" y="{y-12}" width="360" height="12" rx="4" fill="#26354b"/><rect x="235" y="{y-12}" width="{width:.2f}" height="12" rx="4" fill="#72d6cf"/><text x="620" y="{y}" fill="#c6d6e4" font-size="14">{count} repos</text>')
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 330"><rect width="900" height="330" rx="12" fill="#101725"/><g font-family="monospace"><text x="30" y="35" fill="#72d6cf" font-size="16">PUBLIC REPOSITORY TELEMETRY</text><text x="30" y="78" fill="#f1f5f9" font-size="23">{len(repos)} repositories</text><text x="360" y="78" fill="#f1f5f9" font-size="23">{sum(r["stargazers_count"] for r in repos)} stars</text><text x="30" y="110" fill="#a7b8c9" font-size="13">PRIMARY LANGUAGE / REPOSITORY COUNT</text>{"".join(rows)}</g></svg>'
Path('assets/telemetry.svg').write_text(svg + '\n', encoding='utf-8')
