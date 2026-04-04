#!/usr/bin/env python3
"""Build requiem.rest HTML from markdown source files."""

import re, os

ROOT = os.path.dirname(os.path.abspath(__file__))


# ── Parsing ──────────────────────────────────────────────

def parse_frontmatter(text):
    m = re.match(r'^---\n(.*?)\n---\n?(.*)$', text, re.DOTALL)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).split('\n'):
        i = line.find(':')
        if i > 0:
            meta[line[:i].strip()] = line[i + 1:].strip()
    return meta, m.group(2)


def parse_blocks(md):
    blocks = []
    lines = md.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith('```'):
            lang = line[3:].strip()
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i])
                i += 1
            i += 1
            blocks.append(('code', lang, '\n'.join(code)))
            continue

        if line.startswith('## '):
            blocks.append(('h2', line[3:]))
            i += 1
            continue

        if line.strip() == '':
            i += 1
            continue

        m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', line)
        if m:
            blocks.append(('img', m.group(1), m.group(2)))
            i += 1
            continue

        if re.match(r'^[-–—]\s', line):
            items = []
            while i < len(lines) and re.match(r'^[-–—]\s', lines[i]):
                items.append(re.sub(r'^[-–—]\s+', '', lines[i]))
                i += 1
            blocks.append(('list', items))
            continue

        para = []
        while (i < len(lines)
               and lines[i].strip() != ''
               and not re.match(r'^#{1,2}\s', lines[i])
               and not lines[i].startswith('```')
               and not re.match(r'^[-–—]\s', lines[i])):
            para.append(lines[i])
            i += 1
        blocks.append(('p', ' '.join(para)))

    return blocks


# ── Rendering ────────────────────────────────────────────

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def inline(text):
    s = esc(text)
    s = re.sub(r'`([^`]+)`', r'<code class="il">\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    return s


def highlight_http(code):
    out = []
    for line in code.split('\n'):
        m = re.match(r'^(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS|TRACE|CONNECT)(\s+)(.+)$', line)
        if m:
            out.append(f'<span class="t-m">{m[1]}</span>{m[2]}<span class="t-u">{esc(m[3])}</span>')
            continue
        m = re.match(r'^([A-Za-z][A-Za-z0-9-]*)(:.*)$', line)
        if m:
            out.append(f'<span class="t-hn">{esc(m[1])}</span><span class="t-hv">{esc(m[2])}</span>')
            continue
        m = re.match(r'^(\s*)"([^"]+)"\s*:\s*"([^"]*)"(.*)$', line)
        if m:
            out.append(f'{m[1]}<span class="t-k">"{esc(m[2])}"</span>: <span class="t-s">"{esc(m[3])}"</span>{esc(m[4])}')
            continue
        out.append(esc(line))
    return '\n'.join(out)


def render_block(b):
    if b[0] == 'h2':
        return f'      <h2>{inline(b[1])}</h2>\n'
    if b[0] == 'p':
        return f'      <p>{inline(b[1])}</p>\n'
    if b[0] == 'list':
        items = ''.join(f'        <li>{inline(it)}</li>\n' for it in b[1])
        return f'      <ul>\n{items}      </ul>\n'
    if b[0] == 'code':
        content = highlight_http(b[2]) if b[1] == 'http' else esc(b[2])
        return f'      <pre><code>{content}</code></pre>\n'
    if b[0] == 'img':
        return f'      <img src="{esc(b[2])}" alt="{esc(b[1])}" loading="lazy">\n'
    return ''


# ── Page assembly ────────────────────────────────────────

def head(title, description, og_url, css_path='style.css', icon_path='icon.png'):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="theme-color" content="#0c0a0e">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:image" content="https://requiem.rest/icon.png">
  <meta property="og:url" content="{og_url}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary">
  <link rel="icon" type="image/png" href="{icon_path}">
  <link rel="apple-touch-icon" href="{icon_path}">
  <link rel="stylesheet" href="{css_path}">
</head>'''


def footer(landing=False):
    links = []
    if not landing:
        links.append('<a href="/">Home</a>')
    links.append('<a href="/support">Support</a>')
    links.append('<a href="/privacy">Privacy</a>')
    links.append('<a href="https://x-amz.dev">x-amz</a>')
    nav = '\n        '.join(links)
    return f'''
    <footer>
      <nav>
        {nav}
      </nav>
      <div class="copy">&copy; 2026 x-amz</div>
    </footer>'''


# ── Build: landing page ─────────────────────────────────

def build_landing():
    with open(os.path.join(ROOT, 'content', 'index.md')) as f:
        raw = f.read()

    meta, body = parse_frontmatter(raw)
    blocks = parse_blocks(body)

    abstract_blocks = []
    sections = []
    current = None
    for b in blocks:
        if b[0] == 'h2':
            current = {'heading': b[1], 'blocks': []}
            sections.append(current)
        elif current:
            current['blocks'].append(b)
        else:
            abstract_blocks.append(b)

    title = meta.get('title', 'Requiem')
    tagline = meta.get('tagline', '')
    desc = meta.get('description', '')
    store = meta.get('appstore', '#')

    # Meta block rows
    meta_rows = ''
    for key in ('status', 'category', 'platform', 'format'):
        if key in meta:
            label = key[0].upper() + key[1:]
            meta_rows += f'      <div class="row"><span class="label">{label}</span><span class="value">{esc(meta[key])}</span></div>\n'

    # Abstract
    abstract = ''
    for i, b in enumerate(abstract_blocks):
        if i == 0 and b[0] == 'p':
            abstract += f'      <p class="lead">{inline(b[1])}</p>\n'
        else:
            abstract += render_block(b)

    # Sections
    sec_html = ''
    for i, sec in enumerate(sections):
        sec_html += '    <div class="section">\n'
        sec_html += f'      <div class="section-id">&sect;{i + 1}</div>\n'
        sec_html += f'      <h2>{inline(sec["heading"])}</h2>\n'
        for b in sec['blocks']:
            if (b[0] == 'p' and b[1].startswith('*')
                    and b[1].endswith('*') and not b[1].startswith('**')):
                sec_html += f'      <p class="aside">{inline(b[1])}</p>\n'
            else:
                sec_html += render_block(b)
        sec_html += '    </div>\n\n'

    html = f'''{head(f"{title} — {tagline}", desc, "https://requiem.rest")}
<body>
  <div class="page">

    <header class="masthead">
      <img src="icon.png" alt="{esc(title)}" width="88" height="88">
      <div class="wordmark">{esc(title)}</div>
      <div class="tagline">{esc(tagline)}</div>
    </header>

    <hr>

    <div class="meta">
{meta_rows}    </div>

    <div class="abstract">
      <h2>Abstract</h2>
{abstract}    </div>

    <div class="cta">
      <a class="badge" href="{store}"><img src="img/appstore.svg" alt="Download on the App Store"></a>
    </div>

    <hr>

{sec_html}    <div class="ornament">&#x2726; &#x2726; &#x2726;</div>

    <div class="cta">
      <a class="badge" href="{store}"><img src="img/appstore.svg" alt="Download on the App Store"></a>
    </div>
{footer(landing=True)}
  </div>
  <div class="lightbox" onclick="this.classList.remove('active')">
    <img src="" alt="">
  </div>
  <script>
    document.querySelectorAll('.section img').forEach(function(img) {{
      img.addEventListener('click', function() {{
        var lb = document.querySelector('.lightbox');
        lb.querySelector('img').src = img.src;
        lb.querySelector('img').alt = img.alt;
        lb.classList.add('active');
      }});
    }});
    document.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape') document.querySelector('.lightbox').classList.remove('active');
    }});
  </script>
</body>
</html>
'''

    out = os.path.join(ROOT, 'index.html')
    with open(out, 'w') as f:
        f.write(html)


# ── Build: doc pages ─────────────────────────────────────

def build_doc(name):
    with open(os.path.join(ROOT, 'content', f'{name}.md')) as f:
        raw = f.read()

    meta, body = parse_frontmatter(raw)
    blocks = parse_blocks(body)

    title = meta.get('title', name.title())
    desc = meta.get('description', '')
    effective = meta.get('effective', '')

    content = f'      <h1>{esc(title)}</h1>\n'
    if effective:
        content += f'      <p class="effective">Effective {esc(effective)}</p>\n'
    for b in blocks:
        content += render_block(b)

    html = f'''{head(f"{title} — Requiem", desc, f"https://requiem.rest/{name}", css_path="../style.css", icon_path="../icon.png")}
<body>
  <div class="page">

    <a class="backlink" href="/">&larr; requiem.rest</a>

    <div class="doc">
{content}    </div>
{footer()}
  </div>
</body>
</html>
'''

    out_dir = os.path.join(ROOT, name)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'index.html'), 'w') as f:
        f.write(html)


# ── Main ─────────────────────────────────────────────────

if __name__ == '__main__':
    build_landing()
    build_doc('support')
    build_doc('privacy')
    print('Built: index.html, support/index.html, privacy/index.html')
