import discord
import json

from discord import File
from discord.ext import commands
from typing import Optional
from easy_pil import Editor, load_image_async, Font

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Level cog is ready!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.content.startswith(","): # if the msg starts with the bot's prefix give no xp
            if not message.author.bot: # if the message author is a bot give no xp
                with open("db/levels.json", "r") as f:
                    data = json.load(f)
                
                if str(message.author.id) in data:
                    xp = data[str(message.author.id)]["xp"]
                    level = data[str(message.author.id)]["level"]

                    increased_xp = xp + 25
                    new_level = int(increased_xp/100)
                else:
                    data[str(message.author.id)] = {}
                    data[str(message.author.id)]["xp"] = 0
                    data[str(message.author.id)]["level"] = 1
                    
                    with open("db\levels.json", "r") as f:
                        json.dump(data, f)


async def setup(bot):
    await bot.add_cog(Level(bot))