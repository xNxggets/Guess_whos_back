"""Commandes de gestion des salons et catégories du serveur."""

from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils import verifier_permissions


class ConfirmationSuppression(discord.ui.View):
    """Demande une confirmation avant de supprimer un salon ou une catégorie."""

    def __init__(self, author_id: int):
        super().__init__(timeout=60)
        self.author_id = author_id
        self.confirmed = False

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "Seule la personne ayant lancé la commande peut répondre.",
                ephemeral=True,
            )
            return False
        return True

    @discord.ui.button(label="Confirmer", style=discord.ButtonStyle.danger)
    async def confirmer(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        self.confirmed = True
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.secondary)
    async def annuler(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.response.edit_message(
            content="Suppression annulée.", view=None
        )
        self.stop()


class Channels(commands.Cog):
    """Création et suppression de salons textuels, vocaux et catégories."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _verifier_gestion_salons(
        self, interaction: discord.Interaction
    ) -> bool:
        if interaction.guild is None:
            await interaction.response.send_message(
                "Cette commande doit être utilisée sur un serveur.", ephemeral=True
            )
            return False

        if not await verifier_permissions(interaction, "manage_channels"):
            return False

        bot_member = interaction.guild.me
        if bot_member is None or not bot_member.guild_permissions.manage_channels:
            await interaction.response.send_message(
                "Le bot doit avoir la permission **Gérer les salons**.",
                ephemeral=True,
            )
            return False

        return True

    async def _creer_salon(
        self,
        interaction: discord.Interaction,
        nom: str,
        categorie: Optional[discord.CategoryChannel],
        vocal: bool,
    ) -> None:
        if not await self._verifier_gestion_salons(interaction):
            return

        if categorie is not None and categorie.guild_id != interaction.guild_id:
            await interaction.response.send_message(
                "La catégorie choisie doit appartenir à ce serveur.", ephemeral=True
            )
            return

        try:
            if vocal:
                salon = await interaction.guild.create_voice_channel(
                    nom,
                    category=categorie,
                    reason=f"Créé par {interaction.user} via le bot",
                )
            else:
                salon = await interaction.guild.create_text_channel(
                    nom,
                    category=categorie,
                    reason=f"Créé par {interaction.user} via le bot",
                )
        except discord.Forbidden:
            await interaction.response.send_message(
                "Discord a refusé la création. Vérifie les permissions du bot dans "
                "la catégorie choisie.",
                ephemeral=True,
            )
            return
        except discord.HTTPException:
            await interaction.response.send_message(
                "Discord n’a pas pu créer ce salon. Vérifie son nom et réessaie.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"✅ Salon {salon.mention} créé."
        )

    async def _supprimer_salon(
        self,
        interaction: discord.Interaction,
        salon: discord.abc.GuildChannel,
        est_categorie: bool = False,
    ) -> None:
        if not await self._verifier_gestion_salons(interaction):
            return

        if salon.guild.id != interaction.guild_id:
            await interaction.response.send_message(
                "Le salon choisi doit appartenir à ce serveur.", ephemeral=True
            )
            return

        avertissement = ""
        if est_categorie and salon.channels:
            avertissement = (
                f" Elle contient {len(salon.channels)} salon(s), qui resteront sur le "
                "serveur sans catégorie après la suppression."
            )

        view = ConfirmationSuppression(interaction.user.id)
        await interaction.response.send_message(
            f"Confirmer la suppression de **{salon.name}** ?{avertissement}",
            view=view,
            ephemeral=True,
        )

        timed_out = await view.wait()
        if timed_out:
            await interaction.edit_original_response(
                content="Confirmation expirée. Le salon n’a pas été supprimé.",
                view=None,
            )
            return
        if not view.confirmed:
            return

        await interaction.edit_original_response(
            content="Suppression en cours…", view=None
        )
        try:
            await salon.delete(reason=f"Supprimé par {interaction.user} via le bot")
        except discord.Forbidden:
            await interaction.followup.send(
                "Discord a refusé la suppression. Vérifie les permissions du bot.",
                ephemeral=True,
            )
            return
        except discord.HTTPException:
            await interaction.followup.send(
                "Discord n’a pas pu supprimer ce salon. Il a peut-être déjà été supprimé.",
                ephemeral=True,
            )
            return

        await interaction.followup.send(
            f"✅ **{salon.name}** a été supprimé.", ephemeral=True
        )

    @app_commands.command(
        name="creer_salon_textuel", description="Créer un salon textuel"
    )
    @app_commands.describe(
        nom="Nom du salon textuel",
        categorie="Catégorie où placer le salon (facultatif)",
    )
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.guild_only()
    async def creer_salon_textuel(
        self,
        interaction: discord.Interaction,
        nom: str,
        categorie: Optional[discord.CategoryChannel] = None,
    ) -> None:
        await self._creer_salon(interaction, nom, categorie, vocal=False)

    @app_commands.command(
        name="creer_salon_vocal", description="Créer un salon vocal"
    )
    @app_commands.describe(
        nom="Nom du salon vocal",
        categorie="Catégorie où placer le salon (facultatif)",
    )
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.guild_only()
    async def creer_salon_vocal(
        self,
        interaction: discord.Interaction,
        nom: str,
        categorie: Optional[discord.CategoryChannel] = None,
    ) -> None:
        await self._creer_salon(interaction, nom, categorie, vocal=True)

    @app_commands.command(name="creer_categorie", description="Créer une catégorie")
    @app_commands.describe(nom="Nom de la catégorie")
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.guild_only()
    async def creer_categorie(
        self,
        interaction: discord.Interaction,
        nom: str,
    ) -> None:
        if not await self._verifier_gestion_salons(interaction):
            return

        try:
            categorie = await interaction.guild.create_category(
                nom,
                reason=f"Créée par {interaction.user} via le bot",
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "Discord a refusé la création. Vérifie les permissions du bot.",
                ephemeral=True,
            )
            return
        except discord.HTTPException:
            await interaction.response.send_message(
                "Discord n’a pas pu créer cette catégorie. Vérifie son nom et réessaie.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"✅ Catégorie **{categorie.name}** créée."
        )

    @app_commands.command(
        name="supprimer_salon_textuel", description="Supprimer un salon textuel"
    )
    @app_commands.describe(salon="Salon textuel à supprimer")
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.guild_only()
    async def supprimer_salon_textuel(
        self, interaction: discord.Interaction, salon: discord.TextChannel
    ) -> None:
        await self._supprimer_salon(interaction, salon)

    @app_commands.command(
        name="supprimer_salon_vocal", description="Supprimer un salon vocal"
    )
    @app_commands.describe(salon="Salon vocal à supprimer")
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.guild_only()
    async def supprimer_salon_vocal(
        self, interaction: discord.Interaction, salon: discord.VoiceChannel
    ) -> None:
        await self._supprimer_salon(interaction, salon)

    @app_commands.command(
        name="supprimer_categorie", description="Supprimer une catégorie"
    )
    @app_commands.describe(categorie="Catégorie à supprimer")
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.guild_only()
    async def supprimer_categorie(
        self, interaction: discord.Interaction, categorie: discord.CategoryChannel
    ) -> None:
        await self._supprimer_salon(interaction, categorie, est_categorie=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Channels(bot))
