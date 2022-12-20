import nextcord
from nextcord.ext import commands

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Util Cog is ready')
    
    @commands.command()
    async def qna(self, ctx):
        em = nextcord.Embed(title="wtf happened?", description="Well here is a little explination on why I need to re-code the bot")
        em.add_field(name="why tho", value="Reason being is that the bot doesn't send some msgs in general so maybe a full re-code with a diffirent API wrapper will fix it")
        em.add_field(name="when will it be done", value="idk maybe on the weekend")
        em.add_field(name="when will it be back?", value="until railway gets it's shit together and actaully works")
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Util(bot))