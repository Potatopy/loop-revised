import aiosqlite
import asyncio
import discord
import random
from discord.ext import commands

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Level cog is ready!")
        setattr(self.bot, "db", await aiosqlite.connect("levels.db"))
        await asyncio.sleep(3)
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS levels (level INT, xp INT, user INT, guild INT)")

def setup(bot):
    bot.add_cog(Level(bot))