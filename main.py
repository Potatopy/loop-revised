# Dependancies
import discord_ios
import discord
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv

# Load .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Define the bot
activity = discord.Activity(type=discord.ActivityType.competing, name=",help")
bot = commands.Bot(command_prefix=",", intents=discord.Intents.all(), activity=activity, help_command=None)

# Load cogs
async def load():
    for fn in os.listdir("./cogs"):
        if fn.endswith(".py"):
            await bot.load_extension(f"cogs.{fn[:-3]}")

# Events
@bot.event
async def on_ready():
    print("Bot is ready!")
    print(f"Logged in as {bot.user} ({bot.user.id})")
    print("-----------------------")

# Run the bot
async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())