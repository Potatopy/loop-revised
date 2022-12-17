# Dependencies
import discord
import json

# imports
from discord import File
from discord.ext import commands
from typing import Optional
from easy_pil import Editor, load_image_async, Font

# roles + levels
level = ["lvl 5", "lvl 10", "lvl 25", "lvl 50 (vip perks)"]
level_num = [5, 10, 25, 50]

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

                    data[str(message.author.id)]['xp'] = increased_xp
                    with open("db\levels.json", "w") as f:
                        json.dump(data, f)

                    if new_level > level:
                        await message.channel.send(f"{message.author.mention} has leveled up to level {new_level}!")
                        data[str(message.author.id)]['level'] = new_level
                        data[str(message.author.id)]['xp'] = 0

                        with open("db\levels.json", "w") as f:
                            json.dump(data, f)

                        for i in range(len(level)):
                            if new_level == level_num[i]:
                                await message.author.add_roles(discord.utils.get(message.author.guild, name=[level[i]]))

                            await message.channel.send(f"{message.author.mention} now has the {level[i]} role, check <#1049892987070590996> for lvl perks")
                else:
                    data[str(message.author.id)] = {}
                    data[str(message.author.id)]["xp"] = 0
                    data[str(message.author.id)]["level"] = 1
                    
                    with open("db\levels.json", "r") as f:
                        json.dump(data, f)

async def setup(bot):
    await bot.add_cog(Level(bot))