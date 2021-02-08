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
    question['question'] = 'destination'
    message = "Ipswich"
    info = extract_info(question, message, kb)
    print('kb ticket ', kb.service.destination)
    kb.reset()
    kb.run()
    print(kb.knowledge['response'])
    print(info)

    # class Greetings(KnowledgeEngine):
    #     @DefFacts()
    #     def _initial_action(self):
    #         yield Fact(action="greet")
    #
    #     @Rule(Fact(action='greet'), NOT(Fact(name=W())))
    #     def ask_name(self):
    #         self.declare(Fact(name=input("What's your name? ")))
    #
    #     @Rule(Fact(action='greet'), NOT(Fact(location=W())))
    #     def ask_location(self):
    #         self.declare(Fact(location=input("Where are you? ")))
    #
    #     @Rule(Fact(action='greet'), Fact(name=MATCH.name), Fact(location=MATCH.location))
    #     def greet(self, name, location):
    #         print("Hi %s! How is the weather in %s?" % (name, location))
    #
    #
    # engine = Greetings()
    # engine.reset()  # Prepare the engine for the execution.
    # engine.run()  # Run it!


    # #Discord
    # client.run('Nzk2NzQxOTg0NDQ1NzkyMjc2.X_cVyw.-2yYSLY34sKpL3keAFzEjwAWgdU')
    # client.ping()
