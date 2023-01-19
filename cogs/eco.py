import nextcord
import aiosqlite
import asyncio
import random
from nextcord.ext import commands

class ShopView(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=120)

    @nextcord.ui.button(label="Laptop", style=nextcord.ButtonStyle.blurple, custom_id="laptop")
    async def laptop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        db = await aiosqlite.connect("db/bank.sqlite")
        async with db.cursor() as cursor:
            await cursor.execute("SELECT laptop FROM inv WHERE user = ?", (interaction.user.id,))
            item = await cursor.fetchone()
            if item is None:
                await cursor.execute("INSERT INTO inv VALUES (?, ?, ?, ?)", (1, 0, 0, interaction.user.id,))
            else:
                await cursor.execute("UPDATE inv SET laptop = ? WHERE user = ?", (item[0] + 1, interaction.user.id,))
        await db.commit()
        await interaction.response.send_message("You bought a laptop!", ephemeral=True)

    @nextcord.ui.button(label="Phone", style=nextcord.ButtonStyle.blurple, custom_id="phone")
    async def phone(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        db = await aiosqlite.connect("db/bank.sqlite")
        async with db.cursor() as cursor:
            await cursor.execute("SELECT phone FROM inv WHERE user = ?", (interaction.user.id,))
            item = await cursor.fetchone()
            if item is None:
                await cursor.execute("INSERT INTO inv VALUES (?, ?, ?, ?)", (1, 0, 0, interaction.user.id,))
            else:
                await cursor.execute("UPDATE inv SET phone = ? WHERE user = ?", (item[0] + 1, interaction.user.id,))
        await db.commit()
        await interaction.response.send_message("You bought a phone!", ephemeral=True)

    @nextcord.ui.button(label="FakeID", style=nextcord.ButtonStyle.blurple, custom_id="fakeid")
    async def fakeid(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        db = await aiosqlite.connect("db/bank.sqlite")
        async with db.cursor() as cursor:
            await cursor.execute("SELECT fakeid FROM inv WHERE user = ?", (interaction.user.id,))
            item = await cursor.fetchone()
            if item is None:
                await cursor.execute("INSERT INTO inv VALUES (?, ?, ?, ?)", (1, 0, 0, interaction.user.id,))
            else:
                await cursor.execute("UPDATE inv SET fakeid = ? WHERE user = ?", (item[0] + 1, interaction.user.id,))
        await db.commit()
        await interaction.response.send_message("You bought a Fake ID!", ephemeral=True)

class Eco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Eco Cog is ready!')
        db = await aiosqlite.connect("db/bank.sqlite")
        await asyncio.sleep(3)
        async with db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS bank (wallet INT, bank INT, maxbank INT, user INT)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS inv (laptop INT, phone INT, fakeid INT, user INT)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS shop (name TEXT, id TEXT, desc TEXT, cost INT)")
        await db.commit()
        print("Bank database is ready!")

    async def create_inv(self, user):
        db = await aiosqlite.connect("db/bank.sqlite")
        async with db.cursor() as cursor:
            await cursor.execute("INSERT INTO inv VALUES (?, ?, ?, ?)", (0, 0, 0, user.id,))
        await db.commit()
        return

    async def get_inv(self, user):
        db = await aiosqlite.connect("db/bank.sqlite")
        async with db.cursor() as cursor:
            await cursor.execute("SELECT laptop, phone, fakeid FROM inv WHERE user = ?", (user.id,))
            data = await cursor.fetchone()
            if data is None:
                await self.create_inv(user)
                return 0, 0, 0
            laptop, phone, fakeid = data[0], data[1], data[2]
            return laptop, phone, fakeid
    
    async def create_balance(self, user):
        db = await aiosqlite.connect("db/bank.sqlite")
        async with db.cursor() as cursor:
            await cursor.execute("INSERT INTO bank VALUES (?, ?, ?, ?)", (0, 100, 25000, user.id,))
        await db.commit()
        return

    async def get_balance(self, user):
        db = await aiosqlite.connect("db/bank.sqlite")
        async with db.cursor() as cursor:
            await cursor.execute("SELECT wallet, bank, maxbank FROM bank WHERE user = ?", (user.id,))
            data = await cursor.fetchone()
            if data is None:
                await self.create_balance(user)
                return 0, 100, 25000
            wallet, bank, maxbank = data[0], data[1], data[2]
            return wallet, bank, maxbank

    async def update_wallet(self, user, amount: int):
        db = await aiosqlite.connect("db/bank.sqlite")
        async with db.cursor() as cursor:
            await cursor.execute("SELECT wallet FROM bank where user = ?", (user.id,))
            data = await cursor.fetchone()
            if data is None:
                await self.create_balance(user)
                return 0
            await cursor.execute("UPDATE bank SET wallet = ? WHERE user = ?", (data[0] + amount, user.id,))
        await db.commit()

    async def update_bank(self, user, amount):
        db = await aiosqlite.connect("db/bank.sqlite")
        async with db.cursor() as cursor:
            await cursor.execute("SELECT wallet, bank, maxbank FROM bank where user = ?", (user.id,))
            data = await cursor.fetchone()
            if data is None:
                await self.create_balance(user)
                return 0
            capacity = int(data[2] - data[1])
            if amount > capacity:
                await self.update_wallet(user, amount)
                return 1
            await cursor.execute("UPDATE bank SET bank = ? WHERE user = ?", (data[1] + amount, user.id,))
        await db.commit()

    async def update_max_bank(self, user, amount):
        db = await aiosqlite.connect("db/bank.sqlite")
        async with db.cursor() as cursor:
            await cursor.execute("SELECT maxbank FROM bank where user = ?", (user.id,))
            data = await cursor.fetchone()
            if data is None:
                await self.create_balance(user)
                return 0
            await cursor.execute("UPDATE bank SET maxbank = ? WHERE user = ?", (data[0] + amount, user.id,))
        await db.commit()

    async def update_shop(name: str, id: str, desc: str, cost: int):
        db = await aiosqlite.connect("db/bank.sqlite")
        async with db.cursor() as cursor:
            await cursor.execute("INSERT INTO shop VALUES (?, ?, ?, ?)", (name, id, desc, cost))
        await db.commit()
        return

    @commands.group()
    async def eco(self, ctx):
        pass

    @eco.command()
    async def help(self, ctx):
        em = nextcord.Embed(title="Economy Help", description="Commands:")
        em.add_field(name="balance", value="Shows your balance")
        em.add_field(name="shop", value="Shows the shop (doesn't really do anything yet)")
        em.add_field(name="buy", value="Buys an item from the shop")
        em.add_field(name="deposit", value="Deposits money into your bank")
        em.add_field(name="withdraw", value="Withdraws money from your bank")
        em.add_field(name="give", value="Gives money to another user")
        em.add_field(name="add_items", value="Add items to the shop (owner only)")
        await ctx.send(embed=em)
    
    @commands.command()
    @commands.is_owner()
    async def add_items(self, ctx, name: str, id: str, desc: str, cost: int):
        await self.update_shop(name, id, desc, cost)
        await ctx.send("Item added to shop!", delete_after=5)
    
    @commands.command()
    async def balance(self, ctx, member: nextcord.Member = None):
        if not member:
            member = ctx.author
        wallet, bank, maxbank = await self.get_balance(member)
        em = nextcord.Embed(title=f"{member.name}'s Balance")
        em.add_field(name="Wallet", value=f"${wallet}")
        em.add_field(name="Bank", value=f"${bank}/{maxbank}")
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        chances = random.randint(1, 4)
        if chances == 1:
            await ctx.send("You got nothing")
        amount = random.randint(5, 100)
        res = await self.update_wallet(ctx.author, amount)
        if res == 0:
            await ctx.send(f"No account has been found! Creating one for you now... (please wait 30 seconds before running this command again)")
        await ctx.send(f"You got `${amount}` coins")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def withdraw(self, ctx, amount):
        wallet, bank, maxbank = await self.get_balance(ctx.author)
        try:
            amount = int(amount)
        except ValueError:
            pass
        if type(amount) == str:
            if amount.lower() == "max" or amount.lower() == "all":
                amount = int(bank)
        else:
            amount = int(amount)

        bank_res = await self.update_bank(ctx.author, -amount)
        wallet_res = await self.update_wallet(ctx.author, amount)
        
        if bank_res == 0 or wallet_res == 0:
            await ctx.send("No account has been found! Creating one for you now... (please wait 5 seconds before running this command again)")

        wallet, bank, maxbank = await self.get_balance(ctx.author)
        em = nextcord.Embed(title=f"{ctx.author.name}'s New Balance")
        em.add_field(name="New Wallet", value=f"${wallet}")
        em.add_field(name="New Bank", value=f"${bank}/{maxbank}")
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deposit(self, ctx, amount):
        wallet, bank, maxbank = await self.get_balance(ctx.author)
        try:
            amount = int(amount)
        except ValueError:
            pass
        if type(amount) == str:
            if amount.lower() == "max" or amount.lower() == "all":
                amount = int(wallet)
        else:
            amount = int(amount)

        bank_res = await self.update_bank(ctx.author, amount)
        wallet_res = await self.update_wallet(ctx.author, -amount)
        
        if bank_res == 0 or wallet_res == 0:
            await ctx.send("No account has been found! Creating one for you now... (please wait 5 seconds before running this command again)")
        elif bank_res == 1:
            await ctx.send("Woah there champ! You have way to much money in your bank!")

        wallet, bank, maxbank = await self.get_balance(ctx.author)
        em = nextcord.Embed(title=f"{ctx.author.name}'s New Balance")
        em.add_field(name="New Wallet", value=f"${wallet}")
        em.add_field(name="New Bank", value=f"${bank}/{maxbank}")
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def give(self, ctx, member, amount: int):
        wallet, bank, maxbank = await self.get_balance(ctx.author)
        try:
            amount = int(amount)
        except ValueError:
            pass
        if type(amount) == str:
            if amount.lower() == "max" or amount.lower() == "all":
                amount = int(wallet)
        else:
            amount = int(amount)

        wallet_res = await self.update_wallet(ctx.author, -amount)
        wallet_res2 = await self.update_bank(member, amount)
        if wallet_res == 0 or wallet_res2 == 0:
            await ctx.send("No account has been found! Creating one for you now... (please wait 10 seconds before running this command again)")

        wallet2, bank2, maxbank2 = await self.get_balance(ctx.author)
        
        em = nextcord.Embed(title=f"Gave ${amount} to {member.name}")
        em.add_field(name=f"Wallet for {ctx.author.name}", value=f"${wallet}")
        em.add_field(name=f"Wallet for {member.name}", value=f"${wallet2}")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def shop(self, ctx):
        db = await aiosqlite.connect("db/bank.sqlite")
        em = nextcord.Embed(title="Shop", description="Nothing really works tbh")
        async with db.cursor() as cursor:
            await cursor.execute("SELECT name, desc, cost FROM shop")
            shop = await cursor.fetchall()
            for item in shop:
                em.add_field(name=f"{item[0]}", value=f"{item[1]} | Cost: ${item[2]}")
            await ctx.send(embed=em, view=ShopView(self.bot))

def setup(bot):
    bot.add_cog(Eco(bot))