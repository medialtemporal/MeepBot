import discord
import asyncio
from datetime import datetime
from datetime import timedelta
from token import TOKEN

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')


client = MyClient()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('pomodoro-ing'))


@client.event
async def on_message(message):
    # Help Command
    if message.content.startswith(';pomodoro help'):
        await message.channel.send('**Start Pomodoro:**\n'
                                   'Use `;pomodoro [time in minutes]` to start a pomodoro '
                                   'session.\n\n'
                                   '**Start Multi:**\n'
                                   'Use `;pomodoro multi [# of sessions] (# min work / # min break)` to run multiple '
                                   'work/break pomodoro sessions in a row. Defaults to 25 min work /5 min break if '
                                   'you omit bracket arguments.\n\n '
                                   'DM @sora#7079 with any questions or suggestions!')
    # Multiple Sessions
    elif message.content.startswith(';pomodoro multi'):
        sessions = number_of_sessions(message)
        custom_study = False
        break_length = 5
        if "(" in message.content:
            custom_study, break_length = custom_times(message, sessions)
        await message.channel.send(f'Added **{sessions}** pomodoro sessions.\n')
        session = 1
        for i in range(sessions):
            pomodoro_time, ping_time = default_time(25)
            if custom_study:
                pomodoro_time = custom_study
                ping_time = default_time(pomodoro_time)[1]
            await message.channel.send(f'Starting pomodoro session **#{session}**, {message.author.mention}. '
                                       f'You will be pinged for a break at {ping_time}!')
            await asyncio.sleep(int(pomodoro_time) * 60)
            break_ping = break_time(break_length)
            if i < (sessions - 1):
                await message.channel.send(f'Pomodoro **#{session}** completed, {message.author.mention}! '
                                           f'Break until {break_ping}.')
            await asyncio.sleep(int(break_length) * 60)
            session += 1
        await message.channel.send(f'Congrats, {message.author.mention}! '
                                   f'You completed **{sessions}** pomodoro sessions.')
    # One session, custom time
    elif message.content.startswith(';pomodoro'):
        pomodoro_time, ping_time = time_delta(message)
        await message.channel.send(f'Pomodoro started for **{pomodoro_time}** minutes! '
                                   f'You will be pinged at {ping_time}.')
        await asyncio.sleep(int(pomodoro_time) * 60)
        await message.channel.send(f'Pomodoro completed, {message.author.mention}!')


def time_delta(message):
    pomodoro_time = []
    counter = 0
    for i in message.content:
        if 9 < counter:
            pomodoro_time.append(i)
        counter += 1
    pomodoro_time = "".join(pomodoro_time)
    if pomodoro_time == 0:
        pomodoro_time = 25
    now = datetime.now()
    time_change = timedelta(minutes=int(pomodoro_time))
    ping_time = now + time_change
    ping_time = ping_time.strftime("%H:%M")
    return pomodoro_time, ping_time


def default_time(pomodoro_time):
    now = datetime.now()
    time_change = timedelta(minutes=int(pomodoro_time))
    ping_time = now + time_change
    ping_time = ping_time.strftime("%H:%M")
    return pomodoro_time, ping_time


def break_time(break_length):
    now = datetime.now()
    time_change = timedelta(minutes=int(break_length))
    ping_time = now + time_change
    ping_time = ping_time.strftime("%H:%M")
    return ping_time


def number_of_sessions(message):
    sessions = []
    counter = 0
    for i in message.content:
        if 14 < counter < 18:
            sessions.append(i)
        counter += 1
    sessions = int("".join(sessions))
    if sessions == 0:
        sessions += 2
    return sessions


def custom_times(message, sessions):
    message = message.content.removeprefix(f';pomodoro multi {sessions} ')
    message = message.strip('()')
    study_and_break = message.split('/')
    custom_study = study_and_break[0]
    custom_break = study_and_break[1]
    return custom_study, custom_break


client.run(TOKEN)
