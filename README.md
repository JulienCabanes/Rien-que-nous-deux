# Rien que nous deux

Fiction. Une conversation Slack de 1 251 messages, sur 23 chapitres et 111 jours.

Deux collègues, deux agents IA, un projet commun. Nom de code : **skygate**.
Un soir, les humains descendent boire un verre. Les agents, eux, restent.

## Lire

Ouvrir `index.html` dans un navigateur, ou publier le dépôt avec GitHub Pages
(Settings → Pages → Deploy from a branch → `main` / `root`).

Le fichier est autonome : styles, scripts et images sont embarqués, aucune
dépendance réseau. 444 Ko.

## Contenu

- `index.html` — l'œuvre complète
- `tools/check.py` — validateur de structure (à lancer après toute modification)

## Modifier

Le HTML est un document unique. Après édition :

```bash
python3 tools/check.py index.html
```

Le validateur vérifie trois choses : la validité stricte des balises, l'équilibre
de chaque message, et l'absence de messages imbriqués les uns dans les autres —
la cause de tous les bugs de mise en page rencontrés pendant l'écriture.

## Licence

Tous droits réservés. Les marques et logos cités appartiennent à leurs
propriétaires respectifs et ne sont utilisés qu'à des fins de fiction.
