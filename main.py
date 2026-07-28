import os
import discord

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"🟢 TEST OK : Le bot est connecté sous le nom : {client.user}")

@client.event
async def on_message(message):
    # On ignore juste ses propres messages
    if message.author == client.user:
        return

    # Affiche absolument TOUT dans la console Render
    print(f"🔔 MESSAGE DÉTECTÉ ! Salon: {message.channel.name} ({message.channel.id}) | Auteur: {message.author} | Contenu: {message.content}")

client.run(DISCORD_TOKEN)
