import nextcord
import aiosqlite
import asyncio
from nextcord.ext import commands

class Eco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Eco Cog is ready')
        db = await aiosqlite.connect("db/bank.sqlite")
        await asyncio.sleep(3)
        async with db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS bank (wallet INT, bank INT, maxbank INT, user INT)")
        await db.commit()
        print("Bank is ready")

    async def create_balance(self, user):
        db = await aiosqlite.connect("db/bank.sqlite")
        async with db.cursor() as cursor:
            await cursor.execute("INSERT INTO bank VALUES (?, ?, ?, ?)", (0, 100, 25000, user.id))

def setup(bot):
    bot.add_cog(Eco(bot))