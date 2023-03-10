import nextcord
from nextcord.ext import commands
from nextcord import File
from easy_pil import Editor, load_image_async, Font

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events cog is ready!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel

        background = Editor("public/welc/pic2.jpg")
        profile_image = await load_image_async(str(member.display_avatar))

        profile = Editor(profile_image).resize((150, 150)).circle_image()
        poppins = Font.poppins(size=50, variant="bold")

        poppins_small = Font.poppins(size=20, variant="light")

        background.paste(profile, (325, 90))
        background.ellipse((325, 90), 150, 150, outline="white", stroke_width=5)

        background.text((400, 260), f"Welcome to {member.guild.name}!", font=poppins, fill="#FFFFFF", align="center")
        background.text((400, 325), f"{member.name}#{member.discriminator}", font=poppins_small, fill="white", align="center")

        file = File(fp=background.image_bytes, filename="welcome.png")
        await channel.send(f"Welcome {member.mention} to {member.guild.name}", file=file)

def setup(bot):
    bot.add_cog(Events(bot))