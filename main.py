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
    # Ignorer les messages du bot lui-même
    if message.author == client.user:
        return

    print(f"🔔 Message reçu de {message.author} : {message.content}")

    # --- SUPPRESSION DU MESSAGE ---
    try:
        await message.delete()
        print(f"🗑️ Message de {message.author} supprimé avec succès !")
    except discord.Forbidden:
        print("❌ Erreur : Le bot n'a pas la permission de supprimer des messages.")
    except Exception as e:
        print(f"❌ Erreur lors de la suppression : {e}")

client.run(DISCORD_TOKEN)
