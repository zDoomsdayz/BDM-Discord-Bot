import discord
from discord.ext import commands
import gspread
import os
import pandas as pd

class GoogleSheetData(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cp(self, ctx, guild):

        try: # try to open google sheet
            gc = gspread.service_account(filename='credentials.json')
            sh = gc.open_by_key(os.getenv('SHEETKEY'))

            try: # try to retrieve data
                worksheet = sh.worksheet(guild.upper())

                average = worksheet.cell(3, 6).value

                guild_data = worksheet.get('B5:E53')
                headers = guild_data.pop(0)
                df = pd.DataFrame(guild_data, columns=headers)
                # convert string to int
                df['CP'] = pd.to_numeric(df['CP'])
                df = df.sort_values('CP', ascending=False)

                # discord bot message design
                embed = discord.Embed(title = f'{guild.upper()} CP', description = f'{guild.upper()} has an average of {average} CP', color = discord.Color.blue())
                # embed.set_thumbnail(url=ctx.guild.icon_url)
                embed.add_field(name='__**Family Name**__', value=df['Family Name'].to_string(index=False), inline=True)
                embed.add_field(name='__**CP**__', value=df['CP'].to_string(index=False), inline=True)

                await ctx.channel.send(embed=embed) 
            except:
                await ctx.channel.send('No Guild Found!')
        except:
            await ctx.channel.send('Unable to open googlesheet!')


    @commands.command()
    async def family(self, ctx, guild):

        try: # try to open google sheet
            gc = gspread.service_account(filename='credentials.json')
            sh = gc.open_by_key(os.getenv('SHEETKEY'))

            try: # try to retrieve data
                worksheet = sh.worksheet(guild.upper())

                guild_data = worksheet.get('B5:F53')
                headers = guild_data.pop(0)
                df = pd.DataFrame(guild_data, columns=headers)
                # convert string to int
                df['Family CP'] = pd.to_numeric(df['Family CP'])
                df = df.sort_values('Family CP', ascending=False)

                # discord bot message design
                embed = discord.Embed(title = f'{guild.upper()} CP', color = discord.Color.red())
                embed.add_field(name='__**Family Name**__', value=df['Family Name'].to_string(index=False), inline=True)
                embed.add_field(name='__**Family CP**__', value=df['Family CP'].to_string(index=False), inline=True)

                await ctx.channel.send(embed=embed) 
            except:
                await ctx.channel.send('No Guild Found!')
        except:
            await ctx.channel.send('Unable to open googlesheet!')

def setup(bot):
    bot.add_cog(GoogleSheetData(bot))
