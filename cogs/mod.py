import asyncio
import aiosqlite
import datetime
import nextcord
import os

from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()
p = os.getenv("PREFIX")

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mod cog is ready!")
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: nextcord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"smokin that {member.mention} pack 🚬")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} got booted")

    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Cleared {amount} messages.", delete_after=3)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = ctx.guild.bans()

        async for ban_entry in banned_users:
            user = ban_entry.user
                
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def lock(self, ctx, channel:nextcord.TextChannel=None, setting=None):
        if setting == '--server':
            for channel in ctx.guild.channels:
                await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.send('Server locked!')
        
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"Locked {channel.mention}")
    
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def unlock(self, ctx, channel:nextcord.TextChannel=None, setting=None):
        if setting == '--server':
            for channel in ctx.guild.channels:
                await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await ctx.send('Server unlocked!')
        
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"Unlocked {channel.mention}")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def slowmode(self, ctx, seconds: int, channel:nextcord.TextChannel=None):
        if channel is None:
            channel = ctx.channel
        await channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set slowmode delay to {seconds} seconds in {channel.mention}")

    @commands.group()
    async def mod(self, ctx):
        pass

    @mod.command()
    async def help(self, ctx):
        em = nextcord.Embed(title="Mod Help", description="All Mod Commands", color=nextcord.Color.blue())
        em.add_field(name="**Ban**", value=f"{p}ban <member> <reason>", inline=False)
        em.add_field(name="**Kick**", value=f"{p}kick <member> <reason>", inline=False)
        em.add_field(name="**Clear**", value=f"{p}clear <amount>", inline=False)
        em.add_field(name="**Unban**", value=f"{p}unban <member>", inline=False)
        em.add_field(name="**Lock**", value=f"{p}lock <channel> <setting>", inline=False)
        em.add_field(name="**Unlock**", value=f"{p}unlock <channel> <setting>", inline=False)
        em.add_field(name="**Slowmode**", value=f"{p}slowmode <seconds> <channel>", inline=False)
        em.set_footer(text="More commands will be added soon!")
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Mod(bot))