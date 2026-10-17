"""Check every built internal link, asset, fragment and social-image reference."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import argparse
import json
import re

class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids = set()
        self.refs = []
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'a' and a.get('name'):
            self.ids.add(a['name'])
        for key in ['href', 'src', 'poster']:
            if a.get(key):
                self.refs.append((f'{tag}.{key}', a[key]))
        if a.get('srcset'):
            self.refs.extend(('srcset', item.strip().split()[0]) for item in a['srcset'].split(',') if item.strip())
        if tag == 'meta' and a.get('property', a.get('name')) in ['og:image', 'twitter:image']:
            self.refs.append((a.get('property', a.get('name')), a.get('content', '')))

parser = argparse.ArgumentParser()
parser.add_argument('--report')
parser.add_argument('--preview-origin')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
dist = root / 'dist'
pages = {f: Page(f.read_text()) for f in dist.rglob('*.html')}
origins = {'hallm.blog'}
if args.preview_origin:
    origins.add(urlsplit(args.preview_origin).netloc)
errors = []
checked = set()
external = set()
fragments = set()
internal_count = 0
for file, page in pages.items():
    relative = file.relative_to(dist).as_posix()
    path = '/' + (relative[:-10] if relative.endswith('index.html') else relative)
    for kind, ref in page.refs:
        url = urlsplit(urljoin('https://hallm.blog' + path, ref))
        if url.scheme not in ['http', 'https']:
            continue
        if url.netloc not in origins:
            external.add(url.geturl())
            continue
        internal_count += 1
        target = dist / unquote(url.path).lstrip('/')
        if target.is_dir():
            target = target / 'index.html'
        checked.add((url.path, kind))
        if not target.is_file():
            errors.append({'page': path, 'kind': kind, 'url': ref, 'problem': 'missing target'})
            continue
        if url.fragment and target in pages:
            fragment = unquote(url.fragment)
            fragments.add((url.path, fragment))
            if fragment not in pages[target].ids:
                errors.append({'page': path, 'kind': kind, 'url': ref, 'problem': 'missing anchor'})
css_refs = 0
for css in list(dist.rglob('*.css')) + list(pages):
    css_path = '/' + css.relative_to(dist).as_posix()
    for ref in re.findall(r'url\(\s*[\"\']?([^\"\')\s]+)', css.read_text()):
        url = urlsplit(urljoin('https://hallm.blog' + css_path, ref))
        if url.scheme not in ['http', 'https'] or url.netloc not in origins:
            continue
        css_refs += 1
        checked.add((url.path, 'css.url'))
        if not (dist / unquote(url.path).lstrip('/')).is_file():
            errors.append({'page': css_path, 'kind': 'css.url', 'url': ref, 'problem': 'missing CSS asset'})
report = {'cssAssetReferences': css_refs, 'pages': len(pages), 'internalReferences': internal_count, 'uniqueInternalTargetsByKind': len(checked), 'uniqueAnchors': len(fragments), 'externalUrlsNotRequested': len(external), 'errors': errors, 'externalUrls': sorted(external), 'internalTargetPaths': sorted({path for path, kind in checked})}
if args.report:
    Path(args.report).write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['externalUrls', 'internalTargetPaths']}, indent=2))
raise SystemExit(bool(errors))
