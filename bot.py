import discord
import openai
import os
import asyncio
from dotenv import load_dotenv
from personality import get_blacksmith_response

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

active_users = {}  # Dicționar pentru a urmări utilizatorii activi

async def remove_active_user(user_id, timeout=120):
    """ Șterge utilizatorul din lista celor activi după un timeout """
    await asyncio.sleep(timeout)
    if user_id in active_users:
        del active_users[user_id]

@client.event
async def on_ready():
    print(f'Botul {client.user} este online!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = message.author.id
    user_message = message.content.lower()

    # Condiții pentru activarea botului
    keywords = ['fierare', 'esuat', 'upgrade', '+', 'sabia', 'bless', 'fierar', 'plus', 
                'up', 'metal', 'sabie', 'iteme', 'cercei', 'papuci', 'colier', 'coif', 'papucii', 'cerceii', 'pumnale']

    bot_mentioned = client.user.mentioned_in(message)
    bot_replied = message.reference and (await message.channel.fetch_message(message.reference.message_id)).author == client.user
    contains_keyword = any(kw in user_message for kw in keywords)
    is_active_conversation = user_id in active_users

    if bot_mentioned or bot_replied or contains_keyword or is_active_conversation:
        response = get_blacksmith_response(message.content, message.author.name)

        if response:
            await message.channel.send(response)
            active_users[user_id] = True  
            asyncio.create_task(remove_active_user(user_id)) 

client.run(TOKEN)
