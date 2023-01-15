import time

print("\n" * 100)
print("Welcome to the setup process!")
time.sleep(5)
token = input("Please Enter your bot token: ")
prefix = input("Please enter your bot prefix: ")

if token is None:
    print("You need to enter a token!")
    time.sleep(5)
    exit()
elif prefix is None:
    print("You need to enter a prefix!")
    time.sleep(5)
    exit()

try:
    config = f"""TOKEN={token}
PREFIX={prefix}"""

    print("Installing dependancies...")
    os.system("pip install -r requirements.txt")
    print("Installed!")
    print("Creating .env file...")
    open('./.env', 'w').write(config)
    print("Created!")
    print("Setup complete!")
    print("Starting bot...")
    print("\n" * 100)
    os.system("python main.py")
except Exception as e:
    print("Oops something went wrong!" + str(e))
    time.sleep(5)
    exit()