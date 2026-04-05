# Partie du bot discord pour gérer les suggestions et les notes partagées

import discord
from discord import app_commands
from discord.ext import commands
import datetime
from data.storage import storage
from utils import verifier_permissions, create_embed  # IMPORT AJOUTÉ

class Content(commands.Cog):
    """Suggestions et notes"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="suggestion", description="Faire une suggestion")
    @app_commands.describe(suggestion="Votre suggestion")
    async def suggestion(self, interaction: discord.Interaction, suggestion: str):
        """Faire une suggestion"""
        # Vérifier si le canal suggestions existe
        canal_suggestions = discord.utils.get(interaction.guild.text_channels, name="suggestions")
        
        if not canal_suggestions:
            # Créer le canal s'il n'existe pas
            try:
                canal_suggestions = await interaction.guild.create_text_channel(
                    "suggestions",
                    topic="Suggestions des membres",
                    reason="Création automatique pour les suggestions"
                )
                await canal_suggestions.send(
                    f"📝 **Salon des suggestions créé !**\n"
                    f"Utilisez `/suggestion` dans n'importe quel salon pour faire une suggestion."
                )
            except discord.Forbidden:
                await interaction.response.send_message(
                    "❌ Je n'ai pas la permission de créer un salon `#suggestions`.\n"
                    "Veuillez créer ce salon manuellement ou me donner les permissions nécessaires.",
                    ephemeral=True
                )
                return
        
        # Créer l'embed de suggestion
        suggestion_id = len(storage.suggestions) + 1
        
        embed = discord.Embed(
            title=f"💡 Suggestion #{suggestion_id}",
            description=suggestion,
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None
        )
        embed.set_footer(text="Votez avec 👍 ou 👎")
        
        # Envoyer la suggestion
        msg = await canal_suggestions.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        
        # Sauvegarder la suggestion
        storage.suggestions.append({
            "id": suggestion_id,
            "auteur": interaction.user.name,
            "auteur_id": interaction.user.id,
            "suggestion": suggestion,
            "message_id": msg.id,
            "channel_id": canal_suggestions.id,
            "guild_id": interaction.guild.id,
            "date": datetime.datetime.now().isoformat(),
            "votes_pour": 0,
            "votes_contre": 0
        })
        storage.save_data()
        
        await interaction.response.send_message(
            f"✅ Suggestion envoyée dans {canal_suggestions.mention} !",
            ephemeral=True
        )
    
    @app_commands.command(name="creer_note", description="Créer une note partagée")
    @app_commands.describe(nom="Nom de la note", contenu="Contenu de la note")
    async def creer_note(self, interaction: discord.Interaction, nom: str, contenu: str):
        """Créer une note"""
        guild_id = interaction.guild.id
        
        if guild_id not in storage.notes_serveur:
            storage.notes_serveur[guild_id] = {}
        
        storage.notes_serveur[guild_id][nom] = {
            "contenu": contenu,
            "auteur": interaction.user.name,
            "auteur_id": interaction.user.id,
            "date": datetime.datetime.now().isoformat()
        }
        storage.save_data()
        
        await interaction.response.send_message(
            f"✅ Note **{nom}** créée !",
            ephemeral=True
        )
    
    @app_commands.command(name="voir_note", description="Voir une note partagée")
    @app_commands.describe(nom="Nom de la note")
    async def voir_note(self, interaction: discord.Interaction, nom: str):
        """Voir une note"""
        guild_id = interaction.guild.id
        
        if guild_id not in storage.notes_serveur or nom not in storage.notes_serveur[guild_id]:
            await interaction.response.send_message(
                "❌ Cette note n'existe pas",
                ephemeral=True
            )
            return
        
        note = storage.notes_serveur[guild_id][nom]
        
        embed = discord.Embed(
            title=f"📝 Note : {nom}",
            description=note["contenu"],
            color=discord.Color.green(),
            timestamp=datetime.datetime.fromisoformat(note["date"])
        )
        embed.set_footer(text=f"Créée par {note['auteur']}")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="liste_note", description="Voir toutes les notes")
    async def liste_note(self, interaction: discord.Interaction):
        """Lister toutes les notes"""
        guild_id = interaction.guild.id
        
        if guild_id not in storage.notes_serveur or not storage.notes_serveur[guild_id]:
            await interaction.response.send_message(
                "ℹ️ Aucune note n'existe sur ce serveur",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title="📚 Liste des notes",
            description=f"Total: {len(storage.notes_serveur[guild_id])} note(s)",
            color=discord.Color.blue()
        )
        
        for nom, note in storage.notes_serveur[guild_id].items():
            preview = note["contenu"][:100] + "..." if len(note["contenu"]) > 100 else note["contenu"]
            date = datetime.datetime.fromisoformat(note["date"]).strftime("%d/%m/%Y")
            embed.add_field(
                name=f"📄 {nom}",
                value=f"{preview}\n*Par {note['auteur']} le {date}*",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="supprimer_note", description="Supprimer une note")
    @app_commands.describe(nom="Nom de la note à supprimer")
    async def supprimer_note(self, interaction: discord.Interaction, nom: str):
        """Supprimer une note"""
        if not await verifier_permissions(interaction, "manage_messages"):
            return
        
        guild_id = interaction.guild.id
        
        if guild_id in storage.notes_serveur and nom in storage.notes_serveur[guild_id]:
            # Vérifier si l'utilisateur est l'auteur ou a les permissions
            note = storage.notes_serveur[guild_id][nom]
            if note["auteur_id"] != interaction.user.id and not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message(
                    "❌ Vous n'êtes pas l'auteur de cette note et n'avez pas les permissions administrateur",
                    ephemeral=True
                )
                return
            
            del storage.notes_serveur[guild_id][nom]
            storage.save_data()
            await interaction.response.send_message(f"✅ Note **{nom}** supprimée !")
        else:
            await interaction.response.send_message(
                "❌ Cette note n'existe pas",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Content(bot))