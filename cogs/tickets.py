# Partie du bot gérant le système de tickets de support.

import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from data.storage import storage

# Cog pour la gestion des tickets
class Tickets(commands.Cog):
    """Système de tickets"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="creer_ticket", description="Créer un ticket de support")
    @app_commands.describe(sujet="Le sujet de votre ticket")
    @app_commands.guild_only()
    async def creer_ticket(self, interaction: discord.Interaction, sujet: str):
        """Créer un ticket"""
        guilde = interaction.guild

        bot_member = guilde.me
        if bot_member is None or not bot_member.guild_permissions.manage_channels:
            await interaction.response.send_message(
                "Le bot doit avoir la permission **Gérer les salons**.",
                ephemeral=True,
            )
            return

        for ticket_id, proprietaire_id in storage.tickets_actifs.items():
            salon_existant = guilde.get_channel(ticket_id)
            if proprietaire_id == interaction.user.id and salon_existant is not None:
                await interaction.response.send_message(
                    f"Tu as déjà un ticket ouvert : {salon_existant.mention}",
                    ephemeral=True,
                )
                return

        categorie = discord.utils.get(guilde.categories, name="Tickets")
        
        # Créer la catégorie si elle n'existe pas
        if not categorie:
            categorie = await guilde.create_category("Tickets")
        
        # Créer le salon du ticket
        salon_ticket = await categorie.create_text_channel(
            f"ticket-{interaction.user.name}",
            overwrites={
                guilde.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(
                    read_messages=True, 
                    send_messages=True,
                    attach_files=True
                ),
                guilde.me: discord.PermissionOverwrite(
                    read_messages=True, 
                    send_messages=True,
                    manage_channels=True
                )
            }
        )
        
        storage.tickets_actifs[salon_ticket.id] = interaction.user.id
        storage.save_data()
        
        embed = discord.Embed(
            title="🎫 Nouveau Ticket",
            description=f"**Sujet:** {sujet}\n\nUn membre du staff va bientôt vous répondre.",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Utilisez /fermer_ticket pour fermer ce ticket")
        
        await salon_ticket.send(f"{interaction.user.mention}", embed=embed)
        
        # Ajouter un bouton pour fermer le ticket avec une classe View correcte
        class CloseTicketView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
            
            @discord.ui.button(label="Fermer le ticket", style=discord.ButtonStyle.danger, emoji="🔒")
            async def close_button_callback(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                # Vérifier si c'est le créateur du ticket ou un administrateur
                if (button_interaction.user.id != interaction.user.id and 
                    not button_interaction.user.guild_permissions.administrator):
                    await button_interaction.response.send_message(
                        "❌ Seul le créateur du ticket ou un administrateur peut fermer ce ticket.",
                        ephemeral=True
                    )
                    return
                
                # Vérifier si c'est bien un ticket
                if button_interaction.channel.id not in storage.tickets_actifs:
                    await button_interaction.response.send_message(
                        "❌ Ce salon n'est pas un ticket !",
                        ephemeral=True
                    )
                    return
                
                # Confirmer la fermeture
                await button_interaction.response.send_message("🔒 Fermeture du ticket dans 5 secondes...")
                await asyncio.sleep(5)
                
                # Supprimer le ticket de la liste
                if button_interaction.channel.id in storage.tickets_actifs:
                    del storage.tickets_actifs[button_interaction.channel.id]
                    storage.save_data()
                
                # Supprimer le salon
                await button_interaction.channel.delete()
        
        # Envoyer le bouton
        view = CloseTicketView()
        await salon_ticket.send(view=view)
        
        await interaction.response.send_message(
            f"✅ Ticket créé : {salon_ticket.mention}",
            ephemeral=True
        )
    
    @app_commands.command(name="fermer_ticket", description="Fermer un ticket")
    async def fermer_ticket(self, interaction: discord.Interaction):
        """Fermer un ticket"""
        # Vérifier si le salon est un ticket
        if interaction.channel.id not in storage.tickets_actifs:
            await interaction.response.send_message(
                "❌ Ce salon n'est pas un ticket !",
                ephemeral=True
            )
            return
        
        # Vérifier les permissions
        if (interaction.user.id != storage.tickets_actifs[interaction.channel.id] and 
            not interaction.user.guild_permissions.administrator):
            await interaction.response.send_message(
                "❌ Seul le créateur du ticket ou un administrateur peut fermer ce ticket.",
                ephemeral=True
            )
            return
        
        await interaction.response.send_message("🔒 Fermeture du ticket dans 5 secondes...")
        await asyncio.sleep(5)
        
        # Supprimer le ticket de la liste
        if interaction.channel.id in storage.tickets_actifs:
            del storage.tickets_actifs[interaction.channel.id]
            storage.save_data()
        
        # Supprimer le salon
        await interaction.channel.delete()

async def setup(bot):
    await bot.add_cog(Tickets(bot))
