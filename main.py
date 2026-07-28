import os
import threading
from flask import Flask
import discord

# --- Mini serveur Web pour valider le port sur Render ---
app = Flask('')

@app.route('/')
def home():
    return "Bot en ligne !"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# --- Code de test du Bot Discord ---
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"🟢 TEST OK : Le bot est connecté sous le nom : {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f"🔔 MESSAGE DÉTECTÉ ! Salon: {message.channel.name} ({message.channel.id}) | Auteur: {message.author} | Contenu: {message.content}")

client.run(DISCORD_TOKEN)
