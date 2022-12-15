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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        author = message.author
        guild = message.guild
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
            xp = await cursor.fetchone()
            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
            level = await cursor.fetchone()

            if not xp or not level:
                await cursor.execute("INSERT INTO levels VALUES (?, ?, ?, ?)", (0, 0, author.id, guild.id,))
            
            try:
                xp = xp[0]
                level = [0]
            except TypeError:
                xp = 0
                level = 0

            if level < 5:
                xp += random.randint(5, 15)
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))
            else:
                rand = random.randint(5, (level//4))
                if rand == 1:
                    xp += random.randint(5, 15)
                    await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))
            if xp >= 100:
                level += 1
                await cursor.execute("UPDATE levels SET level = ? WHERE user = ? AND guild = ?", (level, author.id, guild.id,))
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (0, author.id, guild.id,))
                await message.channel.send(f"{author.mention} has leveled up to level **{level}**!")
            await self.bot.db.commit()

    @commands.command(description="Shows your level", aliases=['lvl', 'rank'])
    async def level(self, ctx, member:discord.Member=None):
        if member is None:
            member = ctx.author
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
            xp = await cursor.fetchone()
            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
            level = await cursor.fetchone()

            if not xp or not level:
                await cursor.execute("INSERT INTO levels VALUES (?, ?, ?, ?)", (0, 0, member.id, ctx.guild.id,))
            
            try:
                xp = xp[0]
                level = level[0]
            except TypeError:
                xp = 0
                level = 0

            em = discord.Embed(title=f"{member.name}'s level", description=f"Level: `{level}`\nXP: `{xp}`", color=discord.Color.green())
            await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Level(bot))