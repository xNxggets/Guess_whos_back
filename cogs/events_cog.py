# Partie du bot discord pour gérer les commandes anniversaires et concours.

import discord
from discord import app_commands
from discord.ext import commands
import datetime
import random
from utils import verifier_permissions, create_embed
from data.storage import storage

class EventsCog(commands.Cog):
    """Événements et concours"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="definir_anniversaire", description="Définir votre date d'anniversaire")
    @app_commands.describe(jour="Jour (1-31)", mois="Mois (1-12)")
    async def definir_anniversaire(self, interaction: discord.Interaction, jour: app_commands.Range[int, 1, 31], mois: app_commands.Range[int, 1, 12]):
        """Définir son anniversaire"""
        # Validation de la date
        try:
            datetime.datetime(2024, mois, jour)  # Vérifie si la date est valide
        except ValueError:
            await interaction.response.send_message(
                "❌ Date invalide ! Vérifiez le jour et le mois.",
                ephemeral=True
            )
            return
        
        date = f"{jour:02d}/{mois:02d}"
        storage.anniversaires[interaction.user.id] = date
        storage.save_data()
        
        await interaction.response.send_message(
            f"✅ Votre anniversaire a été enregistré : **{jour}/{mois}** 🎂\n"
            f"Vous serez félicité sur ce serveur à cette date !",
            ephemeral=True
        )
    
    @app_commands.command(name="voir_anniversaire", description="Voir votre date d'anniversaire")
    async def voir_anniversaire(self, interaction: discord.Interaction):
        """Voir sa date d'anniversaire"""
        date_anniv = storage.anniversaires.get(interaction.user.id)
        
        if date_anniv:
            jour, mois = date_anniv.split("/")
            await interaction.response.send_message(
                f"🎂 Votre anniversaire est le **{jour}/{mois}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Vous n'avez pas encore défini votre anniversaire.\n"
                "Utilisez `/definir_anniversaire` pour le définir.",
                ephemeral=True
            )
    
    @app_commands.command(name="concours", description="Créer un concours")
    @app_commands.describe(
        duree="Durée en minutes",
        gagnants_nombre="Nombre de gagnants",
        prix="Le prix à gagner"
    )
    async def concours(self, interaction: discord.Interaction, duree: app_commands.Range[int, 1, 10080], gagnants_nombre: app_commands.Range[int, 1, 50], prix: str):
        """Créer un concours"""
        if not await verifier_permissions(interaction, "manage_guild"):
            return
        
        fin = datetime.datetime.now() + datetime.timedelta(minutes=duree)
        timestamp = int(fin.timestamp())
        
        embed = discord.Embed(
            title="🎉 CONCOURS !",
            description=(
                f"**Prix:** {prix}\n\n"
                f"Réagissez avec 🎉 pour participer !\n"
                f"**Nombre de gagnants:** {gagnants_nombre}\n"
                f"**Se termine:** <t:{timestamp}:R> (<t:{timestamp}:f>)"
            ),
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Organisé par {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        await message.add_reaction("🎉")
        
        # Sauvegarder le concours
        storage.giveaways[message.id] = {
            "prix": prix,
            "fin": fin,
            "gagnants": gagnants_nombre,
            "participants": [],
            "channel_id": interaction.channel.id,
            "message_id": message.id
        }
        storage.save_data()
    
    @app_commands.command(name="concours_relancer", description="Retirer un gagnant")
    @app_commands.describe(message_id="ID du message du concours")
    async def concours_relancer(self, interaction: discord.Interaction, message_id: str):
        """Retirer un concours"""
        if not await verifier_permissions(interaction, "manage_guild"):
            return
        
        try:
            msg_id = int(message_id)
        except ValueError:
            await interaction.response.send_message(
                "❌ ID de message invalide",
                ephemeral=True
            )
            return
        
        if msg_id not in storage.giveaways:
            await interaction.response.send_message(
                "❌ Concours non trouvé ou déjà terminé",
                ephemeral=True
            )
            return
        
        concours = storage.giveaways[msg_id]
        
        if not concours["participants"]:
            await interaction.response.send_message(
                "❌ Aucun participant à ce concours",
                ephemeral=True
            )
            return
        
        # Sélectionner un nouveau gagnant
        gagnant_id = random.choice(concours["participants"])
        gagnant = self.bot.get_user(gagnant_id) or f"<@{gagnant_id}>"
        
        embed = discord.Embed(
            title="🎉 NOUVEAU GAGNANT !",
            description=(
                f"Le concours pour **{concours['prix']}** a un nouveau gagnant !\n\n"
                f"🎊 Félicitations à {gagnant} ! 🎊"
            ),
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(EventsCog(bot))