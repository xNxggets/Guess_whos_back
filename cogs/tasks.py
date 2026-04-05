# Partie du bot gérant les tâches périodiques telles que les rappels, anniversaires, giveaways et messages programmés.

import discord
from discord.ext import commands, tasks
import datetime
import random
import asyncio
from data.storage import storage

class Tasks(commands.Cog):
    """Tâches périodiques"""
    
    def __init__(self, bot):
        self.bot = bot
        self.verifier_rappels.start()
        self.verifier_anniversaires.start()
        self.verifier_giveaways.start()
        self.envoyer_messages_programmes.start()
    
    def cog_unload(self):
        """Arrêter les tâches lors du déchargement du cog"""
        self.verifier_rappels.cancel()
        self.verifier_anniversaires.cancel()
        self.verifier_giveaways.cancel()
        self.envoyer_messages_programmes.cancel()
    
    @tasks.loop(minutes=1)
    async def verifier_rappels(self):
        """Vérifier les rappels"""
        maintenant = datetime.datetime.now()
        rappels_a_envoyer = []
        
        # Trouver les rappels à envoyer
        for rappel in storage.rappels:
            if isinstance(rappel["time"], str):
                try:
                    rappel["time"] = datetime.datetime.fromisoformat(rappel["time"])
                except:
                    continue
            
            if rappel["time"] <= maintenant:
                rappels_a_envoyer.append(rappel)
        
        # Envoyer les rappels
        for rappel in rappels_a_envoyer:
            try:
                canal = self.bot.get_channel(rappel["channel_id"])
                utilisateur = self.bot.get_user(rappel["user_id"])
                
                if canal and utilisateur:
                    embed = discord.Embed(
                        title="⏰ Rappel !",
                        description=rappel["message"],
                        color=discord.Color.blue(),
                        timestamp=rappel["time"]
                    )
                    embed.set_footer(text="Rappel programmé")
                    
                    await canal.send(f"{utilisateur.mention}", embed=embed)
                
                storage.rappels.remove(rappel)
            except Exception as e:
                print(f"Erreur avec rappel: {e}")
                storage.rappels.remove(rappel)
        
        if rappels_a_envoyer:
            storage.save_data()
    
    @tasks.loop(hours=1)
    async def verifier_anniversaires(self):
        """Vérifier les anniversaires"""
        aujourd_hui = datetime.datetime.now().strftime("%d/%m")
        
        for user_id, date_anniv in storage.anniversaires.items():
            if date_anniv == aujourd_hui:
                utilisateur = self.bot.get_user(user_id)
                if utilisateur:
                    for guilde in self.bot.guilds:
                        membre = guilde.get_member(user_id)
                        if membre:
                            # Chercher un canal général
                            canal_general = None
                            for channel in guilde.text_channels:
                                if "général" in channel.name.lower() or "general" in channel.name.lower():
                                    canal_general = channel
                                    break
                            
                            if not canal_general and guilde.system_channel:
                                canal_general = guilde.system_channel
                            
                            if canal_general:
                                embed = discord.Embed(
                                    title="🎂 Joyeux Anniversaire !",
                                    description=f"Aujourd'hui c'est l'anniversaire de {membre.mention} ! 🎉\nSouhaitons-lui une excellente journée !",
                                    color=discord.Color.purple()
                                )
                                embed.set_thumbnail(url=membre.avatar.url if membre.avatar else None)
                                
                                await canal_general.send(embed=embed)
    
    @tasks.loop(minutes=1)
    async def verifier_giveaways(self):
        """Vérifier les giveaways"""
        maintenant = datetime.datetime.now()
        giveaways_a_terminer = []
        
        # Identifier les giveaways à terminer
        for msg_id, giveaway in storage.giveaways.items():
            if isinstance(giveaway["fin"], str):
                try:
                    giveaway["fin"] = datetime.datetime.fromisoformat(giveaway["fin"])
                except:
                    continue
            
            if giveaway["fin"] <= maintenant:
                giveaways_a_terminer.append(msg_id)
        
        # Traiter les giveaways terminés
        for msg_id in giveaways_a_terminer:
            giveaway = storage.giveaways[msg_id]
            
            try:
                canal = self.bot.get_channel(giveaway["channel_id"])
                
                if canal and giveaway["participants"]:
                    # Sélectionner les gagnants
                    nombre_gagnants = min(giveaway["gagnants"], len(giveaway["participants"]))
                    gagnants = random.sample(giveaway["participants"], nombre_gagnants)
                    
                    # Annoncer les gagnants
                    mentions_gagnants = " ".join([f"<@{g}>" for g in gagnants])
                    
                    embed = discord.Embed(
                        title="🎉 GIVEAWAY TERMINÉ !",
                        description=(
                            f"Le giveaway pour **{giveaway['prix']}** est terminé !\n\n"
                            f"**Gagnant(s):** {mentions_gagnants}\n\n"
                            f"🎊 Félicitations ! 🎊"
                        ),
                        color=discord.Color.green()
                    )
                    
                    await canal.send(embed=embed)
                
                # Supprimer le giveaway
                del storage.giveaways[msg_id]
                
            except Exception as e:
                print(f"Erreur avec giveaway {msg_id}: {e}")
                del storage.giveaways[msg_id]
        
        if giveaways_a_terminer:
            storage.save_data()
    
    @tasks.loop(minutes=1)
    async def envoyer_messages_programmes(self):
        """Envoyer les messages programmés"""
        maintenant = datetime.datetime.now()
        heure_actuelle = maintenant.strftime("%H:%M")
        jour_actuel = maintenant.strftime("%A").lower()
        
        for msg_prog in storage.messages_programmes:
            if msg_prog["heure"] == heure_actuelle and jour_actuel in msg_prog["jours"]:
                canal = self.bot.get_channel(msg_prog["channel_id"])
                if canal:
                    try:
                        await canal.send(msg_prog["message"])
                    except:
                        pass
    
    @verifier_rappels.before_loop
    async def before_verifier_rappels(self):
        """Attendre que le bot soit prêt"""
        await self.bot.wait_until_ready()
    
    @verifier_anniversaires.before_loop
    async def before_verifier_anniversaires(self):
        """Attendre que le bot soit prêt"""
        await self.bot.wait_until_ready()
    
    @verifier_giveaways.before_loop
    async def before_verifier_giveaways(self):
        """Attendre que le bot soit prêt"""
        await self.bot.wait_until_ready()
    
    @envoyer_messages_programmes.before_loop
    async def before_envoyer_messages_programmes(self):
        """Attendre que le bot soit prêt"""
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Tasks(bot))