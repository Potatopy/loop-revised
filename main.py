import discord_ios
import random, os, signal, time, sys
import nextcord
import colorama

from dotenv import load_dotenv
from nextcord.ext import commands
from pypresence import Presence
from colorama import Fore

load_dotenv()
TOKEN = os.getenv("TOKEN")
prefix = os.getenv("PREFIX")
client_id = "1065077133703135283"

rpc = Presence(client_id)
rpc.connect()

while True:
    rpc.update(
        large_image="og",
        state="Get this project on GitHub!",
        party_id="Version",
        party_size=[1, 1],
        start=int(time.time()),
        buttons=[
            {"label": "Github Project", "url": "https://github.com/Potatopy/loop-revised"}
        ]
    )

    intents = nextcord.Intents.all()
    activity = nextcord.Activity(type=nextcord.ActivityType.competing, name=f"{prefix}help")
    bot = commands.AutoShardedBot(command_prefix=prefix, intents=intents, activity=activity, help_command=None)

    for fn in os.listdir("./cogs"):
        if fn.endswith(".py"):
            bot.load_extension(f"cogs.{fn[:-3]}")

    @bot.event
    async def on_ready():
        print("\n" * 100)
        print(Fore.CYAN + """

                    ██████╗░░█████╗░████████╗░█████╗░████████╗░█████╗░  ██████╗░░█████╗░████████╗
                    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗╚══██╔══╝██╔══██╗  ██╔══██╗██╔══██╗╚══██╔══╝
                    ██████╔╝██║░░██║░░░██║░░░███████║░░░██║░░░██║░░██║  ██████╦╝██║░░██║░░░██║░░░
                    ██╔═══╝░██║░░██║░░░██║░░░██╔══██║░░░██║░░░██║░░██║  ██╔══██╗██║░░██║░░░██║░░░
                    ██║░░░░░╚█████╔╝░░░██║░░░██║░░██║░░░██║░░░╚█████╔╝  ██████╦╝╚█████╔╝░░░██║░░░
                    ╚═╝░░░░░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░  ╚═════╝░░╚════╝░░░░╚═╝░░░

                    © 2023 by h3lped
    """)
        print(Fore.GREEN + f"Bot is ready || Logged in as {bot.user} ID: {bot.user.id}")
        print("RPC is ready")
        print("-----------------")

    bot.run(TOKEN)

    if KeyboardInterrupt():
        print(Fore.WHITE +"\n[!] Shutting down...")
        print("[<3] Thanks for using the bot!\n")
        exit()
    elif nextcord.errors.LoginFailure("Improper token has been passed."):
        print("[!] Invalid token!")
        exit()
    elif ('.env') == None:
        print("[!] .env file is missing! Please run setup.py first!")
        exit()