# Partie du bot discord pour gérer les événements comme les messages, les réactions, les arrivées et départs des membres.

import discord
from discord.ext import commands
import random
import datetime
import asyncio
from utils import calculer_niveau, get_emoji, get_random_emoji, format_with_emojis
from data.storage import storage

class EventsHandler(commands.Cog):
    """Gestionnaire d'événements"""
    
    def __init__(self, bot):
        self.bot = bot
        
        # Liste étendue de mots interdits (peut être configurée via commande)
        self.default_banned_words = [
            "insulte", "raciste", "haine", "violence", "spam", 
            "arnaque", "phishing", "malware", "nude", "porno"
        ]
        
        # Mots déclenchant des réactions automatiques
        self.reaction_triggers = {
            "félicitations": ["🎉", "🎊", "🥳", "👏"],
            "bravo": ["👏", "👍", "🎉", "🏆"],
            "génial": ["✨", "🌟", "🔥", "💯"],
            "super": ["👍", "👌", "💪", "🚀"],
            "triste": ["😢", "😔", "💔", "🫂"],
            "colère": ["😠", "😡", "💢", "⚡"],
            "amour": ["❤️", "💖", "🥰", "😍"],
            "rire": ["😂", "🤣", "😆", "😄"],
            "chat": ["🐱", "😸", "😻", "🐾"],
            "chien": ["🐶", "🐕", "🦴", "🐾"],
            "merci": ["🙏", "😊", "💝", "✨"],
            "bonjour": ["👋", "😊", "🌞", "☕"],
            "bonsoir": ["🌙", "😴", "✨", "🌟"],
            "coucou": ["👋", "😊", "✨", "💫"],
            "pizza": ["🍕", "😋", "👍", "🔥"],
            "café": ["☕", "😌", "⚡", "💪"],
            "musique": ["🎵", "🎶", "🎧", "🎤"],
            "jeu vidéo": ["🎮", "👾", "🕹️", "🎯"],
            "film": ["🎬", "🍿", "📽️", "🎞️"],
            "livre": ["📚", "📖", "🔖", "✍️"],
            "soleil": ["☀️", "😎", "🌴", "🏖️"],
            "pluie": ["🌧️", "☔", "💧", "🌂"],
            "neige": ["❄️", "☃️", "⛄", "🎿"],
            "voyage": ["✈️", "🧳", "🌍", "🗺️"],
            "école": ["📚", "✏️", "📝", "🎒"],
            "travail": ["💼", "👔", "💻", "📊"],
            "sport": ["⚽", "🏀", "🎾", "🏃"],
            "code": ["💻", "👨‍💻", "🔧", "⚙️"],
            "python": ["🐍", "💻", "👨‍💻", "🔥"],
            "discord": ["😊", "💬", "🎮", "👥"]
        }
        
        # Réponses automatiques étendues
        self.auto_responses = {
            "bonjour": (f"Salut {get_emoji('wave')}", "😊"),
            "salut": (f"Coucou {get_emoji('wave')}", "👋"),
            "coucou": (f"Hey {get_emoji('wave')}", "😄"),
            "hello": ("Hello !", "👋"),
            "hi": ("Hi there!", "👋"),
            "hey": ("Hey !", "😊"),
            "bonsoir": ("Bonsoir !", "🌙"),
            "bsr": ("Bonsoir !", "🌙"),
            "bjr": ("Bonjour !", "☀️"),
            "merci": ("De rien !", "😊"),
            "merci beaucoup": ("Avec plaisir !", "❤️"),
            "thanks": ("You're welcome!", "👍"),
            "thank you": ("My pleasure!", "😊"),
            "stp": ("Bien sûr !", "✅"),
            "svp": ("Voilà !", "🎯"),
            "s'il te plait": ("D'accord !", "👍"),
            "s'il vous plait": ("Tout de suite !", "⚡"),
            "aurevoir": ("À bientôt !", "👋"),
            "au revoir": ("À plus !", "👋"),
            "bye": ("Bye !", "👋"),
            "goodbye": ("See you!", "👋"),
            "bonne nuit": ("Dors bien !", "😴"),
            "bonne journée": ("Toi aussi !", "☀️"),
            "bon week-end": ("Merci, toi aussi !", "🎉"),
            "joyeux noël": ("Joyeux Noël !", "🎄"),
            "bonne année": ("Bonne année !", "🎆"),
            "anniversaire": ("Joyeux anniversaire !", "🎂"),
            "félicitations": ("Bravo !", "🎉"),
            "bravo": ("Excellent !", "👏"),
            "génial": ("Super !", "✨"),
            "super": ("Génial !", "🔥"),
            "parfait": ("Parfait !", "✅"),
            "excellent": ("Excellent !", "🌟"),
            "fantastique": ("Fantastique !", "💫"),
            "incroyable": ("Incroyable !", "🤯"),
            "wow": ("Wow !", "😲"),
            "omg": ("Oh mon dieu !", "😱"),
            "lol": ("Haha !", "😂"),
            "mdr": ("Hahaha !", "🤣"),
            "haha": ("😂", "😂"),
            "héhé": ("😄", "😄"),
            "hé": ("😏", "😏"),
            "ok": ("D'accord !", "👌"),
            "d'accord": ("Entendu !", "✅"),
            "compris": ("Parfait !", "👍"),
            "oui": ("👍", "👍"),
            "non": ("👎", "👎"),
            "peut-être": ("🤔", "🤔"),
            "pourquoi": ("Parce que !", "🤷"),
            "comment": ("Comme ça !", "👉"),
            "quand": ("Bientôt !", "⏰"),
            "où": ("Ici !", "📍"),
            "qui": ("Moi !", "🤖"),
            "quoi": ("Ça !", "👉"),
            "help": ("Besoin d'aide ?", "🆘"),
            "aide": ("Utilise /aide !", "📖"),
            "commandes": ("Tape /aide !", "📋"),
            "ping": ("Pong !", "🏓"),
            "pong": ("Ping !", "🏓"),
            "bot": ("C'est moi !", "🤖"),
            "robot": ("Présent !", "🤖"),
            "intelligence": ("Je suis là !", "🧠"),
            "artificielle": ("C'est moi !", "⚡"),
            "python": ("🐍 Python c'est super !", "💻"),
            "discord": ("Discord c'est génial !", "😊"),
            "jeu": ("J'aime les jeux !", "🎮"),
            "musique": ("J'adore la musique !", "🎵"),
            "film": ("Les films c'est cool !", "🎬"),
            "série": ("Binge watching !", "📺"),
            "livre": ("La lecture c'est bien !", "📚"),
            "nourriture": ("J'ai faim maintenant !", "🍕"),
            "faim": ("Moi aussi !", "🍔"),
            "soif": ("Buvez de l'eau !", "💧"),
            "fatigué": ("Repose-toi !", "😴"),
            "malade": ("Soigne-toi bien !", "🤒"),
            "heureux": ("C'est super !", "😄"),
            "triste": ("Ne sois pas triste !", "😢"),
            "énervé": ("Calme-toi !", "😤"),
            "stressé": ("Respire !", "🧘"),
            "excité": ("Woohoo !", "🎉"),
            "amour": ("❤️", "❤️"),
            "ami": ("👫", "👫"),
            "famille": ("👨‍👩‍👧‍👦", "👨‍👩‍👧‍👦"),
            "travail": ("Au boulot !", "💼"),
            "école": ("Bonne chance !", "📚"),
            "vacances": ("Profite !", "🏖️"),
            "week-end": ("Repose-toi !", "😴"),
            "lundi": ("Courage !", "💪"),
            "vendredi": ("Enfin !", "🎉"),
            "samedi": ("Super !", "😎"),
            "dimanche": ("Repos !", "😴")
        }
        
        # Réponses quand on ping le bot
        self.ping_responses = [
            f"Oui ? {get_emoji('thinking')}",
            f"Vous m'avez appelé ? {get_emoji('robot')}",
            f"À votre service ! {get_emoji('salute')}",
            f"Que puis-je faire pour vous ? {get_emoji('help')}",
            f"Je suis là ! {get_emoji('sparkles')}",
            f"Present ! {get_emoji('wave')}",
            f"Oui, c'est moi ! {get_emoji('smile')}",
            f"Comment puis-je vous aider ? {get_emoji('question')}",
            f"Je vous écoute ! {get_emoji('ear')}",
            f"Tout va bien ? {get_emoji('thumbsup')}",
            f"Besoin d'aide ? {get_emoji('help')}",
            f"Je suis prêt à aider ! {get_emoji('muscle')}",
            f"Salut ! Comment ça va ? {get_emoji('wave')}",
            f"Je suis là pour vous servir ! {get_emoji('salute')}",
            f"Que se passe-t-il ? {get_emoji('thinking')}",
            f"Tout va bien de mon côté ! {get_emoji('ok')}",
            f"Prêt à exécuter vos ordres ! {get_emoji('robot')}",
            f"Encore moi ! {get_emoji('smile')}",
            f"Qu'est-ce qui vous amène ? {get_emoji('curious')}",
            f"Je suis tout ouïe ! {get_emoji('ear')}"
        ]
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """Événement déclenché quand une réaction est ajoutée"""
        # Ignorer les réactions des bots
        if user.bot:
            return
        
        # Vérifier si la réaction est sur un message de giveaway
        if reaction.message.id in storage.giveaways:
            giveaway = storage.giveaways[reaction.message.id]
            # Vérifier si la réaction est 🎉
            if str(reaction.emoji) == "🎉":
                if user.id not in giveaway["participants"]:
                    giveaway["participants"].append(user.id)
                    storage.save_data()
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Événement déclenché à chaque message"""
        # Ignorer les messages des bots
        if message.author.bot:
            return
        
        user_id = message.author.id
        
        # Système de niveaux
        if user_id not in storage.niveaux:
            storage.niveaux[user_id] = {"niveau": 1, "xp": 0}
        
        xp_gagne = random.randint(5, 15)
        storage.niveaux[user_id]["xp"] += xp_gagne
        
        # Vérifier si le niveau a augmenté
        nouveau_niveau = calculer_niveau(storage.niveaux[user_id]["xp"])
        if nouveau_niveau > storage.niveaux[user_id]["niveau"]:
            ancien_niveau = storage.niveaux[user_id]["niveau"]
            storage.niveaux[user_id]["niveau"] = nouveau_niveau
            storage.save_data()
            
            # Émojis spéciaux pour les paliers de niveau
            niveau_emojis = {
                5: "🌟",
                10: "✨",
                20: "🔥",
                30: "💎",
                40: "👑",
                50: "🏆",
                69: "😏",  # Niveau spécial
                100: "💯"
            }
            
            emoji_niveau = niveau_emojis.get(nouveau_niveau, "🎉")
            
            embed = discord.Embed(
                title=f"{emoji_niveau} Niveau supérieur !",
                description=format_with_emojis(
                    f"{message.author.mention} vient d'atteindre le **niveau {nouveau_niveau}** !\n"
                    f"Progression : **{ancien_niveau}** → **{nouveau_niveau}**"
                ),
                color=discord.Color.gold()
            )
            
            # Ajouter des émojis de félicitations aléatoires
            felicitation_emojis = ["🎊", "🥳", "🎈", "👏", "🙌", "💪", "🚀"]
            embed.set_footer(text=f"Félicitations ! {random.choice(felicitation_emojis)}")
            
            await message.channel.send(embed=embed)
        
        # Statistiques des messages
        if user_id not in storage.stats_messages:
            storage.stats_messages[user_id] = 0
        storage.stats_messages[user_id] += 1
        
        # Auto-modération : mots interdits
        contenu_bas = message.content.lower()
        
        # Vérifier les mots interdits (stockage + par défaut)
        banned_words = storage.mots_interdits
        
        for mot_interdit in banned_words:
            if mot_interdit and mot_interdit in contenu_bas:
                await message.delete()
                
                # Avertissement privé
                try:
                    warning_dm = discord.Embed(
                        title=f"{get_emoji('warning')} Contenu interdit",
                        description=(
                            f"Votre message a été supprimé du serveur **{message.guild.name}**\n"
                            f"**Raison :** Contenu inapproprié\n"
                            f"**Mot détecté :** ||{mot_interdit}||"
                        ),
                        color=discord.Color.red()
                    )
                    warning_dm.set_footer(text="Répéter cette action peut entraîner un avertissement")
                    await message.author.send(embed=warning_dm)
                except:
                    pass
                
                # Message dans le salon
                warning_embed = discord.Embed(
                    title=f"{get_emoji('warning')} Message supprimé",
                    description=format_with_emojis(
                        f"{message.author.mention}, ce contenu est interdit sur ce serveur !"
                    ),
                    color=discord.Color.red()
                )
                warning_msg = await message.channel.send(embed=warning_embed, delete_after=10)
                return
        
        # Détection de spam (majuscules)
        if len(message.content) > 10:
            lettres = [c for c in message.content if c.isalpha()]
            if lettres:
                majuscules = sum(1 for c in lettres if c.isupper())
                ratio = majuscules / len(lettres)
                if ratio > 0.7:
                    await message.delete()
                    spam_embed = discord.Embed(
                        title=f"{get_emoji('mute')} Trop de majuscules",
                        description=format_with_emojis(
                            f"{message.author.mention}, évitez d'écrire en majuscules !"
                        ),
                        color=discord.Color.orange()
                    )
                    await message.channel.send(embed=spam_embed, delete_after=5)
                    return
        
        # === RÉPONSES AUTOMATIQUES ===
        contenu = message.content.lower().strip()
        
        # Variable pour suivre si on a déjà répondu
        repondu = False
        
        # Réponses aux mots spécifiques
        for mot, (reponse, emoji_reponse) in self.auto_responses.items():
            if mot == contenu or f" {mot} " in f" {contenu} ":
                if random.random() < 0.7:  # 70% de chance de répondre
                    # Parfois ajouter un emoji aléatoire supplémentaire
                    if random.random() < 0.3:  # 30% de chance
                        emoji_supp = get_random_emoji(["positive", "fun"])
                        reponse_complete = f"{reponse} {emoji_supp}"
                    else:
                        reponse_complete = f"{reponse}"
                    
                    await message.channel.send(reponse_complete)
                    repondu = True
                break  # Une seule réponse par message, même si on n'a pas répondu (à cause de la chance)
        
        # === RÉPONSES AUX MENTIONS DU BOT ===
        if not repondu and self.bot.user.mentioned_in(message):
            if len(message.content.split()) <= 5:  # Message court avec mention
                await message.channel.send(random.choice(self.ping_responses))
            else:
                # Si le message est plus long, répondre de manière contextuelle
                responses = [
                    f"Je suis là {message.author.mention} ! {get_emoji('wave')}",
                    f"Oui {message.author.mention} ? {get_emoji('thinking')}",
                    f"Que puis-je faire pour toi {message.author.mention} ? {get_emoji('help')}"
                ]
                await message.channel.send(random.choice(responses))
        
        # === RÉACTIONS AUTOMATIQUES ===
        for mot, reactions in self.reaction_triggers.items():
            if mot in contenu and random.random() < 0.4:  # 40% de chance
                await message.add_reaction(random.choice(reactions))
                # Parfois ajouter une deuxième réaction
                if random.random() < 0.2:  # 20% de chance
                    await asyncio.sleep(0.5)
                    await message.add_reaction(random.choice(reactions))
                break  # Une seule série de réactions par message
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Événement quand un membre rejoint"""
        # Message de bienvenue avec emojis
        canal_bienvenue = discord.utils.get(member.guild.text_channels, name="bienvenue")
        
        if not canal_bienvenue:
            # Chercher un canal avec "bienvenue" dans le nom
            for channel in member.guild.text_channels:
                if "bienvenue" in channel.name.lower():
                    canal_bienvenue = channel
                    break
        
        if canal_bienvenue:
            # Émojis de bienvenue
            welcome_emojis = ["🎉", "👋", "✨", "🌟", "🎊", "🥳"]
            welcome_emoji = random.choice(welcome_emojis)
            
            embed = discord.Embed(
                title=f"{welcome_emoji} Nouveau membre !",
                description=format_with_emojis(
                    f"Bienvenue {member.mention} sur **{member.guild.name}** !"
                ),
                color=discord.Color.green(),
                timestamp=datetime.datetime.now()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.add_field(
                name=f"{get_emoji('calendar')} Compte créé", 
                value=member.created_at.strftime("%d/%m/%Y"), 
                inline=True
            )
            embed.add_field(
                name=f"{get_emoji('chart')} Membre n°", 
                value=str(member.guild.member_count), 
                inline=True
            )
            embed.set_footer(text=f"ID: {member.id} • {get_emoji('confetti')}")
            
            await canal_bienvenue.send(embed=embed)
            
            # Réaction de bienvenue
            try:
                welcome_message = await canal_bienvenue.send(f"{member.mention} 👋")
                await welcome_message.add_reaction("👋")
                await welcome_message.add_reaction("🎉")
                await welcome_message.add_reaction("✨")
            except:
                pass
        
        # Attribution des auto-rôles
        if member.guild.id in storage.auto_roles:
            for role_id in storage.auto_roles[member.guild.id]:
                role = member.guild.get_role(role_id)
                if role:
                    try:
                        await member.add_roles(role)
                    except discord.Forbidden:
                        print(f"Impossible d'ajouter le rôle {role.name} à {member.name}")
                    except Exception as e:
                        print(f"Erreur avec auto-rôle: {e}")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Événement quand un membre quitte"""
        canal_logs = discord.utils.get(member.guild.text_channels, name="logs")
        
        if not canal_logs:
            for channel in member.guild.text_channels:
                if "log" in channel.name.lower():
                    canal_logs = channel
                    break
        
        if canal_logs:
            # Émojis d'au revoir
            goodbye_emojis = ["👋", "😢", "💔", "🚪"]
            goodbye_emoji = random.choice(goodbye_emojis)
            
            embed = discord.Embed(
                title=f"{goodbye_emoji} Membre parti",
                description=format_with_emojis(
                    f"**{member.name}** a quitté le serveur"
                ),
                color=discord.Color.red(),
                timestamp=datetime.datetime.now()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.add_field(
                name=f"{get_emoji('id')} ID", 
                value=str(member.id), 
                inline=True
            )
            embed.add_field(
                name=f"{get_emoji('calendar')} Compte créé", 
                value=member.created_at.strftime("%d/%m/%Y"), 
                inline=True
            )
            embed.set_footer(text=f"{get_emoji('wave')} Au revoir...")
            
            await canal_logs.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """Événement quand un message est supprimé"""
        if message.author.bot:
            return
        
        canal_logs = discord.utils.get(message.guild.text_channels, name="logs")
        
        if not canal_logs:
            for channel in message.guild.text_channels:
                if "log" in channel.name.lower():
                    canal_logs = channel
                    break
        
        if canal_logs:
            embed = discord.Embed(
                title=f"{get_emoji('trash')} Message supprimé",
                color=discord.Color.orange(),
                timestamp=datetime.datetime.now()
            )
            embed.add_field(
                name=f"{get_emoji('person')} Auteur", 
                value=message.author.mention, 
                inline=True
            )
            embed.add_field(
                name=f"{get_emoji('speech')} Salon", 
                value=message.channel.mention, 
                inline=True
            )
            
            if message.content:
                content_preview = message.content[:500] + "..." if len(message.content) > 500 else message.content
                embed.add_field(
                    name=f"{get_emoji('note')} Contenu", 
                    value=content_preview, 
                    inline=False
                )
            
            if message.attachments:
                embed.add_field(
                    name=f"{get_emoji('paperclip')} Pièces jointes", 
                    value=f"{len(message.attachments)} fichier(s)", 
                    inline=True
                )
            
            await canal_logs.send(embed=embed)

async def setup(bot):
    await bot.add_cog(EventsHandler(bot))