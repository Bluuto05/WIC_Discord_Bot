#made by Lucia Ulate, Reva Mahesh, Honey Patel

import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} ready to serve.')

@bot.event
async def on_message(msg):
    if msg.author.id != bot.user.id:
        await msg.channel.send(f'Like the great philosopher {msg.author.mention} once said: "{msg.content}"')


@bot.tree.command(name="greet", description="say HALLO!!! to someone")
async def greet(interaction: discord.Interaction):
    username = interaction.user.mention
    await interaction.response.send_message("HALLO!!! " + username)





#insert play code here

#insert queue code here

# insert other code here
bot.run(TOKEN)