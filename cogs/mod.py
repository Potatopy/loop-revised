import asyncio
import nextcord
from nextcord.ext import commands

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

def setup(bot):
    bot.add_cog(Mod(bot))