"""Check source and production-route preservation after npm run build."""
from pathlib import Path
from urllib.parse import urlparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'scripts/upgrade-baseline.json').read_text())
errors = []
def check(ok, message):
    if not ok:
        errors.append(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None

for name, post in manifest['posts'].items():
    check(sha(root / 'src/content/blog' / name) == post['sha256'], f'Post changed: {name}')
    html = root / 'dist/posts' / post['slug'] / 'index.html'
    check(html.is_file() != post['draft'], f'Post visibility changed: {name}')
    if post['draft']:
        check(not html.parent.joinpath('index.png').exists(), f'Draft OG exposed: {name}')
for name, digest in manifest['assets'].items():
    check(sha(root / name) == digest, f'Original asset changed: {name}')
for url in manifest['urls']:
    path = urlparse(url).path.lstrip('/')
    check((root / 'dist' / path / 'index.html').is_file(), f'Production route missing: {url}')
    if (root / 'dist' / path / 'index.html').is_file():
        html = (root / 'dist' / path / 'index.html').read_text()
        check(f'rel="canonical" href="{url}"' in html, f'Canonical changed: {url}')
        check('Astro v6.' in html, f'Unexpected generator: {url}')
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = {loc.text for f in (root / 'dist').glob('sitemap-[0-9]*.xml') for loc in ET.parse(f).findall('s:url/s:loc', ns)}
check(urls == set(manifest['urls']), f'Sitemap differs: missing={set(manifest["urls"])-urls}, added={urls-set(manifest["urls"])}')
rss = (root / 'dist/rss.xml').read_text()
for name, post in manifest['posts'].items():
    check((f'/posts/{post["slug"]}/' in rss) != post['draft'], f'RSS visibility changed: {name}')
for f in (root / 'dist').rglob('*.html'):
    html = f.read_text()
    for src in re.findall(r'<img[^>]+src="([^"#?]+)', html):
        if src.startswith('/') and not src.startswith('//'):
            check((root / 'dist' / src.lstrip('/')).is_file(), f'Missing image: {src} on {f.relative_to(root)}')
home = (root / 'dist/index.html').read_text()
for url in manifest['socialUrls']:
    check(f'href="{url}"' in home, f'Missing social destination: {url}')
for path in manifest['legacyOgPaths']:
    check((root / 'dist' / path.lstrip('/')).is_file(), f'Legacy OG missing: {path}')
for slug, ids in manifest['headingIds'].items():
    html = (root / 'dist/posts' / slug / 'index.html').read_text()
    for id in ids:
        check(f'id="{id}"' in html, f'Heading anchor changed: {slug}#{id}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(manifest["posts"])} source posts, {sum(not p["draft"] for p in manifest["posts"].values())} published posts, {len(manifest["assets"])} original assets, {len(manifest["urls"])} routes/canonicals; RSS, sitemap, draft/OG visibility and local images preserved.')
