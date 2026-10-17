"""Validate built OG/Twitter metadata, actual image files, and deployment origins."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import argparse
import json
import subprocess
import re

class Metadata(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.meta = {}
        self.canonical = None
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta':
            self.meta.setdefault(a.get('property', a.get('name', '')), []).append(a.get('content', ''))
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical = a.get('href')

parser = argparse.ArgumentParser()
parser.add_argument('--origin', default='https://hallm.blog')
parser.add_argument('--report')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
dist = root / 'dist'
errors = []
local_images = set()
external_images = set()
for f in dist.rglob('*.html'):
    page = Metadata(f.read_text())
    values = page.meta.get('og:image', [])
    if len(values) != 1:
        errors.append(f'{f}: expected exactly one og:image')
        continue
    image = values[0]
    for raw in re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', f.read_text(), re.S):
        data = json.loads(raw)
        if data.get('@type') == 'BlogPosting' and data.get('image') != image:
            errors.append(f'{f}: JSON-LD/OG image differs')
    parsed = urlsplit(image)
    if parsed.scheme != 'https':
        errors.append(f'{f}: image must be absolute HTTPS: {image}')
    if page.meta.get('twitter:image') != [image]:
        errors.append(f'{f}: Twitter/OG image differs')
    if len(page.meta.get('og:type', [])) != 1:
        errors.append(f'{f}: duplicate or missing og:type')
    if urlsplit(page.meta.get('og:url', [''])[0]).netloc != urlsplit(args.origin).netloc:
        errors.append(f'{f}: social page URL uses wrong deployment')
    if urlsplit(page.canonical or '').netloc != 'hallm.blog':
        errors.append(f'{f}: canonical changed away from production')
    if parsed.netloc in ['hallm.blog', urlsplit(args.origin).netloc]:
        if parsed.netloc != urlsplit(args.origin).netloc:
            errors.append(f'{f}: social image uses wrong deployment: {image}')
        asset = dist / unquote(parsed.path).lstrip('/')
        if not asset.is_file():
            errors.append(f'{f}: advertised image missing: {image}')
        else:
            local_images.add(asset.relative_to(root).as_posix())
    else:
        external_images.add(image)
# Decode the bytes with the same image library used by the renderer, not HTTP status alone.
code = '''const sharp=require('sharp');let s='';process.stdin.on('data',d=>s+=d);process.stdin.on('end',async()=>{const result=[];for(const path of JSON.parse(s)){const m=await sharp(path).metadata();result.push({path,format:m.format,width:m.width,height:m.height});}console.log(JSON.stringify(result));});'''
decoded = subprocess.run(['node', '-e', code], cwd=root, input=json.dumps(sorted(local_images)), capture_output=True, text=True, check=True)
images = json.loads(decoded.stdout)
for image in images:
    if not image.get('width') or not image.get('height'):
        errors.append(f'Image has no valid dimensions: {image}')
    if image['path'].endswith('/index.png') and (image['width'],image['height']) != (1200,630):
        errors.append(f'Dynamic image is not 1200x630: {image}')
report = {'origin': args.origin, 'pages':len(list(dist.rglob('*.html'))), 'decodedLocalImages':images, 'externalImages':sorted(external_images), 'errors':errors}
if args.report:
    Path(args.report).write_text(json.dumps(report,indent=2)+'\n')
print(f'Social metadata: {report["pages"]} pages; {len(images)} local images decoded; {len(external_images)} external image URLs; {len(errors)} errors')
for error in errors:
    print(error)
raise SystemExit(bool(errors))
