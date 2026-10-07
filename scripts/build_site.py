"""Build static blog pages from posts/*.md; never edits the source posts."""
from pathlib import Path
from datetime import date, datetime
from html import escape
import math
import re
import shutil
import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'

def text(value, field, path):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{path.name}: {field} must be non-empty text')
    return value.strip()

def read_post(path):
    source = path.read_text(encoding='utf-8')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)\Z', source, re.S)
    if not match:
        raise ValueError(f'{path.name}: start with YAML metadata between two --- lines')
    metadata = yaml.safe_load(match[1])
    if not isinstance(metadata, dict):
        raise ValueError(f'{path.name}: metadata must be a mapping')
    draft = metadata.get('draft', False)
    if not isinstance(draft, bool):
        raise ValueError(f'{path.name}: draft must be true or false without quotes')
    if draft:
        return None
    slug = path.stem
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        raise ValueError(f'{path.name}: use a lowercase filename with words separated by hyphens')
    title = text(metadata.get('title'), 'title', path)
    summary = text(metadata.get('summary'), 'summary', path)
    published = metadata.get('date')
    if isinstance(published, datetime):
        published = published.date()
    elif isinstance(published, str):
        published = date.fromisoformat(published)
    if not isinstance(published, date):
        raise ValueError(f'{path.name}: date must be YYYY-MM-DD')
    body = match[2].strip()
    if not body:
        raise ValueError(f'{path.name}: article body is empty')
    minutes = max(1, math.ceil(len(body.split()) / 200))
    return dict(slug=slug, title=title, summary=summary, date=published,
                category=text(metadata.get('category', 'Network engineering'), 'category', path),
                author=text(metadata.get('author', 'CX22TECH'), 'author', path),
                minutes=minutes, html=markdown.markdown(body, extensions=['fenced_code', 'tables', 'sane_lists']))

def display_date(value):
    return f'{value.day} {value.strftime("%B")} {value.year}'

def meta(post, author=False):
    label = post['author'] if author else post['category']
    return (f'<div class="post-meta"><span>{escape(label)}</span>'
            f'<time datetime="{post["date"].isoformat()}">{display_date(post["date"])}</time>'
            f'<span>{post["minutes"]} min read</span></div>')

def render(template, title, description, prefix, body):
    # One pass means content cannot accidentally act as another template token.
    values = {'TITLE': escape(title), 'DESCRIPTION': escape(description, quote=True),
              'PREFIX': prefix, 'BODY': body}
    return re.sub(r'\{\{(TITLE|DESCRIPTION|PREFIX|BODY)\}\}', lambda m: values[m[1]], template)

def main():
    # Validate all metadata before touching a previous output build.
    posts = [post for path in sorted((ROOT / 'posts').glob('*.md')) if (post := read_post(path))]
    posts.sort(key=lambda p: (p['date'], p['slug']), reverse=True)
    template = (ROOT / 'templates/page.html').read_text(encoding='utf-8')
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for name in ('index.html', 'CNAME', 'robots.txt', 'favicon.ico'):
        if (ROOT / name).exists():
            shutil.copy2(ROOT / name, OUT / name)
    for name in ('assets', 'images'):
        if (ROOT / name).is_dir():
            shutil.copytree(ROOT / name, OUT / name)
    (OUT / '.nojekyll').touch()
    blog = OUT / 'blog'
    blog.mkdir()
    cards = []
    for i, post in enumerate(posts, 1):
        title, summary, slug = escape(post['title']), escape(post['summary']), post['slug']
        cards.append(f'<article class="post-card"><div class="post-number" aria-hidden="true">{i:02d}</div>'
                     f'<div>{meta(post)}<h2><a href="{slug}/">{title}</a></h2><p>{summary}</p>'
                     f'<a class="button secondary" href="{slug}/">Read the article</a></div></article>')
        body = (f'<div class="blog-hero"><div class="wrap"><a class="back-link" href="../">All articles</a>'
                f'<p class="eyebrow">{escape(post["category"])}</p><h1>{title}</h1>{meta(post, True)}</div></div>'
                f'<article class="reading article-body" aria-label="{title}">{post["html"]}</article>')
        folder = blog / slug
        folder.mkdir()
        (folder / 'index.html').write_text(render(template, post['title'], post['summary'], '../../', body), encoding='utf-8')
    cards_html = ''.join(cards) or '<p class="empty-blog">No articles yet. Check back soon for updates from CX22TECH.</p>'
    body = ('<div class="blog-hero"><div class="wrap"><p class="eyebrow">The CX22TECH blog</p>'
            '<h1>Notes on better<br><span>connections.</span></h1>'
            '<p class="lead">Network engineering, cloud connectivity and documentation as code.</p></div></div>'
            f'<section class="wrap blog-list" aria-label="Latest articles">{cards_html}</section>')
    (blog / 'index.html').write_text(render(template, 'Blog', 'Network engineering ideas and company updates from CX22TECH.', '../', body), encoding='utf-8')
    print(f'Built {len(posts)} published article(s) in {OUT}')

if __name__ == '__main__':
    main()
