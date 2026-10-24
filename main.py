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

# Configuration des intents
intents = discord.Intents.all()

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
    """Commande d'aide complète"""
    embed = discord.Embed(
        title="📖 Guide complet du bot",
        description="Voici toutes les commandes disponibles organisées par catégorie\n Utilisez `/` pour les commandes",
        color=discord.Color.blue()
    )
    
    # Récupérer toutes les commandes slash
    slash_commands = []
    for cmd in bot.tree.get_commands():
        if hasattr(cmd, 'name'):
            slash_commands.append(cmd.name)
    
    # Catégories avec les noms des commandes correspondantes 
    categories = {
        "🛡️ Modération": ["avertir", "avertissements", "effacer_avertissements", "mute", "demute", "expulser", "bannir", "mode_lent", "nettoyer"],
        "🏠 Salons": ["creer_salon_textuel", "creer_salon_vocal", "creer_categorie", "supprimer_salon_textuel", "supprimer_salon_vocal", "supprimer_categorie"],
        "🎫 Tickets": ["creer_ticket", "fermer_ticket"],
        "🔧 Utilitaires": ["rappel", "calculer"],
        "🎭 Rôles": ["role_auto_ajouter", "role_auto_retirer", "role_auto_liste"],
        "📊 Statistiques": ["niveau", "classement", "statistiques"],
        "🎉 Événements": ["definir_anniversaire", "voir_anniversaire", "concours", "concours_relancer"],
        "📝 Contenu": ["suggestion", "creer_note", "voir_note", "liste_note", "supprimer_note"],
        "🎨 Créatif": ["citation", "nom_aleatoire", "couleur_aleatoire"],
        "ℹ️ Informations": ["info_serveur", "info_membre", "avatar", "ping", "youtube"],
        "🎮 Fun": ["de", "pile_ou_face", "boule_magique", "sondage", "emoji_aleatoire"]
    }
    
    for category, commands in categories.items():
        # Filtrer les commandes qui existent
        available_commands = [f"`/{cmd}`" for cmd in commands if cmd in slash_commands]
        if available_commands:
            embed.add_field(
                name=category,
                value=" ".join(available_commands),
                inline=False
            )
    
    embed.set_footer(text=f"Bot créé par Noah • Total de : {len(slash_commands)} commandes utilisables")
    
    await interaction.response.send_message(embed=embed)

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
        use_slash_commands=True,
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
