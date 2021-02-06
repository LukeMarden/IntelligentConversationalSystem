import discord
from discord.ext import tasks, commands
from knowledge_base import TrainBooking
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
    # elif(kb[message.author.id] is not None):
    elif (message.channel is await message.author.create_dm()):

#         process content in nlpu


        print(message.author)

    elif(message.content == '!book'):
        channel = await message.author.create_dm()
        kb[message.author.id] = TrainBooking()
        kb[message.author.id].knowledge = {'service':'book'}
        kb[message.author.id].reset()
        kb[message.author.id].run()
        await channel.send('Hello how can I help you? (book)')
    # elif(message.content == '!book'):
    elif(message.content == '!predict'):
        channel = await message.author.create_dm()
        kb[message.author.id] = TrainBooking()
        kb[message.author.id].knowledge = {'service': 'predict'}
        kb[message.author.id].reset()
        kb[message.author.id].run()
        await channel.send('Hello how can I help you? (predict)')
    else:
        print(message.content)

def runClient():
    client.run('Nzk2NzQxOTg0NDQ1NzkyMjc2.X_cVyw.-2yYSLY34sKpL3keAFzEjwAWgdU')

client.run('Nzk2NzQxOTg0NDQ1NzkyMjc2.X_cVyw.-2yYSLY34sKpL3keAFzEjwAWgdU')


# class DiscordUI:
#     def __init__(self):
#         self.client = commands.Bot(command_prefix = '!')
#         self.channel = self.client.get_channel(796742949223530519)
#
#     @client.event
#     async def on_ready():
#         print('Train bot is ready!')
#
#     @client.event
#     async def on_member_join(member):
#         print(f'Welcome (member)! How can I help?')
#
#     @client.event
#     async def on_member_remove(member):
#         print(f'(member) sad to see you go. Bye-bye!')
#
#     @client.command()
#     async def ping(ctx):
#         await ctx.send('pong')
#
#     @client.event
#     async def on_message(ctx, message):
#         ctx.channel
#         await ctx.process_commands(message)
#         print(message.content)
#     #     Add the nlpu stuff here
#
#     async def message(ctx, message):
#         # channel = client.get_channel(796742949223530519)
#         await ctx.send(message)
#         print(message)
#
#     # def runClient(self):
#     client.run('Nzk2NzQxOTg0NDQ1NzkyMjc2.X_cVyw.-2yYSLY34sKpL3keAFzEjwAWgdU')