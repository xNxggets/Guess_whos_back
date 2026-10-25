# Partie du bot discord pour gérer les commandes de modération comme avertir, mute, ban, expulser, nettoyer, mode lent, etc.

import discord
from discord import app_commands
from discord.ext import commands
import datetime
from utils import verifier_permissions, create_embed
from data.storage import storage

class Moderation(commands.Cog):
    """Commandes de modération"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="avertir", description="Avertir un membre")
    @app_commands.describe(membre="Le membre à avertir", raison="La raison de l'avertissement")
    async def avertir(self, interaction: discord.Interaction, membre: discord.Member, raison: str):
        """Avertir un membre"""
        if not await verifier_permissions(interaction, "moderate_members"):
            return
        
        avertissement = {
            "raison": raison,
            "date": datetime.datetime.now().isoformat(),
            "moderateur": interaction.user.name
        }
        
        if membre.id not in storage.avertissements:
            storage.avertissements[membre.id] = []
        storage.avertissements[membre.id].append(avertissement)
        storage.save_data()
        
        nombre_warns = len(storage.avertissements[membre.id])
        
        embed = create_embed(
            title="⚠️ Avertissement",
            description=f"{membre.mention} a reçu un avertissement",
            color=discord.Color.orange(),
            fields=[
                ("Raison", raison, False),
                ("Modérateur", interaction.user.mention, True),
                ("Total d'avertissements", str(nombre_warns), True)
            ]
        )
        
        await interaction.response.send_message(embed=embed)
        
        # Envoyer un MP au membre
        try:
            await membre.send(f"⚠️ Vous avez reçu un avertissement sur **{interaction.guild.name}**\nRaison : {raison}")
        except:
            pass
        
        # Actions automatiques
        if nombre_warns >= 5:
            await membre.ban(reason=f"5 avertissements ou plus")
            await interaction.followup.send(f"🔨 {membre.mention} a été banni automatiquement (5 warns)")
        elif nombre_warns >= 3:
            await membre.timeout(datetime.timedelta(hours=24), reason=f"3 avertissements ou plus")
            await interaction.followup.send(f"🔇 {membre.mention} a été mute 24h (3 warns)")
    
    @app_commands.command(name="avertissements", description="Voir les avertissements d'un membre")
    @app_commands.describe(membre="Le membre dont voir les avertissements")
    async def avertissements(self, interaction: discord.Interaction, membre: discord.Member):
        """Voir les avertissements d'un membre"""
        if not await verifier_permissions(interaction, "moderate_members"):
            return

        warns_membre = storage.avertissements.get(membre.id, [])
        
        if not warns_membre:
            await interaction.response.send_message(
                f"✅ {membre.mention} n'a aucun avertissement",
                ephemeral=True
            )
            return
        
        embed = create_embed(
            title=f"⚠️ Avertissements de {membre.display_name}",
            color=discord.Color.orange()
        )
        
        for i, warn in enumerate(warns_membre, 1):
            embed.add_field(
                name=f"Avertissement #{i}",
                value=f"**Raison:** {warn['raison']}\n**Date:** {warn['date']}\n**Par:** {warn['moderateur']}",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="effacer_avertissements", description="Effacer les avertissements d'un membre")
    @app_commands.describe(membre="Le membre dont effacer les avertissements")
    async def effacer_avertissements(self, interaction: discord.Interaction, membre: discord.Member):
        """Effacer les avertissements d'un membre"""
        if not await verifier_permissions(interaction, "administrator"):
            return
        
        if membre.id in storage.avertissements:
            nombre = len(storage.avertissements[membre.id])
            del storage.avertissements[membre.id]
            storage.save_data()
            await interaction.response.send_message(
                f"✅ {nombre} avertissement(s) effacé(s) pour {membre.mention}"
            )
        else:
            await interaction.response.send_message(
                f"{membre.mention} n'a aucun avertissement",
                ephemeral=True
            )
    
    @app_commands.command(name="mute", description="Rendre muet un membre temporairement")
    @app_commands.describe(
        membre="Le membre à mute",
        duree="Durée en minutes",
        raison="La raison du mute"
    )
    async def mute(self, interaction: discord.Interaction, membre: discord.Member, duree: app_commands.Range[int, 1, 10080], raison: str = "Aucune raison"):
        """Mute temporairement un membre"""
        if not await verifier_permissions(interaction, "moderate_members"):
            return
        
        await membre.timeout(datetime.timedelta(minutes=duree), reason=raison)
        
        embed = create_embed(
            title="🔇 Membre mute",
            description=f"{membre.mention} a été rendu muet",
            color=discord.Color.red(),
            fields=[
                ("Durée", f"{duree} minute(s)", True),
                ("Raison", raison, True),
                ("Modérateur", interaction.user.mention, True)
            ]
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="demute", description="Rendre la parole à un membre")
    @app_commands.describe(membre="Le membre à demute")
    async def demute(self, interaction: discord.Interaction, membre: discord.Member):
        """Demute un membre"""
        if not await verifier_permissions(interaction, "moderate_members"):
            return
        
        await membre.timeout(None)
        await interaction.response.send_message(f"✅ {membre.mention} peut de nouveau parler !")
    
    @app_commands.command(name="expulser", description="Expulser un membre du serveur")
    @app_commands.describe(membre="Le membre à expulser", raison="La raison de l'expulsion")
    async def expulser(self, interaction: discord.Interaction, membre: discord.Member, raison: str = "Aucune raison"):
        """Expulser un membre"""
        if not await verifier_permissions(interaction, "kick_members"):
            return
        
        await membre.kick(reason=raison)
        
        embed = create_embed(
            title="👢 Membre expulsé",
            description=f"{membre.name} a été expulsé du serveur",
            color=discord.Color.red(),
            fields=[
                ("Raison", raison, False),
                ("Modérateur", interaction.user.mention, True)
            ]
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="bannir", description="Bannir un membre du serveur")
    @app_commands.describe(membre="Le membre à bannir", raison="La raison du bannissement")
    async def bannir(self, interaction: discord.Interaction, membre: discord.Member, raison: str = "Aucune raison"):
        """Bannir un membre"""
        if not await verifier_permissions(interaction, "ban_members"):
            return
        
        await membre.ban(reason=raison)
        
        embed = create_embed(
            title="🔨 Membre banni",
            description=f"{membre.name} a été banni du serveur",
            color=discord.Color.dark_red(),
            fields=[
                ("Raison", raison, False),
                ("Modérateur", interaction.user.mention, True)
            ]
        )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="renommer", description="Changer le surnom d'un membre")
    @app_commands.describe(
        membre="Le membre dont tu veux changer le surnom",
        surnom="Le nouveau surnom (32 caractères maximum)",
    )
    @app_commands.guild_only()
    async def renommer(
        self,
        interaction: discord.Interaction,
        membre: discord.Member,
        surnom: str,
    ):
        """Changer le surnom d'un membre du serveur."""
        if not await verifier_permissions(interaction, "manage_nicknames"):
            return

        surnom = surnom.strip()
        if not surnom:
            await interaction.response.send_message(
                "❌ Le surnom ne peut pas être vide.", ephemeral=True
            )
            return
        if len(surnom) > 32:
            await interaction.response.send_message(
                "❌ Le surnom ne peut pas dépasser 32 caractères.", ephemeral=True
            )
            return

        bot_member = interaction.guild.me
        if bot_member is None or not bot_member.guild_permissions.manage_nicknames:
            await interaction.response.send_message(
                "❌ Le bot doit avoir la permission **Gérer les surnoms**.",
                ephemeral=True,
            )
            return

        try:
            await membre.edit(
                nick=surnom,
                reason=f"Surnom modifié par {interaction.user} via le bot",
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Discord a refusé le changement. Vérifie que le rôle du bot est "
                "au-dessus de celui du membre et que le bot peut gérer les surnoms.",
                ephemeral=True,
            )
            return
        except discord.HTTPException:
            await interaction.response.send_message(
                "❌ Discord n’a pas pu modifier ce surnom. Réessaie avec un autre nom.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"✅ Le surnom de {membre.mention} a été changé en **{surnom}**.",
            ephemeral=True,
        )
    
    @app_commands.command(name="mode_lent", description="Activer le mode lent dans un salon")
    @app_commands.describe(secondes="Nombre de secondes entre chaque message (0 pour désactiver)")
    async def mode_lent(self, interaction: discord.Interaction, secondes: app_commands.Range[int, 0, 21600]):
        """Activer le mode lent"""
        if not await verifier_permissions(interaction, "manage_channels"):
            return
        
        await interaction.channel.edit(slowmode_delay=secondes)
        
        if secondes == 0:
            await interaction.response.send_message("✅ Mode lent désactivé !")
        else:
            await interaction.response.send_message(
                f"✅ Mode lent activé : {secondes} seconde(s) entre chaque message"
            )
    
    @app_commands.command(name="nettoyer", description="Supprimer plusieurs messages")
    @app_commands.describe(nombre="Nombre de messages à supprimer (max 100)")
    @app_commands.default_permissions(manage_messages=True)
    async def nettoyer(self, interaction: discord.Interaction, 
                    nombre: app_commands.Range[int, 1, 100]):
        """Supprimer plusieurs messages"""
        if not await verifier_permissions(interaction, "manage_messages"):
            return
        
        await interaction.response.defer(ephemeral=True)
        
        messages_supprimes = await interaction.channel.purge(limit=nombre)
        
        await interaction.followup.send(
            f"✅ {len(messages_supprimes)} message(s) supprimé(s) !",
            ephemeral=True
        )
    
    # ===== COMMANDES POUR LES MOTS INTERDITS =====
    
    @app_commands.command(name="ajouter_mot_interdit", description="Ajouter un mot à la liste des mots interdits")
    @app_commands.describe(mot="Le mot à interdire")
    async def ajouter_mot_interdit(self, interaction: discord.Interaction, mot: str):
        """Ajouter un mot interdit"""
        if not await verifier_permissions(interaction, "manage_guild"):
            return
        
        mot_lower = mot.lower().strip()
        if not mot_lower:
            await interaction.response.send_message(
                "❌ Veuillez spécifier un mot valide.",
                ephemeral=True
            )
            return
        
        if mot_lower not in storage.mots_interdits:
            storage.mots_interdits.append(mot_lower)
            storage.save_data()
            
            embed = create_embed(
                title="✅ Mot interdit ajouté",
                description=f"Le mot a été ajouté à la liste des mots interdits.",
                color=discord.Color.green(),
                fields=[("Mot ajouté", f"`{mot_lower}`", False)]
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(
                f"❌ Le mot `{mot_lower}` est déjà dans la liste des mots interdits.",
                ephemeral=True
            )
    
    @app_commands.command(name="retirer_mot_interdit", description="Retirer un mot de la liste des mots interdits")
    @app_commands.describe(mot="Le mot à retirer")
    async def retirer_mot_interdit(self, interaction: discord.Interaction, mot: str):
        """Retirer un mot interdit"""
        if not await verifier_permissions(interaction, "manage_guild"):
            return
        
        mot_lower = mot.lower().strip()
        if mot_lower in storage.mots_interdits:
            storage.mots_interdits.remove(mot_lower)
            storage.save_data()
            
            embed = create_embed(
                title="✅ Mot interdit retiré",
                description=f"Le mot a été retiré de la liste des mots interdits.",
                color=discord.Color.green(),
                fields=[("Mot retiré", f"`{mot_lower}`", False)]
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(
                f"❌ Le mot `{mot_lower}` n'est pas dans la liste des mots interdits.",
                ephemeral=True
            )
    
    @app_commands.command(name="liste_mots_interdits", description="Voir la liste des mots interdits")
    async def liste_mots_interdits(self, interaction: discord.Interaction):
        """Voir la liste des mots interdits"""
        if not storage.mots_interdits:
            await interaction.response.send_message(
                "ℹ️ Aucun mot interdit n'a été configuré.",
                ephemeral=True
            )
            return
        
        # Ne pas montrer tous les mots dans un message public
        mots_masques = "\n".join([f"• `||{mot}||`" for mot in storage.mots_interdits[:15]])
        
        if len(storage.mots_interdits) > 15:
            mots_masques += f"\n\n... et {len(storage.mots_interdits) - 15} de plus"
        
        embed = create_embed(
            title="🚫 Liste des mots interdits",
            description=f"**{len(storage.mots_interdits)}** mot(s) interdit(s) configuré(s)",
            color=discord.Color.red()
        )
        
        embed.add_field(name="Mots interdits", value=mots_masques, inline=False)
        embed.set_footer(text="Utilisez /ajouter_mot_interdit pour en ajouter")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="vider_mots_interdits", description="Vider toute la liste des mots interdits")
    async def vider_mots_interdits(self, interaction: discord.Interaction):
        """Vider la liste des mots interdits"""
        if not await verifier_permissions(interaction, "administrator"):
            return
        
        mots_supprimes = len(storage.mots_interdits)
        storage.mots_interdits = []
        storage.save_data()
        
        await interaction.response.send_message(
            f"✅ {mots_supprimes} mot(s) interdit(s) supprimé(s).\n"
            f"La liste des mots interdits est maintenant vide.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Moderation(bot))
