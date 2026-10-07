"""Check built local page, asset and fragment links before deployment."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1] / '_site'
class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = set()
        self.links = []
        self.h1 = 0
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'h1':
            self.h1 += 1
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])

def main():
    pages = {p.resolve(): Page(p.read_text(encoding='utf-8')) for p in ROOT.rglob('*.html')}
    for path, page in pages.items():
        if page.h1 != 1:
            raise ValueError(f'{path}: expected one main heading')
        for link in page.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            target = ROOT / unquote(parsed.path).lstrip('/') if parsed.path.startswith('/') else path.parent / unquote(parsed.path) if parsed.path else path
            target = target.resolve()
            if not target.is_relative_to(ROOT.resolve()):
                raise ValueError(f'{path}: link outside site: {link}')
            if target.is_dir():
                target /= 'index.html'
            if not target.exists():
                raise ValueError(f'{path}: missing link or image: {link}')
            if parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
                raise ValueError(f'{path}: missing section: {link}')
    print(f'Checked {len(pages)} HTML pages and all local links.')

if __name__ == '__main__':
    main()
