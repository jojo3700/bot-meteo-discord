import os
import threading
from flask import Flask
import discord

# --- Webserver pour Render ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Météo en ligne !"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# --- Bot Discord ---
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"🟢 CONNECTÉ : Le bot est prêt sous le nom de : {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f"🔔 Message reçu de {message.author} dans #{message.channel}: {message.content}")

client.run(DISCORD_TOKEN)
