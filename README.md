# Guess Who's Back - bot Discord

Bot Discord modulaire en Python avec `discord.py`. Il utilise des commandes slash, des événements de serveur et un fichier JSON local pour conserver les données.

## Fonctionnalités

- Modération : avertissements, mute temporaire, expulsion, bannissement, mode lent, nettoyage des messages et filtre de mots interdits.
- Salons : création et suppression confirmée de salons textuels, vocaux et de catégories.
- Tickets privés avec fermeture par bouton ou commande.
- Rôles automatiques attribués aux nouveaux membres.
- Niveaux et statistiques d'activité.
- Anniversaires, concours et rappels.
- Suggestions, notes partagées, sondages et commandes de divertissement.
- Messages de bienvenue/départ, réponses automatiques et journalisation de suppressions.

## Commandes slash

| Catégorie | Commandes |
| --- | --- |
| Modération | `/avertir`, `/avertissements`, `/effacer_avertissements`, `/mute`, `/demute`, `/expulser`, `/bannir`, `/renommer`, `/mode_lent`, `/nettoyer`, `/ajouter_mot_interdit`, `/retirer_mot_interdit`, `/liste_mots_interdits`, `/vider_mots_interdits` |
| Salons | `/creer_salon_textuel`, `/creer_salon_vocal`, `/creer_categorie`, `/supprimer_salon_textuel`, `/supprimer_salon_vocal`, `/supprimer_categorie` |
| Tickets | `/creer_ticket`, `/fermer_ticket` |
| Utilitaires | `/rappel`, `/calculer` |
| Rôles | `/role_auto_ajouter`, `/role_auto_retirer`, `/role_auto_liste` |
| Statistiques | `/niveau`, `/classement`, `/statistiques` |
| Événements | `/definir_anniversaire`, `/voir_anniversaire`, `/concours`, `/concours_relancer` |
| Contenu | `/suggestion`, `/creer_note`, `/voir_note`, `/liste_note`, `/supprimer_note` |
| Créatif | `/citation`, `/nom_aleatoire`, `/couleur_aleatoire` |
| Informations | `/info_serveur`, `/info_membre`, `/avatar`, `/ping`, `/youtube` |
| Fun | `/de`, `/pile_ou_face`, `/boule_magique`, `/sondage`, `/emoji_aleatoire` |
| Aide | `/aide` |

Les commandes préfixées par `!` sont aussi disponibles : `!invite`, `!test`. `!recharger` et `!cogs` sont réservées au propriétaire du bot.

### Permissions

Les commandes de modération vérifient la permission adaptée au rôle de la personne qui les utilise. `/renommer` requiert **Gérer les surnoms** pour le modérateur et le bot; le rôle du bot doit aussi être au-dessus du membre à renommer. La gestion des salons requiert **Gérer les salons** pour l'utilisateur et pour le bot. Les commandes de suppression demandent une confirmation. La fermeture d'un ticket est réservée à son créateur ou à un administrateur.

Accorde au bot seulement les permissions nécessaires aux fonctionnalités activées. Les commandes de modération ont notamment besoin des permissions Discord correspondantes (gérer les messages, modérer, expulser, bannir); les outils de salons, tickets et rôles nécessitent respectivement gérer les salons ou gérer les rôles.

## Installation locale (Windows / PowerShell)

Prérequis : Git et Python 3.10 ou plus récent.

```powershell
git clone https://github.com/xNxggets/Guess_whos_back.git
cd Guess_whos_back
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Dans `.env`, renseigne le token du bot :

```dotenv
DISCORD_TOKEN=colle_ton_token_ici
```

Dans le Discord Developer Portal, active les intents privilégiés **Server Members**, **Message Content** et **Presence**. Le code active également les intents standards nécessaires aux événements de messages et de réactions.

Démarre le bot depuis le dossier du projet :

```powershell
python main.py
```

Le bot synchronise ses commandes slash lors de sa connexion. Laisse le terminal ouvert pendant son exécution; `Ctrl+C` l'arrête.

## Données et configuration

- `main.py` démarre le bot et charge les extensions répertoriées dans `COGS`.
- `cogs/` contient les commandes et gestionnaires d'événements.
- `utils.py` regroupe les fonctions communes.
- `data/storage.py` charge et sauvegarde les données.
- `data/data.json` est créé et modifié localement. Il contient des identifiants et des données de membres/serveur : il est ignoré par Git et n'est pas fourni dans le dépôt.
- `.env` contient le token Discord et est ignoré par Git. `.env.example` est le modèle sans secret.
- `requirements.txt` liste les dépendances Python.

Pour déployer le bot sur un hébergeur, configure `DISCORD_TOKEN` dans son gestionnaire de secrets et prévois un stockage persistant pour `data/data.json`. Ne place jamais le token dans le code, dans un commit ou dans les journaux.

## Sécurité

Le token du bot donne accès à ses actions selon les permissions accordées sur les serveurs. Si le token a été publié, même brièvement, régénère-le dans le Discord Developer Portal et remplace sa valeur dans `.env` et sur l'hébergeur. Ajouter `.env` au `.gitignore` empêche les futurs ajouts Git, mais n'efface pas les anciens commits ni les copies déjà clonées.
