#!/usr/bin/env python3
"""Build the homepage from simple Markdown using Python's standard library only."""
from pathlib import Path
from html import escape
import re, shutil
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist'

def inline(text):
    text=escape(text,quote=True)
    text=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+|assets/[^\s)]+)\)',r'<a href="\2">\1</a>',text)
    return re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',text)

def slug(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return re.sub(r'[^a-z0-9]+','-',text.lower()).strip('-')

def markdown(text, bold_starred=False):
    out=[]; in_list=False; in_section=False; ids=[]
    for line in text.splitlines():
        line=line.strip()
        if not line:
            if in_list: out.append('</ul>'); in_list=False
            continue
        if line.startswith('# '): continue
        if line.startswith('## '):
            if in_list: out.append('</ul>'); in_list=False
            if in_section: out.append('</section>')
            title=line[3:]; ident=slug(title); ids.append((ident,title)); in_section=True
            out.append(f'<section class="content-section" id="{ident}"><h2>{inline(title)}</h2>')
        elif line.startswith('!['):
            m=re.fullmatch(r'!\[(.*?)\]\((.*?)\)',line)
            if m: out.append(f'<figure><img src="{escape(m[2])}" alt="{escape(m[1])}" loading="lazy"></figure>')
        elif line.startswith('- '):
            if not in_list: out.append('<ul>'); in_list=True
            entry = inline(line[2:])
            if bold_starred and line.rstrip().endswith('*'):
                entry = '<strong>'+entry+'</strong>'
            out.append('<li>'+entry+'</li>')
        else:
            if in_list: out.append('</ul>'); in_list=False
            out.append('<p>'+inline(line)+'</p>')
    if in_list: out.append('</ul>')
    if in_section: out.append('</section>')
    return '\n'.join(out),ids

def build():
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
    template=(ROOT/'templates/page.html').read_text()
    navitems=[('index.html','Home'),('research.html','Research'),('publications.html','Publications'),('cv.html','CV')]
    for key,title,kicker,description in [
        ('home','Home','Astronomy · Yonsei University','Exploring active galactic nuclei, their host galaxies, and the evolution of nearby galaxies.'),
        ('research','Research','Questions at the heart of galaxies','Black holes, their host galaxies, and the changing universe.'),
        ('publications','Publications','Journal articles & manuscripts','Research across active galaxies, black holes, infrared surveys, and galaxy evolution.'),
        ('cv','Curriculum vitae','Education · Experience · Community','Academic appointments, research, service, and students.')]:
        source=(ROOT/'content'/f'{key}.md').read_text()
        body,ids=markdown(source, bold_starred=(key=='publications'))
        filename='index.html' if key=='home' else key+'.html'
        nav=''.join(f'<a href="{url}"'+(' aria-current="page"' if url==filename else '')+f'>{label}</a>' for url,label in navitems)
        side='<aside class="section-nav" aria-label="On this page"><p class="eyebrow">On this page</p>'+''.join(f'<a href="#{i}">{escape(t)}</a>' for i,t in ids)+'</aside>'
        tools=''
        if key=='publications':
            count=sum(1 for l in source.splitlines() if l.startswith('- '))
            tools=f'<div class="pub-tools" hidden><label for="pub-search">Search publications</label><input type="search" id="pub-search" placeholder="Title, author, journal, or year" autocomplete="off"><p id="pub-count" role="status">{count} publications & manuscripts</p></div><p id="no-results" hidden>No publications match your search.</p>'
        if key=='cv': tools='<button class="print-button" type="button" hidden>Print / Save as PDF ↗</button>'
        if key=='home':
            hero='''<section class="hero"><div class="hero-inner"><p class="eyebrow">DEPARTMENT OF ASTRONOMY · YONSEI UNIVERSITY</p><h1>Minjin Kim<span>김민진</span></h1><p class="hero-role">Associate Professor of Astronomy</p><p class="hero-description">Exploring active galactic nuclei, their host galaxies, and the evolution of nearby galaxies.</p><div class="hero-links"><a class="button" href="research.html">Explore my research <span>↗</span></a><a class="text-link" href="publications.html">Publications <span>→</span></a></div></div><p class="hero-caption">AGN and relativistic jets · Artist’s illustration</p></section>'''
            # Name in Korean omitted because the source supplies only the English spelling.
            hero=hero.replace('<span>김민진</span>','')
            body=f'''<div class="home-intro"><p class="eyebrow">ABOUT</p><div><h2>A closer look at galaxies.</h2>{markdown(source.split('## ')[0])[0]}<a class="underlined" href="cv.html">View curriculum vitae →</a></div></div><section class="focus"><div class="section-heading"><p class="eyebrow">RESEARCH FOCUS</p><h2>From galactic nuclei<br>to the wider universe.</h2></div><div class="focus-grid"><a href="research.html#coevolution-between-active-galactic-nuclei-and-host-galaxies"><span class="topic-number">01 /</span><h3>Black holes &<br>their host galaxies</h3><p>Physical properties of active galactic nuclei and their connection to galaxy evolution.</p><span class="arrow">↗</span></a><a href="research.html#evolution-of-nearby-galaxies"><span class="topic-number">02 /</span><h3>The nearby<br>universe</h3><p>Deep imaging and the evolution of nearby galaxies with the KMTNet Nearby Galaxy Survey.</p><span class="arrow">↗</span></a><a href="research.html#spherex-the-spectro-photometer-for-the-history-of-the-universe-and-ices-explorer"><span class="topic-number">03 /</span><h3>Infrared skies &<br>space missions</h3><p>Active involvement in SPHEREx and PRIMA, exploring the universe through infrared surveys.</p><span class="arrow">↗</span></a></div></section><section class="home-links"><div><p class="eyebrow">WRITING & EXPERIENCE</p><h2>Explore the work.</h2></div><a href="publications.html"><h3>Publications <span>↗</span></h3><p>Journal articles and submitted manuscripts.</p></a><a href="cv.html"><h3>Curriculum vitae <span>↗</span></h3><p>Appointments, awards, grants, service, and students.</p></a></section><section class="contact"><p class="eyebrow">GET IN TOUCH</p><h2>Let’s connect.</h2><a href="mailto:mkim.astro@gmail.com">mkim.astro@gmail.com ↗</a><p><a href="https://astro.yonsei.ac.kr/galaxy/index.do">Department of Astronomy</a> · <a href="https://www.yonsei.ac.kr/sc/index.do">Yonsei University</a></p></section>'''
            main=f'{hero}<div class="wrap">{body}</div>'
        else:
            main=f'<header class="page-header wrap"><p class="eyebrow">{kicker}</p><h1>{title}</h1><p>{description}</p>{tools}</header><div class="wrap page-grid">{side}<article class="prose {key}" id="page-content">{body}</article></div>'
        page=template.replace('{{TITLE}}',title+' · Minjin Kim').replace('{{NAV}}',nav).replace('{{MAIN}}',main).replace('{{CLASS}}',key)
        (OUT/filename).write_text(page)
    (OUT/'.nojekyll').touch()
    print('Built four pages in dist/')
if __name__=='__main__': build()
