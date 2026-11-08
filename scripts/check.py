#!/usr/bin/env python3
"""Check generated static pages without claiming browser or email verification."""
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from PIL import Image

R = Path(__file__).resolve().parents[1]
errors = []


def require(condition, message):
    if not condition:
        errors.append(message)


class Element:
    def __init__(self, tag, attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def all(self, tag=None):
        for child in self.children:
            if isinstance(child, Element):
                if tag is None or child.tag == tag:
                    yield child
                yield from child.all(tag)

    def has_class(self, value):
        return value in self.attrs.get('class', '').split()

    def text(self):
        return ''.join(child.text() if isinstance(child, Element) else child
                       for child in self.children)


class Page(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
            'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self, source):
        super().__init__()
        self.root = Element('document')
        self.stack = [self.root]
        self.feed(source)
        self.elements = list(self.root.all())
        self.ids = [n.attrs['id'] for n in self.elements if 'id' in n.attrs]

    def handle_starttag(self, tag, attrs):
        require('<' not in self.get_starttag_text()[1:],
                'Malformed opening tag: ' + self.get_starttag_text()[:120])
        require(len(attrs) == len({name for name, _ in attrs}),
                'Duplicate attributes in ' + tag)
        node = Element(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Element(tag, attrs))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, value):
        self.stack[-1].children.append(value)

    def find(self, tag=None, cls=None, ident=None):
        return [n for n in self.elements
                if (tag is None or n.tag == tag)
                and (cls is None or n.has_class(cls))
                and (ident is None or n.attrs.get('id') == ident)]


sources = {f.name: f.read_text() for f in R.glob('*.html')}
pages = {name: Page(source) for name, source in sources.items()}
css = (R / 'style.css').read_text()
projects = json.loads((R / 'content/projects.json').read_text())
profile = json.loads((R / 'content/profile.json').read_text())
order = ['honeylang-banniere', 'honeylang-affiche', 'myledmask',
         'ethiopik-plaquette', 'ethiopik-catalogue', 'ethiopik-identite',
         'ethiopik-instagram', 'harmonia', 'votre-elegance', 'am-linkedin',
         'am-carrousel', 'am-identite', 'am-site']
expected_pages = {'index.html', 'a-propos.html', 'realisations.html'} | {
    slug + '.html' for slug in order}
full_pages = {name for name, source in sources.items()
              if 'http-equiv="refresh"' not in source}
expected_redirects = {'contact.html', 'honeylang.html', 'ethiopik.html',
                      'am-project.html', 'myledmask-v2.html'}
require(full_pages == expected_pages, 'Exactly 3 main pages and 13 detail pages')
require(set(sources) - full_pages == expected_redirects, 'Exactly 5 compatibility redirects')
require([p['slug'] for p in projects] == order, '13 projects with both myLEDmask versions in one project')
require([p.get('order') for p in projects] == list(range(1, 14)), 'Central project order')
require([p.get('id') for p in projects] == [f'projet-{i:02}' for i in range(1, 14)],
        'Sequential unique project identifiers')

for name, page in pages.items():
    source = sources[name]
    require(len(page.ids) == len(set(page.ids)), name + ': duplicate IDs')
    if name in full_pages:
        require(len(page.find('h1')) == 1, name + ': exactly one h1')
        require(any(n.attrs.get('lang') == 'fr' for n in page.find('html')),
                name + ': French document language')
        require(any(n.attrs.get('name') == 'description' and n.attrs.get('content')
                    for n in page.find('meta')), name + ': meta description')
        nav = page.find('nav', ident='navigation')
        require(len(nav) == 1, name + ': common navigation')
        if nav:
            require([a.attrs.get('href') for a in nav[0].all('a')] == [
                'index.html', 'a-propos.html', 'realisations.html',
                'index.html#contact', 'documents/cv-cerena-maddalena.pdf'],
                name + ': exact navigation and CV link')
        require('og:title' in source and 'og:description' in source,
                name + ': Open Graph metadata')
        require(not re.search('[\u2190-\u21ff\u27f0-\u27ff\u2900-\u297f'
                              '\u2700-\u27bf\U0001f000-\U0001faff]', source),
                name + ': Unicode arrow or decorative emoji')
        for cls in ('button', 'text-link', 'zoom-link'):
            for action in page.find(cls=cls):
                require(any(action.all('svg')), name + ': SVG icon for ' + cls)
        for nav in page.find('nav', cls='case-nav'):
            for action in nav.all('a'):
                require(any(action.all('svg')), name + ': SVG previous/next icon')
    require(not any('data-filter' in n.attrs for n in page.elements),
            name + ': no category filters')
    require('images/accueil/fond-floral.png' not in source and
            'hero-art.webp' not in source, name + ': no unselected historical hero')
    if name != 'index.html':
        require(profile['hero_image'] not in source, name + ': recreated decor limited to homepage hero')
    for node in page.elements:
        for key in ('src', 'href', 'data-zoom', 'action'):
            if key not in node.attrs:
                continue
            ref = node.attrs[key]
            u = urlsplit(ref)
            if u.scheme in ('https', 'mailto', 'tel'):
                continue
            require(not u.scheme and not u.netloc, name + ': invalid protocol ' + ref)
            require(not u.path.startswith('/'), name + ': prefix-breaking path ' + ref)
            target = unquote(u.path) or name
            require((R / target).is_file(), name + ': missing local file ' + ref)
            if u.fragment and target in pages:
                require(u.fragment in pages[target].ids, name + ': missing anchor ' + ref)
    for node in page.find('img'):
        a = node.attrs
        require(bool(a.get('alt')), name + ': image alternative text')
        require('width' in a and 'height' in a, name + ': image dimensions')
        try:
            with Image.open(R / a['src']) as actual:
                require(actual.size == (int(a['width']), int(a['height'])),
                        name + ': incorrect intrinsic image dimensions')
                actual.verify()
        except (KeyError, OSError, ValueError) as exc:
            errors.append(name + ': invalid image: ' + str(exc))

for ref in re.findall(r'url\([\'\"]?([^\)\'\"]+)', css):
    require((R / ref).is_file(), 'CSS missing resource ' + ref)
require('fond-floral.png' not in css and 'hero-art.webp' not in css,
        'No unselected historical hero in stylesheet')
require(not re.search(r'\.milestone:{1,2}before\s*\{[^}]*(?:width|background)', css),
        'No independently positioned CSS timeline dots')
for page_name, slugs in [('realisations.html', order), ('index.html', order[:3])]:
    require([n.attrs.get('href') for n in pages[page_name].find('a', cls='project-card')]
            == [s + '.html' for s in slugs], page_name + ': exact card order/count')
    for card, project in zip(pages[page_name].find('a', cls='project-card'), projects):
        children = [n for n in card.children if isinstance(n, Element)]
        require(len(children) == 2 and children[0].has_class('project-cover') and
                children[1].has_class('project-content'),
                page_name + ': card image precedes its separate text panel')
        if len(children) == 2:
            cover, content = children
            require(not cover.text().strip(), page_name + ': no text overlay on project images')
            images = list(cover.all('img'))
            require(len(images) == 1 and images[0].attrs.get('src') == project['cover'],
                    page_name + ': original project cover preserved')
            items = [n for n in content.children if isinstance(n, Element)]
            require([n.tag for n in items] == ['p', 'h3', 'p'] and
                    [n.text() for n in items] == [project['category'],
                        project['brand'] + ' — ' + project['title'], project['description']],
                    page_name + ': approved category, title and description preserved')

# The title, subtitle and CTA must share the inner content wrapper. Without it,
# the hero's flex layout places them side by side and removes the side margins.
heroes = pages['index.html'].find('section', cls='hero')
require(len(heroes) == 1, 'Homepage has one valid hero section')
if heroes:
    children = [n for n in heroes[0].children if isinstance(n, Element)]
    require(len(children) == 1 and children[0].tag == 'div' and
            children[0].has_class('wrap'), 'Hero content has its margin wrapper')
    if children and children[0].has_class('wrap'):
        content = [n for n in children[0].children if isinstance(n, Element)]
        require([n.tag for n in content] == ['h1', 'p', 'a'],
                'Hero name, subtitle and CTA remain inside the wrapper')
        if content:
            require(content[-1].attrs.get('href') == 'realisations.html',
                    'Hero CTA opens the gallery')

for i, project in enumerate(projects):
    slug = project['slug']
    name = slug + '.html'
    if name not in pages:
        errors.append(name + ': missing detail page')
        continue
    page, source = pages[name], sources[name]
    require(len(project['captions']) == len(project['images']), slug + ': captions match images')
    require(project['cover'] in project['images'] if project['images'] else project['cover'] is None,
            slug + ': central cover is a real project visual')
    for field in ('presentation', 'approach'):
        for paragraph in project[field].split('\n\n'):
            require(html.escape(paragraph) in source, slug + ': approved ' + field + ' text')
    require(f'{i + 1:02} / 13' in source, slug + ': number out of 13')
    require('Démarche créative' in source and 'Présentation du projet' in source,
            slug + ': mandatory detail sections')
    require(any(a.attrs.get('href') == 'realisations.html'
                for a in page.find('a', cls='text-link')), slug + ': return to gallery')
    project_links = [a.attrs.get('href') for nav in page.find('nav', cls='case-nav')
                     for a in nav.all('a')]
    expected = ([order[i - 1] + '.html'] if i else []) + (
        [order[i + 1] + '.html'] if i + 1 < len(order) else [])
    require(project_links == expected, slug + ': previous/next order')
    require([n.attrs.get('data-zoom') for n in page.find('a', cls='zoom-link')]
            == project['images'], slug + ': all original images enlarge in order')
    for caption in project['captions']:
        require(html.escape(caption) in source, slug + ': central caption rendered')
    if not project['images']:
        require(False, slug + ': original project visuals still missing')
        require(bool(project.get('missing_message')), slug + ': missing file explicitly identified')
        require(html.escape(project.get('missing_message', '')) in source,
                slug + ': missing file message rendered')
    if project.get('resource_note'):
        require(html.escape(project['resource_note']) in source, slug + ': resource limitation rendered')

by_slug = {project['slug']: project for project in projects}
require(by_slug['harmonia']['title'] == 'Affiche' and len(by_slug['harmonia']['images']) == 1,
        'Confirmed Harmonia project is one original poster')
require(not any('logo' in image.lower() for image in by_slug['harmonia']['images']),
        'Harmonia logo remains outside the selected poster project')
myledmask = by_slug['myledmask']
require(myledmask['title'] == 'Flyer', 'One myLEDmask project title')
require(myledmask['images'] == [
    'images/myledmask/myledmask-flyer-v1-original.jpg',
    'images/myledmask/myledmask-flyer-v2-visuel-1-original.jpg',
    'images/myledmask/myledmask-flyer-v2-visuel-2-original.jpg'],
    'myLEDmask beige recto, then black recto and verso in the same project')
require(myledmask['captions'] == [
    'myLEDmask — Flyer, version 1 · Recto',
    'myLEDmask — Flyer, version 2 · Recto',
    'myLEDmask — Flyer, version 2 · Verso'],
    'myLEDmask captions distinguish both versions and their reading order')
require(myledmask.get('visual_groups') == [
    {'title': 'Version 1 — Recto seul', 'image_indices': [0]},
    {'title': 'Version 2 — Recto et verso', 'image_indices': [1, 2]}],
    'myLEDmask visual groups partition the three originals by version')
for group in myledmask.get('visual_groups', []):
    require(html.escape(group['title']) in sources['myledmask.html'],
            'myLEDmask version heading rendered: ' + group['title'])
require(myledmask['cover'] == myledmask['images'][0], 'myLEDmask beige cover for gallery and home preview')
require('http-equiv="refresh"' in sources['myledmask-v2.html'] and
        'url=myledmask.html' in sources['myledmask-v2.html'],
        'Previous myLEDmask version 2 URL redirects to the combined project')
require(len(by_slug['am-site']['images']) == 4, 'AM Project original web screenshots')
carousel = by_slug['am-carrousel']
require(len(carousel['images']) == 6 and all(name.lower().endswith('.jpg') for name in carousel['images']),
        'Latest AM Project carousel uses all six original JPGs')
require(carousel['captions'] == [f'Écran {i} du carrousel' for i in range(1, 7)],
        'AM Project carousel pages 01 to 06 in reading order')
require(not any('am-carousel-6.webp' in name for name in carousel['images']),
        'Previous AM Project carousel page 06 is no longer selected')
require(profile.get('hero_image') == 'images/accueil/fond-floral-recree.webp',
        'Recreated homepage background explicitly authorized by Céréna')
hero_path = R / profile['hero_image']
require(hero_path.is_file(), 'Recreated background exists')
if hero_path.is_file():
    with Image.open(hero_path) as hero:
        require(hero.width > hero.height and hero.width >= 1440, 'Landscape hero resolution')
        hero.verify()
require('background-image:url(' + profile['hero_image'] + ')' in sources['index.html'],
        'Homepage uses the recreated floral background')
require('Fond floral original en attente' not in sources['index.html'],
        'Resolved homepage background notice removed')
require(all(profile['hero_image'] not in project['images'] and
            profile['hero_image'] != project['cover'] for project in projects),
        'Generated decor is never used as a professional creation')
require(profile.get('linkedin') ==
        'https://www.linkedin.com/in/c%C3%A9r%C3%A9na-maddalena-bb071b383',
        'Confirmed LinkedIn URL preserved')
require(profile.get('contact_endpoint') == 'https://formsubmit.co/cerenaa.mdl@gmail.com',
        'Contact recipient')
form = pages['index.html'].find('form', ident='contact-form')
require(len(form) == 1, 'Single homepage contact form')
if form:
    require(form[0].attrs.get('data-native-service') == 'true' and
            form[0].attrs.get('method', '').lower() == 'post' and
            form[0].attrs.get('action') == profile['contact_endpoint'],
            'Native service POST with truthful provider handoff')
    inputs = {n.attrs.get('name'): n for n in form[0].all('input')}
    require('_subject' in inputs, 'Contact subject')
    require('_honey' in inputs and inputs['_honey'].attrs.get('tabindex') == '-1',
            'Honeypot excluded from keyboard navigation')
    require('_captcha' not in inputs or inputs['_captcha'].attrs.get('value') != 'false',
            'Provider CAPTCHA not disabled')
    require(all(key in inputs and 'required' in inputs[key].attrs
                for key in ('name', 'email')), 'Required name/email fields')
    require(inputs.get('email') is not None and inputs['email'].attrs.get('type') == 'email',
            'Native email validation')
    require(any('required' in n.attrs and n.attrs.get('name') == 'message'
                for n in form[0].all('textarea')), 'Required message field')

about = pages['a-propos.html']
timelines = about.find(cls='timeline')
require(len(timelines) == 1, 'One timeline on About')
if timelines:
    svgs = list(timelines[0].all('svg'))
    require(len(svgs) == 1, 'Timeline curve and three points share a single SVG')
    if svgs:
        paths, dots = list(svgs[0].all('path')), list(svgs[0].all('circle'))
        require(len(paths) == 1 and len(dots) == 3, 'One curve and three SVG dots')
        if paths:
            require(paths[0].attrs.get('pathlength') == '1', 'Normalized timeline draw animation')
            endpoints = []
            for command, values in re.findall(r'([MCS])([^MCS]+)', paths[0].attrs.get('d', '')):
                numbers = re.findall(r'-?\d+(?:\.\d+)?', values)
                if len(numbers) >= 2:
                    endpoints.append(tuple(map(float, numbers[-2:])))
            require(all((float(dot.attrs.get('cx', 'nan')), float(dot.attrs.get('cy', 'nan')))
                        in endpoints for dot in dots), 'Each SVG dot lies exactly on a curve endpoint')
require(not pages['index.html'].find(cls='timeline'), 'No timeline on homepage')
require('DUT Techniques de commercialisation' in sources['a-propos.html'] and
        'BUT' not in sources['a-propos.html'], 'Approved DUT education wording')
require((R / 'documents/cv-cerena-maddalena.pdf').read_bytes().startswith(b'%PDF'), 'Valid CV PDF')
require('url=index.html#contact' in sources['contact.html'], 'Legacy Contact redirects to homepage')

if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} HTML documents; 13 ordered projects and 3 previews; '
      'original visual mappings, links, metadata, SVG actions/timeline, CV and native contact configuration. '
      'Browser rendering, production deployment and real email delivery are separate checks.')
