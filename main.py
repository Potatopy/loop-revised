# Dependencies
import asyncio
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

# Main Bot
intents=discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents)

# Load Cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

# On Ready
@bot.event
async def on_ready():
    print("Bot is ready!")
    print(f"Logged in as {bot.user} ({bot.user.id})")
    print("---------------------")

# Run Bot
bot.run(TOKEN)