#!/usr/bin/env python3
"""Build the GitHub Pages static portfolio from its reusable components."""
import html,json
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
projects=json.loads((R/'content/projects.json').read_text())
projects.sort(key=lambda p:p['order'])
profile=json.loads((R/'content/profile.json').read_text())
e=html.escape
BASE='https://maddalenacerena-iut.github.io/portfolio/'

def paragraphs(s): return ''.join('<p>'+e(x)+'</p>' for x in s.split('\n\n'))
def icon(name):
 paths={'email':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>','phone':'<path d="M6 3h4l2 5-3 2c2 4 3 5 6 6l2-3 4 2v4c0 4-7 2-12-3S2 3 6 3Z"/>','linkedin':'<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7m0-10v.1M11 17v-7m0 3c0-4 6-4 6 0v4"/>','star':'<path d="M12 1c0 8-3 11-11 11 8 0 11 3 11 11 0-8 3-11 11-11-8 0-11-3-11-11Z"/>'}
 paths.update({'education':'<path d="m2 9 10-5 10 5-10 5-10-5Zm4 2v6c4 3 8 3 12 0v-6M22 9v8"/>','experience':'<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V3h8v4M3 13h18M10 12v3h4v-3"/>','skills':'<path d="m2 8 10-5 10 5-10 5L2 8Zm0 5 10 5 10-5M2 18l10 5 10-5"/>','marketing':'<path d="M3 10h5l12-6v16L8 14H3v-4Zm4 4 2 7h4l-3-6M21 9l2-1M21 15l2 1"/>','content':'<path d="M13 4H4v16h16v-9M10 14l1-4L20 1l3 3-9 9-4 1Z"/>','analysis':'<path d="M5 21V12M12 21V7M19 21V2"/>','screen':'<rect x="2" y="3" width="20" height="14" rx="1"/><path d="M8 21h8M12 17v4"/>','edit':'<path d="M5 19 8 10 19 2l3 3L11 16l-6 3Z"/>','video':'<rect x="2" y="5" width="14" height="14" rx="2"/><path d="m16 10 6-4v12l-6-4"/>','sheet':'<rect x="3" y="3" width="18" height="18" rx="1"/><path d="M3 9h18M3 15h18M9 3v18"/>','office':'<path d="M4 5 15 2l5 3v16l-5 2-11-4V5Zm11-3v21M8 8v8"/>','code':'<rect x="1" y="4" width="22" height="16" rx="2"/><path d="m8 9-3 3 3 3m8-6 3 3-3 3m-3-8-2 10"/>'})
 paths.update({'arrow-right':'<path d="M4 12h16m-6-6 6 6-6 6"/>','arrow-left':'<path d="M20 12H4m6-6-6 6 6 6"/>','expand':'<path d="M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5"/>','close':'<path d="m6 6 12 12M6 18 18 6"/>'})
 return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'+paths[name]+'</svg>'
def image(name,alt,lazy=True):
 with Image.open(R/name) as im: w,h=im.size
 return f'<img src="{e(name)}" alt="{e(alt)}" width="{w}" height="{h}" '+('loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"')+'>'
def Header(active):
 links=''.join(f'<a href="{url}" '+('aria-current="page"' if label==active else '')+f'>{label}</a>' for url,label in [('index.html','Accueil'),('a-propos.html','À propos'),('realisations.html','Réalisations'),('index.html#contact','Contact')])
 return f'<header class="header"><a class="brand" href="index.html" aria-label="Céréna Maddalena — Accueil">Céréna Maddalena</a><button class="menu" aria-expanded="false" aria-controls="navigation">Menu <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button><nav id="navigation" aria-label="Navigation principale">{links}<a class="cv-button" href="documents/cv-cerena-maddalena.pdf" download>Télécharger mon CV</a></nav></header>'
def social():
 linkedin=f'<a href="{e(profile["linkedin"])}" target="_blank" rel="noopener" aria-label="LinkedIn">{icon("linkedin")}</a>' if profile['linkedin'] else f'<span class="unavailable" role="img" aria-label="LinkedIn : lien non fourni" title="Profil LinkedIn à renseigner">{icon("linkedin")}</span>'
 return linkedin+f'<a href="tel:+33679996265" aria-label="Téléphoner">{icon("phone")}</a><a href="mailto:{profile["email"]}" aria-label="Envoyer un email">{icon("email")}</a>'
def Footer(): return f'<footer><div class="footer-ornament" aria-hidden="true">{icon("star")}</div><a class="footer-name" href="index.html">Céréna Maddalena</a><p>Portfolio</p><div class="footer-rule"></div><div class="social">{social()}</div><p class="thanks">Merci d’avoir pris le temps de découvrir mon univers ♡</p></footer>'
def SectionHeading(title,subtitle='',level=2):
 symbols={'Ma présentation':'star','Mon parcours':'education','Mes expériences':'experience','Mes compétences':'skills'}
 badge='<span class="section-badge">'+icon(symbols[title])+'</span>' if title in symbols else ''
 return f'<div class="section-heading">{badge}<h{level}>{e(title)}</h{level}><span class="heading-rule" aria-hidden="true"></span>'+ (f'<p>{e(subtitle)}</p>' if subtitle else '')+'</div>'
def shell(name,title,desc,active,content):
 return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#321B34"><meta name="description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:locale" content="fr_FR"><meta property="og:title" content="{e(title)} | Céréna Maddalena"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{BASE+name}"><link rel="canonical" href="{BASE+name}"><title>{e(title)} | Céréna Maddalena</title><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><script src="script.js" defer></script></head><body><a class="skip" href="#contenu">Aller au contenu</a>{Header(active)}<main id="contenu">{content}</main>{Footer()}<dialog class="lightbox" aria-label="Création en grand format"><button class="close-lightbox" aria-label="Fermer le visuel" autofocus>Fermer {icon('close')}</button><div class="zoom-stage"></div><p class="zoom-caption"></p></dialog></body></html>'''
def write(name,title,desc,active,content): (R/name).write_text(shell(name,title,desc,active,content))
def ProjectCard(p):
 visual=image(p['cover'],p['brand']+' — '+p['title']) if p['cover'] else '<span class="missing-visual">'+e(p['missing_message'])+'</span>'
 return f'<article class="project reveal"><a class="project-card" href="{p["slug"]}.html"><div class="project-cover">{visual}</div><div class="project-content"><p class="project-category">{e(p["category"])}</p><h3>{e(p["brand"])} — {e(p["title"])}</h3><p class="project-description">{e(p["description"])}</p></div></a></article>'
def ProjectGallery(items): return '<div class="projects-grid">'+''.join(ProjectCard(p) for p in items)+'</div>'
def ContactForm():
 endpoint=profile.get('contact_endpoint')
 return f'''<form id="contact-form" {'action="'+e(endpoint)+'" method="post"' if endpoint else ''} data-native-service="true" data-configured="{str(bool(endpoint)).lower()}" aria-describedby="form-status"><input type="hidden" name="_subject" value="Portfolio — Nouveau message"><div class="form-honeypot" aria-hidden="true"><label for="website">Laisser ce champ vide</label><input id="website" type="text" name="_honey" tabindex="-1" autocomplete="off"></div><div class="form-row"><div><label for="name">Nom</label><input id="name" name="name" autocomplete="name" required maxlength="150" pattern=".*\\S.*" title="Indiquez votre nom."></div><div><label for="email">Email</label><input id="email" type="email" name="email" autocomplete="email" required maxlength="254"></div></div><label for="message">Message</label><textarea id="message" name="message" rows="5" required maxlength="10000"></textarea><button class="button" type="submit" {'disabled' if not endpoint else ''}>Envoyer {icon('arrow-right')}</button><p id="form-status" role="status">{'L’envoi se poursuit sur FormSubmit, qui affiche son résultat. La réception des messages reste à vérifier après activation du service.' if endpoint else 'L’envoi par formulaire est indisponible : configuration du service en attente. Vous pouvez me contacter directement par email.'}</p></form>'''
intro='Je suis Céréna Maddalena, étudiante en troisième année de licence Management des Technologies et des Sciences à l’IAE de Montpellier, après un DUT Techniques de commercialisation.'
home_about=intro+'\n\nAu fil de mes études et de mes projets, j’ai développé un intérêt particulier pour la communication, le marketing et la création de contenus. J’aime réfléchir à la manière dont une idée peut prendre forme, se construire et devenir un projet concret.\n\nÀ travers ce portfolio, je vous invite à découvrir une partie de mon travail, de mes compétences et de mon parcours.'
hero_image=profile.get('hero_image')
hero=f'<section class="hero {"has-image" if hero_image else "awaiting-image"}"'+(f' style="background-image:url({e(hero_image)})"' if hero_image else '')+f'><div class="wrap"><h1>Céréna<br>Maddalena</h1><p>Étudiante en management, marketing &amp; communication</p><a class="button light" href="realisations.html">Découvrir mes réalisations {icon("arrow-right")}</a></div>'+( '' if hero_image else '<p class="asset-note">Fond floral original en attente d’intégration</p>')+'</section>'
about_visual='<figure>'+image(profile['about_image'],'Photographie d’ambiance')+'</figure>' if profile['about_image'] else ''
home=hero+f'<section class="section home-about reveal"><div class="wrap about-preview {"with-image" if about_visual else ""}"><div>{SectionHeading("À propos")}{paragraphs(home_about)}<a class="button" href="a-propos.html">En savoir plus {icon("arrow-right")}</a></div>{about_visual}</div></section>'
home+='<section class="section selection"><div class="wrap">'+SectionHeading('Mes réalisations','Une sélection de projets qui reflètent ma créativité et mon engagement.')+ProjectGallery(projects[:3])+f'<div class="center"><a class="button" href="realisations.html">Voir plus de projets {icon("arrow-right")}</a></div></div></section>'
linkedin=f'<a href="{e(profile["linkedin"])}" rel="noopener" target="_blank">LinkedIn</a>' if profile['linkedin'] else '<span class="pending-link">LinkedIn : profil à renseigner</span>'
home+=f'<section class="section contact" id="contact"><div class="wrap contact-layout"><div class="reveal">{SectionHeading("Contact")}<p class="contact-lead">Une question ? Un projet ?</p><p>N’hésitez pas à me contacter, je vous répondrai avec plaisir.</p><address><a href="mailto:{profile["email"]}">{icon("email")}{profile["email"]}</a><a href="tel:+33679996265">{icon("phone")}{profile["phone"]}</a><div>{icon("linkedin")}{linkedin}</div></address></div>{ContactForm()}</div></section>'
write('index.html','Portfolio','Étudiante en management, marketing & communication, Céréna Maddalena présente ses réalisations, ses compétences et son parcours.','Accueil',home)
write('realisations.html','Mes réalisations',f'Découvrez les {len(projects)} réalisations de Céréna Maddalena en communication, marketing et création graphique.','Réalisations','<section class="section gallery-section"><div class="wrap">'+SectionHeading('Mes réalisations','Une sélection de projets qui reflètent ma créativité et mon engagement.',1)+ProjectGallery(projects)+'</div></section>')
def Timeline():
 data=[('2024','Baccalauréat STMG','Mention bien','Lycée du Grésivaudan, Meylan'),('2024–2026','DUT Techniques de commercialisation','Parcours Marketing digital, e-business et entrepreneuriat','IUT de Montpellier-Sète'),('2026–2027','Licence 3 Management, Technologies et Sciences','','IAE de Montpellier')]
 # One SVG owns both the curve and its points. JS updates their shared coordinates
 # to the date centres after layout, on resize and after fonts have loaded.
 svg='<svg class="timeline-path" viewBox="0 0 32 350" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="M16 16 C-16 67 48 119 16 170 S-16 273 16 324"/>'+''.join(f'<circle cx="16" cy="{y}" r="4.5"/>' for y in [16,170,324])+'</svg>'
 return '<div class="timeline">'+svg+''.join(f'<article class="milestone"><span class="date">{d}</span><div class="formation"><h3>{title}</h3>'+(''+f'<p>{sub}</p>' if sub else '')+f'<p>{school}</p></div></article>' for d,title,sub,school in data)+'</div>'
about='<section class="section presentation"><div class="wrap narrow">'+SectionHeading('À propos',level=1)+SectionHeading('Ma présentation')+paragraphs(intro+'\n\nAu fil de mes études et de mes projets, j’ai développé un réel intérêt pour la communication, le marketing et la création de contenus. Curieuse, créative et organisée, j’aime transformer une idée en contenu pertinent et adapter les messages aux différents canaux de communication.\n\nMotivée et impliquée, je souhaite aujourd’hui mettre mes compétences au service de projets concrets et enrichir mon expérience professionnelle dans le domaine de la communication.')+'</div></section>'
about+='<section class="section education"><div class="wrap">'+SectionHeading('Mon parcours')+Timeline()+'</div></section>'
about+='<section class="section experience"><div class="wrap">'+SectionHeading('Mes expériences')+'<div class="experience-grid">'
for x in profile['experiences']:
 about+=f'<article class="experience-card reveal"><h3>{e(x["role"])}</h3><p class="company">{e(x["company"])} — {e(x["period"])}</p><ul>'+''.join(f'<li>{e(m)}</li>' for m in x['missions'])+'</ul></article>'
about+='</div></div></section><section class="section skills"><div class="wrap">'+SectionHeading('Mes compétences')+'<div class="skills-grid">'
for title,items in [('Marketing & Communication',['Marketing digital : SEO, SEA, veille concurrentielle.','Stratégie de marque et plan de communication.','Réseaux sociaux et gestion de l’e-réputation.','Prospection, relation client et négociation.']),('Création de contenu',['Rédaction web.','Création de contenus visuels (Canva, CapCut).','Création et gestion de site web.']),('Analyse & Organisation',['Statistiques marketing et analyse des performances.','Gestion de projet.','Autonomie, rigueur et travail d’équipe.'])]:
 about+='<article class="skill-card reveal"><h3>'+icon({'Marketing & Communication':'marketing','Création de contenu':'content','Analyse & Organisation':'analysis'}[title])+e(title)+'</h3><ul>'+''.join('<li>'+e(t)+'</li>' for t in items)+'</ul></article>'
about+='</div><div class="tools-band"><h3>'+icon('screen')+'Outils</h3><ul class="tools">'+''.join('<li>'+icon(symbol)+e(t)+'</li>' for t,symbol in [('Canva','edit'),('CapCut','video'),('Excel','sheet'),('Pack Office','office'),('Création de site web','code')])+'</ul></div></div></section>'

write('a-propos.html','À propos','Présentation, parcours, expériences et compétences de Céréna Maddalena.','À propos',about)
def ProjectDetail(p,i):
 detail='<section class="section detail"><div class="wrap"><a class="text-link" href="realisations.html">'+icon('arrow-left')+'Retour aux réalisations</a><div class="detail-heading"><p class="eyebrow">Réalisation '+f'{p["order"]:02} / {len(projects)}</p><h1>'+e(p['brand'])+' — '+e(p['title'])+'</h1><p class="category">'+e(p['category'])+'</p></div><div class="project-intro"><h2>Présentation du projet</h2>'+paragraphs(p['presentation'])+'</div>'
 detail+='<section class="case-visuals" aria-label="Créations originales">'
 groups=p.get('visual_groups') or [{'image_indices':list(range(len(p['images'])))}]
 for group in groups:
  if group.get('title'): detail+='<h3 class="visual-group-heading">'+e(group['title'])+'</h3>'
  detail+='<div class="visual-grid '+('horizontal' if p['orientation']=='horizontal' else '')+'">'
  for j in group['image_indices']:
   name,caption=p['images'][j],p['captions'][j]
   detail+=f'<figure class="reveal"><a class="zoom-link" href="{e(name)}" data-zoom="{e(name)}" aria-label="Agrandir : {e(caption)}">{image(name,p["brand"]+" — "+caption)}<span>Agrandir {icon("expand")}</span></a><figcaption>{e(caption)}</figcaption></figure>'
  detail+='</div>'
 if not p['images']: detail+='<div class="missing-detail">'+e(p['missing_message'])+'</div>'
 if p['resource_note']: detail+='<p class="resource-note">'+e(p['resource_note'])+'</p>'
 detail+='</section><section class="approach"><h2>Démarche créative</h2>'+paragraphs(p['approach'])+'</section><nav class="case-nav" aria-label="Navigation entre les projets">'
 for label,idx,symbol in [('Projet précédent',i-1,'arrow-left'),('Projet suivant',i+1,'arrow-right')]:
  if 0<=idx<len(projects):
   x=projects[idx];action=(icon(symbol)+label) if idx<i else (label+icon(symbol));detail+=f'<a href="{x["slug"]}.html"><small>{action}</small>{e(x["brand"])} — {e(x["title"])}</a>'
  else: detail+='<span></span>'
 return detail+'</nav></div></section>'
for i,p in enumerate(projects): write(p['slug']+'.html',p['brand']+' — '+p['title'],p['presentation'].split('\n')[0],'Réalisations',ProjectDetail(p,i))
# Preserve old incoming URLs without retaining an independent Contact page.
for old,new in {'contact.html':'index.html#contact','honeylang.html':'honeylang-banniere.html','ethiopik.html':'ethiopik-plaquette.html','am-project.html':'am-identite.html','myledmask-v2.html':'myledmask.html'}.items():
 (R/old).write_text(f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={new}"><title>Redirection | Céréna Maddalena</title></head><body><p><a href="{new}">Continuer vers le portfolio</a></p></body></html>')
(R/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+x+'</loc></url>' for x in ['index.html','a-propos.html','realisations.html']+[p['slug']+'.html' for p in projects])+'</urlset>')
(R/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n')
print(f'Generated 3 main pages, {len(projects)} project pages and 5 legacy redirects.')
