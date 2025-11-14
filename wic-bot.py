#made by Lucia Ulate, Reva Mahesh, Honey Patel and Emily Messenger

import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import yt_dlp
import asyncio

# Load token and guild
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1438688578560593980

# Intents
intents = discord.Intents.default()
intents.message_content = True

# Bot
bot = commands.Bot(command_prefix="!", intents=intents)



# ---------------------- YTDLP SEARCH --------------------------

async def search_ytdlp_async(query, ydl_opts):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, lambda: _extract(query, ydl_opts)
    )

def _extract(query, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query, download=False)



# ---------------------- EVENTS --------------------------------

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    synced = await bot.tree.sync(guild=guild)
    print(f"Synced {len(synced)} commands for guild {GUILD_ID}")
    print(f"{bot.user} is ready to serve!")



@bot.event
async def on_message(msg):

    # Ignore bot messages
    if msg.author.bot:
        return

    # Ignore system messages (joins, boosts, pins, etc.)
    if msg.type != discord.MessageType.default:
        return

    # Ignore messages with only images/files
    if not msg.content or msg.content.strip() == "":
        return

    # Respond only to real user text
    await msg.channel.send(
        f'Like the great philosopher {msg.author.mention} once said: "{msg.content}"'
    )

    # Allow prefix commands (e.g. !play)
    await bot.process_commands(msg)

    # Allow slash commands (e.g. /greet)
    await bot.process_application_commands(msg)



# ---------------------- SLASH COMMANDS -------------------------

@bot.tree.command(name="greet", description="say HALLO!!! to someone")
async def greet(interaction: discord.Interaction):
    username = interaction.user.mention
    await interaction.response.send_message("HALLO!!! " + username)


@bot.tree.command(name="play", description="Play a song from YouTube")
async def play(interaction: discord.Interaction, song_query: str):

    await interaction.response.defer()

    # User must be in voice channel
    if interaction.user.voice is None:
        await interaction.followup.send("You must be in a voice channel.")
        return

    voice_channel = interaction.user.voice.channel
    voice_client = interaction.guild.voice_client

    # Connect or move to proper channel
    if voice_client is None:
        voice_client = await voice_channel.connect()
    elif voice_client.channel != voice_channel:
        await voice_client.move_to(voice_channel)

    # Correct YT-DLP options
    ydl_options = {
        "format": "bestaudio[abr<=96]/bestaudio",
        "noplaylist": True,
        "youtube_include_dash_manifest": False,
        "youtube_include_hls_manifest": False,
    }

    query = "ytsearch1:" + song_query
    results = await search_ytdlp_async(query, ydl_options)
    tracks = results.get("entries", [])

    if not tracks:
        await interaction.followup.send("No results found.")
        return

    first_track = tracks[0]
    audio_url = first_track["url"]
    title = first_track.get("title", "untitled")

    ffmpeg_options = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn"
    }

    # Play audio
    source = discord.FFmpegOpusAudio(
        audio_url,
        executable=r"C:\Users\lucia\OneDrive\Documents\Code\discord-bot\WIC_Discord_Bot\bin\ffmpeg\ffmpeg.exe",
        **ffmpeg_options
    )

    voice_client.play(source)

    await interaction.followup.send(f"🎵 Now playing **{title}**!")



# ---------------------- RUN BOT -------------------------------

bot.run(TOKEN)
