import discord
import asyncio
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    snipe_message_content = None
    snipe_message_author = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Mod commands are online!')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        global snipe_message_content
        global snipe_message_author

        snipe_message_content = message.content
        snipe_message_author = message.author
        await asyncio.sleep(60)
        snipe_message_author = None
        snipe_message_content = None
    
    @commands.command(description='Clears a certain amount of messages')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amt:int):
        await ctx.channel.purge(limit=amt)
        await ctx.send(f"Deleted {amt} messages!", delete_after=5)

    @commands.command(description='Kicks a member')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"get out {member.mention}, Reason: {reason}")

    @commands.command(description='Bans a member')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"smokin that {member.mention} pack 🚬, Reason: {reason}")

    @commands.command(description='Unbans a member')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = ctx.guild.bans()

        async for ban_entry in banned_users:
            user = ban_entry.user
                
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')

    @commands.command(description='Locks a channel/server')
    @commands.has_permissions(manage_guild=True)
    async def lock(self, ctx, channel:discord.TextChannel=None, setting=None):
        if setting == '--server':
            for channel in ctx.guild.channels:
                await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.send('Server locked!')
        
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"Locked {channel.mention}")
    
    @commands.command(description='Locks a channel/server')
    @commands.has_permissions(manage_guild=True)
    async def unlock(self, ctx, channel:discord.TextChannel=None, setting=None):
        if setting == '--server':
            for channel in ctx.guild.channels:
                await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await ctx.send('Server unlocked!')
        
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"Unlocked {channel.mention}")

    @commands.command(description='Snipes a deleted message')
    async def snipe(self, message):
        if snipe_message_content == None:
            await message.channel.send("There is nothing to snipe!")
        else:
            em = discord.Embed(color=discord.Color.random(), description=f"{snipe_message_content}")
            em.set_footer(text=f"Requested by {message.author.name}#{message.author.discriminator}")
            em.set_author(name=f"{snipe_message_author.name}#{snipe_message_author.discriminator}", icon_url=snipe_message_author.avatar_url)
            await message.channel.send(embed=em)
            return

def setup(bot):
    bot.add_cog(Mod(bot)) 