# loop-revised

This is a revised version of the [loop-bot](https://github.com/Potatopy/loop-bot)

bot made by domain#0001 for .gg/loop (at least thats the future vanity)

**Note: This is not a fully completed project, and bugs WILL be present. If you find any, please report them in the support server.

## Features

- [x] Welcome system
- [x] An economy system (In Development)
- [x] A moderation system
- [x] Anime commands (NSFW + SFW)
- [x] A music system

And Many More To Come!

## Requirements

- Python 3.9 or higher
- A Discord Bot token
- A Lavalink host - (included but you can use your own)

## Setup

Run `setup.py` and follow the on-screen instructions!

## Common Issues

- `Connection Failure: Cannot connect to host (lavalink server) ssl:default [The remote computer refused the network connection]`: This is a common issue with Lavalink. It is caused by the host being down. You can either wait for it to come back up or use a different host. You can find a list of hosts [here](https://lavalink.darrennathanael.com/NoSSL/lavalink-without-ssl/)

- `nextcord.errors.LoginFailure: Improper token has been passed.` This is caused by an invalid token. Make sure you are using the correct token.

- `.env is in unreadable text format`: This is caused by the `.env` file being corrupted. Delete the `.env` file and run `setup.py` again.

- `nextcord is incompatible with discord.py`: This is caused by having both `discord.py` and `nextcord` installed. Uninstall `discord.py` by running `pip uninstall discord.py` and run `setup.py` again. And remove the original wavelink and install the one in the requirements.txt file.

If you still need help join the discord server and i'll try to help you out!

## Credits

[Glowstik](https://www.youtube.com/@glowstik) - for making almost all the code lmfao

[Civo](https://www.youtube.com/@CivoCode) - for coding the welcome system & anime commands 😏

[VoiceMaster](https://github.com/SamSanai/VoiceMaster-Discord-Bot) - the join to create system

[Me!](https://solo.to/wtr) - made the setup system and customized the UI

## Links

[MIT](https://choosealicense.com/licenses/mit/)

[Support](https://discord.gg/9j8qcsVFQX)

~~[Documentation](https://loop-3.gitbook.io/api-docs/)~~ removed since it's so simple.
