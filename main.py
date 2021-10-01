# GNU GENERAL PUBLIC LICENSE

# Version 3, 29 June 2007

# Copyright (C) 2021 AbHiK Inc.

# Everyone is permitted to copy and distribute verbatim copies of this
# license document, but changing it is not allowed.

# If anyone wants to use it for profitable or personal use than please contack us at our email.

# Author --> Abhinav Kulkarni
# Email --> abhivbk13@gmail.com


import discord
from discord.ext import commands
import youtube_dl
import os
from youtubesearchpython import VideosSearch
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix="!")

youtube_dl.utils.bug_reports_message = lambda:''



@bot.event
async def on_ready():
    print(f"{bot.user} is Online and is in the following SERVERS \n {bot.guilds}\n")

@bot.command()
async def play(ctx, song_name:str):
    #joining voice channel
    try:
        if not ctx.message.author.voice:
            await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
            return
        else:
            channel = ctx.message.author.voice.channel
            print(channel)
        await channel.connect()

    except Exception as e:
        print(e)

    #downloadind the song
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3") # If already song is downloaded delete it
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voice = ctx.message.guild.voice_client

    # Preferences for Youtube video download
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    await ctx.send(f"Searching... for :mag_right: {song_name}")

    # Searching fot the song on youtube
    videosSearch = VideosSearch(song_name, limit = 1)
    results = str(videosSearch.result())
    partial_url = results[results.index('https://www.youtube.com/watch?') + 1:]
    partial_url = partial_url[:partial_url.index("'") ]
    url = str('h' + partial_url)

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")
                        voice.play(discord.FFmpegPCMAudio("song.mp3"))
                        await ctx.send(f'Playing {url}')

    except Exception as e:
        print(e)

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
        await ctx.send("OK leaving the Voice Channel")
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    try:
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
            await ctx.send("Song Paused. To resume the song just type '!resume'")
        else:
            await ctx.send("The bot is not playing anything at the moment.")
    except Exception as e:
        print(e)
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    try:
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
            await ctx.send("Song resumed. To pause the song just type '!pause'")

        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")
    except Exception as e:
        print(e)

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    try:
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
            await ctx.send("Song Stopped")
        else:
            await ctx.send("The bot is not playing anything at the moment.")
    except Exception as e:
        print(e)

if __name__ == "__main__" :
        bot.run(TOKEN)

