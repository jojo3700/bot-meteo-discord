import os
from threading import Thread
from flask import Flask
import google.generativeai as genai
import discord
from discord.ext import commands

# --- LECTURE SECURISEE DE VOS CLES VIA RENDER ---
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
ID_SALON_METEO = int(os.environ.get("ID_SALON_METEO", "0"))

# --- MINI-SERVEUR WEB POUR MINTENIR EN VIE SUR RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Météo en ligne !"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURATION DE GEMINI ET DISCORD ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🟢 Bot prêt et connecté sous le nom de : {bot.user} !")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # TEST : Affiche TOUS les messages reçus dans les logs avec l'ID du salon
    print(f"📩 Message reçu dans le salon [{message.channel.id}] par {message.author}: {message.content}")

    if message.channel.id == ID_SALON_METEO:
        prompt = f"""
        Tu es un modérateur pour le serveur "La Météo du futur".
        Analyse le message suivant envoyé par un utilisateur.
        Est-ce que ce message a un rapport avec la météo, le climat, la prévision, la température ou l'observation du temps ?
        
        Message : "{message.content}"
        
        Réponds STRICTEMENT par un seul mot : OUI ou NON.
        """

        try:
            response = model.generate_content(prompt)
            reponse_ia = response.text.strip().upper()

            if "NON" in reponse_ia:
                await message.delete()
                print(f"❌ Message hors-sujet supprimé : {message.content}")
            else:
                print(f"✅ Message météo conservé : {message.content}")

        except Exception as e:
            print(f"⚠️ Erreur lors de l'analyse : {e}")

    await bot.process_commands(message)

# --- DÉMARRAGE DU BOT ET DU SERVEUR WEB ---
keep_alive()
bot.run(DISCORD_TOKEN)
