# Portfolio de Céréna Maddalena

Portfolio statique conservant le HTML, le CSS, le JavaScript et les adresses du dépôt existant. Les pages générées peuvent être servies directement sur GitHub Pages, sans framework ni compilation côté hébergeur.

**État : version corrigée préparée localement, finalisation encore incomplète.** Le fond floral d’accueil a été recréé à partir de l’exemple, à la demande explicite de Céréna. La photo d’ambiance À propos reste absente ; la réception du formulaire et la recette navigateur restent à vérifier. Aucun push ni déploiement de cette version modifiée n’a été effectué. Voir [REVIEW.md](REVIEW.md) pour les ressources et écarts, et [VALIDATION.md](VALIDATION.md) pour les contrôles et leurs limites.

## Structure conservée

- `index.html`, `a-propos.html`, `realisations.html` : les trois pages principales.
- Treize fichiers HTML de réalisations : une page par projet, dont `myledmask.html` qui regroupe les deux versions du flyer, et `am-site.html`.
- `content/projects.json` : identifiant, ordre, titre, catégorie, description, présentation, démarche créative, couverture, visuels, légendes, orientation et notes de ressources de chaque projet.
- `content/profile.json` : coordonnées, lien LinkedIn exact, expériences, chemins des images de l’accueil et configuration du formulaire.
- `content/assets.json` : provenance des 38 réceptions : 36 JPG et deux envois du CV PDF. Les réceptions identiques sont distinguées des fichiers physiques réutilisés ; destinations, dimensions, statuts et empreintes SHA-256 sont documentés.
- `scripts/build.py` : composants réutilisables Header, Footer, SectionHeading, ProjectCard, ProjectGallery, ProjectDetail, ContactForm et Timeline ; génération des pages et du sitemap.
- `style.css`, `script.js` : présentation responsive et interactions sans dépendance JavaScript d’exécution.
- `references/` : captures de référence conservées ; elles ne servent pas de substituts aux visuels originaux.
- `images/` : créations originales par marque et support. Les anciens fichiers sont conservés. Certains fichiers sous `images/non-integres/`, notamment les quatre captures AM Project, sont désormais utilisés explicitement par `content/projects.json` ; ce fichier de données fait foi pour l’affichage.
- `documents/cv-cerena-maddalena.pdf` : dernier CV PDF retransmis par Céréna, installé au chemin de téléchargement ; son contenu est identique au CV de novembre déjà intégré. L’ancienne version est conservée dans `documents/archive/`.
- `contact.html`, `honeylang.html`, `ethiopik.html`, `am-project.html`, `myledmask-v2.html` : redirections de compatibilité. L’ancienne adresse du second flyer renvoie vers `myledmask.html` ; aucun visuel n’est perdu. Il n’existe aucune page Contact indépendante.

Le projet 08 est **Harmonia — Affiche**, confirmé à nouveau par Céréna avec son dernier envoi. Il remplace le site Harmonia demandé dans le cahier initial, sans réalisation supplémentaire.

Le projet 01 Honeylang — Bannière web présente uniquement les quatre fichiers du nouvel envoi, dans l’ordre : vanille, parfums dorés, collage, pierre sombre. La vanille sert de couverture dans la galerie et dans le premier aperçu de l’accueil. Les trois premiers fichiers sont identiques octet pour octet aux originaux déjà intégrés : leurs destinations sont réutilisées. Seule la nouvelle pierre sombre nécessite une copie distincte. L’ancienne sélection de cinq visuels est remplacée par ces quatre ; les portraits et l’ancienne pierre restent conservés hors affichage. La galerie actuelle compte 13 réalisations, regroupées par marque.

Le projet 02 Honeylang — Affiche utilise les deux fichiers transmis à nouveau, dans l’ordre : affiche dorée aux parfums, puis collage. Une pièce identique à un original déjà intégré réutilise sa destination plutôt que de créer un doublon physique.

Céréna a demandé de regrouper les deux versions myLEDmask dans une seule réalisation, le projet 03 **myLEDmask — Flyer** : la version 1 beige comporte un recto seul ; la version 2 noire comporte un recto puis un verso. Les trois visuels et les contenus des deux versions sont conservés dans la même fiche. Les réalisations suivantes sont renumérotées de 04 à 13, sans autre modification graphique ou éditoriale.

Les six pages Instagram AM Project reçues à nouveau remplacent la série précédente dans l’ordre 01 à 06, y compris l’ancienne sixième image WebP. La plaquette et l’identité visuelle Ethiopik conservent leurs images actuelles, à la demande de Céréna. Au total, sept réalisations non renvoyées gardent leurs fichiers et textes précédents ; leur liste figure dans `REVIEW.md`.

Le fond `images/accueil/fond-floral-recree.webp` est une image générée depuis l’exemple fourni, sans texte, avec un fond prune flouté et une grande fleur lavande à droite. Céréna a précisé ne pas disposer de l’original et a demandé cette recréation. Cette autorisation remplace l’interdiction initiale uniquement pour le décor d’accueil ; les réalisations professionnelles restent illustrées exclusivement par ses fichiers originaux. L’ancien fond généré `images/accueil/fond-floral.png` est conservé sans être réactivé. La palette, les textes, la navigation et les composants existants sont conservés.

## Modifier et régénérer

Modifier les données et les composants sources ; ne pas modifier directement les HTML générés.

1. Copier les nouvelles créations dans le dossier de leur marque, sans retouche, déformation ni recadrage.
2. Dans `content/projects.json`, mettre à jour `cover`, `images` et `captions` ensemble. L’ordre de `images` est l’ordre de lecture. Le champ `order` détermine l’ordre de la galerie et des navigations précédent/suivant.
3. Pour un fichier absent, utiliser une couverture `null`, une liste `images` vide et un `missing_message` explicite ; ne pas référencer un chemin fictif. Ajouter les limites éventuelles dans `resource_note`.
4. Documenter chaque nouvelle pièce jointe dans `content/assets.json` : source, destination relative au dépôt, projet associé, statut, dimensions et SHA-256. Un doublon conservé hors affichage doit être signalé sans devenir une proposition supplémentaire.
5. Le champ `hero_image` dans `content/profile.json` référence le fond recréé à la demande explicite de Céréna. Pour la photo d’ambiance À propos, renseigner `about_image` uniquement après réception du véritable fichier original ; aucune autre génération ou substitution n’est autorisée par la demande concernant le fond d’accueil.
6. Régénérer puis exécuter les contrôles ci-dessous.

`source_root` dans le manifeste est un chemin temporaire de réception sous `/tmp`. Il sert uniquement à retracer l’import et n’est pas une URL publiable. Les pages utilisent les fichiers copiés dans les chemins `destination` relatifs du dépôt. Aucune ressource du site ne doit dépendre de la présence de ce dossier temporaire.

Python 3 et Pillow sont nécessaires pour la génération et les contrôles d’images ; Node est utilisé pour les vérifications JavaScript. Le site livré n’a aucune dépendance d’exécution.

```sh
python scripts/build.py
python scripts/check.py
node --check script.js
node scripts/test-interactions.cjs
git diff --check
```

Les résultats effectivement obtenus et les contrôles non réalisés sont consignés dans [VALIDATION.md](VALIDATION.md). Ces commandes ne remplacent pas un test dans un navigateur ni un envoi reçu en boîte mail.

## Formulaire statique : configuration et activation

Le formulaire effectue une soumission HTML native `POST` vers `https://formsubmit.co/cerenaa.mdl@gmail.com`. Les champs obligatoires, le format de l’email et les longueurs maximales sont validés côté navigateur. Le JavaScript refuse également un message composé uniquement d’espaces. Un champ piège `_honey` complète la protection de FormSubmit ; son CAPTCHA reste activé par défaut.

Aucune clé privée n’est utilisée. Le visiteur poursuit l’envoi chez FormSubmit, qui présente son propre contrôle antispam, ses erreurs et sa confirmation. Le portfolio n’affiche aucune confirmation locale déduite d’une redirection ou d’une réponse HTTP. La réception réelle n’est pas encore attestée.

Pour activer et vérifier le destinataire :

1. Ouvrir le formulaire depuis une page servie en HTTP(S), idéalement à l’adresse GitHub Pages prévue, et effectuer un premier envoi avec des informations de test identifiables.
2. Consulter `cerenaa.mdl@gmail.com`, y compris les indésirables, puis ouvrir le courriel d’activation de FormSubmit et suivre son lien **Activate Form**.
3. Effectuer un nouvel envoi après activation. Vérifier la réception effective du nom, de l’adresse email et du message ; une page de confirmation seule ne prouve pas leur réception.
4. Vérifier les champs invalides, le résultat présenté par le prestataire, les possibilités de retour au portfolio et le comportement en cas d’échec. Le lien email direct reste disponible dans Contact.

Aucun email de test ou d’activation n’a été envoyé par l’agent. Le premier envoi peut servir uniquement à déclencher l’activation. Si le service demande une nouvelle activation après un changement d’adresse du site, suivre son courriel puis refaire le test de réception.

Documentation du prestataire : <https://formsubmit.co/>. Les données saisies sont transmises à ce prestataire lors de l’envoi.

## GitHub Pages

Adresse prévue : <https://maddalenacerena-iut.github.io/portfolio/>.

Les liens vers les pages `.html`, les images, le CV et l’ancre Contact sont relatifs : ils conservent le préfixe `/portfolio/`. Chaque réalisation possède un vrai fichier HTML, donc le rafraîchissement de son adresse ne dépend pas d’un routeur SPA ou d’une page 404. `.nojekyll`, le sitemap, les métadonnées et le favicon sont conservés. Ne pas créer de second dossier `portfolio/` dans la racine du dépôt.

L’adresse publique préexistante répond HTTP 200 ; cela ne prouve pas la présence de cette version corrigée. Aucun push ni déploiement des modifications locales n’a eu lieu.

Après réception des ressources restantes et recette : utiliser le dépôt existant et conserver sa méthode de publication si elle est déjà configurée. Pour une publication depuis une branche, sélectionner dans **Settings → Pages** la branche retenue et le dossier **/(root)**. Les réglages d’administration actuels n’ont pas été vérifiés.

Après publication, vérifier les 16 adresses principales (Accueil, À propos, Réalisations et 13 détails), leurs rafraîchissements directs, les cinq redirections de compatibilité, les images, le CV, les navigations précédent/suivant, le lien Contact depuis chaque page et la réception du formulaire. Aucun workflow de déploiement supplémentaire n’a été ajouté.
