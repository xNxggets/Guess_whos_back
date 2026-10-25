# Partie du bot gérant les commandes utilitaires telles que les rappels et la calculatrice.

import discord
import ast
import math
from discord import app_commands
from discord.ext import commands
import datetime
import random
from utils import create_embed
from data.storage import storage


def calculer_expression(expression: str):
    """Évalue une expression arithmétique simple sans exécuter de code Python."""
    if len(expression) > 100:
        raise ValueError("Expression trop longue.")

    arbre = ast.parse(expression, mode="eval")
    if sum(1 for _ in ast.walk(arbre)) > 40:
        raise ValueError("Expression trop complexe.")

    limite = 1_000_000_000_000

    def evaluer(noeud, profondeur=0):
        if profondeur > 20:
            raise ValueError("Expression trop complexe.")

        if isinstance(noeud, ast.Expression):
            resultat = evaluer(noeud.body, profondeur + 1)
        elif isinstance(noeud, ast.Constant) and type(noeud.value) in (int, float):
            resultat = noeud.value
        elif isinstance(noeud, ast.UnaryOp) and isinstance(
            noeud.op, (ast.UAdd, ast.USub)
        ):
            valeur = evaluer(noeud.operand, profondeur + 1)
            resultat = valeur if isinstance(noeud.op, ast.UAdd) else -valeur
        elif isinstance(noeud, ast.BinOp) and isinstance(
            noeud.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)
        ):
            gauche = evaluer(noeud.left, profondeur + 1)
            droite = evaluer(noeud.right, profondeur + 1)
            if isinstance(noeud.op, ast.Add):
                resultat = gauche + droite
            elif isinstance(noeud.op, ast.Sub):
                resultat = gauche - droite
            elif isinstance(noeud.op, ast.Mult):
                resultat = gauche * droite
            else:
                resultat = gauche / droite
        else:
            raise ValueError("Seuls +, -, * et / sont autorisés.")

        if not math.isfinite(resultat) or abs(resultat) > limite:
            raise ValueError("Le résultat dépasse la limite autorisée.")
        return resultat

    return evaluer(arbre)


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
            resultat = calculer_expression(expression)
            
            embed = discord.Embed(
                title="🔢 Calculatrice",
                color=discord.Color.blue()
            )
            embed.add_field(name="Expression", value=f"```{expression}```", inline=False)
            embed.add_field(name="Résultat", value=f"```{resultat}```", inline=False)
            
            await interaction.response.send_message(embed=embed)
        except (ArithmeticError, SyntaxError, TypeError, ValueError, OverflowError):
            await interaction.response.send_message(
                "❌ Expression invalide ou résultat hors limites. Utilise seulement "
                "les nombres et les opérations +, -, * et /.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Utilities(bot))
