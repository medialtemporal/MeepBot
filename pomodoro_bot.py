import discord
import asyncio
from datetime import datetime
from datetime import timedelta
import discord.ext
from discord.ext import commands
import random
import os
from discord.ext.commands import cooldown, BucketType

TOKEN = 'insert token here'

help_command = commands.DefaultHelpCommand(no_category='Commands')

client = commands.Bot(command_prefix=';', help_command=help_command)


@client.event
async def on_ready():
    print("bot online")
    await client.change_presence(activity=discord.Game('pomodoro-ing'))


@client.command()
async def pomo(ctx, *arg):
    """
    Use ;pomo help for syntax.
    """
    try:
        arg = "".join(arg)
        # Help Command
        if 'help' in arg:
            await ctx.send('**Start Pomodoro:**\n'
                           'Use `;pomo [time in minutes]` to start a pomodoro session.\n\n'
                           '**Start Multi:**\n'
                           'Use `;multi [# of sessions] (# min work / # min break)` to run multiple work/break '
                           'pomodoro sessions in a row. Defaults to 25 min work /5 min break if you omit bracket '
                           'arguments.\n\n'
                           'DM @sora#7079 with any questions or suggestions!')
        # Basic single pomodoro command
        elif arg:
            try:
                pomodoro_time = int(arg.strip())
                if pomodoro_time > 500:
                    raise OverflowError
                ping_time = time_delta(pomodoro_time)

                await ctx.send(f'Pomodoro started for **{pomodoro_time}** minutes! '
                               f'You will be pinged at {ping_time}.')
                # this plus while loop is new
                stop = False
                i = 0
                while not stop and i < (pomodoro_time):
                    print('while looping')
                    msg = await client.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=5)
                    if msg.content == ";stop":
                        await ctx.send(f'Cancelling pomodoro for {msg.author.display_name}.')
                        print('cancelled pomo')
                        stop = True
                    await asyncio.sleep(1)
                    i += 1
                # await asyncio.sleep(int(pomodoro_time) * 60)
                await ctx.send(f'Pomodoro completed, {ctx.author.mention}!')
            except ValueError:
                await ctx.send('Please enter an integer value in minutes. Use `;pomodoro help` for commands help.')
            except OverflowError:
                await ctx.send('Please enter an integer value smaller than 500.')
    except TypeError:
        print('type error')


@pomo.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"", description=f"Try again in {error.retry_after:.2f}s.")
        await ctx.send(embed=em)


@client.command()
async def stop(ctx):
    return


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
        await ctx.send(f'Added **{sessions}** pomodoro sessions.\n')
        session = 1
        print(pomodoro_length)
        print(break_length)
        for i in range(sessions):
            ping_time = time_delta(pomodoro_length)
            await ctx.send(f'Starting pomodoro session **#{session}**, {ctx.author.mention}. '
                           f'You will be pinged for a break at {ping_time}!')
            await asyncio.sleep(int(pomodoro_length) * 60)
            break_ping = time_delta(break_length)
            if i < (sessions - 1):
                await ctx.send(f'Pomodoro **#{session}** completed, {ctx.author.mention}! '
                               f'Break until {break_ping}.')
                await asyncio.sleep(int(break_length) * 60)
            session += 1
        await ctx.send(f'Congrats, {ctx.author.mention}! '
                       f'You completed **{sessions}** pomodoro sessions.')
    except TypeError:
        await ctx.send('You messed up the syntax somehow. Try `;pomo help` to see the proper syntax.')


@client.command()
async def seica(ctx):
    """
    parallelograms are eternal
    """
    await ctx.send(random.choice(seica_choices))


@client.command()
async def engineer(ctx):
    """
    ingegnere
    """
    if ctx.author == client.user:
        return
    else:
        await ctx.send("https://tenor.com/view/engineer-joke-working-gif-11519872")


@client.command()
async def norbert(ctx):
    """
    corb
    """
    await ctx.send('https://cdn.discordapp.com/attachments/695289756082372670/816706807073865748/unknown.png')


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


seica_choices = [
    'https://media.discordapp.net/attachments/734673462865690675/759141838677868564/seicagod.png',
    'https://media.discordapp.net/attachments/713560205887275022/757693374760484964/seicaegypt.png',
    'https://cdn.discordapp.com/attachments/695289756082372670/761056869074468885/unknown.png',
    'https://cdn.discordapp.com/attachments/731289549551960104/773265984085164042/video0.mp4',
    'https://cdn.discordapp.com/attachments/731289549551960104/775852662880731176/Seicasong2.mp4',
    'https://media.discordapp.net/attachments/752358887872790630/780133600162480189/seica20heart.gif',
    'https://cdn.discordapp.com/attachments/731289549551960104/788166482445992006/ugly.png',
    'https://cdn.discordapp.com/attachments/827329952353091594/855265691292663818/image_2.png',
    'https://cdn.discordapp.com/attachments/772125589393375303/774495156778172427/seica_swiming.mp4',
    '"Are we not made by the madness that we find in forbidden texts, touched by the warp that Seica created? '
    'Betwixst curses and unfathomable horror, Seica has given us insight. we are made by the parallelogram, '
    'we exist by the parallelogram, we are unmade by the parallelogram"',
    'https://cdn.discordapp.com/attachments/765391827280461834/772667806855987230/video0.mov',
    'https://cdn.discordapp.com/attachments/731289549551960104/770992342848241694'
    '/final_5f98fcfb953837009934bceb_655557.mp4 ',
    'https://cdn.discordapp.com/attachments/695289756082372670/857460416980713482/image0.png',
]

client.run(TOKEN)
