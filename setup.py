# ik its a mess this was kinda rushed lmao

import time
import os

print('\n' * 100)
print("""

██████╗░░█████╗░████████╗░█████╗░████████╗░█████╗░  ░██████╗███████╗████████╗██╗░░░██╗██████╗░
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗╚══██╔══╝██╔══██╗  ██╔════╝██╔════╝╚══██╔══╝██║░░░██║██╔══██╗
██████╔╝██║░░██║░░░██║░░░███████║░░░██║░░░██║░░██║  ╚█████╗░█████╗░░░░░██║░░░██║░░░██║██████╔╝
██╔═══╝░██║░░██║░░░██║░░░██╔══██║░░░██║░░░██║░░██║  ░╚═══██╗██╔══╝░░░░░██║░░░██║░░░██║██╔═══╝░
██║░░░░░╚█████╔╝░░░██║░░░██║░░██║░░░██║░░░╚█████╔╝  ██████╔╝███████╗░░░██║░░░╚██████╔╝██║░░░░░
╚═╝░░░░░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░  ╚═════╝░╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░░░

© 2023 by h3lped
""")
print("[*] Note: You ONLY run this file once. \n")
TOKEN = input("[?] Your Discord Token: ")
prefix = input("[?] What would you like your prefix to be: ")

lavalink = input("[?] Would you like to use your own lavalink server? (y/n): ")
if lavalink.lower() == "y" or lavalink.lower() == "yes":
    lavalink_host = input("Lavalink Host: ")
    lavalink_port = input("Lavalink Port: ")
    lavalink_password = input("Lavalink Password: ")
elif lavalink.lower() == "n" or lavalink.lower() == "no":
    lavalink_host = "lavalink4africa.islantay.tk" # Default Lavalink Server
    lavalink_port = 8800
    lavalink_password = "AmeliaWatsonisTheBest**!"
    print("[*] Added default lavalink server!")

if TOKEN is None:
    print("Please Insert A Discord Token")
    exit()
elif prefix is None:
    print("Please Insert A Prefix")
    exit()
elif lavalink is None:
    print("Please reply with yes or no")
    exit()

try:
    config = f"""# Main Bot Config
TOKEN={TOKEN}
PREFIX={prefix}

# Lavalink Config
LAVALINK_HOST="{lavalink_host}"
LAVALINK_PORT={lavalink_port}
LAVALINK_PASSWORD="{lavalink_password}"
"""
    print("[*] Installing Dependancies...")
    os.system('pip install -r requirements.txt')
    print("\n" * 100)
    print("[*] Dependancies Installed!")
    print("[*] Creating .env file...")
    open('./.env', 'w').write(config)
    print("\n[*] Created .env file!")
    time.sleep(3)
    print("[!] Running the bot...")
    print("[*] Note: From now on only run main.py \n[*] All Settings can be changed in the .env file!")
    os.system('py main.py')
except Exception as e:
    print("\n[!] An error occured while creating the config file!\n" + str(e))
    exit()