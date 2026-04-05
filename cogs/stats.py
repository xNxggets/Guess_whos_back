# Partie du bot discord pour gérer les commandes de statistiques comme le niveau, le classement et les statistiques du serveur.

import discord
from discord import app_commands
from discord.ext import commands
from utils import create_embed, calculer_niveau
from data.storage import storage

class Stats(commands.Cog):
    """Commandes de statistiques"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="niveau", description="Voir votre niveau et XP")
    async def niveau(self, interaction: discord.Interaction):
        """Voir son niveau"""
        user_id = interaction.user.id
        
        # Initialiser si pas encore
        if user_id not in storage.niveaux:
            storage.niveaux[user_id] = {"niveau": 1, "xp": 0}
        
        niveau_data = storage.niveaux[user_id]
        niveau_actuel = niveau_data["niveau"]
        xp_actuel = niveau_data["xp"]
        xp_prochain = (niveau_actuel + 1) ** 2 * 100
        progression = (xp_actuel / xp_prochain) * 100
        
        barre = "█" * int(progression / 5) + "░" * (20 - int(progression / 5))
        
        embed = create_embed(
            title=f"📊 Niveau de {interaction.user.display_name}",
            color=discord.Color.purple(),
            thumbnail=interaction.user.avatar.url if interaction.user.avatar else None,
            fields=[
                ("🎯 Niveau actuel", str(niveau_actuel), True),
                ("⭐ XP", str(xp_actuel), True),
                ("📈 Progression", f"{progression:.1f}%", True),
                ("⏭️ XP pour niveau suivant", f"{xp_prochain - xp_actuel} XP", False),
                ("━━━━━━━━━━━━━━━━━━━━", f"`[{barre}]`", False)
            ]
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="classement", description="Voir le classement des membres")
    async def classement(self, interaction: discord.Interaction):
        """Voir le classement"""
        if not storage.niveaux:
            await interaction.response.send_message("📊 Aucune donnée de niveau disponible.", ephemeral=True)
            return
        
        # Trier les niveaux
        classement = sorted(storage.niveaux.items(), key=lambda x: x[1]["niveau"] * 1000 + x[1]["xp"], reverse=True)[:10]
        
        embed = create_embed(
            title="🏆 Classement des membres",
            color=discord.Color.gold()
        )
        
        for i, (user_id, data) in enumerate(classement, 1):
            membre = interaction.guild.get_member(user_id)
            nom = membre.display_name if membre else f"Utilisateur {user_id}"
            niveau = data["niveau"]
            xp = data["xp"]
            
            medaille = ""
            if i == 1: medaille = "🥇"
            elif i == 2: medaille = "🥈"
            elif i == 3: medaille = "🥉"
            else: medaille = f"{i}."
            
            embed.add_field(
                name=f"{medaille} {nom}",
                value=f"Niveau {niveau} • {xp} XP",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="statistiques", description="Voir les statistiques du serveur")
    async def statistiques(self, interaction: discord.Interaction):
        """Voir les statistiques"""
        guilde = interaction.guild
        
        # Calculer les stats
        total_messages = sum(storage.stats_messages.values())
        membres_actifs = len([m for m in guilde.members if not m.bot])
        bots = len([m for m in guilde.members if m.bot])
        
        embed = create_embed(
            title=f"📈 Statistiques de {guilde.name}",
            color=discord.Color.blue(),
            fields=[
                ("👥 Membres", f"Humains: {membres_actifs}\nBots: {bots}\nTotal: {guilde.member_count}", True),
                ("💬 Messages", f"Total: {total_messages}\nPar membre: {total_messages // max(1, membres_actifs)}", True),
                ("🎯 Niveaux", f"Membres enregistrés: {len(storage.niveaux)}", True),
                ("📅 Anniversaires", f"Enregistrés: {len(storage.anniversaires)}", True),
                ("⚠️ Avertissements", f"Total donnés: {sum(len(w) for w in storage.avertissements.values())}", True)
            ]
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Stats(bot))