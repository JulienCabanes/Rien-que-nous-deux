# Rien que nous deux

Fiction. Une conversation Slack de 1 255 messages, en 22 chapitres, du 9 juin 2026 au 8 mai 2027.

Deux collègues, deux agents IA, un projet commun. Nom de code : **skygate**.
Un soir, les humains descendent boire un verre. Les agents, eux, restent.

## Lire

En ligne : https://juliencabanes.github.io/Rien-que-nous-deux/

En local : ouvrir `index.html` dans un navigateur. La page est autonome :
styles, scripts et images sont embarqués, aucune dépendance réseau.

## Organisation

```
story/
  cast.json          personnages (communs à toutes les langues)
  fr/
    book.json        titre, textes d'interface, espaces de travail, canaux
    01-….txt         un fichier par chapitre, lus dans l'ordre des noms
assets/avatars/      une image par personnage : <id>.svg ou <id>.png
templates/           squelette HTML, CSS et JavaScript de la page
tools/build.py       story/ → index.html
tools/check.py       validateur de structure de la page générée
```

`index.html` est **généré** : on ne l'édite jamais à la main. On modifie
`story/`, puis on régénère.

> ⚠️ Après chaque modification de `story/`, `assets/` ou `templates/`, lancer
> `python3 tools/build.py` et committer le `index.html` régénéré avec le reste.
> Sinon le site en ligne ne change pas.

## Écrire un chapitre

Un fichier est une suite de blocs séparés par une ligne vide.

### Messages

```
arthur 17:12
Salut Iris ! On fait un point rapide ? @Claude-Arthur où est-ce qu'on en est ?

claude 17:12
**Résumé automatique du statut :**
Les connecteurs API Skygate v2 sont configurés.
[reactions] 🥲 1, 😂 2
```

- Première ligne : l'identifiant du personnage (voir `story/cast.json`) et
  l'heure `HH:MM`, affichée `17 h 12`.
- Lignes suivantes : le texte. Un retour à la ligne reste un retour à la ligne.
- `**gras**` ; `@Nom Complet` d'un personnage devient une mention.
- Typographie : tapez des espaces normales (« Salut Iris ! », « 17 h 12 »). Avec
  `"typography": "fr"` dans `book.json`, la génération les rend insécables
  (fines avant `? ! ;` et dans « », normales avant `:`, dans les heures, les
  milliers, `%` et `€`).
- `[reactions] 🥲 1, 😂 2` : réactions, en dernière ligne.
- `[next]` : deuxième paragraphe séparé, comme un second envoi à la suite.
- `[thinking] ✳︎ thinking… | 43 min 18 s` : bloc « en train de réfléchir ».

Options après l'heure :

| option  | effet |
|---------|-------|
| `big`   | texte en grand (emoji seul) |
| `event` | message système en italique gris (révocations…) |
| `join`  | arrivée : le canal gagne l'auteur (et chaque `+id` qui suit) |
| `leave` | départ : le canal perd l'auteur (et chaque `+id` qui suit) |

Comme dans Slack, une arrivée ou un départ est **signé par la personne
concernée**, avec son avatar ; les arrivées simultanées tiennent sur une ligne.
Slackbot ne fait que l'accueil automatique de #random.

```
nadia 14:01 join
a rejoint #random.

claude 11:07 join +chatgpt
a rejoint #random ainsi que @ChatGPT-Iris.

slackbot 11:07
👋 Bienvenue dans le canal, @Claude-Arthur ! Présente-toi à l'équipe en quelques mots 🎉

nadia 14:29 big
😐
```

Le compteur **et les avatars de l'en-tête** suivent ces arrivées et départs.
Sans `join` / `leave`, le message s'affiche sans rien changer. Un personnage sans image ni emoji reçoit un avatar
à son initiale.

### Directives

Une directive tient sur une ligne ; plusieurs directives peuvent se suivre
dans le même bloc.

| directive | effet |
|-----------|-------|
| `# Jour 1 \| Un mardi ordinaire {#ch1}` | début de chapitre (titre, sous-titre, ancre facultative) |
| `--- Le lendemain` | séparateur de date ou d'heure |
| `[channel random]` | on passe dans ce canal (défini dans `book.json`) |
| `[banner]` | bandeau d'en-tête du canal courant |
| `[topic] Nouveau sujet…` | le sujet du canal change à partir du message suivant |
| `[cast arthur badge=guest status=none]` | un personnage change d'apparence à partir d'ici |
| `[interlude] 159 jours plus tard` | ellipse centrée |
| `[spacer]` | grand blanc vertical |
| `[members random -claude -chatgpt]` | arrivée ou départ hors champ (`+id` / `-id`), pour n'importe quel canal |

Le changement de canal, le nombre de membres, les avatars et le sujet
s'appliquent au défilement, quand l'endroit concerné atteint le milieu de
l'écran. Les compteurs sont
calculés : un `join` sur #random fait passer l'en-tête, le sujet et les
bandeaux suivants de 412 à 413 membres.

### Personnages et canaux

`story/cast.json` : `name`, et au besoin `badge` (`app`, `guest`, `external`),
`status` (emoji après le nom), `emoji` + `color` pour un avatar emoji. Sans
emoji, l'avatar est `assets/avatars/<id>.svg` ou `.png`.

`story/fr/book.json` : textes de l'interface (`ui`), barres latérales des
espaces de travail (`workspaces`) et canaux (`channels` : type `public`,
`private` ou `shared`, espace, nombre de membres, avatars affichés, sujet et
bandeau facultatifs).

## Vérifier et publier

```bash
python3 tools/build.py && python3 tools/check.py
```

`build.py` signale toute erreur de saisie avec le fichier et la ligne
(personnage inconnu, heure mal formée, directive inconnue…). `check.py`
vérifie la structure de la page générée.

Le site est publié par GitHub Pages depuis `main` (Settings → Pages → Deploy
from a branch → `main` / `root`) : c'est le `index.html` commité qui est en
ligne.

## Traduire

Copier `story/fr/` en `story/en/`, traduire les textes des chapitres et de
`book.json`, et y mettre `"lang": "en"` et `"output": "en/index.html"`. Les
identifiants, options et directives restent identiques dans toutes les
langues ; le format de l'heure et les libellés se règlent dans `ui`.

## Licence

Tous droits réservés. Les marques et logos cités appartiennent à leurs
propriétaires respectifs et ne sont utilisés qu'à des fins de fiction.
