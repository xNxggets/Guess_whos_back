# Partie du bot gérant le stockage et la persistance des données utilisateur et serveur.

import json
from pathlib import Path

class Storage:
    def __init__(self):
        self.data_file = Path(__file__).with_name("data.json")
        self.anniversaires = {}
        self.niveaux = {}
        self.avertissements = {}
        self.auto_roles = {}
        self.notes_serveur = {}
        self.suggestions = []
        self.giveaways = {}
        self.rappels = []
        self.tickets_actifs = {}
        self.stats_messages = {}
        
        # Liste étendue de mots interdits par défaut
        self.mots_interdits = [
            "insulte1", "insulte2", "raciste", "haine", "violence",
            "spam", "arnaque", "phishing", "malware", "virus",
            "nude", "porno", "xxx", "nsfw", "explicit"
        ]
        
        self.messages_programmes = []
        
        self.load_data()
    
    def load_data(self):
        """Charge les données depuis le fichier JSON"""
        try:
            if self.data_file.exists():
                with self.data_file.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    # Charger chaque dictionnaire
                    self.anniversaires = data.get("anniversaires", {})
                    self.niveaux = data.get("niveaux", {})
                    self.avertissements = data.get("avertissements", {})
                    self.auto_roles = data.get("auto_roles", {})
                    self.notes_serveur = data.get("notes_serveur", {})
                    self.suggestions = data.get("suggestions", [])
                    self.giveaways = data.get("giveaways", {})
                    self.rappels = data.get("rappels", [])
                    self.tickets_actifs = data.get("tickets_actifs", {})
                    self.stats_messages = data.get("stats_messages", {})
                    self.mots_interdits = data.get("mots_interdits", self.mots_interdits)  # Garder par défaut si pas dans le fichier
                    self.messages_programmes = data.get("messages_programmes", [])
                    
                    # Convertir les IDs en int (JSON les stocke comme strings)
                    self.anniversaires = {int(k): v for k, v in self.anniversaires.items()}
                    self.niveaux = {int(k): v for k, v in self.niveaux.items()}
                    self.avertissements = {int(k): v for k, v in self.avertissements.items()}
                    self.auto_roles = {int(k): v for k, v in self.auto_roles.items()}
                    self.notes_serveur = {int(k): v for k, v in self.notes_serveur.items()}
                    self.giveaways = {int(k): v for k, v in self.giveaways.items()}
                    self.tickets_actifs = {int(k): v for k, v in self.tickets_actifs.items()}
                    self.stats_messages = {int(k): v for k, v in self.stats_messages.items()}
                    
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
    
    def save_data(self):
        """Sauvegarde les données dans un fichier JSON"""
        try:
            # Convertir pour JSON
            data = {
                "anniversaires": {str(k): v for k, v in self.anniversaires.items()},
                "niveaux": {str(k): v for k, v in self.niveaux.items()},
                "avertissements": {str(k): v for k, v in self.avertissements.items()},
                "auto_roles": {str(k): v for k, v in self.auto_roles.items()},
                "notes_serveur": {str(k): v for k, v in self.notes_serveur.items()},
                "suggestions": self.suggestions,
                "giveaways": {str(k): v for k, v in self.giveaways.items()},
                "rappels": self.rappels,
                "tickets_actifs": {str(k): v for k, v in self.tickets_actifs.items()},
                "stats_messages": {str(k): v for k, v in self.stats_messages.items()},
                "mots_interdits": self.mots_interdits,
                "messages_programmes": self.messages_programmes
            }
            
            with self.data_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, default=str)
                
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des données: {e}")

# Instance globale
storage = Storage()
