import os
import platform
import discord
from discord.ext import commands
import youtube_dl
from cogs.search import Search

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.voice_channel = None
        self.song_url = None
        self.song_title = None
        self.song = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.client.user.name}")
        print(f"Discord.py API version: {discord.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        print("-------------------")

        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                                    name='your Commands'))

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel")
        if ctx.voice_client is None:
            self.voice_channel = ctx.author.voice.channel
            await ctx.send("Joined You Voice channel")
            await self.voice_channel.connect()
        else:
            await ctx.send("Joined You Voice channel")
            await ctx.voice_client.move_to(self.voice_channel)

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from the Voice Channel")

    @commands.command()
    async def play(self, ctx):
        self.song = ctx.message.content.replace("!play", "").strip()
        # self.song = self.song.replace("!play", "")
        print(self.song)
        if ctx.voice_client is None:
            await ctx.send("I am not in any Voice channel. Call me By '\Join' command")

        search_engine = Search()
        self.song_title, self.song_url = search_engine.getYt_song(self.song)
        ctx.voice_client.stop()

        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}

        voice_channel = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(self.song_url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, executable='bin/ffmpeg.exe')
            await ctx.send(f"Now Playing {self.song_title} --> {self.song_url}")
            voice_channel.play(source)

        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,
                                                                    name=self.song_title))

    @commands.command()
    async def pause(self, ctx):
        await ctx.send("PAUSED ⏸")
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                                    name='your Commands'))
        await ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        await ctx.send("RESUMED ⏯")
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,
                                                                    name=self.song_title))
        await ctx.voice_client.resume()



def setup(client):
    client.add_cog(music(client))
