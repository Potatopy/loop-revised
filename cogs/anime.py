import nextcord
import requests
import os

from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()
p = os.getenv("PREFIX")

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Anime cog is ready!")

    @commands.command()
    @commands.is_nsfw()
    async def hentai(self, ctx):
        r = requests.get('https://nekobot.xyz/api/image?type=hentai')
        res = r.json()
        em = nextcord.Embed()
        em.set_image(url=res['message'])
        em.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.display_avatar)
        await ctx.send(embed=em)

    @commands.group()
    async def anime(self, ctx):
        pass

    @anime.command()
    async def help(self, ctx):
        em = nextcord.Embed(title="Anime Help", description="All Anime Commands", color=nextcord.Color.blue())
        em.add_field(name="**Hentai**", value=f"{p}hentai", inline=False)
        em.set_footer(text="More commands will be added soon!")
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Anime(bot))