# Partie du bot gérant les commandes utilitaires telles que les rappels et la calculatrice.

import discord
from discord import app_commands
from discord.ext import commands
import datetime
import random
from utils import create_embed
from data.storage import storage

class Utilities(commands.Cog):
    """Commandes utilitaires"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="rappel", description="Créer un rappel")
    @app_commands.describe(
        duree="Durée en minutes",
        message="Le message du rappel"
    )
    async def rappel(self, interaction: discord.Interaction, duree: app_commands.Range[int, 1, 10080], message: str):
        """Créer un rappel"""
        temps_rappel = datetime.datetime.now() + datetime.timedelta(minutes=duree)
        
        storage.rappels.append({
            "user_id": interaction.user.id,
            "channel_id": interaction.channel.id,
            "message": message,
            "time": temps_rappel
        })
        storage.save_data()
        
        await interaction.response.send_message(
            f"⏰ Rappel créé ! Je vous rappellerai dans {duree} minute(s)",
            ephemeral=True
        )
    
    @app_commands.command(name="calculer", description="Effectuer un calcul mathématique")
    @app_commands.describe(expression="L'expression à calculer (ex: 2+2, 5*10)")
    async def calculer(self, interaction: discord.Interaction, expression: str):
        """Effectuer un calcul"""
        try:
            # Sécurité : n'autoriser que les opérations mathématiques de base
            caracteres_autorises = "0123456789+-*/()., "
            if not all(c in caracteres_autorises for c in expression):
                await interaction.response.send_message(
                    "❌ Expression invalide ! Utilisez seulement des chiffres et + - * / ( ) .",
                    ephemeral=True
                )
                return
            
            # Éviter les calculs dangereux
            if len(expression) > 100:
                await interaction.response.send_message(
                    "❌ Expression trop longue !",
                    ephemeral=True
                )
                return
            
            resultat = eval(expression)
            
            embed = discord.Embed(
                title="🔢 Calculatrice",
                color=discord.Color.blue()
            )
            embed.add_field(name="Expression", value=f"```{expression}```", inline=False)
            embed.add_field(name="Résultat", value=f"```{resultat}```", inline=False)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Erreur de calcul : {str(e)}",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Utilities(bot))