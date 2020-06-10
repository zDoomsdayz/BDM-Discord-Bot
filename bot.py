import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()

client = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Testing123'))
    print('Server up')

extensions = ['cogs.GoogleSheetData']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)

client.run(os.getenv('TOKEN'))
