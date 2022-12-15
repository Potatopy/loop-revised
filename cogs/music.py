import datetime
import discord
import wavelink
from discord.ext import commands
from wavelink.ext import spotify

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host="lavalink4africa.islantay.tk", port=8880, password="AmeliaWatsonisTheBest**!", spotify_client=spotify.SpotifyClient(client_id="b3ec1a336be5419a8f856a28c173e396", client_secret="cca55cffc7294c24a9c76285495e0a89"))

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node <{node.identifier}> is ready.")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        ctx = player.ctx
        vc: player = ctx.voice_client

        if vc.loop:
            return await vc.play(track)
        
        next_song = vc.queue.get()
        await vc.play(next_song)
        await ctx.send(f"now playing {next_song.title}")

    @commands.command(description="Plays a song from YouTube.", aliases=["p", "search"])
    async def play(self, ctx, *, search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("connect to a vc")
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty and vc.is_playing() == False:
            await vc.play(search)
            await ctx.send(f"now playing {search.title}")
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f"added `{search.title}` to the queue")
        vc.ctx = ctx
        setattr(vc, "loop", False)

    @commands.command(description="Pauses the current song.", aliases=["pa"])
    async def pause(self, ctx):
        if not ctx.voice_client:
            return await ctx.send("no music is in the queue")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("connect to a vc")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.pause()
        await ctx.send("paused")

    @commands.command(description="Resumes the current song.", aliases=["res", "r", "unpause"])
    async def resume(self, ctx):
        if not ctx.voice_client:
            return await ctx.send("no music is in the queue")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("connect to a vc")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.resume()
        await ctx.send("resumed")

    @commands.command(description="Disconnects the bot + Clears the queue.", aliases=["dc", "disconnect"])
    async def stop(self, ctx):
        if not ctx.voice_client:
            return await ctx.send("no music is in the queue")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("connect to a vc")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.disconnect()
        await ctx.send("disconnected. bye bye!")

    @commands.command(description="Repeat the current track", aliases=["l", "repeat"])
    async def loop(self, ctx):
        if not ctx.voice_client:
            return await ctx.send("no music is in the queue")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("connect to a vc")
        else:
            vc: wavelink.Player = ctx.voice_client

        try:
            vc.loop ^= True
        except Exception:
            setattr(vc, "loop", False)

        if vc.loop:
            return await ctx.send("looping")
        else:
            return await ctx.send("loop is disabled")

    @commands.command(description="View the current queue.", aliases=["q"])
    async def queue(self, ctx):
        if not ctx.voice_client:
            return await ctx.send("no music is in the queue")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("connect to a vc")
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty:
            return await ctx.send("no music is in the queue")

        em = discord.Embed(title="Queue")
        queue = vc.queue.copy()
        song_count = 0
        for song in queue:
            song_count += 1
            em.add_field(name=f"Song Num {song_count}", value=f"`{song.title}`")

        return await ctx.send(embed=em)

    @commands.command(description="Set the volume of the song", aliases=["vol"])
    async def volume(self, ctx, volume: int):
        if not ctx.voice_client:
            return await ctx.send("no music is in the queue")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("connect to a vc")
        else:
            vc: wavelink.Player = ctx.voice_client

        if volume > 100:
            return await ctx.send("volume can't be more than 100%")
        elif volume < 0:
            return await ctx.send("volume can't be less than 0%")

        await ctx.send(f"set volume to {volume}%")
        return await vc.set_volume(volume)

    @commands.command(description="Now playing", aliases=["np", "now_playing"])
    async def nowplaying(self, ctx):
        if not ctx.voice_client:
            return await ctx.send("no music is in the queue")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("connect to a vc")
        else:
            vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            return await ctx.send("no music is playing")

        em = discord.Embed(title=f"Now Playing {vc.track.title}", description=f"Artist: {vc.track.author}")
        em.add_field(name="Duration", value=f"`{str(datetime.timedelta(seconds=vc.track.length))}`")
        em.add_field(name="Volume", value=f"`{vc.volume}`")
        em.add_field(name="Link", value=f"[Click Here]({str(vc.track.uri)})")
        return await ctx.send(embed=em)

    @commands.command(description="Play a track with spotify")
    async def splay(self, ctx, *, search: str):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("connect to a vc")
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty and vc.is_playing() == False:
            try:
                track = await spotify.SpotifyTrack.search(query=search, return_first=True)
                await vc.play(track)
                await ctx.send(f"now playing {track.title}")
            except Exception as e:
                await ctx.send("no results found, please enter a song url from spotify")
                return print(e)
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f"added `{search.title}` to the queue")
        vc.ctx = ctx
        setattr(vc, "loop", False)

def setup(bot):
    bot.add_cog(Music(bot))