import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()

client = commands.Bot(command_prefix = "x!")
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="x!help"))
    print('Server up')

@client.command()
async def help(ctx):
    embed = discord.Embed(description='Every command start with `x!`',color = discord.Color(0xecf00e))
    embed.set_author(name='XVII Bot | Help', icon_url='https://cdn.discordapp.com/attachments/661862380996919325/693228158559977542/image0.jpg')
    embed.add_field(name='__**Guild CP**__', value='**x!cp guild**\nExample: `x!cp xvii`', inline=False)
    embed.add_field(name='__**Guild Family CP**__', value='**x!family guild or x!fam guild**\nExample: `x!fam xvii`', inline=False)
    embed.add_field(name='__**Guild Strength**__', value='**x!strength guild or x!str guild**\nExample: `x!str xvii`', inline=False)
    embed.add_field(name='__**Guild Class**__', value='**x!class guild**\nExample: `x!class xvii`', inline=False)
    embed.add_field(name='__**Node War**__', value='Example: `x!node role` or `x!node all`', inline=False)
    await ctx.channel.send(embed=embed)


extensions = ['cogs.GoogleSheetData']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)

client.run(os.getenv('TOKEN'))
