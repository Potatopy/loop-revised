import discord
import os
from discord.ext import commands
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO = os.getenv("MONGO_DB")

bot_channel = 1049886726199455794
talk_channels = [1049886706280714302, 1049889178772590673, 1049889231239118858, 1049890194645581924, 1049886865458737182]

level = ["lvl 5", "lvl 10", "lvl 25", "lvl 50 (vip perks)"]
levelnum = [5, 10, 25, 50]

cluster = MongoClient(MONGO)
leveling = cluster["discord"]["leveling"]

class LevelSys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Leveling system is ready!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in talk_channels:
            stats = leveling.find_one({"id": message.author.id})
            if not message.author.bot:
                if stats is None:
                    newuser = {"id": message.author.id, "xp": 100}
                    leveling.insert_one(newuser)
                else:
                    xp = stats["xp"] + 5
                    leveling.update_one({"id": message.author.id}, {"$set": {"xp": xp}})
                    lvl = 0
                    while True:
                        if xp < ((50*(lvl**2))+(50*(lvl-1))):
                            break
                        lvl += 1
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    if xp == 0:
                        await message.channel.send(f"{message.author.mention} has leveled up to level {lvl}!")
                        for i in range(len(levelnum)):
                            if lvl == levelnum[i]:
                                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
                                em = discord.Embed(description=f"{message.author.mention} now has {level[i]} perks!", color=0x00ff00)
                                em.set_thumbnail(url=message.author.avatar_url)
                                await message.channel.send(embed=em)

    @commands.command()
    async def test(self, ctx):
        if ctx.channel.id == bot_channel:
            stats = leveling.find_one({"id": ctx.author.id})
            if stats is None:
                em = discord.Embed(description=f"{ctx.author.mention} has no xp yet!", color=0xff0000)
                await ctx.channel.send(embed=em)
            else:
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                    if xp < ((50*(lvl**2))+(50*(lvl-1))):
                        break
                    lvl += 1
                xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                boxes = int((xp/(200*((1/2)*lvl)))*20)
                rankings = leveling.find().sort("xp", -1)
                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                        em = discord.Embed(title=f"{ctx.author.id}'s level")
                        em.add_field(name="Name", value=ctx.author.mention, inline=True)
                        em.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
                        em.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                        em.add_field(name="Progress Bar [lvl]", value=boxes * ":blue_square:" + (20-boxes) * "white_large_square", inline=True)
                        await ctx.channel.send(embed=em)

    @commands.command(aliases=['lb', 'top'])
    async def leaderboard(self, ctx):
        if (ctx.channel.id == bot_channel):
            rankings = leveling.find().sort("xp", -1)
            i = 1
            em = discord.Embed(title="Leaderboard:", color=0x00ff00)
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    em.add_field(name=f"{i}: {temp.name}", value=f"XP: {tempxp}", inline=False)
                    i += 1
                except:
                    pass
                if i == 11:
                    break
            await ctx.channel.send(embed=em)


async def setup(bot):
    await bot.add_cog(LevelSys(bot))