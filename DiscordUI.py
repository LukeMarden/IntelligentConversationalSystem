from discord.ext import commands
from nlpspacy import *
client = commands.Bot(command_prefix = '!')
kb = {}

# when the bot is running the console is given this message
@client.event
async def on_ready():
    channel = client.get_channel(796742949223530519)
    print('Train bot is ready!')

# when the user joins they are prompted with these messages
@client.event
async def on_member_join(member):
    channel = client.get_channel(796742949223530519)
    await channel.send(f'Welcome {member}! How can I help?')
    await channel.send('Type \'!book\' to begin the booking process')
    await channel.send('Type \'!predict\' to begin the prediction process')
    await channel.send('Type \'!help\' for help')

# When the user leaves the channel they are sent this message
@client.event
async def on_member_remove(member):
    channel = client.get_channel(796742949223530519)
    await channel.send(f' {member} sad to see you go. Bye-bye!')

# When the user messages the bot this function activates
@client.event
async def on_message(message):
    channel = client.get_channel(796742949223530519)
    if (message.channel is await message.author.create_dm()): #checks if the message is a direct message or not
        channel = message.channel
        if message.author.id in kb: #Checks that the user has a knowledge base
            #This checks that the users input is valid and decodes it
            info = extract_info(kb[message.author.id].knowledge, message.content, kb[message.author.id])
            if (info != 1):
                await channel.send('Invalid response please try again.')
            #This finds the next output based on the users input
            kb[message.author.id].reset()
            kb[message.author.id].run()
            await channel.send(kb[message.author.id].knowledge['response'])
        else:
            #Printed if the users input is not valid
            await channel.send('Can you please go to the main channel and give the bot a command')

    elif(message.content == '!book'): #Starts the booking process
        channel = await message.author.create_dm()
        kb[message.author.id] = TrainBooking()
        kb[message.author.id].knowledge = {'service':'book'} #lets the kb know that the service is to book
        kb[message.author.id].reset()
        kb[message.author.id].run()
        await channel.send(kb[message.author.id].knowledge['response'])
    elif(message.content == '!predict'): #Starts the prediction process
        channel = await message.author.create_dm()
        kb[message.author.id] = TrainBooking()
        kb[message.author.id].knowledge = {'service': 'predict'} #lets the kb know that the service is to predict
        kb[message.author.id].reset()
        kb[message.author.id].run()
        await channel.send(kb[message.author.id].knowledge['response'])
    elif (message.content == '!help'): #Prompt to help the user understand how to use the system
        await channel.send('Type \'!book\' to begin the booking process')
        await channel.send('Type \'!predict\' to begin the prediction process')
    else:
        print(message.content)

def runClient():
    client.run('Nzk2NzQxOTg0NDQ1NzkyMjc2.X_cVyw.-2yYSLY34sKpL3keAFzEjwAWgdU')

client.run('Nzk2NzQxOTg0NDQ1NzkyMjc2.X_cVyw.-2yYSLY34sKpL3keAFzEjwAWgdU')