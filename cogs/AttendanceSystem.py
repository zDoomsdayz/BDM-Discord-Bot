import discord
from discord.ext import tasks, commands
import asyncio
import time

class AttendanceSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time_left = 24

    @tasks.loop(hours=1.0)
    async def count_down(self):
        self.time_left -= 1

    @commands.command()
    @commands.has_any_role('Officer')
    async def cpoll(self, ctx):
        self.count_down.cancel()
    @cpoll.error
    async def cpoll_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.channel.send('**Officer Only!**')

    @commands.command()
    @commands.has_any_role('Officer')
    async def poll(self, ctx, question, discord_role, hours=24):

        try:
            ''' Wait for discord api 1.4
            if self.count_down.is_running():
                await ctx.channel.send('Current event is running, please wait for it to end.')
                return'''

            #temp cancel all task while waiting for discord 1.4
            self.count_down.cancel()

            role = discord.utils.get(ctx.guild.roles, name=discord_role)

            g_member = []
            yes = []
            no = []
            no_responds = []

            # discord bot message design
            embed = discord.Embed(description =f':loudspeaker: **{question}**', color = discord.Color(0xd2f700))
            embed.set_author(name='XVII Bot | Poll', icon_url='https://cdn.discordapp.com/attachments/661862380996919325/693228158559977542/image0.jpg')
            embed.add_field(name='\u200b', value='**✅ Yes - 0**', inline=False)
            embed.add_field(name='\u200b', value='**❌ No - 0**', inline=False)
            embed.add_field(name='\u200b', value='**Waiting for Responds - 0**', inline=False)
            embed.set_footer(text=f'⏰ Time Left: ')
            msg = await ctx.channel.send(embed=embed)

            await msg.add_reaction('✅')
            await msg.add_reaction('❌')

            self.time_left = hours + 1
            self.count_down.start()

            while self.time_left > 0:
                
                embed.clear_fields()
                g_member.clear()
                yes.clear()
                no.clear()
                no_responds.clear()

                try:
                    message = await ctx.channel.fetch_message(msg.id)
                except:
                    return

                for member in ctx.guild.members:
                    if role in member.roles:
                        if member.display_name not in g_member:
                            g_member.append(member.display_name)

                for reaction in message.reactions:
                    async for user in reaction.users():
                        if reaction.emoji == '✅':
                            if user.display_name not in yes:
                                yes.append(user.display_name)

                        if reaction.emoji == '❌':
                            if user.display_name not in no:
                                no.append(user.display_name)

                for num in g_member:
                    if num not in yes and num not in no:
                        no_responds.append(num)
                        
                embed.add_field(name='\u200b', value=f'**✅ Yes - {len(yes) - 1}**\n{", ".join(yes[1:])}', inline=False)
                embed.add_field(name='\u200b', value=f'**❌ No - {len(no) - 1}**\n{", ".join(no[1:])}', inline=False)
                embed.add_field(name='\u200b', value=f'**Waiting for Responds - {len(no_responds)}**\n{", ".join(no_responds)}', inline=False)
                embed.set_footer(text=f'⏰ Time Left: {self.time_left} hrs')
                await msg.edit(embed=embed)
                await asyncio.sleep(3)

            self.count_down.stop()

            embed.set_footer(text=f'⏰ Time Left: Ended')
            await msg.edit(embed=embed)
        except:
            await ctx.channel.send('Remember to include Quotation mark, Command: x!poll "Question" "Roles(Case-sensitive)" "Hours(Default 24hrs if didnt include)"\nExample: `x!poll "Do you watch anime?" "XVII" 48`')
    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.channel.send('**Officer Only!**')


    @commands.command()
    @commands.has_any_role('Officer')
    async def pollv2(self, ctx, question, *options: str):
        if len(options) <= 1:
            await ctx.channel.send('Error! Please have at least 1 option.')
            return
        if len(options) > 10:
            await ctx.channel.send('Too much options')
            return

        if len(options) == 2 and options[0].lower() == 'yes' and options[1].lower() == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for i, option in enumerate(options):
            description += f'\n {reactions[i]} {option.title()}'

        embed = discord.Embed(title=f'**{question.title()}**', description=''.join(description), color = discord.Color(0xd2f700))
        embed.set_author(name='XVII Bot | Poll v2', icon_url='https://cdn.discordapp.com/attachments/661862380996919325/693228158559977542/image0.jpg')
        msg = await ctx.channel.send(embed=embed)

        for reaction in reactions[:len(options)]:
            await msg.add_reaction(reaction)
        embed.set_footer(text=f'Poll ID: {msg.id}')
        await msg.edit(embed=embed)
    @poll.error
    async def poll2_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.channel.send('**Officer Only!**')

    @commands.command()
    async def result(self, ctx, discord_channel, id):
        try:
            discord_channel_cleanup = int(str(discord_channel)[2:-1])
            c = discord.utils.get(ctx.guild.channels, id=discord_channel_cleanup)

            user_dict = {}

            message = await c.fetch_message(id)

            # get the emoji used and add them to dict collection
            for reaction in message.reactions:
                async for user in reaction.users():
                    if user.display_name != 'XVII':
                        if reaction.emoji not in user_dict.keys():
                            user_dict[reaction.emoji] = []
                    
                        user_dict.setdefault(reaction.emoji, []).append(user.display_name)

            embed = discord.Embed(color = discord.Color(0xd2f700))
            embed.set_author(name='XVII Bot | Result', icon_url='https://cdn.discordapp.com/attachments/661862380996919325/693228158559977542/image0.jpg')

            for k, v in user_dict.items():
                if len(v) > 0:
                    embed.add_field(name='\u200b', value=f'**{k} - {len(v)}**\n{", ".join(v)}', inline=False)

            msg = await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send('No ID Found!')

    @commands.command()
    async def dr(self, ctx, discord_channel, discord_role, id):
        try:
            discord_channel_cleanup = int(str(discord_channel)[2:-1])
            c = discord.utils.get(ctx.guild.channels, id=discord_channel_cleanup)

            g_member = []
            member_react = []
            member_didnt_react = []

            message = await c.fetch_message(id)

            role = discord.utils.get(ctx.guild.roles, name=discord_role)

            for member in ctx.guild.members:
                if role in member.roles:
                    g_member.append(member.display_name)

            for reaction in message.reactions:
                async for user in reaction.users():
                    if user.display_name not in member_react:
                        member_react.append(user.display_name)

            for num in g_member:
                if num not in member_react:
                    member_didnt_react.append(num)

            embed = discord.Embed(color = discord.Color(0xd2f700))
            embed.set_author(name='XVII Bot | Didn\'t React', icon_url='https://cdn.discordapp.com/attachments/661862380996919325/693228158559977542/image0.jpg')
            embed.add_field(name='\u200b', value=f'**React - {len(member_react)}**\n{", ".join(member_react)}', inline=False)
            embed.add_field(name='\u200b', value=f'**Didn\'t React - {len(member_didnt_react)}**\n{", ".join(member_didnt_react)}', inline=False)

            msg = await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send('No ID Found!')

    @commands.command()
    async def vc(self, ctx, discord_role):
        try:
            g_member = []
            member_vc = []
            member_didnt_vc = []
            channel_dict = {}

            voice_channel_list = ctx.guild.voice_channels
            role = discord.utils.get(ctx.guild.roles, name=discord_role)
            
            for member in ctx.guild.members:
                if role in member.roles:
                    g_member.append(member.display_name)

            for voice_channels in voice_channel_list:
                if len(voice_channels.members) != 0:
                    for members in voice_channels.members:
                        member_vc.append(members.display_name)
                        channel_dict.setdefault(voice_channels.name, []).append(members.display_name)

            for num in g_member:
                if num not in member_vc:
                    member_didnt_vc.append(num)

            embed = discord.Embed(color = discord.Color(0xfbe8ff))
            embed.set_author(name='XVII Bot | Voice Chat', icon_url='https://cdn.discordapp.com/attachments/661862380996919325/693228158559977542/image0.jpg')

            for k, v in channel_dict.items():
                embed.add_field(name='\u200b', value=f'**{k} - {len(v)}**\n{", ".join(v)}', inline=False)

            embed.add_field(name='\u200b', value=f'**Not In Any Voice Channel - {len(member_didnt_vc)}**\n{", ".join(member_didnt_vc)}', inline=False)

            msg = await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send('Wrong Command')

    @commands.command(name='discord', aliases=['dis'])
    @commands.has_any_role('Officer')
    async def discord(self, ctx, discord_role):
        try:
            g_member = []

            if discord_role == 'Everyone':
                for member in ctx.guild.members:
                        g_member.append(member.display_name)

            else:
                role = discord.utils.get(ctx.guild.roles, name=discord_role)

                for member in ctx.guild.members:
                    if role in member.roles:
                        g_member.append(member.display_name)

                if len(g_member) == 0:
                    await ctx.channel.send('No Such Roles ¯\\_(ツ)_/¯')
                    return

            g_member.sort()

            # discord bot message design
            embed = discord.Embed(description = f'**{discord_role} - {len(g_member)}**\n{", ".join(g_member)}', color = discord.Color(0xd2f700))
            embed.set_author(name=f'XVII Bot | Roles', icon_url='https://cdn.discordapp.com/attachments/661862380996919325/693228158559977542/image0.jpg')
            msg = await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send('Wrong Command')
    @poll.error
    async def discord_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.channel.send('**Officer Only!**')

def setup(bot):
    bot.add_cog(AttendanceSystem(bot))
