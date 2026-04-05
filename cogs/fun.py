# Partie du bot discord pour gérer les commandes fun comme lancer un dé, pile ou face, boule magique, sondage et emoji aléatoire.

import discord
from discord import app_commands
from discord.ext import commands
import random
from utils import create_embed, get_emoji, get_random_emoji, format_with_emojis, emojize_text

class Fun(commands.Cog):
    """Commandes fun"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="de", description="Lance un dé")
    @app_commands.describe(faces="Nombre de faces du dé (par défaut 6)")
    async def de(self, interaction: discord.Interaction, faces: app_commands.Range[int, 2, 1000] = 6):
        """Lancer un dé"""
        resultat = random.randint(1, faces)
        
        # Émoji selon le résultat avec plus de variété
        if resultat == 1:
            emoji_result = get_emoji("skull") or "💀"  # Échec critique
        elif resultat == faces:
            emoji_result = get_emoji("tada") or "🎉"  # Succès critique
        elif resultat <= faces * 0.2:
            emoji_result = get_emoji("thumbsdown") or "👎"
        elif resultat >= faces * 0.8:
            emoji_result = get_emoji("thumbsup") or "👍"
        elif resultat <= faces * 0.4:
            emoji_result = get_emoji("neutral") or "😐"
        elif resultat >= faces * 0.6:
            emoji_result = get_emoji("smile") or "😊"
        else:
            emoji_result = get_emoji("dice") or "🎲"
        
        # Ajouter un message amusant selon le résultat
        messages = {
            1: "Ouch... c'est un échec critique !",
            faces: "Wow ! Succès critique !",
        }
        
        message_special = messages.get(resultat, "")
        
        embed = create_embed(
            title=f"{emoji_result} Lancer de dé",
            description=format_with_emojis(
                f"{interaction.user.mention} a lancé un dé à **{faces}** faces\n"
                f"{message_special}"
            ),
            color=discord.Color.gold(),
            fields=[
                (f"{get_emoji('dart')} Résultat", f"**{resultat}**", False)
                # (f"{get_emoji('chart')} Pourcentage", f"**{round((resultat/faces)*100, 1)}%** de la valeur max", True)
            ]
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="pile_ou_face", description="Joue à pile ou face")
    async def pile_ou_face(self, interaction: discord.Interaction):
        """Jouer à pile ou face"""
        resultat = random.choice(["Pile", "Face"])
        emoji_coin = get_emoji("coin") or "🪙"
        
        # Animation de la pièce qui tourne
        coin_states = ["🔄", "⏳", "⌛", emoji_coin]
        
        embed = create_embed(
            title=f"{get_emoji('magic')} La pièce tourne...",
            description="La pièce est en l'air !",
            color=discord.Color.yellow()
        )
        
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        
        # Animation
        for state in coin_states:
            embed.title = f"{state} La pièce tourne..."
            await message.edit(embed=embed)
            import asyncio
            await asyncio.sleep(0.5)
        
        # Résultat final
        result_emoji = "👑" if resultat == "Pile" else "👸"  # Différents emojis pour pile/face
        
        embed_final = create_embed(
            title=f"{emoji_coin} Pile ou Face",
            description=format_with_emojis(
                f"**Résultat : {result_emoji} {resultat} !**\n\n"
                f"La pièce est tombée sur... **{resultat}** !"
            ),
            color=discord.Color.gold(),
            thumbnail="https://www.joffeassocies.com/wp-content/uploads/2023/03/2399729-illustration-d-un-podium-et-la-coupe-d-or-vectoriel.jpg"
            # https://cdn-icons-png.flaticon.com/512/2173/2173475.png : ancienne image 
        )
        
        await message.edit(embed=embed_final)
    
    @app_commands.command(name="boule_magique", description="Pose une question à la boule magique")
    @app_commands.describe(question="Ta question")
    async def boule_magique(self, interaction: discord.Interaction, question: str):
        """Boule magique"""
        reponses = [
            {"reponse": "Oui, absolument !", "type": "positive", "emoji": "✅"},
            {"reponse": "Sans aucun doute !", "type": "positive", "emoji": "✨"},
            {"reponse": "Très certainement !", "type": "positive", "emoji": "🌟"},
            {"reponse": "Les signes pointent vers oui.", "type": "positive", "emoji": "🔮"},
            {"reponse": "Je pense que oui.", "type": "positive", "emoji": "👍"},
            {"reponse": "Peut-être...", "type": "neutral", "emoji": "🤔"},
            {"reponse": "Je ne peux pas prédire maintenant.", "type": "neutral", "emoji": "🎭"},
            {"reponse": "Demande à nouveau plus tard.", "type": "neutral", "emoji": "⏰"},
            {"reponse": "Concentre-toi et demande à nouveau.", "type": "neutral", "emoji": "🧘"},
            {"reponse": "Ne compte pas dessus.", "type": "negative", "emoji": "👎"},
            {"reponse": "Ma réponse est non.", "type": "negative", "emoji": "❌"},
            {"reponse": "Non, certainement pas.", "type": "negative", "emoji": "💀"},
            {"reponse": "Très douteux.", "type": "negative", "emoji": "👻"},
            {"reponse": "C'est peu probable.", "type": "negative", "emoji": "☁️"},
            {"reponse": "Les étoiles ne sont pas alignées.", "type": "negative", "emoji": "🌌"},
            {"reponse": "La réponse est écrite dans les étoiles... mais je ne sais pas lire.", "type": "funny", "emoji": "🤪"},
            {"reponse": "Demande à ton chat, il sait tout.", "type": "funny", "emoji": "🐱"},
            {"reponse": "42. C'est toujours la réponse.", "type": "funny", "emoji": "🤖"},
            {"reponse": "Je vois du fromage dans ton futur... attend, c'est ma vision.", "type": "funny", "emoji": "🧀"},
        ]
        
        reponse_choisie = random.choice(reponses)
        
        # Couleur selon le type de réponse
        color_map = {
            "positive": discord.Color.green(),
            "negative": discord.Color.red(),
            "neutral": discord.Color.orange(),
            "funny": discord.Color.purple()
        }
        
        color = color_map.get(reponse_choisie["type"], discord.Color.blue())
        emoji_reponse = reponse_choisie.get("emoji", "🔮")
        
        # Animation de la boule qui tourne
        embed_loading = create_embed(
            title="🔮 La boule magique réfléchit...",
            description="La boule se trouble...",
            color=discord.Color.dark_purple(),
            thumbnail="https://img.freepik.com/vecteurs-libre/boule-cristal-magique-fond-blanc_1308-79447.jpg?semt=ais_se_enriched&w=740&q=80"
        ) # https://cdn-icons-png.flaticon.com/512/3522/3522665.png : lien de l'ancienne image
        
        await interaction.response.send_message(embed=embed_loading)
        message = await interaction.original_response()
        
        # Animation
        crystal_emojis = ["💎", "🔮", "✨", "🌟", "💫"]
        for crystal in crystal_emojis:
            embed_loading.title = f"{crystal} La boule magique réfléchit..."
            await message.edit(embed=embed_loading)
            import asyncio
            await asyncio.sleep(0.3)
        
        # CORRECTION ICI : Utiliser directement "Question" et "Réponse" sans get_emoji
        embed = create_embed(
            title=f"{emoji_reponse} Boule Magique",
            color=color,
            fields=[
                ("Question", question, False),
                ("Réponse", f"**{reponse_choisie['reponse']}**", False)
            ],
            thumbnail="https://img.freepik.com/vecteurs-libre/boule-cristal-magique-fond-blanc_1308-79447.jpg?semt=ais_se_enriched&w=740&q=80"
        )
        
        # Ajouter une note amusante pour les réponses drôles
        if reponse_choisie["type"] == "funny":
            embed.set_footer(text="✨ La boule magique est d'humeur facétieuse aujourd'hui !")
        
        await message.edit(embed=embed)
    
    @app_commands.command(name="sondage", description="Créer un sondage")
    @app_commands.describe(
        question="La question du sondage",
        option1="Première option",
        option2="Deuxième option",
        option3="Troisième option (optionnel)",
        option4="Quatrième option (optionnel)",
        option5="Cinquième option (optionnel)"
    )
    async def sondage(self, interaction: discord.Interaction, question: str, option1: str, option2: str, option3: str = None, option4: str = None, option5: str = None):
        """Créer un sondage"""
        # Émojis de sondage plus variés
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "🇦", "🇧", "🇨", "🇩", "🇪"]
        options = [option1, option2]
        
        if option3:
            options.append(option3)
        if option4:
            options.append(option4)
        if option5:
            options.append(option5)
        
        description_lines = []
        for i, option in enumerate(options, 1):
            emoji = emojis[i-1] if i-1 < len(emojis) else f"{i}."
            description_lines.append(f"{emoji} **{option}**")
        
        embed = create_embed(
            title=f"{get_emoji('chart')} Sondage : {question}",
            description="\n".join(description_lines),
            color=discord.Color.purple(),
            footer=f"Sondage créé par {interaction.user.display_name} {get_emoji('pencil')}",
            thumbnail=interaction.user.avatar.url if interaction.user.avatar else None
        )
        
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        
        # Ajouter les réactions avec des emojis améliorés
        for i in range(len(options)):
            reaction_emoji = emojis[i] if i < len(emojis) else f"{i+1}\ufe0f\u20e3"
            await message.add_reaction(reaction_emoji)
    
    @app_commands.command(name="emoji_aleatoire", description="Obtenir un emoji aléatoire")
    @app_commands.describe(categorie="Catégorie d'emoji")
    @app_commands.choices(categorie=[
        app_commands.Choice(name="😊 Visages", value="faces"),
        app_commands.Choice(name="🐾 Animaux", value="animals"),
        app_commands.Choice(name="🍔 Nourriture", value="food"),
        app_commands.Choice(name="⚽ Sports", value="sports"),
        app_commands.Choice(name="🚗 Transports", value="transport"),
        app_commands.Choice(name="🎨 Créatif", value="creative"),
        app_commands.Choice(name="🎉 Fête", value="party"),
        app_commands.Choice(name="🌍 Nature", value="nature"),
    ])
    async def emoji_aleatoire(self, interaction: discord.Interaction, categorie: str = None):
        """Obtenir un emoji aléatoire"""
        categories_emojis = {
            "faces": ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "🥲", "☺️", "😊", "😇", "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚", "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🥸", "🤩", "🥳", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹️", "😣", "😖", "😫", "😩", "🥺", "😢", "😭", "😤", "😠", "😡", "🤬", "🤯", "😳", "🥵", "🥶", "😱", "😨", "😰", "😥", "😓", "🤗", "🤔", "🤭", "🤫", "🤥", "😶", "😐", "😑", "😬", "🙄", "😯", "😦", "😧", "😮", "😲", "🥱", "😴", "🤤", "😪", "😵", "🤐", "🥴", "🤢", "🤮", "🤧", "😷", "🤒", "🤕"],
            "animals": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐽", "🐸", "🐵", "🙈", "🙉", "🙊", "🐒", "🐔", "🐧", "🐦", "🐤", "🐣", "🐥", "🦆", "🦅", "🦉", "🦇", "🐺", "🐗", "🐴", "🦄", "🐝", "🪱", "🐛", "🦋", "🐌", "🐞", "🐜", "🪰", "🪲", "🪳", "🦟", "🦗", "🕷️", "🦂", "🐢", "🐍", "🦎", "🦖", "🦕", "🐙", "🦑", "🦐", "🦞", "🦀", "🐡", "🐠", "🐟", "🐬", "🐳", "🐋", "🦈", "🐊", "🐅", "🐆", "🦓", "🦍", "🦧", "🦣", "🐘", "🦛", "🦏", "🐪", "🐫", "🦒", "🦘", "🦬", "🐃", "🐂", "🐄", "🐎", "🐖", "🐏", "🐑", "🦙", "🐐", "🦌", "🐕", "🐩", "🦮", "🐕‍🦺", "🐈", "🐈‍⬛", "🪶", "🐓", "🦃", "🦤", "🦚", "🦜", "🦢", "🦩", "🕊️", "🐇", "🦝", "🦨", "🦡", "🦫", "🦦", "🦥", "🐁", "🐀", "🐿️", "🦔"],
            "food": ["🍏", "🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🫐", "🍈", "🍒", "🍑", "🥭", "🍍", "🥥", "🥝", "🍅", "🍆", "🥑", "🥦", "🥬", "🥒", "🌶️", "🫑", "🌽", "🥕", "🫒", "🧄", "🧅", "🥔", "🍠", "🥐", "🥯", "🍞", "🥖", "🥨", "🧀", "🥚", "🍳", "🧈", "🥞", "🧇", "🥓", "🥩", "🍗", "🍖", "🦴", "🌭", "🍔", "🍟", "🍕", "🫓", "🥪", "🥙", "🧆", "🌮", "🌯", "🫔", "🥗", "🥘", "🫕", "🥫", "🍝", "🍜", "🍲", "🍛", "🍣", "🍱", "🥟", "🦪", "🍤", "🍙", "🍚", "🍘", "🍥", "🥠", "🥮", "🍢", "🍡", "🍧", "🍨", "🍦", "🥧", "🧁", "🍰", "🎂", "🍮", "🍭", "🍬", "🍫", "🍿", "🍩", "🍪", "🌰", "🥜", "🫘", "🍯", "🥛", "🍼", "🫖", "☕", "🍵", "🧃", "🥤", "🧋", "🍶", "🍺", "🍻", "🥂", "🍷", "🥃", "🍸", "🍹", "🧉", "🍾", "🧊", "🥄", "🍴", "🍽️", "🥣", "🥡", "🥢", "🧂"],
            "sports": ["⚽", "⚾", "🥎", "🏀", "🏐", "🏈", "🏉", "🎾", "🥏", "🎳", "🏏", "🏑", "🏒", "🥍", "🏓", "🏸", "🥊", "🥋", "🥅", "⛳", "⛸️", "🎣", "🤿", "🥌", "🎿", "🛷", "🛼", "🛹", "🛶", "🪂", "🏹", "🎯", "🥏", "🪁", "🏒", "🏑", "🥍", "🏏", "🥊", "🥋", "🎽", "🛹", "🛷", "⛷️", "🏂", "🏋️", "🤼", "🤸", "🤺", "🤾", "🏌️", "🏇", "🧘", "🏄", "🏊", "🤽", "🚣", "🧗", "🚴", "🚵", "🤹", "🤸‍♀️", "🤸‍♂️"],
            "transport": ["🚗", "🚕", "🚙", "🚌", "🚎", "🏎️", "🚓", "🚑", "🚒", "🚐", "🛻", "🚚", "🚛", "🚜", "🛵", "🏍️", "🛺", "🚔", "🚍", "🚘", "🚖", "🚡", "🚠", "🚟", "🚃", "🚋", "🚞", "🚝", "🚄", "🚅", "🚈", "🚂", "🚆", "🚇", "🚊", "🚉", "✈️", "🛫", "🛬", "🛩️", "💺", "🛰️", "🚀", "🛸", "🚁", "🛶", "⛵", "🛥️", "🚤", "🛳️", "⛴️", "🚢", "⚓", "🛟", "🚧", "⛽", "🚏", "🚦", "🚥", "🗺️", "🗿", "🛂", "🛃", "🛄", "🛅"],
            "creative": ["🎨", "🎭", "🎬", "🎤", "🎧", "🎼", "🎹", "🥁", "🪘", "🎷", "🎺", "🪗", "🎸", "🪕", "🎻", "🪈", "🎲", "♟️", "🎯", "🎳", "🎮", "🎰", "🧩", "🎪", "🤹", "🎭", "🩰", "🎨", "✏️", "🖌️", "🖍️", "📝", "📚", "📖", "🔖", "🧾", "📄", "📃", "📜", "📑", "🎫", "💰", "🪙", "💎", "💍", "👑", "🎀", "🎁", "🎈", "🎉", "🎊", "🎂", "🍰", "🧁", "🍭", "🍬", "🍫"],
            "party": ["🎉", "🎊", "🎈", "🎁", "🎂", "🍾", "🥂", "🍻", "🍸", "🍹", "🧉", "🥳", "🤩", "🥰", "😍", "😎", "🤪", "🕺", "💃", "👯", "🎭", "🎪", "🎨", "🎤", "🎧", "🎼", "🎹", "🥁", "🎷", "🎺", "🎸", "🎻", "🪕", "🎮", "🎲", "♟️", "🎯", "🎳", "🎰", "🎪", "🤹", "🎭", "🩰", "🎨"],
            "nature": ["🌱", "🌲", "🌳", "🌴", "🌵", "🌾", "🌿", "☘️", "🍀", "🍁", "🍂", "🍃", "🍄", "🌰", "🪵", "🌻", "🌼", "🌸", "🌺", "🌹", "🥀", "🌷", "💐", "🪴", "🎍", "🎋", "🍃", "🍂", "🍁", "🍄", "🌰", "🪵", "🌻", "🌼", "🌸", "🌺", "🌹", "🥀", "🌷", "💐", "🪴", "🎍", "🎋"]
        }
        
        if categorie and categorie in categories_emojis:
            emoji_choisi = random.choice(categories_emojis[categorie])
            categorie_nom = {
                "faces": "Visages",
                "animals": "Animaux",
                "food": "Nourriture",
                "sports": "Sports",
                "transport": "Transports",
                "creative": "Créatif",
                "party": "Fête",
                "nature": "Nature"
            }.get(categorie, categorie)
        else:
            # Tous les emojis mélangés
            all_emojis = []
            for cat in categories_emojis.values():
                all_emojis.extend(cat)
            emoji_choisi = random.choice(all_emojis)
            categorie_nom = "Aléatoire"
        
        embed = create_embed(
            title=f"{get_emoji('sparkles')} Emoji Aléatoire",
            description=f"**{emoji_choisi}**",
            color=discord.Color.random()
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))