# Partie du bot discord pour gérer les rôles automatiques.

import discord
from discord import app_commands
from discord.ext import commands
from utils import verifier_permissions, create_embed
from data.storage import storage

class Roles(commands.Cog):
    """Gestion des rôles"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="role_auto_ajouter", description="Ajouter un rôle automatique")
    @app_commands.describe(role="Le rôle à attribuer automatiquement")
    async def role_auto_ajouter(self, interaction: discord.Interaction, role: discord.Role):
        """Ajouter un auto-rôle"""
        if not await verifier_permissions(interaction, "manage_roles"):
            return
        
        guild_id = interaction.guild.id
        
        # Initialiser si nécessaire
        if guild_id not in storage.auto_roles:
            storage.auto_roles[guild_id] = []
        
        if role.id not in storage.auto_roles[guild_id]:
            storage.auto_roles[guild_id].append(role.id)
            storage.save_data()
            await interaction.response.send_message(
                f"✅ Le rôle {role.mention} sera désormais attribué automatiquement aux nouveaux membres"
            )
        else:
            await interaction.response.send_message(
                f"❌ Ce rôle est déjà dans les auto-rôles",
                ephemeral=True
            )
    
    @app_commands.command(name="role_auto_retirer", description="Retirer un rôle automatique")
    @app_commands.describe(role="Le rôle à retirer des auto-rôles")
    async def role_auto_retirer(self, interaction: discord.Interaction, role: discord.Role):
        """Retirer un auto-rôle"""
        if not await verifier_permissions(interaction, "manage_roles"):
            return
        
        guild_id = interaction.guild.id
        
        if guild_id in storage.auto_roles and role.id in storage.auto_roles[guild_id]:
            storage.auto_roles[guild_id].remove(role.id)
            storage.save_data()
            await interaction.response.send_message(
                f"✅ Le rôle {role.mention} ne sera plus attribué automatiquement"
            )
        else:
            await interaction.response.send_message(
                f"❌ Ce rôle n'est pas dans les auto-rôles",
                ephemeral=True
            )
    
    @app_commands.command(name="role_auto_liste", description="Voir la liste des auto-rôles")
    async def role_auto_liste(self, interaction: discord.Interaction):
        """Voir la liste des auto-rôles"""
        guild_id = interaction.guild.id
        
        if guild_id not in storage.auto_roles or not storage.auto_roles[guild_id]:
            await interaction.response.send_message(
                "ℹ️ Aucun auto-rôle configuré sur ce serveur",
                ephemeral=True
            )
            return
        
        roles_list = []
        for role_id in storage.auto_roles[guild_id]:
            role = interaction.guild.get_role(role_id)
            if role:
                roles_list.append(f"• {role.mention} (ID: {role.id})")
        
        embed = create_embed(
            title="📋 Liste des auto-rôles",
            description="\n".join(roles_list) if roles_list else "Aucun auto-rôle",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"{len(roles_list)} auto-rôle(s) configuré(s)")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Roles(bot))