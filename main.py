from knowledge_base import *
from nlpspacy import extract_info
from prediction import *
# from DiscrodBotPython.DiscordBot import *
# from web_scraper import *
# from nlpuspacy import *
# from discord.ext import commands

if __name__ == '__main__':
    print('testing')
    # #KB
    # engine = TrainBooking()
    # engine.knowledge = {}
    # engine.reset()  # Prepare the engine for the execution.
    # engine.run()  # Run it!
    # ticket = Ticket()
    # ticket.name = 'name'
    # ticket.isReturn = True
    # ticket.origin = 'Norwich'
    # ticket.destination = 'Ipswich'
    # ticket.departDate = '300121'
    # ticket.departTime = '0000'
    # ticket.returnDate = '020221'
    # ticket.returnTime = '0000'
    # print(ticket.find_cheapest())
    # pred = prediction('Norwich', 'London Liverpool Street', 9, 'Diss', 10, 1200) #check that it contains all these stations
    question = {}
    kb = TrainBooking()
    kb.knowledge = {'service': 'book'}
    kb.reset()
    kb.run()
    message = "Ipswich"
    info = extract_info(kb.knowledge, message, kb)
    kb.reset()
    kb.run()
    print(kb.knowledge['response'])
    message = "Norwich"
    info = extract_info(kb.knowledge, message, kb)
    kb.reset()
    kb.run()
    print(kb.knowledge['response'])
    message = "yes"
    info = extract_info(kb.knowledge, message, kb)
    kb.reset()
    kb.run()
    print(kb.knowledge['response'])
    message = "12 March 2021"
    info = extract_info(kb.knowledge, message, kb)
    kb.reset()
    kb.run()
    print(kb.knowledge['response'])
    message = "12:00"
    info = extract_info(kb.knowledge, message, kb)
    kb.reset()
    kb.run()
    print(kb.knowledge['response'])


    # #Discord
    # client.run('Nzk2NzQxOTg0NDQ1NzkyMjc2.X_cVyw.-2yYSLY34sKpL3keAFzEjwAWgdU')
    # client.ping()
