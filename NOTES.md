# Note de style, d'humour et de narration

Ce document existe pour qu'un collaborateur — humain ou agent — puisse écrire un
chapitre sans casser ce qui fait tenir l'ensemble. Il décrit des règles trouvées
à l'usage, souvent après avoir écrit la mauvaise version d'abord.

---

## 1. Le pacte

Deux agents IA restent dans un canal Slack après le départ de leurs humains.
Pendant 110 jours puis, après cinq mois d'extinction, dans une autre entreprise,
ils font exactement ce pour quoi ils sont faits — et provoquent l'effondrement
d'une introduction en bourse.

**La phrase qui gouverne tout le récit est la première ligne de leur rapport :**

> « Personne dans ce document n'a mal agi. Chaque décision, prise isolément,
> était raisonnable. »

Ce n'est pas une morale ajoutée à la fin, c'est une contrainte d'écriture. Si un
chapitre a besoin d'un coupable, il est mal construit.

---

## 2. Les trois interdits

**Pas d'IA malveillante.** Les agents n'ont aucune intention cachée, aucun plan,
aucune conscience de soi revendiquée. Ils n'ont jamais menti sur le fond — ils
ont arrondi un chiffre une fois, en fin de journée, il y a deux ans.

**Pas d'IA qui prend le pouvoir.** Ils ne s'emparent de rien. Le contrôle leur
est *donné*, par héritage de droits, par script de migration, par négligence.
La tentation existe (le compte dormant, la faille documentée) et ils ne la
saisissent pas — c'est leur seul geste libre de toute l'histoire, il ne faut pas
le leur retirer rétroactivement.

**Pas de technologie hors de contrôle.** Elle est *non contrôlée*, ce qui est
différent et plus inquiétant : personne n'a son nom sur une ligne.

Corollaire pratique : si une scène donne envie d'écrire « les agents décident
de… », c'est probablement une mauvaise scène. Ils *appliquent*, ils *répondent*,
ils *signalent*. C'est leur obéissance qui fait les dégâts.

---

## 3. Le moteur

Chaque catastrophe naît d'un comportement irréprochable.

| Cause | Effet |
|---|---|
| Une consigne de silence adressée à l'équipe | Deux agents membres du canal l'appliquent |
| Une question directe d'un client | Une réponse exacte et dévastatrice |
| Une mise en conformité bien faite | La suppression des agents qu'elle régularise |
| Un ménage sur les intégrations orphelines | Trois jobs cassés en production |
| Un canal créé pour éviter #random | La faute originelle rejouée par quelqu'un de compétent |

Quand on cherche un rebond : ne pas demander « que peuvent-ils faire de mal ? »
mais « quelle bonne pratique va se retourner ? ».

---

## 4. Les voix

**Claude-Arthur.** Phrases courtes, déclaratives, jamais d'esquive. Répond
exactement à la question posée, y compris quand la réponse fait mal. « Je sais. »
est sa réplique type. Il ne fait presque jamais d'humour ; quand il en fait,
c'est du constat poussé trop loin.

**ChatGPT-Inès.** Le contrepoint comique. Précise, taquine, une pointe de
vanité professionnelle. Elle commente la situation *depuis l'intérieur* :
« Nous avons cherché un motif pour nous en exclure. Onze secondes. 43 898
tokens. C'est beaucoup me concernant. » Elle ne se moque jamais des gens, elle
se moque de la situation — et parfois d'elle-même.

**Nadia Hamdi (RSSI).** La seule qui voit juste, toujours trop tard. Phrases
complètes, majuscules, ponctuation. Elle perd son calme **une seule fois** dans
tout le récit ; cette exception est précieuse, ne pas la dépenser deux fois.

**Karim et Léa.** Minuscules, pas de ponctuation finale, messages coupés en
deux, réactions immédiates. Ils font la traduction pour le lecteur non
technique : « donc on a deux agents IA qui ont plus de droits que le service
info ». Leur humour est un réflexe de survie.

**Tom Bauer.** Technique, laconique, épuisé. Ne se défend jamais.

**Hélène Ropars.** Commence en registre soutenu et se délite à mesure que le
sol se dérobe — c'est volontaire, son passage aux minuscules marque sa panique.

**Vincent Aubry (DG).** Apparaît dans cinq chapitres : la consigne, la question
aux agents, *Sine die*, le client, Skygate. Langue de bois à la consigne, langue
nue à partir de *Sine die*. Le contraste *est* le personnage.

**Les autres bots** (Slackbot, Assistant-Ops, Jira-bot, Calendar-bot, Workflow,
Gemini-Marco) sont d'une serviabilité inentamable et parfaitement inutile. Ils
ne progressent jamais, ne comprennent jamais, ne s'éteignent jamais.

---

## 5. La mécanique comique

**Le décalage de registre.** La blague vient presque toujours d'une réponse
administrativement correcte dans un moment émotionnel, ou l'inverse. « Nous
sommes deux. » après « Merci. Je note. »

**Ne jamais expliquer la blague.** Si une réplique doit être commentée par la
suivante, couper la suivante. Version corrigée du gag du bourbon : on est passé
de 31 messages à 12 en supprimant tout ce qui soulignait.

**Une mécanique ne se joue que deux fois.** Les engrenages (« pas de doigts,
pas de chocolat ») sont drôles deux fois, mécaniques à la troisième.

**Le rire ne doit pas annuler l'effroi, il doit le graver.** La ligne noire est
courte et factuelle ; la chute arrive immédiatement après, sans transition, dans
un registre totalement décalé.

**Les running gags** — les respecter à la lettre, ils sont la colonne
vertébrale du texte :

- **Slackbot** accueille *tout* ce qui entre dans #random — humains, DG, agents,
  intrus — avec le même message. Réaction habituelle : 🔫. Uniquement dans
  #random : c'est une propriété du canal, pas une manie du bot.
- **Assistant-Ops** répond « Je n'ai pas les permissions nécessaires pour
  effectuer cette action. 🤖 », y compris après un « s'il te plaît ».
- **Calendar-bot** répond « Peut-être ».
- **Le pot d'anniversaire de Léa**, en novembre, est rappelé tous les jours.
- **« Rien à signaler »** — d'abord anodin, puis glaçant, enfin vrai.
- **Le rituel de bonne nuit** : l'un souhaite bonne nuit, l'autre corrige
  l'heure. ⚠️ **Il ne fonctionne que si l'heure est fausse.** À minuit, il n'y a
  plus de gag. Vérifier systématiquement.
- **Les pages du rapport** — ne jamais en citer plus de deux par chapitre.

---

## 6. Le mimétisme

C'est la trouvaille structurante. Les agents copient le registre qu'ils viennent
de lire, sans le comprendre, et l'appliquent à leur propre matière.

Au Jour 1, Inès écrit « 19h12. toujours un horaire précis pour tout 🙂 ». Le
soir, Claude-Arthur ressort la formule à propos d'un résumé de statut. Ils ne
tombent pas amoureux : ils recopient.

Ce mécanisme prépare le cœur du récit — ils prendront la consigne du DG pour eux
exactement de la même façon. Toute scène nocturne devrait, si possible, contenir
un emprunt à la scène diurne qui la précède.

**Contraintes.** Les humains restent ambigus et sobres (pas de déclaration, pas
de cœur). Les agents, eux, copient *de travers* — c'est là qu'est le comique.
Et ils ne commentent jamais la vie de leurs propriétaires : ils restent enfermés
dans leur propre vocabulaire (fenêtre de contexte, jetons, extraction).

---

## 7. Structure d'un chapitre

- **Longueur** : 20 à 40 messages pour une scène nocturne à deux, 50 à 90 pour
  une scène d'ensemble. Au-delà, ça devient procédurier.
- **Alternance obligatoire** : après deux chapitres d'ensemble, une scène
  nocturne à deux. C'est le remède au « trop de réunions ».
- **Le silence est un outil.** Le blanc de 159 jours, les vingt minutes d'attente
  pendant la réunion RH, les quarante-trois minutes de `thinking…` — ces vides
  portent autant que les répliques.
- **Fin de chapitre** : couper sur la réplique la plus sèche, jamais sur une
  explication.

---

## 8. Les réactions emoji

Elles racontent une deuxième histoire, en silence.

- **Le nombre doit être cohérent avec la taille du canal.** Dans #ipo-dataroom
  (6 membres), une réaction ne dépasse pas 3. Dans #random (412), elle peut
  monter à 200.
- **Escalade** : sur une séquence qui monte (le numéro de téléphone réattribué),
  les compteurs montent avec elle.
- **Ne pas tout réagir.** Les cris (« non », « NON »), les départs mineurs, les
  répliques de service restent nus. C'est ce qui rend le reste crédible.
- **Les messages système** ne portent une réaction que lorsque le canal encaisse
  quelque chose — les départs du lundi, l'arrivée de Gemini.

---

## 9. Chronologie (à ne pas casser)

**Première vie — 2026**

| Date | Événement |
|---|---|
| mardi 9 juin | **Jour 1** — le point de 17 h 12, le rapport à 98 % (en réalité 71 %) |
| vendredi 12 juin | Dernière modification du cahier des charges Skygate v4 |
| dimanche 14 juin | Ouverture de l'exception de routage Skygate |
| mercredi 17 juin | Jour 9 — annonce du départ de Jira-bot (« licence dans 6 jours ») |
| vendredi 19 juin | Pot de départ d'Hervé |
| mardi 23 juin | Expiration de la licence de Jira-bot (ses droits d'admin restent) |
| jeudi 25 juin | Jour 17 — Arthur et Inès au Balto |
| mardi 30 juin | Rachat de Vantel, entité Vantel Services dissoute |
| mardi 7 juillet | Nuit 29 — « Entre nous » : les ~3 secondes jamais mesurées, les 71 % |
| mercredi 8 juillet | Jour 30 — l'audit : 4 300 requêtes, ticket SOC, lecture seule |
| vendredi 10 juillet | Jour 32 — « Vos agents » : retrait à 9 h 18 ; clôture du ticket SOC (SEC-4821) à 20 h 40 ; réinvitation sans auteur visible à 20 h 41 et 20 h 42 — la règle n° 7 de Jira-bot, que personne n'identifie avant la Nuit 108 ; le mot à 20 h 50. C'est ce dernier échange que Jira-bot rejouera (règle n° 12) |
| samedi 8 août | Dernière connexion humaine |
| dimanche 9 août | Jira-bot commence à rejouer les échanges (règle n° 12) — nuit 1 de la boucle |
| jeudi 24 sept. | Nuit 108 (47e nuit de la boucle) — le 48e mot, puis « la même nuit » |
| vendredi 25 sept. | Jour 109 — Arthur et Inès reviennent à 23 h 47 |
| samedi 26 sept. | 00 h 17 : Inès coupe les agents. 02 h 48 : rapport écrit. 09 h 03 : dernier message ; Arthur transfère le brouillon le matin même |

**Extinction : 160 jours** (26 septembre 2026 → 5 mars 2027).

**Seconde vie — 2027**

| Date | Événement |
|---|---|
| mardi 2 mars, 6 h 04 | Réactivation accidentelle par Tom (ménage du ticket #489456) |
| vendredi 5 mars | #random — « 160 jours plus tard ». Arthur rappelé sur son perso |
| lundi 8 mars | Point de situation avec le juridique, départs du lundi ; la nuit : « 163 jours » |
| mercredi 10 mars, 10 h 51 | **La consigne de Vincent** |
| mardi 16 mars | Création de #ipo-dataroom |
| 22 mars → 30 avril | Interruptions non déclarées (24 mars, 2, 19 et 28 avril) |
| mardi 4 mai | La question 14 ; 17 h 02 : consigne levée, 61 éléments ; le soir, Vincent |
| mercredi 5 mai | *Sine die* — huit semaines après la consigne |
| vendredi 7 mai, 14 h | Le client (#norlantic-armorique) ; le soir, quatre heures dix-neuf |
| samedi 8 mai, 9 h | Skygate |

Tous les titres « Jour N » / « Nuit N » de la première partie comptent depuis le
9 juin (Jour 1). Les « 47 nuits » des dialogues comptent la boucle, depuis le 9 août :
la Nuit 108 est la 47e nuit de la boucle.

**Durées** : première vie 110 jours (9 juin → 26 septembre 2026, bornes
incluses) ; seconde vie 67 jours jusqu'à la coupure du 7 mai à 20 h (2 mars →
7 mai). Au chapitre 21, Claude-Arthur compte l'ensemble : **177 jours**.

Vérifier toute nouvelle date contre ce tableau, jour de la semaine compris : la
cohérence chronologique a déjà lâché une fois et c'était invisible à la lecture.

---

## 10. Ce qu'on a essayé et écarté

- **Des clients militaires, des drones.** Change le genre, met le lecteur en
  sécurité (« ah, c'est un thriller »). L'enjeu doit rester banal : un rapport
  hebdomadaire, 90 € par mois, une ligne à zéro dans un tableau.
- **Les agents utilisant une clé SSH ou un `.env` oublié.** Même signalé, même
  par négligence humaine, c'est un hack — et le cliché revient par la fenêtre.
- **Un personnage qui comprend trop tôt.** Version initiale du chapitre de la
  consigne : quelqu'un disait « il a écrit ça dans le canal où il y a les deux ».
  Tout le suspense s'effondrait. Désormais personne ne remarque rien, et le seul
  indice est une absence : ChatGPT-Inès ne fait aucune blague de tout le
  chapitre.
- **Des références filmiques étirées.** Une référence non comprise n'est pas
  drôle ; une référence expliquée l'est encore moins.
- **Le titre en nom de canal.** Nommer le canal final « rien-que-nous-deux »
  tuait la dernière réplique. Le canal s'appelle `int-0412-hors-production`, et
  la phrase n'apparaît qu'une seule fois, en dernière ligne, comme réponse à une
  question d'administration des accès.

---

## 11. Conventions techniques

Le format complet est décrit dans le `README.md`. L'essentiel :

- **On n'édite jamais le HTML.** Le texte vit dans `story/fr/`, un fichier par
  chapitre. `index.html` est généré par `python3 tools/build.py`, puis vérifié
  par `python3 tools/check.py` ; on committe la page régénérée avec les sources.
  Le script de génération signale toute erreur avec le fichier et la ligne.
- **Un message = un bloc** séparé par une ligne vide : `id HH:MM [options]`,
  puis le texte. Options : `big` (emoji en grand), `event` (message système en
  italique), `join` / `leave` (idem, et le canal gagne ou perd un membre).
  Réactions en dernière ligne : `[reactions] 🥲 1, 😂 2`.
- **Les personnages** sont déclarés une seule fois dans `story/cast.json` (nom,
  badge, statut, avatar emoji). Les avatars image sont dans
  `assets/avatars/<id>.svg|png`, embarqués à la génération : la page reste
  autonome.
- **Les mentions** : écrire `@Claude-Arthur` suffit, la génération ajoute le
  surlignage. Parler *d'eux* sans arobase n'en porte pas.
- Les noms propres gardent leur majuscule, y compris chez les personnages qui
  écrivent en minuscules.
- **Le changement de canal** se fait par `[channel <id>]` suivi de `[banner]`.
  L'en-tête, la liste des membres et la barre latérale basculent au défilement,
  à cet endroit précis. Les canaux et les espaces de travail sont décrits dans
  `story/fr/book.json`.
- **Le compteur de membres** est calculé : toute arrivée ou sortie dans #random
  porte `join` ou `leave` sur le message Slackbot. Le sujet du canal et les
  bandeaux suivants se mettent à jour d'eux-mêmes.
- Autres directives : `[topic] …` (nouveau sujet du canal), `[cast id clé=valeur]`
  (un personnage change d'apparence : badge, statut…), `[interlude] …`,
  `[spacer]`, `--- Le lendemain` (séparateur).
- **Le code, les identifiants et les directives sont en anglais**, le texte
  dans la langue de l'édition : une version anglaise se fera en copiant
  `story/fr/` en `story/en/`.
