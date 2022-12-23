import asyncio
import aiosqlite
import datetime
import nextcord
from nextcord.ext import commands

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mod cog is ready!")
        setattr(self.bot, "db", await aiosqlite.connect("db/warn.db"))
        await asyncio.sleep(3)
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS warns (user INT, reason TEXT, time INT, guild INT)")
            await self.bot.db.commit()
    
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

    async def warn(self, ctx, member: nextcord.Member, *, reason=None):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("INSERT INTO warns (user, reason, time, guild) VALUES (?, ?, ?, ?)", (member.id, reason, int(datetime.datetime.now().timestamp()), ctx.guild.id))
        await self.bot.db.commit()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: nextcord.Member, *, reason=None):
        await self.warn(ctx, member, reason=reason)
        await ctx.send(f"Warned {member.mention} for {reason}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def removewarn(self, ctx, member: nextcord.Member):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT reason FROM warns WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("DELETE FROM warns WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
                await ctx.send(f"Removed warn for {member.mention}")
            else:
                await ctx.send("No warns found for this user.")
        await self.bot.db.commit()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warns(self, ctx, member: nextcord.Member):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT reason, time FROM warns WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
            data = await cursor.fetchall()
            if data:
                em = nextcord.Embed(title=f"Warns for {member}", color=nextcord.Color.red())
                warnnum = 0
                for table in data:
                    warnnum += 1
                    em.add_field(name=f"Warn {warnnum}", value=f"Reason: {table[0]} | Date Issued: <t:{int(table[1])}:F>")
                await ctx.send(embed=em)
            else:
                await ctx.send("No warns found for this user.")
        await self.bot.db.commit()

def setup(bot):
    bot.add_cog(Mod(bot))