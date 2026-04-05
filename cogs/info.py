# Partie du bot discord pour gérer les commandes d'information comme le ping, les infos serveur et membre, avatar et YouTube.

import discord
from discord import app_commands
from discord.ext import commands
import datetime
import platform
from utils import create_embed

class Info(commands.Cog):
    """Commandes d'information"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="youtube", description="Envoie le lien de ma chaîne YouTube")
    async def youtube(self, interaction: discord.Interaction):
        """Partager le lien YouTube"""
        embed = create_embed(
            title="📺 Ma chaîne YouTube",
            description="🎥 Découvrez ma chaîne YouTube et abonnez-vous pour ne rien manquer !",
            color=discord.Color.red(),
            thumbnail="https://cdn-icons-png.flaticon.com/512/1384/1384060.png"
        )
        embed.add_field(name="🔗 Lien", value="[iiSparkTV sur YouTube](https://www.youtube.com/@iiSparkTV)", inline=False)
        embed.add_field(name="🎬 Contenu", value="• Tutoriels Discord\n• Développement de bots\n• Projets créatifs", inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="info_serveur", description="Affiche les informations du serveur")
    async def info_serveur(self, interaction: discord.Interaction):
        """Afficher les informations du serveur"""
        guilde = interaction.guild
        
        # Calculer les statistiques
        age_jours = self.calculate_days_difference(guilde.created_at)
        roles_count = len(guilde.roles) - 1  # Exclure @everyone
        emojis_count = len(guilde.emojis)
        
        embed = create_embed(
            title=f"📊 Informations sur {guilde.name}",
            color=discord.Color.blue(),
            thumbnail=guilde.icon.url if guilde.icon else None,
            fields=[
                ("👑 Propriétaire", guilde.owner.mention, True),
                ("📅 Créé le", self.format_datetime(guilde.created_at), True),
                ("🎂 Âge", f"{age_jours} jours", True),
                ("👥 Membres", str(guilde.member_count), True),
                ("💬 Salons", f"Textuel: {len(guilde.text_channels)}\nVocal: {len(guilde.voice_channels)}", True),
                ("🎭 Rôles", str(roles_count), True),
                ("😀 Émojis", str(emojis_count), True),
                ("🔐 Sécurité", f"Niveau: {guilde.verification_level.name}", True),
                ("🌍 Région", str(guilde.preferred_locale).upper(), True)
            ],
            footer=f"ID: {guilde.id}"
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="info_membre", description="Affiche les informations d'un membre")
    @app_commands.describe(membre="Le membre dont vous voulez voir les informations")
    async def info_membre(self, interaction: discord.Interaction, membre: discord.Member = None):
        """Afficher les informations d'un membre"""
        membre = membre or interaction.user
        
        # Calculer l'ancienneté de manière sécurisée
        anciennete_jours = 0
        if membre.joined_at:
            anciennete_jours = self.calculate_days_difference(membre.joined_at)
        
        # Vérifier les dates pour éviter les erreurs de fuseau horaire
        compte_cree = self.format_datetime(membre.created_at)
        a_rejoint = self.format_datetime(membre.joined_at) if membre.joined_at else "Inconnu"
        
        embed = create_embed(
            title=f"👤 Informations sur {membre.name}",
            color=membre.color,
            thumbnail=membre.avatar.url if membre.avatar else None,
            fields=[
                ("🏷️ Pseudo", membre.display_name, True),
                ("🆔 ID", str(membre.id), True),
                ("📅 Compte créé", compte_cree, True),
                ("📆 A rejoint", a_rejoint, True),
                ("🎂 Ancienneté", f"{anciennete_jours} jours", True),
                ("🎭 Rôles", f"{len(membre.roles) - 1} rôle(s)", True),
                ("🤖 Bot", "✅ Oui" if membre.bot else "❌ Non", True),
                ("📊 Statut", self.format_status(membre.status), True)
            ]
        )
        
        # Ajouter les rôles (limités)
        if len(membre.roles) > 1:
            roles = [role.mention for role in reversed(membre.roles) if role.name != "@everyone"]
            roles_text = " ".join(roles[:10])
            if len(roles) > 10:
                roles_text += f" ... et {len(roles) - 10} de plus"
            embed.add_field(name="🎖️ Rôles principaux", value=roles_text, inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="avatar", description="Affiche l'avatar d'un membre")
    @app_commands.describe(membre="Le membre dont vous voulez voir l'avatar")
    async def avatar(self, interaction: discord.Interaction, 
                    membre: discord.Member = None):
        """Afficher l'avatar d'un membre"""
        membre = membre or interaction.user
        avatar_url = membre.avatar.url if membre.avatar else membre.default_avatar.url
        
        embed = create_embed(
            title=f"🖼️ Avatar de {membre.display_name}",
            color=membre.color,
            image=avatar_url,
            fields=[
                ("🔗 Liens", f"[PNG]({avatar_url.replace('.webp', '.png')}) | "f"[JPG]({avatar_url.replace('.webp', '.jpg')}) | "f"[WEBP]({avatar_url})", False)
            ]
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="ping", description="Affiche la latence du bot")
    async def ping(self, interaction: discord.Interaction):
        """Afficher le ping"""
        latence = round(self.bot.latency * 1000)
        
        # Couleur selon la latence
        if latence < 100:
            color = discord.Color.green()
            status = "🚀 Excellent"
        elif latence < 200:
            color = discord.Color.green()
            status = "👍 Bon"
        elif latence < 300:
            color = discord.Color.orange()
            status = "⚠️ Moyen"
        else:
            color = discord.Color.red()
            status = "🐌 Lent"
        
        embed = create_embed(
            title="🏓 Pong !",
            color=color,
            fields=[
                ("📡 Latence", f"**{latence}ms**", True),
                ("📊 Statut", status, True),
                ("💻 Version", f"Python {platform.python_version()}", True)
            ]
        )
        
        await interaction.response.send_message(embed=embed)
    
    # ===== FONCTIONS UTILITAIRES =====
    
    def calculate_days_difference(self, date_time):
        """Calcule la différence en jours de manière sécurisée pour les fuseaux horaires"""
        if not date_time:
            return 0
        
        # Convertir en datetime naïf si nécessaire
        if date_time.tzinfo is not None:
            # C'est un datetime avec fuseau horaire (aware), on le convertit en naïf
            import pytz
            utc_time = date_time.astimezone(pytz.UTC)
            naive_time = utc_time.replace(tzinfo=None)
            now = datetime.datetime.utcnow()
        else:
            # C'est déjà un datetime naïf
            naive_time = date_time
            now = datetime.datetime.utcnow()
        
        # Calculer la différence
        difference = now - naive_time
        return difference.days
    
    def format_datetime(self, dt):
        """Formate une date de manière sécurisée"""
        if not dt:
            return "Inconnu"
        
        try:
            # Si c'est un datetime avec fuseau horaire
            if dt.tzinfo is not None:
                # Convertir en fuseau horaire local
                import pytz
                local_tz = pytz.timezone('Europe/Paris')  # Ajustez selon votre fuseau
                local_dt = dt.astimezone(local_tz)
                return local_dt.strftime("%d/%m/%Y à %H:%M")
            else:
                # Datetime naïf
                return dt.strftime("%d/%m/%Y à %H:%M")
        except Exception:
            # Fallback simple
            return dt.strftime("%d/%m/%Y")
    
    def format_status(self, status):
        """Formate le statut d'un membre"""
        status_map = {
            discord.Status.online: "🟢 En ligne",
            discord.Status.idle: "🟡 Inactif",
            discord.Status.dnd: "🔴 Ne pas déranger",
            discord.Status.offline: "⚫ Hors ligne",
            discord.Status.invisible: "👻 Invisible"
        }
        return status_map.get(status, str(status).title())

async def setup(bot):
    await bot.add_cog(Info(bot))