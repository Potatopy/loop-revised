import datetime
import nextcord
import wavelink
import os

from nextcord.ext import commands
from wavelink.ext import spotify
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("LAVALINK_HOST")
port = os.getenv("LAVALINK_PORT")
password = os.getenv("LAVALINK_PASSWORD")
p = os.getenv("PREFIX")

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host=host, port=port, password=password, spotify_client=spotify.SpotifyClient(client_id="b3ec1a336be5419a8f856a28c173e396", client_secret="cca55cffc7294c24a9c76285495e0a89"))

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node <{node.identifier}> is ready.')

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        ctx = player.ctx
        vc: player = ctx.voice_client

        if vc.loop:
            return await vc.play(track)
        
        next_song = vc.queue.get()
        await vc.play(next_song)
        await ctx.send(f"Now Playing: {next_song.title}")
    
    @commands.group()
    async def music(self, ctx):
        pass

    @music.command()
    async def help(self, ctx):
        em = nextcord.Embed(title="Music Help", description="**Commands**", color=0x00ff00)
        em.add_field(name=f"**{p}play**", value="Plays a song from youtube", inline=False)
        em.add_field(name=f"**{p}pause**", value="Pauses the current song", inline=False)
        em.add_field(name=f"**{p}resume**", value="Resumes the current song", inline=False)
        em.add_field(name=f"**{p}stop**", value="Stops the current song", inline=False)
        em.add_field(name=f"**{p}skip**", value="Skips the current song", inline=False)
        em.add_field(name=f"**{p}queue**", value="Shows the current queue", inline=False)
        em.add_field(name=f"**{p}loop**", value="Loops the current song", inline=False)
        em.add_field(name=f"**{p}nowplaying**", value="Shows the current song", inline=False)
        em.add_field(name=f"**{p}volume**", value="Sets the volume", inline=False)
        em.add_field(name=f"**{p}splay**", value="Plays a song from spotify", inline=False)
        await ctx.send(embed=em)
    
    @commands.command(aliases=['p'])
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not ctx.author.voice:
            return await ctx.send("you are not in a vc, join one")
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            await ctx.send(f"Now Playing: **{search.title}**")
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f"Added **{search.title}** to the queue")

        vc.ctx = ctx
        setattr(vc, "loop", False)

    @commands.command()
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
           return await ctx.send('play something first')
        elif not ctx.author.voice:
            return await ctx.send("you are not in a vc, join one")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.pause()
        await ctx.send('Paused!')

    @commands.command(aliases=['res'])
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
           return await ctx.send('play something first')
        elif not ctx.author.voice:
            return await ctx.send("you are not in a vc, join one")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.resume()
        await ctx.send('Resumed!')

    @commands.command(aliases=['dc', 'leave', 'disconnect'])
    async def stop(self, ctx: commands.Context):
        if not ctx.voice_client:
           return await ctx.send('play something first')
        elif not ctx.author.voice:
            return await ctx.send("you are not in a vc, join one")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.disconnect()
        await ctx.send('Bye Bye!')

    @commands.command(aliases=['l'])
    async def loop(self, ctx: commands.Context):
        if not ctx.voice_client:
           return await ctx.send('play something first')
        elif not ctx.author.voice:
            return await ctx.send("you are not in a vc, join one")
        else:
            vc: wavelink.Player = ctx.voice_client

        try:
            vc.loop ^= True
        except Exception:
            setattr(vc, "loop", False)

        if vc.loop:
            return await ctx.send("Looping is now enabled!")
        else:
            return await ctx.send("Looping is now disabled!")

    @commands.command()
    async def queue(self, ctx: commands.Context):
        if not ctx.voice_client:
           return await ctx.send('play something first')
        elif not ctx.author.voice:
            return await ctx.send("you are not in a vc, join one")
        vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty:
            return await ctx.send("Queue is empty!")

        em = nextcord.Embed(title="Queue", color=nextcord.Color.purple())

        queue = vc.queue.copy()
        songCount = 0
        for song in queue:
            songCount += 1
            em.add_field(name=f"Song {songCount}", value=f"{song.title}", inline=False)
        
        await ctx.send(embed=em)
    
    @commands.command(aliases=['vol'])
    async def volume(self, ctx: commands.Context, volume: int):
        if not ctx.voice_client:
           return await ctx.send('play something first')
        elif not ctx.author.voice:
            return await ctx.send("you are not in a vc, join one")
        else:
            vc: wavelink.Player = ctx.voice_client

        if volume > 100:
            return await ctx.send("Volume can't be more than 100!")
        elif volume < 0:
            return await ctx.send("Volume can't be less than 0!")
        else:
            await ctx.send(f"Set the volume to {volume}%")
            return await vc.set_volume(volume)

    @commands.command(aliases=['np'])
    async def nowplaying(self, ctx: commands.Context):
        if not ctx.voice_client:
           return await ctx.send('play something first')
        elif not ctx.author.voice:
            return await ctx.send("you are not in a vc, join one")
        else:
            vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            return await ctx.send("Nothing is playing!")

        em = nextcord.Embed(title=f"Now playing {vc.track.title}", description=f"Artisit: {vc.track.author}")
        em.add_field(name="Duration", value=f"`{str(datetime.timedelta(seconds=vc.track.length))}`")
        em.add_field(name="Info", value=f"Song URL: [Click Me]({str(vc.track.uri)})")
        return await ctx.send(embed=em)

    @commands.group()
    async def spotify(self, ctx: commands.Context):
        pass
    
    @spotify.command()
    async def play(self, ctx: commands.Context, *, search: str):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not ctx.author.voice:
            return await ctx.send("you are not in a vc, join one")
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty and not vc.is_playing():
            try:
                track = await spotify.SpotifyTrack.search(query=search, return_first=True)
                await vc.play(track)
                await ctx.send(f"Now Playing: **{track.title}**")
            except Exception as e:
                await ctx.send("No results found!, Try entering a Spotify URL")
                return print(e)
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f"Added **{search.title}** to the queue")

        vc.ctx = ctx
        if vc.loop:
            return
        setattr(vc, "loop", False)

def setup(bot):
    bot.add_cog(Music(bot))