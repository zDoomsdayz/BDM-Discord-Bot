import discord
from discord.ext import commands
import gspread
import os
import pandas as pd

class GoogleSheetData(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_data_frame(ctx, guild):

        # login and open google sheet
        gc = gspread.service_account(filename='credentials.json')
        sh = gc.open_by_key(os.getenv('SHEETKEY'))

        # go to that worksheet
        worksheet = sh.worksheet(guild.upper())

        # create a dataframe from the data here
        guild_data = worksheet.get('B5:F53')
        headers = guild_data.pop(0)
        df = pd.DataFrame(guild_data, columns=headers)

        return df

    @commands.command()
    async def cp(self, ctx, guild):
        try:
            df = self.get_data_frame(ctx, guild)

            df['CP'] = pd.to_numeric(df['CP'])
            df = df.sort_values('CP', ascending=False)

            average = round(df['CP'].mean()).astype(int)

            # discord bot message design
            embed = discord.Embed(description = f'{guild.upper()} has an average of {average} CP', color = discord.Color(0xe81300))
            embed.set_author(name=f'XVII Bot | {guild.upper()} CP', icon_url='https://cdn.discordapp.com/attachments/661862380996919325/693228158559977542/image0.jpg')
            # embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name='__**Family Name**__', value=df['Family Name'].to_string(index=False), inline=True)
            embed.add_field(name='__**CP**__', value=df['CP'].to_string(index=False), inline=True)

            await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send('No Guild Found!')


    @commands.command(name='family', aliases=['fam'])
    async def family(self, ctx, guild):
        try:
            df = self.get_data_frame(ctx, guild)

            df['Family CP'] = pd.to_numeric(df['Family CP'])
            df = df.sort_values('Family CP', ascending=False)

            # discord bot message design
            embed = discord.Embed(color = discord.Color(0x08ffde))
            embed.set_author(name=f'XVII Bot | {guild.upper()} Family CP', icon_url='https://cdn.discordapp.com/attachments/661862380996919325/693228158559977542/image0.jpg')
            embed.add_field(name='__**Family Name**__', value=df['Family Name'].to_string(index=False), inline=True)
            embed.add_field(name='__**Family CP**__', value=df['Family CP'].to_string(index=False), inline=True)

            await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send('No Guild Found!')

    @commands.command(name='strength', aliases=['str'])
    async def strength(self, ctx, guild):
        try:
            df = self.get_data_frame(ctx, guild)

            df['CP'] = pd.to_numeric(df['CP'])

            # use pandas build-in function to calculate the stats then convert it to dict
            dict_desc = df['CP'].describe()
            dict_desc = dict_desc.round(0).astype(int)
            dict_desc = dict_desc.to_dict()

            dKeys = '\n'.join(list(dict_desc.keys()))
            dValue = '\n'.join(map(str, list(dict_desc.values())))

            # discord bot message design
            embed = discord.Embed(color = discord.Color(0x8934ba))
            embed.set_author(name=f'XVII Bot | {guild.upper()} Strength', icon_url='https://cdn.discordapp.com/attachments/661862380996919325/693228158559977542/image0.jpg')
            embed.add_field(name='__**Stats**__',value=dKeys, inline=True)
            embed.add_field(name='__**Value**__',value=dValue, inline=True)

            await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send('No Guild Found!')

def setup(bot):
    bot.add_cog(GoogleSheetData(bot))
