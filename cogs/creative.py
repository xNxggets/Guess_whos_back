# Partie du bot Discord - Cogs créatifs pour les commandes citation, nom aléatoire et couleur aléatoire.

import discord
from discord import app_commands
from discord.ext import commands
import random
from utils import create_embed, get_emoji, get_random_emoji, format_with_emojis

class Creative(commands.Cog):
    """Commandes créatives"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="citation", description="Obtenir une citation inspirante")
    async def citation(self, interaction: discord.Interaction):
        """Obtenir une citation aléatoire"""
        citations = [
            {"texte": "Ne te compare pas personnellement aux autres, ils seront toujours meilleurs que toi.", "auteur": "Emmanuel Macaron", "emoji" : "🤡"},
            {"texte": "La vie est comme une bicyclette, il faut avancer pour ne pas perdre l'équilibre.", "auteur": "Albert Einstein", "emoji": "🚲"},
            {"texte": "Le succès c'est d'aller d'échec en échec sans perdre son enthousiasme.", "auteur": "Winston Churchill", "emoji": "💪"},
            {"texte": "Soyez le changement que vous voulez voir dans le monde.", "auteur": "Gandhi", "emoji": "🌍"},
            {"texte": "La seule façon de faire du bon travail est d'aimer ce que vous faites.", "auteur": "Steve Jobs", "emoji": "❤️"},
            {"texte": "L'imagination est plus importante que le savoir.", "auteur": "Albert Einstein", "emoji": "🧠"},
            {"texte": "Ne rêvez pas votre vie, vivez vos rêves.", "auteur": "Anonyme", "emoji": "💭"},
            {"texte": "Le plus grand risque est de ne prendre aucun risque.", "auteur": "Mark Zuckerberg", "emoji": "🎲"},
            {"texte": "Croyez que vous pouvez et vous serez à mi-chemin.", "auteur": "Theodore Roosevelt", "emoji": "🌟"},
            {"texte": "La meilleure façon de prédire l'avenir est de le créer.", "auteur": "Peter Drucker", "emoji": "🔮"},
            {"texte": "Le seul endroit où le succès vient avant le travail, c'est dans le dictionnaire.", "auteur": "Vidal Sassoon", "emoji": "📚"},
            {"texte": "La patience est la clé de la réussite.", "auteur": "Bill Gates", "emoji": "⏳"},
            {"texte": "N'abandonne jamais, car tu ne sais jamais à quel point tu es proche du but.", "auteur": "Thomas Edison", "emoji": "🎯"},
            {"texte": "La créativité, c'est l'intelligence qui s'amuse.", "auteur": "Albert Einstein", "emoji": "🎨"},
            {"texte": "Les opportunités ne se présentent pas, elles se créent.", "auteur": "Chris Grosser", "emoji": "✨"},
            {"texte": "Le seul moyen de faire du excellent travail est d'aimer ce que vous faites.", "auteur": "Steve Jobs", "emoji": "🔥"},
            {"texte": "Les rêves ne se réalisent pas magiquement, il faut de la détermination.", "auteur": "Oprah Winfrey", "emoji": "💫"},
            {"texte": "L'échec n'est que l'opportunité de recommencer de manière plus intelligente.", "auteur": "Henry Ford", "emoji": "🔄"},
            {"texte": "Le courage n'est pas l'absence de peur, mais la capacité de la vaincre.", "auteur": "Nelson Mandela", "emoji": "🦁"},
            {"texte": "La simplicité est la sophistication suprême.", "auteur": "Leonardo da Vinci", "emoji": "🎨"},
            {"texte": "La seule limite à notre réalisation de demain sera nos doutes d'aujourd'hui.", "auteur": "Franklin D. Roosevelt", "emoji": "🚀"},
        ]
        
        citation_choisie = random.choice(citations)
        
        # Couleur aléatoire basée sur l'emoji
        color = discord.Color.random()
        
        embed = create_embed(
            title=f"{citation_choisie['emoji']} Citation du jour",
            description=format_with_emojis(f"*{citation_choisie['texte']}*"),
            color=color,
            footer=f"— {citation_choisie['auteur']} {get_random_emoji('positive')}",
            thumbnail="https://cdn-icons-png.flaticon.com/512/3281/3281306.png"
        )
        
        # Ajouter une réaction au message
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        await message.add_reaction(citation_choisie['emoji'])
        await message.add_reaction("💭")  # Pensée
        await message.add_reaction("✨")  # Inspiration
    
    @app_commands.command(name="nom_aleatoire", description="Générer un nom aléatoire")
    @app_commands.describe(type_nom="Type de nom")
    @app_commands.choices(type_nom=[
        app_commands.Choice(name="🧙 Fantaisie", value="fantaisie"),
        app_commands.Choice(name="🚀 Science-fiction", value="science-fiction"),
        app_commands.Choice(name="🏙️ Moderne", value="moderne"),
        app_commands.Choice(name="🏛️ Historique", value="historique"),
        app_commands.Choice(name="🏺 Mythologique", value="mythologique"),
        app_commands.Choice(name="🐉 Médiéval", value="medieval"),
        app_commands.Choice(name="🌌 Futuriste", value="futuriste"),
        app_commands.Choice(name="🌊 Marin", value="marin"),
        app_commands.Choice(name="🌲 Nature", value="nature"),
        app_commands.Choice(name="⚔️ Guerrier", value="guerrier"),
    ])
    async def nom_aleatoire(self, interaction: discord.Interaction, type_nom: str = "fantaisie"):
        """Générer un nom aléatoire"""
        noms = {
            "fantaisie": [
                {"nom": "Aldric", "signification": "Noble souverain", "emoji": "👑"},
                {"nom": "Elara", "signification": "Étoile brillante", "emoji": "🌟"},
                {"nom": "Thorin", "signification": "Audacieux", "emoji": "⚔️"},
                {"nom": "Lyanna", "signification": "Lune gracieuse", "emoji": "🌙"},
                {"nom": "Gareth", "signification": "Douceur", "emoji": "🕊️"},
                {"nom": "Freya", "signification": "Déesse de l'amour", "emoji": "❤️"},
                {"nom": "Dorian", "signification": "Cadeau", "emoji": "🎁"},
                {"nom": "Selene", "signification": "Déesse de la lune", "emoji": "🌕"},
                {"nom": "Kaelen", "signification": "Guerrier puissant", "emoji": "🛡️"},
                {"nom": "Isolde", "signification": "Belle princesse", "emoji": "👸"},
            ],
            "science-fiction": [
                {"nom": "Zyx", "signification": "Inconnu", "emoji": "👽"},
                {"nom": "Nova", "signification": "Nouvelle étoile", "emoji": "✨"},
                {"nom": "Kael", "signification": "Étranger", "emoji": "🚀"},
                {"nom": "Aria", "signification": "Mélodie cosmique", "emoji": "🎵"},
                {"nom": "Rex", "signification": "Roi des étoiles", "emoji": "👑"},
                {"nom": "Luna", "signification": "Satellite", "emoji": "🌙"},
                {"nom": "Orion", "signification": "Constellation", "emoji": "🌌"},
                {"nom": "Vega", "signification": "Étoile brillante", "emoji": "⭐"},
                {"nom": "Nexus", "signification": "Point de connexion", "emoji": "🔗"},
                {"nom": "Cyra", "signification": "Cybernétique", "emoji": "🤖"},
            ],
            "moderne": [
                {"nom": "Alex", "signification": "Défenseur", "emoji": "🛡️"},
                {"nom": "Emma", "signification": "Universelle", "emoji": "🌍"},
                {"nom": "Lucas", "signification": "Lumière", "emoji": "💡"},
                {"nom": "Sophie", "signification": "Sagesse", "emoji": "📚"},
                {"nom": "Nathan", "signification": "Don de Dieu", "emoji": "🙏"},
                {"nom": "Léa", "signification": "Fatiguée", "emoji": "😴"},
                {"nom": "Hugo", "signification": "Esprit", "emoji": "🧠"},
                {"nom": "Chloé", "signification": "Jeune pousse", "emoji": "🌱"},
                {"nom": "Louis", "signification": "Guerrier célèbre", "emoji": "⚔️"},
                {"nom": "Camille", "signification": "Jeune cérémonieuse", "emoji": "🎭"},
            ],
            "historique": [
                {"nom": "Arthur", "signification": "Ours noble", "emoji": "🐻"},
                {"nom": "Éléonore", "signification": "Lumière", "emoji": "🕯️"},
                {"nom": "Guillaume", "signification": "Protection volontaire", "emoji": "🛡️"},
                {"nom": "Marguerite", "signification": "Perle", "emoji": "💎"},
                {"nom": "Richard", "signification": "Roi puissant", "emoji": "👑"},
                {"nom": "Blanche", "signification": "Blancheur", "emoji": "❄️"},
                {"nom": "Henri", "signification": "Maître de maison", "emoji": "🏰"},
                {"nom": "Catherine", "signification": "Pure", "emoji": "✨"},
                {"nom": "Philippe", "signification": "Amoureux des chevaux", "emoji": "🐎"},
                {"nom": "Anne", "signification": "Grâce", "emoji": "🎀"},
            ],
            "mythologique": [
                {"nom": "Apollon", "signification": "Dieu du soleil", "emoji": "☀️"},
                {"nom": "Athéna", "signification": "Déesse de la sagesse", "emoji": "🦉"},
                {"nom": "Zeus", "signification": "Roi des dieux", "emoji": "⚡"},
                {"nom": "Héra", "signification": "Reine des dieux", "emoji": "👑"},
                {"nom": "Odin", "signification": "Père de tout", "emoji": "🐦‍⬛"},
                {"nom": "Freyja", "signification": "Dame", "emoji": "💖"},
                {"nom": "Thor", "signification": "Tonnerre", "emoji": "🔨"},
                {"nom": "Sif", "signification": "Mariée", "emoji": "💍"},
                {"nom": "Loki", "signification": "Trompeur", "emoji": "🦊"},
                {"nom": "Hel", "signification": "Monde souterrain", "emoji": "💀"},
            ],
        }
        
        if type_nom not in noms:
            type_nom = "fantaisie"
        
        nom_genere = random.choice(noms[type_nom])
        
        type_emojis = {
            "fantaisie": "🧙",
            "science-fiction": "🚀",
            "moderne": "🏙️",
            "historique": "🏛️",
            "mythologique": "🏺",
            "medieval": "🐉",
            "futuriste": "🌌",
            "marin": "🌊",
            "nature": "🌲",
            "guerrier": "⚔️",
        }
        
        embed = create_embed(
            title=f"{type_emojis.get(type_nom, '🎭')} Nom aléatoire généré",
            description=f"**{nom_genere['emoji']} {nom_genere['nom']}**",
            color=discord.Color.teal(),
            fields=[
                ("📂 Type", type_nom.capitalize(), True),
                ("📖 Signification", nom_genere['signification'], True),
                ("🌟 Caractéristique", nom_genere['emoji'], True)
            ],
            footer=f"Un nom unique pour vos créations ! {get_random_emoji('creative')}"
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="couleur_aleatoire", description="Générer une couleur aléatoire")
    async def couleur_aleatoire(self, interaction: discord.Interaction):
        """Générer une couleur aléatoire"""
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        
        # Nom de la couleur basé sur les valeurs RGB
        color_names = {
            (255, 0, 0): "Rouge vif 🔴",
            (0, 255, 0): "Vert vif 🟢",
            (0, 0, 255): "Bleu vif 🔵",
            (255, 255, 0): "Jaune vif 🟡",
            (255, 0, 255): "Magenta 💜",
            (0, 255, 255): "Cyan 💠",
            (255, 255, 255): "Blanc ⚪",
            (0, 0, 0): "Noir ⚫",
            (255, 165, 0): "Orange 🟠",
            (128, 0, 128): "Violet 🟣",
        }
        
        color_name = "Couleur personnalisée 🎨"
        for rgb, name in color_names.items():
            if abs(r - rgb[0]) < 30 and abs(g - rgb[1]) < 30 and abs(b - rgb[2]) < 30:
                color_name = name
                break
        
        # Créer une image de couleur (URL vers un service d'image)
        color_image_url = f"https://singlecolorimage.com/get/{hex_color[1:]}/150x150"
        
        # Émoji basé sur la luminosité
        brightness = (r + g + b) / 3
        if brightness < 50:
            brightness_emoji = "🌙"  # Sombre
        elif brightness < 150:
            brightness_emoji = "🌓"  # Moyen
        else:
            brightness_emoji = "☀️"  # Clair
        
        embed = create_embed(
            title=f"{brightness_emoji} Couleur aléatoire",
            description=f"**{color_name}**",
            color=discord.Color.from_rgb(r, g, b),
            thumbnail=color_image_url,
            fields=[
                ("🎨 Nom", color_name, True),
                ("🟥 Hexadécimal", f"`{hex_color}`", True),
                ("🟩 RGB", f"`({r}, {g}, {b})`", True),
                ("🟦 Décimal", f"`{r*65536 + g*256 + b}`", True),
                ("💡 Luminosité", f"`{brightness:.1f}/255`", True),
            ],
            footer=f"Cliquez pour copier le code couleur ! {get_emoji('clipboard')}"
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Creative(bot))