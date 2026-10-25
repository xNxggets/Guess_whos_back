# Partie principale du bot discord Guess Who's Back gérant le démarrage, les évènements de connexion, et le chargement des cogs.

import discord
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from discord.ext import commands
import traceback

# Chargement des variables d'environnement
load_dotenv(Path(__file__).with_name(".env"))
print("Lancement du bot...")

# Intents utilisés par les événements et commandes du bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
intents.reactions = True

# Création du bot
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None  # Nous créons notre propre commande d'aide
)

# Liste des cogs à charger
COGS = [
    'cogs.moderation',
    'cogs.channels',
    'cogs.tickets',
    'cogs.utilities',
    'cogs.roles',
    'cogs.stats',
    'cogs.events_cog',
    'cogs.content',
    'cogs.creative',
    'cogs.info',
    'cogs.fun',
    'cogs.events_handler',
    'cogs.tasks'
]

# Fonction pour charger les cogs
async def load_cogs():
    """Charge tous les cogs"""
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"Cog chargé: {cog}")
        except Exception as e:
            print(f"Erreur lors du chargement de {cog}: {e}")
            traceback.print_exc()

# Événement de connexion du bot
@bot.event
async def on_ready():
    """Événement déclenché quand le bot est prêt"""
    print(f"═══════════════════════════════════════")
    print(f"Bot connecté en tant que {bot.user.name}")
    print(f"ID: {bot.user.id}")
    print(f"Discord.py version: {discord.__version__}")
    print(f"═══════════════════════════════════════")
    print(f"Connecté à {len(bot.guilds)} serveur(s):")
    for guild in bot.guilds:
        print(f"  - {guild.name} (ID: {guild.id})")
    print(f"═══════════════════════════════════════")
    
    # Synchronisation des commandes slash
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commandes slash synchronisées")
    except Exception as e:
        print(f"Erreur lors de la synchronisation: {e}")
    
    # Définir le statut du bot en ligne avec une biographie personnalisée
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="pour afficher les commandes : /aide"
        ),
        status=discord.Status.online
    )

# Gestion des erreurs globales
@bot.event
async def on_command_error(ctx, error):
    """Gestion des erreurs de commandes"""
    if isinstance(error, commands.CommandNotFound):
        return  # Ignorer les commandes non trouvées
    
    print(f"Erreur dans la commande {ctx.command}: {error}")
    
    embed = discord.Embed(
        title="❌ Erreur",
        description=f"Une erreur est survenue : ```{str(error)[:100]}```",
        color=discord.Color.red()
    )
    
    try:
        await ctx.send(embed=embed)
    except:
        pass

# Gestion des erreurs des commandes slash
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    """Gestion des erreurs des commandes slash"""
    print(f"Erreur dans la commande slash: {error}")
    
    embed = discord.Embed(
        title="❌ Erreur",
        description=f"Une erreur est survenue avec la commande slash.",
        color=discord.Color.red()
    )
    
    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Commande d'aide personnalisée 
@bot.tree.command(name="aide", description="Affiche toutes les commandes disponibles")
async def aide(interaction: discord.Interaction):
    """Affiche les commandes publiques et le panneau staff selon les permissions."""
    commandes_membres = [
        ("🎫 Tickets", [
            ("creer_ticket", "Ouvre un ticket privé; un seul ticket ouvert par membre."),
            ("fermer_ticket", "Ferme le ticket courant si tu l’as créé ou si tu es administrateur."),
        ]),
        ("🔧 Utilitaires", [
            ("rappel", "Programme un rappel personnel, de 1 minute à 7 jours."),
            ("calculer", "Calcule une expression avec les opérations +, -, * et /."),
        ]),
        ("🎭 Rôles", [
            ("role_auto_liste", "Affiche les rôles qui seront attribués aux nouveaux membres."),
        ]),
        ("📊 Statistiques", [
            ("niveau", "Affiche ton niveau et ton expérience."),
            ("classement", "Affiche le classement des membres selon leur expérience."),
            ("statistiques", "Affiche les statistiques générales du serveur."),
        ]),
        ("🎉 Anniversaires", [
            ("definir_anniversaire", "Enregistre ton jour et ton mois d’anniversaire."),
            ("voir_anniversaire", "Affiche l’anniversaire que tu as enregistré."),
        ]),
        ("📝 Contenu", [
            ("suggestion", "Publie une suggestion dans le salon prévu à cet effet."),
            ("creer_note", "Crée une note partagée sur le serveur."),
            ("voir_note", "Affiche une note partagée par son nom."),
            ("liste_note", "Affiche les notes partagées du serveur."),
        ]),
        ("🛡️ Modération", [
            ("liste_mots_interdits", "Affiche la liste des mots filtrés automatiquement."),
        ]),
        ("🎨 Créatif", [
            ("citation", "Affiche une citation inspirante choisie au hasard."),
            ("nom_aleatoire", "Génère un nom selon le type demandé."),
            ("couleur_aleatoire", "Génère une couleur aléatoire avec son code."),
        ]),
        ("ℹ️ Informations", [
            ("info_serveur", "Affiche les informations du serveur actuel."),
            ("info_membre", "Affiche les informations d’un membre."),
            ("avatar", "Affiche l’avatar d’un membre en grand format."),
            ("ping", "Affiche la latence du bot."),
            ("youtube", "Affiche le lien de la chaîne YouTube du créateur."),
        ]),
        ("🎮 Fun", [
            ("de", "Lance un dé; le nombre de faces peut être choisi."),
            ("pile_ou_face", "Lance une pièce et affiche le résultat."),
            ("boule_magique", "Répond à une question comme une boule magique."),
            ("sondage", "Crée un sondage avec deux à cinq choix."),
            ("emoji_aleatoire", "Affiche un emoji aléatoire, éventuellement d’une catégorie."),
        ]),
        ("📖 Aide", [
            ("aide", "Affiche ce panneau et, si tu as les permissions staff, le panneau modération."),
        ]),
    ]

    commandes_staff = [
        ("🛡️ Modération", [
            ("avertir", "Ajoute un avertissement à un membre avec une raison.", "moderate_members"),
            ("avertissements", "Consulte en privé les avertissements d’un membre.", "moderate_members"),
            ("effacer_avertissements", "Efface tous les avertissements d’un membre.", "administrator"),
            ("mute", "Empêche temporairement un membre de parler, en minutes.", "moderate_members"),
            ("demute", "Retire le mute temporaire d’un membre.", "moderate_members"),
            ("expulser", "Expulse un membre du serveur.", "kick_members"),
            ("bannir", "Bannit un membre du serveur.", "ban_members"),
            ("mode_lent", "Règle le délai entre les messages d’un salon.", "manage_channels"),
            ("nettoyer", "Supprime jusqu’à 100 messages du salon courant.", "manage_messages"),
            ("ajouter_mot_interdit", "Ajoute un mot au filtre automatique du serveur.", "manage_guild"),
            ("retirer_mot_interdit", "Retire un mot du filtre automatique du serveur.", "manage_guild"),
            ("vider_mots_interdits", "Vide entièrement la liste des mots filtrés.", "administrator"),
        ]),
        ("🏠 Salons", [
            ("creer_salon_textuel", "Crée un salon textuel, avec catégorie facultative.", "manage_channels"),
            ("creer_salon_vocal", "Crée un salon vocal, avec catégorie facultative.", "manage_channels"),
            ("creer_categorie", "Crée une catégorie de salons.", "manage_channels"),
            ("supprimer_salon_textuel", "Supprime un salon textuel après confirmation.", "manage_channels"),
            ("supprimer_salon_vocal", "Supprime un salon vocal après confirmation.", "manage_channels"),
            ("supprimer_categorie", "Supprime une catégorie après confirmation; ses salons restent sur le serveur.", "manage_channels"),
        ]),
        ("🎭 Rôles", [
            ("role_auto_ajouter", "Ajoute un rôle à la liste attribuée aux nouveaux membres.", "manage_roles"),
            ("role_auto_retirer", "Retire un rôle de la liste des rôles automatiques.", "manage_roles"),
        ]),
        ("🎉 Concours", [
            ("concours", "Lance un concours avec une durée et un nombre de gagnants.", "manage_guild"),
            ("concours_relancer", "Relance le tirage d’un concours existant.", "manage_guild"),
        ]),
        ("📝 Notes", [
            ("supprimer_note", "Supprime une note partagée; permission Gérer les messages requise.", "manage_messages"),
        ]),
    ]

    permissions = getattr(interaction.user, "guild_permissions", discord.Permissions.none())
    permissions_staff = {
        permission
        for _, commandes in commandes_staff
        for _, _, permission in commandes
    }
    est_staff = any(getattr(permissions, permission, False) for permission in permissions_staff)

    def ajouter_categories(embed, categories):
        commandes_disponibles = {
            commande.name for commande in bot.tree.get_commands()
        }
        for categorie, commandes in categories:
            lignes = [
                f"`/{nom}` — {description}"
                for nom, description in commandes
                if nom in commandes_disponibles
            ]
            if lignes:
                embed.add_field(name=categorie, value="\n".join(lignes), inline=False)

    panneau_membres = discord.Embed(
        title="📖 Aide — commandes membres",
        description="Commandes disponibles sur le serveur. Utilise `/` pour les lancer.",
        color=discord.Color.blue(),
    )
    ajouter_categories(panneau_membres, commandes_membres)
    panneau_membres.add_field(
        name="Commandes préfixées",
        value="`!test` — vérifie que le bot répond.\n`!invite` — affiche le lien d’invitation du bot.",
        inline=False,
    )
    panneau_membres.set_footer(text="Les commandes réservées au staff dépendent de tes permissions Discord.")

    panneaux = [panneau_membres]
    if est_staff:
        commandes_autorisees = []
        for categorie, commandes in commandes_staff:
            visibles = [
                (nom, description)
                for nom, description, permission in commandes
                if getattr(permissions, permission, False)
            ]
            if visibles:
                commandes_autorisees.append((categorie, visibles))

        panneau_staff = discord.Embed(
            title="🛡️ Aide — modération et administration",
            description="Ce panneau n’affiche que les commandes autorisées par tes permissions.",
            color=discord.Color.orange(),
        )
        ajouter_categories(panneau_staff, commandes_autorisees)
        if await bot.is_owner(interaction.user):
            panneau_staff.add_field(
                name="Commandes propriétaire",
                value="`!recharger [cog]` — recharge un cog ou toutes les extensions.\n`!cogs` — affiche les extensions chargées.",
                inline=False,
            )
        panneaux.append(panneau_staff)

    await interaction.response.send_message(
        embeds=panneaux,
        ephemeral=est_staff,
    )

# Commande pour inviter le bot
@bot.command(name="invite")
async def invite(ctx):
    """Génère un lien d'invitation pour le bot"""
    # Les permissions nécessaires pour que le bot fonctionne correctement
    permissions = discord.Permissions(
        # Permissions générales
        view_channel=True,
        send_messages=True,
        embed_links=True,
        attach_files=True,
        read_message_history=True,
        add_reactions=True,
        
        # Permissions de modération
        manage_messages=True,
        manage_channels=True,
        moderate_members=True,
        manage_nicknames=True,
        manage_roles=True,
        kick_members=True,
        ban_members=True,
        
        # Autres
        create_public_threads=True,
        create_private_threads=True,
        send_messages_in_threads=True,
        manage_threads=True
    )
    
    oauth_url = discord.utils.oauth_url(
        client_id=bot.user.id,
        permissions=permissions,
        scopes=["bot", "applications.commands"]
    )
    
    embed = discord.Embed(
        title="🔗 Lien d'invitation",
        description=f"Clique sur le lien ci-dessous pour m'inviter sur ton serveur !",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Lien d'invitation",
        value=f"[Invite-moi ici !]({oauth_url})",
        inline=False
    )
    embed.add_field(
        name="Permissions requises",
        value="Le bot a besoin de ces permissions pour fonctionner correctement. Tu peux ajuster les permissions après l'invitation si nécessaire.",
        inline=False
    )
    embed.set_footer(text="Le bot sera disponible dans tous les salons où il a les permissions nécessaires.")
    
    await ctx.send(embed=embed)

# Commande pour recharger les cogs (seulement pour les admins)
@bot.command(name="recharger")
@commands.is_owner()
async def recharger(ctx, cog: str = None):
    """Recharge un cog (propriétaire du bot uniquement)"""
    if cog is None:
        # Recharger tous les cogs
        for cog_name in COGS:
            try:
                await bot.reload_extension(cog_name)
            except Exception as e:
                await ctx.send(f"❌ Erreur avec {cog_name}: {e}")
        await ctx.send("✅ Tous les cogs ont été rechargés")
    else:
        # Recharger un cog spécifique
        cog_path = f"cogs.{cog}"
        if cog_path in COGS:
            try:
                await bot.reload_extension(cog_path)
                await ctx.send(f"✅ Cog `{cog}` rechargé")
            except Exception as e:
                await ctx.send(f"❌ Erreur: {e}")
        else:
            await ctx.send(f"❌ Cog `{cog}` non trouvé")

# Commande pour lister les cogs
@bot.command(name="cogs")
@commands.is_owner()
async def liste_cogs(ctx):
    """Liste tous les cogs chargés (propriétaire du bot uniquement)"""
    loaded_cogs = list(bot.cogs.keys())
    
    embed = discord.Embed(
        title="📁 Cogs chargés",
        description=f"{len(loaded_cogs)} cogs actifs",
        color=discord.Color.green()
    )
    
    for cog_name in loaded_cogs:
        cog = bot.get_cog(cog_name)
        commands_list = [cmd.name for cmd in cog.get_commands() if hasattr(cmd, 'name')]
        embed.add_field(
            name=cog_name,
            value=f"Commandes: {len(commands_list)}",
            inline=True
        )
    
    await ctx.send(embed=embed)

# Commande de test
@bot.command(name="test")
async def test(ctx):
    """Commande de test pour vérifier que le bot fonctionne"""
    embed = discord.Embed(
        title="✅ Bot en ligne !",
        description=f"Salut {ctx.author.mention} ! Le bot fonctionne correctement. 😊",
        color=discord.Color.green()
    )
    embed.add_field(name="Latence", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="Commandes", value=f"{len(bot.commands)} disponibles", inline=True)
    embed.add_field(name="Version", value="2.0 (Français)", inline=True)
    
    await ctx.send(embed=embed)

async def main():
    """Fonction principale"""
    await load_cogs()
    
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ ERREUR : Token Discord non trouvé dans le fichier .env")
        print("❌ Créez un fichier .env avec DISCORD_TOKEN=votre_token")
        return
    
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        print("\n👋 Arrêt du bot...")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        traceback.print_exc()
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
