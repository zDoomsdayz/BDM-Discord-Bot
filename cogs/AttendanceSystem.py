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
    @commands.has_any_role('XVII', 'XVLL')
    async def cpoll(self, ctx):
        self.count_down.cancel()
    @cpoll.error
    async def cpoll_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.channel.send('**Members Only!**')

    @commands.command()
    @commands.has_any_role('XVII', 'XVLL')
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
                embed.set_footer(text=f'⏰ Time Left: {self.time_left}hrs')
                await msg.edit(embed=embed)
                await asyncio.sleep(1)

            self.count_down.stop()

            embed.set_footer(text=f'⏰ Time Left: Ended')
            await msg.edit(embed=embed)
        except:
            await ctx.channel.send('Remember to include Quotation mark, Command: x!poll "Question" "Roles(Case-sensitive)" "Hours(Default 24hrs if didnt include)"\nExample: `x!poll "Do you watch anime?" "XVII" 48`')
    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.channel.send('**Members Only!**')
def setup(bot):
    bot.add_cog(AttendanceSystem(bot))
