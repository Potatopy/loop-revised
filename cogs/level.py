import aiosqlite
import asyncio
import discord
import random
from discord.ext import commands
from easy_pil import *

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
                level = level[0]
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
            await self.bot.process_commands(message)

    @commands.command(description="Shows your level", aliases=['lvl', 'rank', 'xp'])
    async def level(self, ctx, member:discord.Member=None):
        """
        This Command Shows Your Level + XP
        """
        if member is None:
            member = ctx.author
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
            xp = await cursor.fetchone()
            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
            level = await cursor.fetchone()

            if not xp or not level:
                await cursor.execute("INSERT INTO levels VALUES (?, ?, ?, ?)", (0, 0, member.id, ctx.guild.id,))
                await self.bot.db.commit()
            
            try:
                xp = xp[0]
                level = level[0]
            except TypeError:
                xp = 0
                level = 0

            user_data = {
                "name" : f"{member.name}#{member.discriminator}",
                "xp" : xp,
                "level" : level,
                "next_level_xp" : 100,
                "progress" : xp,
            }

            # Custom Level Card
            background = Editor(Canvas((900, 300), color="#141414"))
            pfp = await load_image_async(str(member.avatar_url))
            profile = Editor(pfp).resize((150, 150)).circle_image()

            # Font
            poppins = Font.poppins(size=40)
            poppins_small = Font.poppins(size=30)

            # Card Shape
            card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]
            
            # profile pic
            background.polygon(card_right_shape, fill="#FFFFFF")
            background.paste(profile, (30, 30))

            # progress bar
            background.rectangle((30, 220), width=650, height=40, color="#FFFFFF")
            background.bar((30, 220), max_width=650, height=40, percentage=user_data["progress"], color="#FFFFFF", radius=20)
            background.text((200, 50), user_data["name"], font=poppins, color="#FFFFFF")

            # level and xp
            background.rectangle((200, 100), width=350, height=2, fill="#FFFFFF")
            background.text(
                (200, 130),
                f"Level - {user_data['level']} | XP - {user_data['xp']}/{user_data['next_level_xp']}",
                font = poppins_small,
                color = "#FFFFFF"
            )

            await ctx.send(file=discord.File(filename="lvl.png", fp=background.image_bytes))

async def setup(bot):
    await bot.add_cog(Level(bot))