import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '')

@client.event
async def on_ready():
    print('Train bot is ready!')

@client.event
async def on_member_join(member):
    print(f'Welcome (member)! How can I help?')

@client.event
async def on_member_remove(member):
    print(f'(member) sad to see you go. Bye-bye!')

@client.command()
async def ping(ctx):
    await ctx.send('pong')

client.run('Nzk2NzQxOTg0NDQ1NzkyMjc2.X_cVyw.-2yYSLY34sKpL3keAFzEjwAWgdU')
