import discord

from discord.ext import commands
from datetime import datetime, timezone
from config import target_channel_id, message_channel_id, token
intents = discord.Intents.all()


bot = commands.Bot(command_prefix='!', intents=intents)
# configuration ici (de linge 12 et 13)
voice_times = {}
participants = {}  # Dictionnaire pour stocker les temps de participation de chaque membre

@bot.event
async def on_voice_state_update(member, before, after):
    # Vérifier si l'utilisateur rejoint le salon vocal spécifique
    if before.channel is None and after.channel is not None and after.channel.id == target_channel_id:
        voice_times[member.id] = datetime.now(timezone.utc)
        participants[member.id] = member.name

    # Vérifier si l'utilisateur quitte le salon vocal spécifique
    elif before.channel is not None and after.channel is None and before.channel.id == target_channel_id:
        if member.id in voice_times:
            start_time = voice_times.pop(member.id)
            duration = datetime.now(timezone.utc) - start_time
            total_seconds = int(duration.total_seconds())

            # Calculer la durée totale de l'appel
            if total_seconds < 60:
                duration_str = f"{total_seconds} secondes"
            else:
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                duration_str = f"{minutes} minutes {seconds} secondes" if seconds else f"{minutes} minutes"
            
            # Si le dernier membre quitte, envoyer le message
            if len(voice_times) == 0:
                # Créer l'embed
                embed = discord.Embed(
                    title="**Fin de l'appel vocal**",
                    color=discord.Color.from_str("#00FFFF")  # metre la couleur avce le code couleur hexadécimal de votre choix
                )
                
                # Ajouter la liste des participants et la durée totale de l'appel à la description
                participant_list = "\n".join([f"- {name}" for name in participants.values()])
                description = f"**Participants :**\n{participant_list if participant_list else 'Aucun participant'}\n\n**Durée totale de l'appel :** {duration_str}"
                
                embed.description = description
                
                # Envoyer l'embed dans le salon spécifié
                channel = bot.get_channel(message_channel_id)
                await channel.send(embed=embed)
                
                # Réinitialiser les participants après l'envoi du message
                participants.clear()
# Ajouter le token de votre bot
bot.run(token) 
