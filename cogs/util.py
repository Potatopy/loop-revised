import discord
from discord.ext import commands

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("Util cog is ready!")

    @commands.Cog.listener()
    async def on_message(self, message):
        for i in range(len(self.data)):
            if (f"<@{self.data[i]}>" in message.content) and (not message.author.bot):
                await message.channel.send(f"<@{self.data[i+1]}> is AFK ")

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        if user.id in self.data:
            self.data.index(user.id)
            self.data.remove(self.data[i+1])
            self.data.remove(user.id)
            await channel.send(f"Welcome back {user.mention}", delete_after=3)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def help(self, ctx):
        em = discord.Embed(description="documentation + commands: [click](https://loop-3.gitbook.io/api-docs/)", color=discord.Color.purple())
        await ctx.send(embed=em)

    @commands.command()
    async def echo(self, ctx, *, arg = ""):
        if arg == "":
            await ctx.send("Please enter a message to echo")
        else:
            await ctx.send(arg)

    @commands.command()
    async def poll(self, ctx, *, message):
        em = discord.Embed(title="Poll", description=message, color=discord.Color.purple())
        msg = await ctx.channel.send(embed=em)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    @commands.command()
    async def afk(self, ctx, *args):
        msg = ' '.join(args)
        self.data.append(ctx.author.id)
        self.data.append(msg)
        await ctx.send("afk set", delete_after=3)

async def setup(bot):
    await bot.add_cog(Util(bot))