'''Partie des utilitaires pour le bot Discord Guess Who's Back, incluant 
la création d'embeds, le calcul de niveaux, la vérification des permissions, 
la gestion des dates et heures, ainsi que les fonctions liées aux emojis.'''

import discord
import datetime
import math
import emoji

def create_embed(title=None, description=None, color=None, fields=None, footer=None, thumbnail=None, image=None, author=None, timestamp=None):
    """Crée un embed Discord proprement formaté"""
    embed = discord.Embed()
    
    if title:
        embed.title = title
    if description:
        embed.description = description
    if color:
        embed.color = color
    if timestamp:
        embed.timestamp = timestamp
    
    if fields:
        for field in fields:
            if len(field) == 3:
                name, value, inline = field
                embed.add_field(name=name, value=value, inline=inline)
            elif len(field) == 2:
                name, value = field
                embed.add_field(name=name, value=value, inline=False)
    
    if footer:
        embed.set_footer(text=footer)
    
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    
    if image:
        embed.set_image(url=image)
    
    if author:
        if isinstance(author, discord.User) or isinstance(author, discord.Member):
            embed.set_author(name=author.display_name, icon_url=author.avatar.url if author.avatar else None)
        elif isinstance(author, dict):
            embed.set_author(name=author.get("name"), icon_url=author.get("icon_url"))
        elif isinstance(author, str):
            embed.set_author(name=author)
    
    return embed

def calculer_niveau(xp):
    """Calcule le niveau à partir de l'XP"""
    if xp <= 0:
        return 1
    return int(math.sqrt(xp / 100)) + 1

async def verifier_permissions(interaction, permission):
    """Vérifie si l'utilisateur a la permission requise"""
    # Permissions Discord correspondantes
    permissions_map = {
        "manage_guild": "gérer_le_serveur",
        "manage_roles": "gérer_les_rôles",
        "manage_channels": "gérer_les_salons",
        "manage_messages": "gérer_les_messages",
        "manage_nicknames": "gérer_les_surnoms",
        "moderate_members": "modérer_les_membres",
        "kick_members": "expulser_des_membres",
        "ban_members": "bannir_des_membres",
        "administrator": "administrateur"
    }
    
    permission_fr = permissions_map.get(permission, permission)
    
    if not getattr(interaction.user.guild_permissions, permission, False):
        await interaction.response.send_message(
            f"❌ Vous n'avez pas la permission de faire cela !\n"
            f"Permission requise : `{permission_fr.replace('_', ' ').title()}`",
            ephemeral=True
        )
        return False
    return True

def calculate_days_difference(date_time):
    """Calcule la différence en jours de manière sécurisée"""
    if not date_time:
        return 0
    
    now = datetime.datetime.now(datetime.timezone.utc)
    
    # S'assurer que la date a un fuseau horaire
    if date_time.tzinfo is None:
        # Si la date est naïve, on suppose UTC
        naive_time = date_time
    else:
        # Convertir en UTC
        naive_time = date_time.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    
    # Convertir maintenant en naïve aussi pour la comparaison
    now_naive = now.replace(tzinfo=None)
    
    # Calculer la différence
    difference = now_naive - naive_time
    return difference.days

def format_datetime(dt):
    """Formate une date de manière sécurisée"""
    if not dt:
        return "Inconnu"
    
    try:
        # Si c'est un datetime avec fuseau horaire
        if dt.tzinfo is not None:
            # Convertir en fuseau horaire local (Europe/Paris)
            try:
                import pytz
                local_tz = pytz.timezone('Europe/Paris')
                local_dt = dt.astimezone(local_tz)
                return local_dt.strftime("%d/%m/%Y à %H:%M")
            except:
                # Fallback sans pytz
                local_dt = dt.astimezone(datetime.timezone(datetime.timedelta(hours=1)))
                return local_dt.strftime("%d/%m/%Y à %H:%M")
        else:
            # Datetime naïf
            return dt.strftime("%d/%m/%Y à %H:%M")
    except Exception:
        # Fallback simple
        try:
            return dt.strftime("%d/%m/%Y")
        except:
            return "Date inconnue"

def format_status(status):
    """Formate le statut d'un membre"""
    status_map = {
        discord.Status.online: "🟢 En ligne",
        discord.Status.idle: "🟡 Inactif",
        discord.Status.dnd: "🔴 Ne pas déranger",
        discord.Status.offline: "⚫ Hors ligne",
        discord.Status.invisible: "👻 Invisible"
    }
    return status_map.get(status, str(status).title())

def safe_time_difference(date1, date2=None):
    """
    Calcule la différence entre deux dates de manière sécurisée
    pour éviter les erreurs de fuseaux horaires.
    """
    if date2 is None:
        date2 = datetime.datetime.now(datetime.timezone.utc)
    
    # S'assurer que les deux dates ont un fuseau horaire
    if date1.tzinfo is None:
        date1 = date1.replace(tzinfo=datetime.timezone.utc)
    if date2.tzinfo is None:
        date2 = date2.replace(tzinfo=datetime.timezone.utc)
    
    # Calculer la différence
    diff = date2 - date1
    
    # Extraire les composants
    jours = diff.days
    heures, reste = divmod(diff.seconds, 3600)
    minutes, secondes = divmod(reste, 60)
    
    return jours, heures, minutes

def format_duration(days, hours=0, minutes=0):
    """Formate une durée en chaîne lisible"""
    parts = []
    
    if days > 0:
        parts.append(f"{days} jour{'s' if days > 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} heure{'s' if hours > 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    
    if not parts:
        return "quelques instants"
    
    return ", ".join(parts)

def discord_timestamp(dt, style='R'):
    """
    Crée un timestamp Discord formaté.
    
    Styles:
        't' - 16:20
        'T' - 16:20:30
        'd' - 20/04/2021
        'D' - 20 avril 2021
        'f' - 20 avril 2021 16:20
        'F' - lundi 20 avril 2021 16:20
        'R' - il y a 2 heures (relative)
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    
    timestamp = int(dt.timestamp())
    return f"<t:{timestamp}:{style}>"

# FONCTIONS POUR LES EMOJIS 

def emojize_text(text):
    """Convertit les codes d'emoji textuels en emojis réels"""
    return emoji.emojize(text, language='alias')

def get_emoji(emoji_name):
    """Récupère un emoji par son nom"""
    emoji_map = {
        # Émojis de réaction
        "check": "✅",
        "cross": "❌",
        "warning": "⚠️",
        "info": "ℹ️",
        "star": "⭐",
        "fire": "🔥",
        "heart": "❤️",
        "tada": "🎉",
        "confetti": "🎊",
        "dice": "🎲",
        "coin": "🪙",
        "ball": "🔮",
        "magic": "✨",
        "crystal": "💎",
        "medal1": "🥇",
        "medal2": "🥈",
        "medal3": "🥉",
        "trophy": "🏆",
        "crown": "👑",
        
        # Émojis de catégories
        "moderation": "🛡️",
        "ticket": "🎫",
        "utility": "🔧",
        "role": "🎭",
        "stats": "📊",
        "event": "🎉",
        "content": "📝",
        "creative": "🎨",
        "info": "ℹ️",
        "fun": "🎮",
        "help": "📖",
        "invite": "🔗",
        "test": "🧪",
        
        # Émojis de statut
        "online": "🟢",
        "idle": "🟡",
        "dnd": "🔴",
        "offline": "⚫",
        "invisible": "👻",
        
        # Émojis météo
        "sun": "☀️",
        "cloud": "☁️",
        "rain": "🌧️",
        "snow": "❄️",
        "storm": "⛈️",
        "fog": "🌫️",
        "wind": "💨",
        "thermometer": "🌡️",
        "umbrella": "☔",
        
        # Émojis pour boule magique et autres
        "speech": "💬",
        "magic": "✨",
        "question": "❓",
        "answer": "💭",
        "clipboard": "📋",
        "chart": "📊",
        "dart": "🎯",
        "pencil": "✏️",
        "thinking": "🤔",
        "robot": "🤖",
        "salute": "🫡",
        "sparkles": "✨",
        "moon": "🌙",
        "sleep": "😴",
        "wave": "👋",
        "smile": "😊",
        
        # Émojis divers
        "calendar": "📅",
        "clock": "⏰",
        "birthday": "🎂",
        "gift": "🎁",
        "note": "📝",
        "book": "📚",
        "microphone": "🎤",
        "headphones": "🎧",
        "camera": "📷",
        "video": "📹",
        "music": "🎵",
        "game": "🎮",
        "puzzle": "🧩",
        "alien": "👾",
        "ghost": "👻",
        "poo": "💩",
        
        # Émojis de personnes
        "clap": "👏",
        "ok": "👌",
        "thumbsup": "👍",
        "thumbsdown": "👎",
        "point_up": "☝️",
        "point_down": "👇",
        "point_left": "👈",
        "point_right": "👉",
        "raised_hand": "✋",
        "vulcan": "🖖",
        "metal": "🤘",
        "callme": "🤙",
        "handshake": "🤝",
        "muscle": "💪",
        "brain": "🧠",
        "bone": "🦴",
        "tooth": "🦷",
        "eye": "👁️",
        "tongue": "👅",
        "nose": "👃",
        "ear": "👂",
        "foot": "🦶",
        
        # Émojis d'objets
        "paperclip": "📎",
        "trash": "🗑️",
        "id": "🆔",
        "person": "👤",
    }
    
    # Si l'emoji n'est pas trouvé, retourner un point d'interrogation
    return emoji_map.get(emoji_name, "❓")

def create_emoji_reaction(emoji_name):
    """Crée une réaction d'emoji sécurisée"""
    emoji_char = get_emoji(emoji_name)
    
    # S'assurer que l'emoji est valide pour Discord
    if emoji_char and len(emoji_char) <= 4:  # Les emojis standards font 1-4 caractères
        return emoji_char
    return "❓"  # Fallback

def get_random_emoji(category=None):
    """Récupère un emoji aléatoire d'une catégorie"""
    categories = {
        "positive": ["✅", "👍", "👌", "🎉", "✨", "🌟", "💫", "🔥", "💯", "🥳"],
        "negative": ["❌", "👎", "💀", "☠️", "💔", "😢", "😭", "😡", "🤬", "👿"],
        "neutral": ["🤔", "😐", "😶", "🫥", "😑", "😴", "🥱", "😪", "💤", "🫨"],
        "fun": ["🎲", "🃏", "🎯", "🎮", "👾", "🕹️", "🎪", "🎭", "🎨", "🎤"],
        "nature": ["🌱", "🌿", "🍃", "🍀", "🌻", "🌺", "🌸", "🌼", "🌹", "💐"],
        "food": ["🍕", "🍔", "🌭", "🥪", "🌮", "🌯", "🍣", "🍜", "🍦", "🍩"],
        "animals": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯"],
    }
    
    if category and category in categories:
        import random
        return random.choice(categories[category])
    return "🎲"

def format_with_emojis(text):
    """Formate un texte avec des emojis automatiques"""
    # Mapping de mots vers emojis
    emoji_mapping = {
        r'\bbonjour\b': '👋',
        r'\bsalut\b': '👋',
        r'\bcoucou\b': '👋',
        r'\bmerci\b': '🙏',
        r'\bde rien\b': '😊',
        r'\bstp\b': '🙏',
        r'\bsvp\b': '🙏',
        r'\bhelp\b': '🆘',
        r'\baide\b': '❓',
        r'\bwarning\b': '⚠️',
        r'\berreur\b': '❌',
        r'\bsuccès\b': '✅',
        r'\bgagné\b': '🏆',
        r'\bperdu\b': '💀',
        r'\bfélicitations\b': '🎉',
        r'\banniversaire\b': '🎂',
        r'\bjoyeux\b': '🥳',
        r'\btemps\b': '⏰',
        r'\bdate\b': '📅',
        r'\bjour\b': '☀️',
        r'\bnuit\b': '🌙',
        r'\bmétéo\b': '🌤️',
        r'\bsoleil\b': '☀️',
        r'\bpluie\b': '🌧️',
        r'\bneige\b': '❄️',
        r'\bvent\b': '💨',
        r'\bnote\b': '📝',
        r'\bidée\b': '💡',
        r'\bsuggestion\b': '💭',
        r'\bquestion\b': '❓',
        r'\bréponse\b': '💬',
        r'\bsecret\b': '🤫',
        r'\bmystère\b': '🕵️',
        r'\bmagie\b': '✨',
        r'\bsort\b': '🪄',
        r'\bpouvoir\b': '⚡',
        r'\bforce\b': '💪',
        r'\bsanté\b': '❤️',
        r'\bcoeur\b': '❤️',
        r'\bamour\b': '💖',
        r'\bamitié\b': '🤝',
        r'\bfamille\b': '👨‍👩‍👧‍👦',
        r'\bami\b': '👫',
        r'\bchat\b': '🐱',
        r'\bchien\b': '🐶',
        r'\boiseau\b': '🐦',
        r'\bpoisson\b': '🐠',
        r'\bpizza\b': '🍕',
        r'\bburger\b': '🍔',
        r'\bfrites\b': '🍟',
        r'\bboisson\b': '🥤',
        r'\bcafé\b': '☕',
        r'\bthé\b': '🍵',
        r'\bjeu\b': '🎮',
        r'\bmusique\b': '🎵',
        r'\bdanse\b': '💃',
        r'\bchante\b': '🎤',
        r'\bfilm\b': '🎬',
        r'\blivre\b': '📚',
        r'\bécrit\b': '✍️',
        r'\blis\b': '📖',
        r'\bapprend\b': '🧠',
        r'\bécole\b': '🏫',
        r'\btravail\b': '💼',
        r'\bargent\b': '💰',
        r'\brêve\b': '💭',
        r'\bespoir\b': '🌟',
        r'\bvoyage\b': '✈️',
        r'\bmaison\b': '🏠',
        r'\bville\b': '🏙️',
        r'\bcampagne\b': '🌳',
        r'\bmer\b': '🌊',
        r'\bmontagne\b': '⛰️',
        r'\bforêt\b': '🌲',
        r'\bfleur\b': '🌸',
        r'\barbre\b': '🌳',
        r'\bplante\b': '🌿',
        r'\bjardin\b': '🌻',
        r'\bsport\b': '⚽',
        r'\bcourse\b': '🏃',
        r'\bnage\b': '🏊',
        r'\byoga\b': '🧘',
        r'\bmedite\b': '☮️',
        r'\bcalme\b': '😌',
        r'\bstress\b': '😫',
        r'\bfatigue\b': '😴',
        r'\bmalade\b': '🤒',
        r'\bsanté\b': '🏥',
        r'\bdocteur\b': '👨‍⚕️',
        r'\bhôpital\b': '🏥',
        r'\bmédicament\b': '💊',
        r'\bvoiture\b': '🚗',
        r'\bvélo\b': '🚲',
        r'\btrain\b': '🚆',
        r'\bavion\b': '✈️',
        r'\bbateau\b': '🚢',
        r'\busine\b': '🏭',
        r'\bbureau\b': '🏢',
        r'\bmagasin\b': '🏪',
        r'\brestaurant\b': '🍽️',
        r'\bcafétéria\b': '☕',
        r'\bcinéma\b': '🎬',
        r'\bthéâtre\b': '🎭',
        r'\bmusée\b': '🏛️',
        r'\bparc\b': '🏞️',
        r'\bplage\b': '🏖️',
        r'\bpiscine\b': '🏊',
    }
    
    import re
    for pattern, emoji_char in emoji_mapping.items():
        text = re.sub(pattern, lambda m: f"{m.group(0)} {emoji_char}", text, flags=re.IGNORECASE)
    
    return text
