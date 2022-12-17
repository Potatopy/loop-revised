import discord
from datetime import datetime
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logging cog is ready!")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        z = bot.get_channel(1053526656217796628)
        em = discord.Embed(title=f"Message Deleted by {message.author}", description=f"**Message:** {message.content}\nAuthor: {message.author.mention}\nChannel: {message.channel.mention}", color=discord.Color.red(), timestamp=datetime.utcnow())
        em.set_author(name=after.name, icon_url=after.avatar_url)
        await z.send(embed=em)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        z = bot.get_channel(1053526656217796628)
        em = discord.Embed(title=f"Message Edited by {message.author}", description=f"**Before:** {before.content}\nAfter: {after.content}\nAuthor: {before.author.mention}\nChannel: {message.channel.mention}", color=discord.Color.yellow(), timestamp=datetime.utcnow())
        em.set_author(name=after.author.name, icon_url=after.avatar_url)
        await z.send(embed=em)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        z = bot.get_channel(1053526656217796628)
        if len(before.roles) > len(after.roles):
            role = next(role for role in before.roles if role not in after.roles)
            em = discord.Embed(title=f"Role Removed!", description=f"{role.name} was removed from {before.mention}", color=discord.Color.red(), timestamp=datetime.utcnow())
        elif len(after.roles) > len(before.roles):
            role = next(role for role in after.roles if role not in before.roles)
            em = discord.Embed(title=f"Role Added!", description=f"{role.name} was added to {before.mention}", color=discord.Color.green(), timestamp=datetime.utcnow())
        elif before.nick != after.nick:
            em = discord.Embed(title=f"Nickname Changed!", description=f"{before.mention}'s nickname was changed from {before.nick} to {after.nick}", color=discord.Color.blue(), timestamp=datetime.utcnow())
        else:
            return
        em.set_author(name=after.name, icon_url=after.avatar_url)
        await z.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        z = bot.get_channel(1053526656217796628)
        em = discord.Embed(title=f"Channel Created!", description=f"{channel.mention} was created", color=discord.Color.green(), timestamp=datetime.utcnow())
        em.set_author(name=channel.guild.name, icon_url=channel.guild.icon_url)
        await z.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        z = bot.get_channel(1053526656217796628)
        em = discord.Embed(title=f"Channel Deleted!", description=f"{channel.mention} was deleted", color=discord.Color.red(), timestamp=datetime.utcnow())
        em.set_author(name=channel.guild.name, icon_url=channel.guild.icon_url)
        await z.send(embed=em)

async def setup(bot):
    await bot.add_cog(Logging(bot))