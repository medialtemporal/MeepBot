import discord
import asyncio
from datetime import datetime
from datetime import timedelta
import discord.ext
from discord.ext import commands

# Bot token
TOKEN = 'insert token'

# Sets up a help command - very basic for now
help_command = commands.DefaultHelpCommand(no_category='Commands')

# Sets up client as a bot with prefix specified
client = commands.Bot(command_prefix=';', help_command=help_command)


@client.event
async def on_ready():
    """
    Prints to console and sets bot status
    """
    print("bot online")
    await client.change_presence(activity=discord.Game('pomodoro-ing'))


@client.command()
async def pomo(ctx, *arg):
    """
    Use ;pomo help for syntax.
    """
    try:
        arg = "".join(arg)  # Turning all args into one string
        # Help Command
        if 'help' in arg:
            await ctx.send('**Start Pomodoro:**\n'
                           'Use `;pomo [time in minutes]` to start a pomodoro session.\n\n'
                           '**Start Multi:**\n'
                           'Use `;multi [# of sessions] (# min work / # min break)` to run multiple work/break '
                           'pomodoro sessions in a row. Defaults to 25 min work /5 min break if you omit bracket '
                           'arguments.\n\n'
                           '**Join a Group Session:**\n'
                           'React to any `;pomo` or `;multi` command to be added to that study session and get pinged '
                           'when the session is complete.\n\n '
                           'DM @sora#7079 with any questions or suggestions!')
        # Basic single pomodoro command
        elif arg:
            try:
                pomodoro_time = int(arg.strip())  # If the argument is an integer (as specified) we get the time value
                # If argument is not an integer, an exception (ValueError) gets raised at this point
                if pomodoro_time > 250:  # If time requested is greater than 250 minutes
                    raise OverflowError  # Raise OverflowError and specify that user should enter a value under 250

                # Group study feature
                await ctx.send(f'{ctx.author.name} has started a Pomodoro session! React to the original message to '
                               f'join in.')
                group_members = []
                string_to_ping = ""
                async with ctx.channel.typing():
                    await asyncio.sleep(5)  # Adds a 5-second delay for other users to react to the Pomodoro message

                # Starting Pomodoro
                ping_time = time_delta(pomodoro_time)  # Calculates the appropriate time in the future to ping user
                await ctx.send(f'Pomodoro started for **{pomodoro_time}** minutes! '
                               f'You will be pinged at {ping_time}.')
                await asyncio.sleep(pomodoro_time * 60)  # Minutes to seconds conversion for asyncio

                # Group Study
                if ctx.message.reactions:
                    for reaction in ctx.message.reactions:
                        member_list = await reaction.users().flatten()
                        for member in member_list:
                            if ctx.author != member and member not in member_list:
                                group_members.append(member.id)
                    string_to_ping = ""
                    for member in group_members:
                        temp = " <@" + str(member) + ">"
                        string_to_ping = string_to_ping + temp

                await ctx.send(f'Pomodoro completed, {ctx.author.mention}{string_to_ping}!')
            except ValueError:
                await ctx.send('Please enter an integer value in minutes. Use `;pomodoro help` for commands help.')
            except OverflowError:
                await ctx.send('Please enter an integer value smaller than 250.')
    except TypeError:
        print('type error')


@pomo.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"", description=f"Try again in {error.retry_after:.2f}s.")
        await ctx.send(embed=em)


@client.command()
async def multi(ctx, sessions, *timing):
    """
    Use ;pomo help for syntax.
    """
    try:
        pomodoro_length = 25
        break_length = 5
        if "(" in sessions:
            raise TypeError
        else:
            sessions = int(sessions)
            if len(timing):
                if "(" in timing[0]:
                    pomodoro_length, break_length = custom_times(timing[0])
                else:
                    raise TypeError
            else:
                await ctx.send('Defaulting to 25 min work/5 min break.')

        # Group study feature
        await ctx.send(f'Added **{sessions}** pomodoro sessions. React to the original message to join in with '
                       f'{ctx.author.name}!')
        group_members = []
        async with ctx.channel.typing():
            await asyncio.sleep(5)  # Adds a 5-second delay for other users to react to the Pomodoro message

        session = 1
        print(pomodoro_length)
        print(break_length)
        string_to_ping = ""
        for i in range(sessions):
            ping_time = time_delta(pomodoro_length)
            await ctx.send(f'Starting pomodoro session **#{session}**, {ctx.author.mention}. '
                           f'You will be pinged for a break at {ping_time}!')
            await asyncio.sleep(int(pomodoro_length) * 60)

            # Group Study
            if ctx.message.reactions:
                for reaction in ctx.message.reactions:
                    member_list = await reaction.users().flatten()
                    for member in member_list:
                        if ctx.author != member and member not in member_list:
                            group_members.append(member.id)
                string_to_ping = ""
                for member in group_members:
                    temp = " <@" + str(member) + ">"
                    string_to_ping = string_to_ping + temp

            break_ping = time_delta(break_length)
            if i < (sessions - 1):
                await ctx.send(f'Pomodoro **#{session}** completed, {ctx.author.mention}{string_to_ping}! '
                               f'Break until {break_ping}.')
                await asyncio.sleep(int(break_length) * 60)
            session += 1
        await ctx.send(f'Congrats, {ctx.author.mention}{string_to_ping}! '
                       f'You completed **{sessions}** pomodoro sessions.')
    except TypeError:
        await ctx.send('You messed up the syntax somehow. Try `;pomo help` to see the proper syntax.')


# HELPER FUNCTIONS

def time_delta(pomodoro_time):
    """
    Takes in a duration of time in minutes. Returns the time in EST after that duration, in 24hr format.
    """
    now = datetime.now()
    time_change = timedelta(minutes=int(pomodoro_time))
    ping_time = now + time_change
    ping_time = ping_time.strftime("%H:%M")
    return ping_time


def custom_times(message):
    """
    pass it string in format ([study time]/[break time]) and get back study and break time
    """
    message = message.strip("()")
    study_and_break = message.split('/')
    custom_study = study_and_break[0]
    custom_break = study_and_break[1]
    return custom_study, custom_break


client.run(TOKEN)
