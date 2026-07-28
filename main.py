import os
import threading
from flask import Flask
import discord
import google.generativeai as genai

# --- Webserver pour Render ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Météo en ligne !"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# --- Configuration Gemini ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

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
    # Ignorer les messages envoyés par le bot
    if message.author == client.user:
        return

    print(f"🔔 Message reçu de {message.author} : {message.content}")

    if not GEMINI_API_KEY:
        print("⚠️ Pas de clé GEMINI_API_KEY configurée dans Render.")
        return

    # Prompt strict envoyé à Gemini
    prompt = f"""
    Tu es un modérateur strict pour un serveur Discord dédié exclusivement à la MÉTÉO.
    Message à analyser : "{message.content}"

    RÈGLES STRICTES :
    - Réponds OUI SEULEMENT SI le message parle de temps, température, pluie, soleil, nuages, vent, prévisions, climat ou observations météorologiques.
    - Réponds NON pour TOUT LE RESTE (salutations simples, discussions générales, questions hors-sujet, blagues, etc.).

    Réponds UNIQUEMENT par le mot "OUI" ou "NON".
    """

    try:
        response = model.generate_content(prompt)
        decision = response.text.strip().upper()
        print(f"🤖 Décision Gemini pour '{message.content}' : {decision}")

        if "NON" in decision:
            await message.delete()
            print(f"🗑️ Message non-météo de {message.author} supprimé.")
        else:
            print(f"✅ Message météo conservé !")

    except Exception as e:
        print(f"❌ Erreur lors de la vérification Gemini : {e}")

client.run(DISCORD_TOKEN)
