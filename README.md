# 🤖 Bot Discord Polyvalent

Un bot Discord complet et modulaire développé en Python avec la bibliothèque `discord.py`. Ce bot offre plus de 40 commandes organisées en 10 catégories différentes, avec un système de stockage de données, des tâches automatisées et des fonctionnalités avancées.

## 📋 Table des matières
- [Fonctionnalités](#-fonctionnalités)
- [Architecture du code](#-architecture-du-code)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Système de stockage](#-système-de-stockage)
- [Structure des fichiers](#-structure-des-fichiers)
- [Personnalisation](#-personnalisation)
- [Dépannage](#-dépannage)
- [Contribution](#-contribution)

## ✨ Fonctionnalités

### 🛡️ **Modération (9 commandes)**
- **`/avertir`** : Avertir un membre avec une raison
- **`/avertissements`** : Voir les avertissements d'un membre
- **`/effacer_avertissements`** : Supprimer tous les avertissements d'un membre
- **`/mute`** : Muter temporairement un membre
- **`/demute`** : Retirer le mute d'un membre
- **`/expulser`** : Expulser un membre du serveur
- **`/bannir`** : Bannir un membre du serveur
- **`/mode_lent`** : Activer/désactiver le mode lent
- **`/nettoyer`** : Supprimer plusieurs messages

### 🎫 **Tickets (2 commandes)**
- **`/creer_ticket`** : Créer un canal privé de support
- **`/fermer_ticket`** : Fermer un ticket (avec bouton de fermeture)

### 🔧 **Utilitaires (4 commandes)**
- **`/rappel`** : Programmer un rappel
- **`/calculer`** : Calculatrice mathématique
- **`/traduire`** : Traduction de texte (avec API optionnelle)
- **`/meteo`** : Météo d'une ville (avec API optionnelle)

### 🎭 **Rôles (3 commandes)**
- **`/role_auto_ajouter`** : Ajouter un rôle automatique
- **`/role_auto_retirer`** : Retirer un rôle automatique
- **`/role_auto_liste`** : Lister les rôles automatiques

### 📊 **Statistiques (3 commandes)**
- **`/niveau`** : Voir son niveau et XP
- **`/classement`** : Classement des membres par niveau
- **`/statistiques`** : Statistiques du serveur

### 🎉 **Événements (4 commandes)**
- **`/definir_anniversaire`** : Définir sa date d'anniversaire
- **`/voir_anniversaire`** : Voir sa date d'anniversaire
- **`/concours`** : Créer un concours/giveaway
- **`/concours_relancer`** : Retirer un gagnant de concours

### 📝 **Contenu (5 commandes)**
- **`/suggestion`** : Faire une suggestion
- **`/creer_note`** : Créer une note partagée
- **`/voir_note`** : Voir une note
- **`/liste_note`** : Lister toutes les notes
- **`/supprimer_note`** : Supprimer une note

### 🎨 **Créatif (3 commandes)**
- **`/citation`** : Citation inspirante aléatoire
- **`/nom_aleatoire`** : Générer un nom aléatoire
- **`/couleur_aleatoire`** : Générer une couleur aléatoire

### ℹ️ **Informations (5 commandes)**
- **`/info_serveur`** : Informations du serveur
- **`/info_membre`** : Informations d'un membre
- **`/avatar`** : Afficher l'avatar d'un membre
- **`/ping`** : Latence du bot
- **`/youtube`** : Lien vers la chaîne YouTube

### 🎮 **Fun (5 commandes)**
- **`/de`** : Lancer un dé
- **`/pile_ou_face`** : Pile ou face avec animation
- **`/boule_magique`** : Poser une question
- **`/sondage`** : Créer un sondage
- **`/emoji_aleatoire`** : Emoji aléatoire par catégorie

### 🔄 **Fonctionnalités automatiques**
- **Système de niveaux** : Gain d'XP par message
- **Auto-modération** : Détection de mots interdits et majuscules
- **Réponses automatiques** : Réponses aux salutations
- **Bienvenue/départ** : Messages automatisés
- **Auto-rôles** : Attribution automatique de rôles
- **Logs** : Journal des messages supprimés
- **Tâches périodiques** : Rappels, anniversaires, concours

## 🏗️ Architecture du code

### **Structure modulaire (Cogs)**
Le bot utilise le système de Cogs (extensions) de discord.py pour organiser le code :

cogs/
├── 🛡️ moderation.py # Commandes de modération
├── 🎫 tickets.py # Système de tickets
├── 🔧 utilities.py # Utilitaires avec APIs
├── 🎭 roles.py # Gestion des rôles
├── 📊 stats.py # Statistiques et niveaux
├── 🎉 events_cog.py # Événements et concours
├── 📝 content.py # Suggestions et notes
├── 🎨 creative.py # Commandes créatives
├── ℹ️ info.py # Commandes d'information
├── 🎮 fun.py # Commandes fun
├── 🔄 events_handler.py # Gestionnaire d'événements
└── ⏰ tasks.py # Tâches périodiques


### **Système de stockage**
- **`data/storage.py`** : Classe Singleton pour gérer les données
- **`data/data.json`** : Fichier local de persistance, ignoré par Git car il contient des données de serveur et de membres
- **`.env`** : Configuration locale contenant le token Discord, ignorée par Git
- Stockage en mémoire avec sauvegarde automatique

### **Fonctions utilitaires**
- **`utils.py`** : Fonctions helper pour les embeds, permissions, dates, emojis
- Système d'emoji personnalisé avec mapping de noms
- Formateurs de date sécurisés pour les fuseaux horaires

## 📥 Installation

### **Prérequis**
- Python 3.8 ou supérieur
- Compte Discord Developer
- Token de bot Discord

### **Étapes d'installation (Windows / PowerShell)**

1. Cloner le dépôt et entrer dans son dossier :
   ```powershell
   git clone https://github.com/xNxggets/Guess_whos_back.git
   cd Guess_whos_back
   ```
2. Créer et activer un environnement Python, puis installer les dépendances :
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```
3. Créer le fichier local `.env` à partir du modèle et y renseigner le token Discord :
   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```
4. Dans le Discord Developer Portal, activer les intents **Presence**, **Server Members** et **Message Content**.
5. Démarrer le bot :
   ```powershell
   python main.py
   ```

Les sauvegardes restent dans `data/data.json` sur la machine qui exécute le bot. Elles ne sont pas envoyées à GitHub.
