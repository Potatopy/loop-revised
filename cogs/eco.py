import aiosqlite
import asyncio
import discord
from discord.ext import commands

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy cog is ready!")
        db = await aiosqlite.connect("db/eco.db")
        await asyncio.sleep(3)
        async with db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS bank (wallet INT, bank INT, maxbank INT, user INT)")
        await db.commit()
        print('Database1 is ready!')

    async def create_balance(self, user):
        async with db.cursor() as cursor:
            await cursor.execute("INSERT INTO bank VALUES (?, ?, ?, ?)", (0, 100, 25000, user.id))
        await db.commit()
        return

    async def get_balance(self, user):
        async with db.cursor() as cursor:
            await cursor.execute("SELECT wallet, bank, maxbank")
            data = await cursor.fetchone()
            if data is None:
                await self.create_balance(user)
                return 0, 100, 25000
            wallet, bank, maxbank = data[0], data[1], data[2]
            return wallet, bank, maxbank

    async def update_wallet(self, user, amount: int):
        async with db.cursor() as cursor:
            await cursor.execute("SELECT wallet FROM bank WHERE user = ?", (user.id,))
            data = await cursor.fetchone()
            if data is None:
                await self.create_balance(user)
                return 0
            await cursor.execute("UPDATE bank SET wallet = ? WHERE user = ?", (data[0] + amount, user.id))
        await db.commit()

    @commands.command()
    async def balance(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        wallet, bank, maxbank = await self.get_balance(member)
        em = discord.Embed(title=f"{member.name}'s balance", color=discord.Color.green())
        em.add_field(name="Wallet", value=f"${wallet}")
        em.add_field(name="Bank", value=f"${bank}/{maxbank}")
        await ctx.send(embed=em)

async def setup(bot):
    await bot.add_cog(Economy(bot))