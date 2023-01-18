import discord_ios
import random, os, signal, time, sys
import nextcord

from dotenv import load_dotenv
from nextcord.ext import commands
from pypresence import Presence

load_dotenv()
TOKEN = os.getenv("TOKEN")
prefix = os.getenv("PREFIX")
client_id = "1065077133703135283"

rpc = Presence(client_id)
rpc.connect()

while True:
    rpc.update(
        large_image="og",
        large_text="Running Potato Bot!",
        state="Get this project on GitHub! (Click the button!)",
        start=int(time.time()),
        buttons=[
            {"label": "Github Project", "url": "https://github.com/Potatopy/loop-revised"}
        ]
    )

    intents = nextcord.Intents.all()
    activity = nextcord.Activity(type=nextcord.ActivityType.competing, name=f"{prefix}help")
    bot = commands.Bot(command_prefix=prefix, intents=intents, activity=activity, help_command=None)

    for fn in os.listdir("./cogs"):
        if fn.endswith(".py"):
            bot.load_extension(f"cogs.{fn[:-3]}")

    @bot.event
    async def on_ready():
        print("\n" * 100)
        print("""

    ██████╗░░█████╗░████████╗░█████╗░████████╗░█████╗░  ██████╗░░█████╗░████████╗
    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗╚══██╔══╝██╔══██╗  ██╔══██╗██╔══██╗╚══██╔══╝
    ██████╔╝██║░░██║░░░██║░░░███████║░░░██║░░░██║░░██║  ██████╦╝██║░░██║░░░██║░░░
    ██╔═══╝░██║░░██║░░░██║░░░██╔══██║░░░██║░░░██║░░██║  ██╔══██╗██║░░██║░░░██║░░░
    ██║░░░░░╚█████╔╝░░░██║░░░██║░░██║░░░██║░░░╚█████╔╝  ██████╦╝╚█████╔╝░░░██║░░░
    ╚═╝░░░░░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░  ╚═════╝░░╚════╝░░░░╚═╝░░░

    © 2023 by h3lped
    """)
        print(f"Bot is ready || Logged in as {bot.user} ID: {bot.user.id}")
        print("RPC is ready")
        print("-----------------")

    @bot.command
    async def help(self, ctx):
        embed = nextcord.Embed(title="Help", description=f"All Help Commands\nJust run `{p}(category) help` All available categories are below", color=nextcord.Color.blue())
        embed.add_field(name="**Music**", value=f"{p}music help", inline=False)
        embed.add_field(name="**Utility**", value=f"{p}util help", inline=False)
        embed.add_field(name="**Level**", value=f"{p}level help", inline=False)
        embed.add_field(name="**Voice**", value=f"{p}voice help", inline=False)
        embed.set_footer(text="More categories will be added soon!")
        await ctx.send(embed=embed)

    bot.run(TOKEN)

    if KeyboardInterrupt():
        print("\n[!] Shutting down...")
        print("[<3] Thanks for using the bot!\n")
        quit()
    elif nextcord.errors.LoginFailure("Improper token has been passed."):
        print("[!] Invalid token!")
        quit()