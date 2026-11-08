# Audit et intégration — 8 novembre 2026

## Cartes de réalisations adaptées au nouvel exemple

À la demande de Céréna, les cartes de l’accueil et de la galerie reprennent la composition de sa nouvelle référence : image au-dessus, contenu en dessous, catégorie dans une capsule, puis titre et description. Le cadre présente une bordure fine lilas, des coins arrondis, un fond crème et des titres prune, avec les typographies du portfolio. Le flou des aperçus est conservé après confirmation explicite ; les détails restent nets.

La modification porte sur `ProjectCard` dans `scripts/build.py`, les styles des cartes dans `style.css` et les deux pages générées `index.html` et `realisations.html`. Aucun texte de projet, image source, ordre, URL, fiche détaillée, navigation, formulaire ou footer n’a changé. Les trois aperçus et les treize réalisations conservent leurs associations. La correction HTML qui replace le texte d’accueil dans son conteneur est incluse dans cette version.

Les contrôles statiques vérifient aussi l’image de couverture originale, son absence de texte superposé et la présence des catégorie, titre et description approuvés dans le panneau inférieur de chaque carte. Le rendu navigateur reste à vérifier : aucun outil de contrôle navigateur n’est disponible dans cette session.

## Correction de l’accueil après la photo de Céréna

Le générateur omettait le caractère `>` qui ferme la balise d’ouverture de la section d’accueil, juste avant `<div class="wrap">`. Le navigateur absorbait alors ce conteneur dans les attributs de la section : le nom, le sous-titre et le bouton devenaient trois enfants du conteneur flex, disposés côte à côte et sans les marges prévues. Le défaut a été confirmé dans le ZIP fourni et dans la page GitHub Pages lue lors du diagnostic.

Correction limitée à ce caractère dans `scripts/build.py`, puis régénération de `index.html`. Les styles, le fond, les textes et les autres pages restent inchangés. Le contrôle `scripts/check.py` rejette désormais une balise d’ouverture mal formée, les attributs dupliqués et l’absence du conteneur commun au nom, au sous-titre et au bouton. Il a échoué sur l’ancienne page et réussi sur la version corrigée. L’archive corrigée doit remplacer le fichier `index.html` publié pour corriger GitHub Pages ; cette publication n’a pas été effectuée par l’agent.

Dépôt examiné : <https://github.com/maddalenacerena-iut/portfolio>, branche `main`, commit source `49a852d`. Technologie HTML/CSS/JavaScript et adresses existantes conservées. Les modifications restent locales : aucun push, aucun nouveau dépôt et aucun déploiement de cette version.

## État de la correction

- Galerie actuelle : 13 réalisations, regroupées par marque. Les aperçus de l’accueil sont Honeylang — Bannière web, Honeylang — Affiche et myLEDmask — Flyer.
- À la demande de Céréna, les deux versions myLEDmask sont regroupées dans une seule fiche, avec les trois visuels conservés. AM Project — Site web dispose de sa fiche et des quatre captures retrouvées dans le dépôt. Les réalisations suivant myLEDmask sont renumérotées de 04 à 13.
- Nouvelle confirmation de Céréna après son dernier envoi : le projet 08 est **Harmonia — Affiche**, avec la nouvelle affiche originale et les textes déjà validés du dépôt initial. Le site Harmonia est remplacé ; le logo est conservé hors affichage, sans projet supplémentaire.
- Fonds trop blancs réchauffés vers le blanc cassé beige, sans changement des violets, des familles typographiques, de l’alternance lilas/crème ou des fonds prune.
- Flèches des CTA remplacées par des SVG au trait fin ; action Agrandir réduite et reliée à la visionneuse existante, avec fermeture et restauration du focus.
- Frise : courbe et trois points appartiennent au même SVG. Le tracé utilise les coordonnées des points comme extrémités de segments ; les positions sont recalculées après mise en page et redimensionnement. L’animation de tracé et la préférence de réduction des mouvements sont conservées. La recette visuelle sur appareils reste à effectuer.
- Navigation commune : Accueil, À propos, Réalisations, Contact ; téléchargement du véritable CV. Contact pointe vers `index.html#contact`, y compris depuis les fiches. Aucun filtre ni rubrique Parcours indépendante ajouté.
- Fond d’accueil recréé à partir de l’exemple après demande explicite de Céréna, qui ne possède pas l’original : décor prune sombre et flouté, grande fleur lavande à droite, espace dégagé à gauche pour les textes existants. Cette intervention conserve les autres éléments du site.

## Correspondance des réalisations

Les chemins et légendes détaillés sont centralisés dans `content/projects.json`.

| Nº | Réalisation | Visuels affichés |
| --- | --- | --- |
| 01 | Honeylang — Bannière web | Quatre fichiers du dernier envoi : vanille, parfums dorés, collage, pierre sombre ; couverture vanille |
| 02 | Honeylang — Affiche | Deux propositions originales : parfums et collage |
| 03 | myLEDmask — Flyer | Une fiche, deux versions : beige recto seul, puis noire recto et verso |
| 04 | Ethiopik Travel — Plaquette commerciale | Volets extérieurs puis intérieurs actuels conservés à la demande de Céréna |
| 05 | Ethiopik Travel — Catalogue | Pages 1, 2, 8, 13, 18, 20 et 25, dans cet ordre |
| 06 | Ethiopik Travel — Identité visuelle | Logo actuel conservé à la demande de Céréna ; périmètre de contribution à préciser |
| 07 | Ethiopik Travel — Publications Instagram | Cinq publications du dépôt : Addis, Awash, Entoto, Melka et vol |
| 08 | Harmonia — Affiche | Nouvelle affiche originale seule |
| 09 | Votre Élégance — Logo | Logo original conservé |
| 10 | AM Project — Publications LinkedIn | Nouveau JPG original fourni |
| 11 | AM Project — Publications Instagram | Six JPG du dernier envoi, dans l’ordre 01 à 06 |
| 12 | AM Project — Identité visuelle | Bannière du dépôt ; distinction entre création et éléments préexistants à préciser |
| 13 | AM Project — Site web | Captures `am-web-1.webp` à `am-web-4.webp`, dans cet ordre ; aucune URL externe non confirmée ajoutée |

Les images sont floutées uniquement dans les cartes, par CSS. Les détails et agrandissements utilisent les originaux nets dans leur intégralité. Les bandes noires et les éléments présents dans les fichiers fournis sont conservés.

## Réalisations non renvoyées et conservées

Céréna a demandé de garder comme avant les réalisations qu’elle n’a pas renvoyées. Pour ces sept projets, les fichiers et les textes restent inchangés ; seule la numérotation suit le regroupement des versions myLEDmask :

- **04 — Ethiopik Travel — Plaquette commerciale** : volets extérieur et intérieur actuels.
- **05 — Ethiopik Travel — Catalogue** : pages déjà disponibles, dans leur ordre actuel.
- **06 — Ethiopik Travel — Identité visuelle** : logo actuel.
- **07 — Ethiopik Travel — Publications Instagram** : cinq publications actuelles.
- **09 — Votre Élégance — Logo** : logo original actuel.
- **12 — AM Project — Identité visuelle** : bannière actuelle.
- **13 — AM Project — Site web** : quatre captures actuelles.

Les derniers fichiers reçus concernent les six autres projets : 01, 02, 03, 08, 10 et 11, ainsi que le CV. Aucune réalisation supplémentaire n’est créée.

## Nouveaux fichiers originaux et traçabilité

Les 38 réceptions comprennent 36 JPG et deux envois du CV PDF. Les fichiers retransmis pour Honeylang, myLEDmask, Harmonia et les publications AM Project sont prioritaires pour les projets concernés. Les pièces identiques aux fichiers déjà intégrés réutilisent leur destination. `content/assets.json` consigne la provenance, la destination, le statut et le SHA-256 des fichiers. Le dossier de réception sous `/tmp` n’est qu’une source temporaire : les destinations relatives du dépôt sont les ressources utilisées par les pages.

- Les quatre bannières du lot `0CBDDB8B-841A-4323-9637-1F36510DD8F8` sont les seuls visuels actifs du projet 01. Les trois premières sont identiques octet pour octet aux fichiers déjà intégrés : les destinations `honeylang-banniere-vanille-original.jpg`, `honeylang-banniere-parfums-original.jpg` et `honeylang-banniere-collage-original.jpg` sont réutilisées, dans cet ordre. La quatrième est copiée sous `honeylang-banniere-pierre-novembre.jpg`, dans le même dossier `images/honeylang/bannieres/`. La vanille est la couverture, y compris pour la carte d’accueil.
- L’ancienne sélection de cinq visuels est remplacée par les quatre du dernier envoi. Les portraits et l’ancienne pierre sombre restent conservés hors affichage. Le doublon visuel des photos 4 et 7 du premier lot reste archivé ; il ne crée aucune proposition supplémentaire. Le total de 38 pièces reçues distingue les réceptions des fichiers physiques : les pièces identiques réutilisent leur destination existante.
- Les deux affiches du lot `CC35FEFF-8CF2-48BC-BA87-BB99BC8F2CC3` correspondent au projet 02, dans l’ordre : affiche dorée aux parfums, puis collage. Les fichiers du dernier envoi sont prioritaires ; une destination existante n’est réutilisée que si l’identité octet pour octet est vérifiée.
- Les trois visuels du lot `FA18EC50-D24C-4147-B871-894900852C00` sont regroupés dans le projet 03 : version beige recto seul, puis version noire recto et verso. La fusion de ces deux versions dans une fiche et les mentions Recto et Verso sont explicitement confirmées par Céréna. L’ancienne adresse `myledmask-v2.html` redirige vers cette fiche ; les textes des deux versions sont conservés.
- Les six pages Instagram AM Project du lot `BF898544-0FE2-4C92-B92C-3681EA721E4C` remplacent toute la série précédente, dans l’ordre 01 à 06. Les cinq premières sont identiques aux JPG déjà intégrés et réutilisent leur destination ; la sixième, de 820 × 1025 px, est `images/am-project/instagram/am-carousel-06-original.jpg` et remplace l’ancien sixième WebP. Les paysages et nuages visibles dans l’écran 04 appartiennent au fichier reçu ; ils n’ont pas été ajoutés par l’agent.
- La publication LinkedIn AM Project du lot `6C498113-96A4-4FA5-B262-B45F0192159F` est identique au fichier déjà intégré et reste la référence du projet 10.
- L’affiche Harmonia retransmise est identique au JPG déjà intégré ; Céréna confirme à nouveau **Harmonia — Affiche**, sans attente de captures de site.
- Le dernier CV PDF retransmis, de 283 903 octets, est identique au CV de novembre déjà intégré et a été installé par copie exacte au chemin de téléchargement. L’ancien PDF antérieur reste archivé dans `documents/archive/`.
- Les anciens visuels restent conservés ; aucune création n’est remplacée par une image Internet ou générée.

## Ressources et précisions restantes

1. **Photo d’ambiance de l’Accueil — À propos** : absente ; `about_image` reste `null`. Aucun remplacement arbitraire.
2. **Catalogue Ethiopik complet et PDF de plaquette** : seuls les sept extraits de catalogue et les deux volets de plaquette sont disponibles. Les limites sont indiquées sur les fiches ; aucun téléchargement fictif.
3. **Identités Ethiopik et AM Project** : le périmètre exact des créations de Céréna n’est pas documenté. Les notes de contribution restent visibles ; les éléments de marque préexistants ne sont pas présentés comme intégralement créés par elle.
4. **Adresse du site AM Project** : non confirmée ; aucun lien externe inventé. Les outils, fonctionnalités et rôle exact ne sont pas extrapolés à partir des captures.

### Fond d’accueil : exception explicitement autorisée

Céréna a précisé ne pas disposer de la photo originale et a demandé de créer le fond à partir de l’exemple joint. Cette nouvelle instruction autorise une image générée uniquement pour ce décor et remplace sur ce point l’interdiction du cahier. Le fichier `images/accueil/fond-floral-recree.webp` est une recréation, et non l’original de la référence. Il est utilisé par `hero_image`, sans texte intégré, sans recadrage du fichier généré et sans nouvelle signature ou slogan. L’ancien `images/accueil/fond-floral.png` est préservé mais reste hors affichage.

Cette exception ne concerne ni la photo d’ambiance À propos ni les réalisations : leurs visuels restent soumis aux fichiers originaux fournis. Aucun projet, texte validé, composant de navigation ou autre élément graphique n’a été modifié pour cette recréation.

LinkedIn est repris de la capture fournie : `https://www.linkedin.com/in/c%C3%A9r%C3%A9na-maddalena-bb071b383`. Il est présent dans Contact et le footer ; sa disponibilité distante n’est pas attestée par l’intégration du lien.

## Vérification du CV de novembre 2026

Le nouveau CV confirme le DUT Techniques de commercialisation et la L3 Management des Technologies et Sciences. L’ancien écart BUT/L3 appartient au PDF archivé et n’est plus un blocage du CV téléchargeable.

Céréna a ensuite confirmé explicitement **Hôtel Mocka / Anyx**, comme dans son nouveau CV. La carte de l’expérience est alignée sur cette orthographe validée. Cet écart est résolu et ne bloque plus la publication. Les quatre cartes demandées sont conservées ; aucune expérience ou certification supplémentaire n’est ajoutée.

## Formulaire et publication

Le formulaire utilise un POST natif vers FormSubmit, sans clé privée. Champs obligatoires, format email, longueurs maximales et refus des messages vides sont prévus ; champ piège `_honey` et CAPTCHA du prestataire conservé par défaut. FormSubmit prend en charge la poursuite de l’envoi, ses erreurs et sa confirmation. Le portfolio n’annonce aucune réussite locale.

L’activation du destinataire et la réception d’un message restent à vérifier dans la boîte de Céréna. Aucun envoi réel ni email d’activation n’a été déclenché par l’agent. Les étapes d’activation, de réception et de vérification du retour/échec sont décrites dans [README.md](README.md).

L’URL publique préexistante répond HTTP 200, ce qui vérifie uniquement sa disponibilité au moment du contrôle. Les modifications locales n’y sont pas déployées. Les routes HTML et chemins relatifs sont préparés pour `/portfolio/` ; une vérification en production de la version corrigée reste nécessaire après publication.

## Contrôles et limites

Les commandes et résultats sont consignés dans [VALIDATION.md](VALIDATION.md). Aucun contrôle statique ni test d’interaction simulé ne valide à lui seul le rendu, l’absence de débordement sur iPad, le dialogue natif ou la réception du formulaire.

Aucune recette navigateur n’est revendiquée. Dans cet environnement, `SITES_MANAGED_LINUX_CONTAINER=1` ; le chemin navigateur `cua_repl.js` n’est pas disponible comme outil utilisable. Le guide Sites interdit de lancer un autre chemin de prévisualisation dans cette situation. Les largeurs 375, 430, 768, 1024 et 1440 px restent donc à vérifier dans un navigateur, ainsi que la navigation clavier, l’agrandissement mobile et la fidélité aux captures.

La version ne peut être considérée comme complètement finalisée tant que les ressources essentielles, la réception du formulaire et la recette visuelle ne sont pas vérifiées.

## Fichiers concernés

- Sources : `content/projects.json`, `content/profile.json`, nouveau `content/assets.json`, `scripts/build.py`, `style.css`, `script.js`.
- Pages générées : les trois pages principales et les 13 fiches, dont `myledmask.html` regroupant ses deux versions et `am-site.html` ; `sitemap.xml`. `myledmask-v2.html` devient la cinquième redirection de compatibilité.
- Ressources : nouveaux JPG aux destinations documentées dans le manifeste, nouveau CV téléchargeable et archive de l’ancien.
- Contrôles et documentation : `scripts/check.py`, `scripts/test-interactions.cjs`, `README.md`, `REVIEW.md`, `VALIDATION.md`.
