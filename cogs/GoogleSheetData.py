import discord
from discord.ext import commands
import gspread
import os
import pandas as pd
import operator

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

            text = df.set_index('Family Name')['CP'].to_dict()
            text = '\n'.join([f'`{key}{" " * (24 - len(key))}{value}`' for (key, value) in text.items()])

            # discord bot message design
            embed = discord.Embed(description = 
                f'{guild.upper()} has an average of **{average}** CP\n\n' 
                + '__**Family Name**__\n'
                + text, 
                color = discord.Color(0xe81300))
            embed.set_author(name=f'XVII Bot | {guild.upper()} CP', icon_url='https://cdn.discordapp.com/attachments/661862380996919325/693228158559977542/image0.jpg')


            await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send('No Guild Found!')


    @commands.command(name='family', aliases=['fam'])
    async def family(self, ctx, guild):
        try:
            df = self.get_data_frame(ctx, guild)

            df['Family CP'] = pd.to_numeric(df['Family CP'])
            df = df.sort_values('Family CP', ascending=False)

            text = df.set_index('Family Name')['Family CP'].to_dict()
            text = '\n'.join([f'`{key}{" " * (22 - len(key))}{value}`' for (key, value) in text.items()])

            # discord bot message design
            embed = discord.Embed(description = 
                '\n__**Family Name**__\n'
                + text, 
                color = discord.Color(0x08ffde))
            embed.set_author(name=f'XVII Bot | {guild.upper()} Family CP', icon_url='https://cdn.discordapp.com/attachments/661862380996919325/693228158559977542/image0.jpg')

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

            text = '\n'.join([f'`{key}{" " * (15 - len(key))}{value}`' for (key, value) in dict_desc.items()])

            # discord bot message design
            embed = discord.Embed(description = 
                '\n__**Statistics**__\n'
                + text, 
                color = discord.Color(0x8934ba))
            embed.set_author(name=f'XVII Bot | {guild.upper()} Strength', icon_url='https://cdn.discordapp.com/attachments/661862380996919325/693228158559977542/image0.jpg')


            await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send('No Guild Found!')

    @commands.command(name='class')
    async def bdm_class(self, ctx, guild):

        df = self.get_data_frame(ctx, guild)

        df['CP'] = pd.to_numeric(df['CP'])
        df = df.sort_values(['Class', 'CP'], ascending=False)

        # easier comparison
        df['Class'] = df['Class'].str.lower()

        # get the different type of class and count them up
        num_of_diff_class = df.groupby(df['Class']).size()
        class_dict = num_of_diff_class.to_dict()
        class_dict = dict(sorted(class_dict.items(), key=operator.itemgetter(1),reverse=True))

         # discord bot message design
        embed = discord.Embed(color = discord.Color(0xfdb8ff))
        embed.set_author(name=f'XVII Bot | {guild.upper()} Class', icon_url='https://cdn.discordapp.com/attachments/661862380996919325/693228158559977542/image0.jpg')

        # display the group of class
        for i in range(num_of_diff_class.count()): 
            filt = df['Class'].str.contains(list(class_dict.keys())[i])
            roles = df.loc[filt, ['Family Name', 'CP']]
            roles = roles.set_index('Family Name')['CP'].to_dict()
            roles = '\n'.join([f'`{key}{" " * (15 - len(key))}{value}`' for (key, value) in roles.items()])

            embed.add_field(name=f'__**{list(class_dict.keys())[i].title()}**__ - {list(class_dict.values())[i]}',value=roles, inline=True)

        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(GoogleSheetData(bot))
