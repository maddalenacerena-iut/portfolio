# Vérifications — version corrigée du 8 novembre 2026

## Nouvelle présentation des cartes de réalisations

Les treize cartes de galerie et les trois aperçus d’accueil utilisent l’image au-dessus d’un panneau de contenu séparé : catégorie en capsule lilas, titre prune et description sur crème. Le flou est conservé à la demande explicite de Céréna, avec les originaux nets sur les fiches. La grille reste à trois colonnes sur ordinateur, deux sous 850 px et une sous 600 px ; les capsules acceptent le retour à la ligne des catégories longues.

`python scripts/build.py`, `python scripts/check.py` et `git diff --check` : **PASS** après cette adaptation. Le contrôle des cartes vérifie leur nombre, leur ordre, leur couverture originale, l’absence de texte superposé et leurs textes validés, ainsi que la structure corrigée du hero. Les pages détaillées, textes, données et ressources originales sont inchangés. Ces contrôles ne constituent pas une recette visuelle dans un navigateur ; cette limite reste applicable.

## Régression de l’accueil : correction après la photo

Un défaut non détecté par les anciens contrôles statiques a été confirmé : la balise d’ouverture du hero ne se terminait pas par `>` avant son `<div class="wrap">`. Il était présent dans le fichier livré et dans le HTML public consulté. Ce défaut explique les trois éléments alignés horizontalement sur la photo.

- Contrôle ajouté avant correction : **échec attendu**, balise mal formée, attribut `class` dupliqué et conteneur du hero absent.
- Correction du caractère manquant dans le générateur, puis `python scripts/build.py` : **PASS**.
- `python scripts/check.py` sur la page régénérée : **PASS**, avec vérification du conteneur qui regroupe les trois éléments.
- `git diff --check` : **PASS**.

Cette correction ne modifie aucun CSS, texte, image ou autre projet. Aucun nouveau rendu navigateur n’est revendiqué. Le HTML de GitHub Pages a été lu et le défaut y a été confirmé ; la version corrigée reste à publier sur ce site.

Ces résultats concernent les fichiers locaux issus du commit `49a852d` et les nouvelles pièces jointes. Ils ne constituent pas une validation du site corrigé en production.

Derniers envois reçus : quatre bannières et deux affiches Honeylang, trois visuels myLEDmask, six pages Instagram et une publication LinkedIn AM Project, puis l’affiche Harmonia et le CV retransmis. Le total est de 38 réceptions : 36 JPG et deux envois du CV PDF. Le projet 01 affiche quatre bannières uniquement, dans l’ordre vanille, parfums dorés, collage, pierre sombre ; sa couverture et le premier aperçu d’accueil utilisent la vanille. Les trois premières bannières et les deux affiches sont identiques aux destinations existantes ; pour ces deux projets Honeylang, seule la nouvelle pierre sombre nécessite un fichier physique distinct. Les portraits et l’ancienne pierre restent conservés hors affichage.

À la demande explicite de Céréna, les deux versions myLEDmask sont regroupées dans une seule fiche, le projet 03 **myLEDmask — Flyer**, avec le beige Recto puis le noir Recto et Verso, et une couverture beige. Les présentations et démarches existantes des deux versions sont conservées sans réécriture. L’ancienne adresse `myledmask-v2.html` redirige vers `myledmask.html`. La galerie compte donc 13 réalisations et les suivantes sont renumérotées de 04 à 13. La plaquette et l’identité visuelle Ethiopik conservent leurs images actuelles, comme demandé. Les six JPG Instagram AM Project du lot `BF898544-0FE2-4C92-B92C-3681EA721E4C` remplacent toute l’ancienne série, y compris le sixième WebP ; la publication LinkedIn du lot `6C498113-96A4-4FA5-B262-B45F0192159F` devient prioritaire.

La génération, les contrôles statiques des associations et des routes, et le contrôle du diff ont été relancés avec succès après le regroupement et les derniers imports : 21 documents HTML, dont 13 fiches et cinq redirections. Le contrôle global des 38 réceptions est également réussi : chaque source correspond à sa destination et à son empreinte SHA-256. Les liens de téléchargement pointent tous vers le dernier CV installé ; les marques restent regroupées et les sept projets conservés sont présents. Les tests d’interactions simulées existants concernent le code JavaScript inchangé ; aucun nouveau test navigateur n’est revendiqué.

## Contrôles réussis

| Contrôle | Résultat et portée |
| --- | --- |
| `python scripts/build.py` | PASS : 3 pages principales, 13 fiches et 5 redirections de compatibilité. |
| `python scripts/check.py` | PASS : 21 documents HTML, ordre des 13 projets et des 3 aperçus, liens locaux, ancres, images, dimensions, textes alternatifs, métadonnées, contenus des deux versions myLEDmask conservés, CV et navigation précédent/suivant. |
| `node --check script.js` | PASS : syntaxe JavaScript. |
| `node scripts/test-interactions.cjs` | PASS dans un DOM simulé : menu, Échap et focus, fermeture après navigation, visionneuse et retour du focus, lien original de secours sans dialogue, déclenchement des apparitions, géométrie SVG et redimensionnement, animations réduites, absence d’observateurs, formulaire natif et erreurs de validation. Aucun email envoyé. |
| `git diff --check` | PASS : pas d’erreur d’espacement du diff. |
| Empreintes SHA-256 | PASS global : les 38 réceptions du manifeste ont été vérifiées ; chaque source correspond octet pour octet à sa destination et à son empreinte SHA-256. Les réceptions identiques réutilisent leurs fichiers ; les nouvelles copies sont préservées sans retouche. Les 42 images et références initiales restent conservées et l’ancien CV est archivé à l’identique. |
| URL publique existante | HTTP 200 à `https://maddalenacerena-iut.github.io/portfolio/`. Vérifie seulement sa disponibilité, pas la publication des corrections locales. |

Le contrôle statique vérifie notamment un seul SVG de frise contenant le tracé et les trois cercles, chacun sur un endpoint du tracé. Le test JavaScript fournit cinq scénarios de rectangles correspondant aux largeurs demandées 375, 430, 768, 1024 et 1440 px : il vérifie les coordonnées communes, le rayon circulaire et leur recalcul. **Ces rectangles sont simulés et ne sont pas des mesures d’une mise en page de navigateur.**

Les sept projets non renvoyés, conservés selon la consigne de Céréna, sont listés dans `REVIEW.md` : leurs fichiers et textes sont inchangés, hors numérotation.

Les images floutées sont exclusivement celles des cartes. Les détails utilisent les originaux nets, sans redimensionnement des fichiers sources. La liste et les légendes sont centralisées dans `content/projects.json`, la provenance dans `content/assets.json`.

## Corrections confirmées après réception des fichiers

- Dernier CV retransmis : contenu identique au CV de novembre 2026, copié exactement au chemin de téléchargement ; DUT et L3 cohérents avec le portfolio.
- Orthographe **Hôtel Mocka / Anyx** alignée après confirmation explicite de Céréna.
- **Harmonia — Affiche** est confirmé à nouveau par Céréna ; l’affiche retransmise est identique au JPG intégré. Aucune capture de site Harmonia n’est attendue.
- myLEDmask version 1 : original beige, recto seul ; version 2 : noir et rouge, recto puis verso. Céréna a confirmé cet ordre, puis demandé de conserver les deux versions et les trois visuels dans une seule fiche myLEDmask — Flyer.
- AM Project — Site web : les quatre captures originales du dépôt sont utilisées ; aucune adresse publique non confirmée ajoutée.
- Aucune flèche Unicode ou emoji dans les pages : actions en SVG. Action Agrandir discrète. Focus clair sur les fonds sombres et bouton de fermeture aligné avec son icône.
- Fond floral généré historique conservé sur disque sans affichage. Après demande explicite de Céréna, qui ne possède pas l’original, une nouvelle image a été créée depuis l’exemple et intégrée sous `images/accueil/fond-floral-recree.webp`. Cette autorisation est limitée au décor d’accueil ; aucune création professionnelle n’est remplacée par une image générée.

La nouvelle image du fond d’accueil est une recréation sans texte, optimisée en WebP sans recadrage de la source générée : 1942 × 809 px, 36 448 octets. Elle a été inspectée visuellement comme fichier image. Le générateur, le contrôle statique, la syntaxe JavaScript, les tests d’interactions simulées et le contrôle du diff ont été relancés avec succès après son intégration. Le contrôle statique vérifie aussi sa présence dans l’accueil, la disparition de la mention d’attente et l’absence de ce décor dans les réalisations. Le positionnement à droite sur petits écrans et le voile sombre mobile sont préparés dans le CSS. Cela ne constitue pas une validation de fidélité ou de responsive dans un navigateur.

## Vérifications non réalisées

### Navigateur et appareils

Aucune recette dans un navigateur réel ni sur iPad n’a été effectuée. Le contrôle d’environnement annonce un bureau distant activé, d’état `unknown`, mais aucun outil `cua_repl.js` n’est proposé dans la session. Les modules installés ne constituent pas un outil navigateur utilisable dans cette conversation.

L’environnement est configuré avec `SITES_MANAGED_LINUX_CONTAINER=1`. Le [guide Sites](skill://plugin_connector_1p_689987207de08191979cf68eca2941c6/sites/SKILL.md) prescrit : « If `cua_repl.js` is unavailable, skip browser QA: do not start a preview server, install a browser, or improvise another browser-control path. » Aucun serveur de prévisualisation ni autre chemin navigateur n’a donc été lancé.

Environnement concerné : `ccarenv_b64_Y2NhcmVudl8yZWNhMjc1OGU2Yjg4MTkxYjhlZmQ0MDhiOTk2MTIyOQ`.

Il reste à vérifier à **375, 430, 768, 1024 et 1440 px** : fidélité aux captures, débordements, lisibilité, alignement de la frise pendant le défilement et après changement d’orientation, menu, clavier, focus piégé dans le dialogue natif, Échap, agrandissement mobile et réduction des animations. Les styles responsives et les tests simulés ne remplacent pas ces contrôles.

### Formulaire

FormSubmit est configuré en POST natif, avec validation des champs, email, limites de longueur, refus des messages composés uniquement d’espaces, champ piège `_honey` et CAPTCHA du prestataire non désactivé. Il n’existe aucune confirmation locale simulée ni requête AJAX interprétée comme une preuve de livraison.

Activation dans la boîte destinataire, réception effective, erreurs réseau et parcours de confirmation du prestataire **non vérifiés**. Aucun envoi réel n’a été effectué. Les étapes restent décrites dans [README.md](README.md).

### Déploiement

Aucun push et aucun déploiement de la version corrigée. Les fichiers HTML autonomes et chemins relatifs conservent `/portfolio/` sans routeur SPA ; leur rafraîchissement sur GitHub Pages reste à contrôler après publication, pour les 16 adresses principales et les cinq redirections, ainsi que les images, le CV et Contact depuis chaque fiche.

## Éléments encore nécessaires

- Photographie d’ambiance À propos ; le fond floral original n’est plus attendu puisque Céréna a explicitement demandé sa recréation depuis l’exemple.
- Catalogue Ethiopik complet et PDF de plaquette si disponibles ; seuls les extraits effectivement reçus sont présentés.
- Périmètre exact de contribution aux identités Ethiopik et AM Project ; notes conservées sans attribution inventée.
- URL publique AM Project si un lien externe est souhaité.

**La version corrigée est préparée et ses contrôles automatiques passent. La finalisation visuelle, la réception du formulaire et la publication ne sont pas déclarées terminées.**
