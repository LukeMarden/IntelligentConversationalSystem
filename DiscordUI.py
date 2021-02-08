import discord
from discord.ext import tasks, commands
from knowledge_base import TrainBooking
from nlpspacy import *
import asyncio
client = commands.Bot(command_prefix = '!')
kb = {}


@client.event
async def on_ready():
    channel = client.get_channel(796742949223530519)
    print('Train bot is ready!')
    # await channel.send('Train bot is ready!')

@client.event
async def on_member_join(member):
    channel = client.get_channel(796742949223530519)
    await channel.send(f'Welcome {member}! How can I help?')
    await channel.send('Type \'!book\' to begin the booking process')
    await channel.send('Type \'!predict\' to begin the prediction process')
    await channel.send('Type \'!help\' for help')

@client.event
async def on_member_remove(member):
    channel = client.get_channel(796742949223530519)
    await channel.send(f' {member} sad to see you go. Bye-bye!')

# @client.command()
# async def ping(ctx):
#     await ctx.send('pong')

@client.event
async def on_message(message):
    channel = client.get_channel(796742949223530519)
    # print(message.channel)
    # print(await message.author.create_dm())
    if message.content == '!ping':
        channel.send('pong')
    elif (message.channel is await message.author.create_dm()):
        channel = message.channel
        if message.author.id in kb:
            info = extract_info(kb[message.author.id].knowledge, message.content, kb[message.author.id])
            if (info != 1):
                await channel.send('Invalid response please try again.')
            kb[message.author.id].reset()
            kb[message.author.id].run()
            await channel.send(kb[message.author.id].knowledge['response'])
        else:
            await channel.send('Can you please go to the main channel and give the bot a command')

    elif(message.content == '!book'):
        channel = await message.author.create_dm()
        kb[message.author.id] = TrainBooking()
        kb[message.author.id].knowledge = {'service':'book'}
        kb[message.author.id].reset()
        kb[message.author.id].run()
        await channel.send(kb[message.author.id].knowledge['response'])
    elif(message.content == '!predict'):
        channel = await message.author.create_dm()
        kb[message.author.id] = TrainBooking()
        kb[message.author.id].knowledge = {'service': 'predict'}
        kb[message.author.id].reset()
        kb[message.author.id].run()
        await channel.send(kb[message.author.id].knowledge['response'])
    elif (message.content == '!help'):
        await channel.send('Type \'!book\' to begin the booking process')
        await channel.send('Type \'!predict\' to begin the prediction process')
    else:
        print(message.content)

def runClient():
    client.run('Nzk2NzQxOTg0NDQ1NzkyMjc2.X_cVyw.-2yYSLY34sKpL3keAFzEjwAWgdU')

client.run('Nzk2NzQxOTg0NDQ1NzkyMjc2.X_cVyw.-2yYSLY34sKpL3keAFzEjwAWgdU')