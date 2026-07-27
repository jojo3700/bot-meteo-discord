import os
from threading import Thread
from flask import Flask
import google.generativeai as genai
import discord
from discord.ext import commands

# --- REMPLACEZ CES 3 LIGNES AVEC VOS INFORMATIONS ---
DISCORD_TOKEN = "VOTRE_TOKEN_BOT_DISCORD"   # Collez le Token de votre Bot Discord
GEMINI_API_KEY = "VOTRE_CLE_API_GEMINI"     # Collez votre clé API Gemini
ID_SALON_METEO = 123456789012345678         # Collez l'ID de votre salon météo (sans guillemets)

# --- MINI-SERVEUR WEB POUR KEEP ALIVE RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Discord Météo en cours d'exécution !"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# --- CONFIGURATION BOT & GEMINI ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

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
                print(f"❌ Message hors-sujet supprimé de {message.author}: {message.content}")
            else:
                print(f"✅ Message météo conservé : {message.content}")

        except Exception as e:
            print(f"⚠️ Erreur lors de l'analyse : {e}")

    await bot.process_commands(message)

# Lancement du serveur Web factice puis du bot
keep_alive()
bot.run(DISCORD_TOKEN)
