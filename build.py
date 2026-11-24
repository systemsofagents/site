from html import escape
from pathlib import Path
import re, json, shutil
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'content'
ASSETS=ROOT/'dist'
TOKEN=re.compile(r'`([^`]+)`|\[([^\]\n]+)\]\(([^\s()]+)\)')
def inline(text):
    result=[]; start=0
    for m in TOKEN.finditer(text):
        result.append(escape(text[start:m.start()]))
        if m[1] is not None:
            result.append('<code>'+escape(m[1])+'</code>')
        else:
            href=m[3]; url=urlsplit(href)
            safe=not any(ord(c)<33 for c in href) and '\\' not in href and ((url.scheme in ('https','http') and url.netloc) or (not url.scheme and not url.netloc and not href.startswith('//')))
            result.append('<a href="'+escape(href,quote=True)+'">'+escape(m[2])+'</a>' if safe else escape(m[0]))
        start=m.end()
    return ''.join(result)+escape(text[start:])

def markdown(source):
    out=[]; paragraph=[]; listing=None; fence=None
    def flush():
        if paragraph:
            out.append('<p>'+inline(' '.join(paragraph))+'</p>'); paragraph.clear()
    def close_list():
        nonlocal listing
        if listing: out.append('</'+listing+'>'); listing=None
    for line in source.splitlines():
        if fence is not None:
            if re.fullmatch(r'```\s*',line):
                out.append('<pre><code>'+escape('\n'.join(fence))+'</code></pre>'); fence=None
            else: fence.append(line)
            continue
        if re.fullmatch(r'```[\w+-]*\s*',line):
            flush(); close_list(); fence=[]; continue
        h=re.match(r'^(#{1,5})\s+(.+)$',line)
        item=re.match(r'^\s*(-|\d+\.)\s+(.+)$',line)
        if h:
            flush(); close_list(); level=len(h[1])+1
            out.append(f'<h{level}>{inline(h[2])}</h{level}>')
        elif item:
            flush(); tag='ul' if item[1]=='-' else 'ol'
            if tag!=listing:
                close_list(); listing=tag; out.append('<'+tag+'>')
            out.append('<li>'+inline(item[2])+'</li>')
        elif not line.strip(): flush(); close_list()
        else: close_list(); paragraph.append(line.strip())
    if fence is not None: out.append('<pre><code>'+escape('\n'.join(fence))+'</code></pre>')
    flush(); close_list()
    return '\n'.join(out)

def render(template, dest, md, values):
    source=md.read_text(encoding='utf-8')
    html=(ROOT/'templates'/template).read_text(encoding='utf-8')
    replacements={'MARKDOWN':markdown(source),'MARKDOWN_RAW':escape(source), **values}
    for key,value in replacements.items(): html=html.replace('%%'+key+'%%',value)
    if re.search(r'%%[A-Z_]+%%',html): raise ValueError('Unfilled template')
    dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(html,encoding='utf-8')
    return html

def main():
    ASSETS.mkdir(exist_ok=True)
    for file in ('terminal.css','terminal.js','favicon.svg'):
        shutil.copyfile(ROOT/'static'/file, ASSETS/file)
    for file in ("logos/mark-dark.svg","icons/icon-180.png","social/og-home.png","social/og-track-01.png"):
        target=ASSETS/"brand"/file
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/"brand"/file,target)
    docs=[]; pages={}
    track=SOURCE/'tracks'/'01'
    for md in sorted(track.glob('*.md')):
        if md.name=='README.md': continue
        if not re.fullmatch(r'\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*\.md',md.name):
            raise ValueError(f'Invalid experiment filename: {md.name}')
        title=md.read_text(encoding='utf-8').splitlines()[0]
        if not title.startswith('# '): raise ValueError(f'Expected a top-level heading: {md.name}')
        slug=md.stem
        docs.append(f'<li><a href="/tracks/01/{slug}/">{escape(title[2:])}</a></li>')
        target=ASSETS/'tracks'/'01'/slug/'index.html'
        pages['/tracks/01/'+md.name]=(target, '/tracks/01/'+slug+'/', render('experiment.html',target,md,{'TITLE':escape(title[2:]),'SLUG':slug}))
    pages['/README.md']=(ASSETS/'index.html','/',render('home.html',ASSETS/'index.html',SOURCE/'README.md',{}))
    target=ASSETS/'tracks'/'01'/'index.html'
    pages['/tracks/01/README.md']=(target,'/tracks/01/',render('track.html',target,track/'README.md',{'EXPERIMENTS':'<ul aria-label="Experiments">'+''.join(docs)+'</ul>' if docs else ''}) )
    assemble(pages)

def assemble(pages):
    from html import unescape
    from posixpath import dirname, normpath
    fs={}; shells={}
    for key,(target,url,html) in pages.items():
        before,split=re.split(r'</header>',html,maxsplit=1)
        contents,after=split.split('<form class="command"',1)
        def replace_link(match):
            href=unescape(match[1])
            root_path=normpath(href if href.startswith('/') else dirname(key)+'/'+href) if href.lower().endswith('.md') and not urlsplit(href).scheme else None
            chosen=root_path if root_path in pages else next((k for k,rec in pages.items() if rec[1]==href),None)
            return f'href="{pages[chosen][1]}" data-file="{chosen}"' if chosen else match[0]
        contents=re.sub(r'href="([^"]*)"',replace_link,contents)
        contents=re.sub(r'(<h1)(>)',r'\1 tabindex="-1"\2',contents)
        contents=re.sub(r'<template id="document-source">.*?</template>','',contents,flags=re.S)
        title=unescape(re.search(r'<title>(.*?)</title>',html)[1])
        fs[key]={'url':url,'html':contents,'title':title}
        shells[key]=(target,before,after)
    payload=json.dumps(fs,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    for key,(target,before,after) in shells.items():
        echo="README.md" if key=="/README.md" else key
        content=re.sub(r'<code>cat [^<]*</code>',lambda m:'<code>cat '+escape(echo)+'</code>',fs[key]['html'],count=1)
        html=before+'</header>\n<div id="screen">'+content+'</div>\n<form class="command"'+after
        html=html.replace('</body>','<script id="virtual-files" type="application/json">'+payload+'</script></body>')
        target.write_text(html,encoding='utf-8')

if __name__=='__main__': main()
