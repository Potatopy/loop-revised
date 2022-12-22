import nextcord
from nextcord.ext import commands

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = []

    @commands.Cog.listener()
    async def on_ready(self):
        print('Util Cog is ready')

    @commands.Cog.listener()
    async def on_message(self, message):
        for i in range(len(self.data)):
            if (f"<@{self.data[i]}>" in message.content) and (not message.author.bot):
                await message.channel.send(f"<@{self.data[i]}> is AFK, reason: {self.data[i+1]}")

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        if user.id in self.data:
            i = self.data.index(user.id)
            self.data.remove(self.data[i+1])
            self.data.remove(user.id)
            await channel.send(f"Welcome back {user.mention}", delete_after=3)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        global snipe_message_content
        global snipe_message_author

        snipe_message_content = message.content
        snipe_message_author = message.author
        await asyncio.sleep(60)
        snipe_message_author = None
        snipe_message_content = None

    @commands.command()
    async def help(self, ctx):
        em = nextcord.Embed(description="documentation + commands: [click](https://loop-3.gitbook.io/api-docs/)")
        await ctx.send(embed=em)

    @commands.command()
    async def afk(self, ctx, *args):
        msg = ' '.join(args)
        self.data.append(ctx.author.id)
        self.data.append(msg)
        await ctx.send("afk set")

    @commands.command(aliases=['s'])
    async def snipe(self, message):
        if snipe_message_content == None:
            await message.channel.send("There is nothing to snipe!")
        else:
            em = nextcord.Embed(color=nextcord.Color.random(), description=f"{snipe_message_content}")
            em.set_footer(text=f"Requested by {message.author.name}#{message.author.discriminator}")
            em.set_author(name=f"{snipe_message_author.name}#{snipe_message_author.discriminator}", icon_url=snipe_message_author.display_avatar)
            await message.channel.send(embed=em)
            return

        @commands.command()
        async def echo(self, ctx, *, arg = ""):
            if arg == "":
                await ctx.send("Please enter a message to echo")
            else:
                await ctx.send(arg)

        @commands.command()
        @commands.has_permissions(manage_messages=True)
        async def poll(self, ctx, *, message):
            em = nextcord.Embed(title="Poll", description=message, color=nextcord.Color.purple())
            msg = await ctx.channel.send(embed=em)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

def setup(bot):
    bot.add_cog(Util(bot))