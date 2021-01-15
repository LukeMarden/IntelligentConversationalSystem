from experta import *
import json
from random import choice
# from experta.watchers import RULES, AGENDA

class Ticket(Fact):
    def __init__(self):
        self.name = None
        self.isReturn = None
        self.origin = None
        self.destination = None
        self.departTime = None
        self.departDate = None
        self.returnTime = None
        self.returnDate = None

    def generate_ticket_url(self):
        url = 'https://ojp.nationalrail.co.uk/service/timesandfares/'
        url += self.find_location_code(self.origin) + '/'
        url += self.find_location_code(self.destination) + '/'
        url += self.departDate + '/' + self.departTime + 'dep/'
        if (self.isReturn is True):
            url += self.returnDate + '/' + self.returnTime + '/' + 'dep/'
        return url

    def find_location_code(self, station):
        stations = json.load(open('train_codes.json', 'r'))
        print(stations[station])


class TrainBooking(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        self.ticket = Ticket()
        yield Fact(action="greet")

        if not 'question' in self.knowledge:
            self.knowledge['question'] = str()

    # @Rule(Fact(action='greet'), NOT(Fact(name=W())))
    # def ask_name(self):
    #     self.declare(Fact(name=input("What's your name? ")))
    #
    # @Rule(Fact(action='greet'), NOT(Fact(location=W())))
    # def ask_location(self): self.declare(Fact(location=input("Where are you? ")))
    #
    # @Rule(Fact(action='greet'), Fact(name=MATCH.name),
    #       Fact(location=MATCH.location))
    # def greet(self, name, location):
    #     print("Hi %s! How is the weather in %s?" % (name, location))

    @Rule(Fact(action='greet'), NOT(Fact(name=W())))
    def name(self):
        print("test")
        if self.ticket.name is not None:
            self.declare(Fact(name = self.ticket.name))
            self.knowledge['name'] = self.ticket.name
        else:
            if self.knowledge['question'] == 'askName':
                return 'ask name'
                # Message.emit_feedback('display received message', 'unknown_message')
            else:
                self.knowledge['question'] = 'askName'
                return 'ask name'
                # Message.emit_feedback('display received message', 'ask_name')

    @Rule(Fact(action='greet'), Fact(name = MATCH.name))
    def service(self):
        print("TEST")
        if self.knowledge['question'] == 'askService':
            print("AskService1")
            # Message.emit_feedback('display received message', 'unknown_message')
        else:
            self.knowledge['question'] = 'askService'
            print("AskService2")
            # Message.emit_feedback('display received message', 'ask_booking')

    @Rule(Fact(action='book'), NOT(Fact(destination=W())), NOT(Fact(origin=W())))
    def destination(self):
        if self.ticket.destination is not None:
            self.declare(Fact(destination = self.ticket.destination))
            self.knowledge['destination'] = self.ticket.destination
        else:
            if self.knowledge['question'] == 'destination':
                print()
            else:
                self.knowledge['question'] = 'destination'
                print()

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination), NOT(Fact(origin=W())))
    def origin(self):
        if self.ticket.origin is not None:
            self.declare(Fact(destination = self.ticket.origin))
            self.knowledge['destination'] = self.ticket.origin
        else:
            if self.knowledge['question'] == 'origin':
                print()
            else:
                self.knowledge['question'] = 'origin'
                print()

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), NOT(Fact(isReturn=W())))
    def isReturn(self):
        if self.ticket.destination is not None:
            self.declare(Fact(isReturn = self.ticket.isReturn))
            self.knowledge['return'] = self.ticket.isReturn
        else:
            if self.knowledge['question'] == 'return':
                print()
            else:
                self.knowledge['question'] = 'return'
                print()

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=MATCH.isReturn),
          NOT(Fact(departDate=W())), NOT(Fact(departTime=W())))
    def departDate(self):
        if self.ticket.departDate is not None:
            self.declare(Fact(departDate=self.ticket.departDate))
            self.knowledge['departDate'] = self.ticket.departDate
        else:
            if self.knowledge['question'] == 'departDate':
                print()
            else:
                self.knowledge['question'] = 'departDate'
                print()

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=MATCH.isReturn),
          Fact(departDate=MATCH.departDate), NOT(Fact(departTime=W())))
    def departTime(self):
        if self.ticket.departTime is not None:
            self.declare(Fact(departTime=self.ticket.departTime))
            self.knowledge['departTime'] = self.ticket.departTime
        else:
            if self.knowledge['question'] == 'departTime':
                print()
            else:
                self.knowledge['question'] = 'departTime'
                print()

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=True),
          Fact(departDate=MATCH.departDate), Fact(departTime=MATCH.departTime),
          NOT(Fact(returnDate=W())), NOT(Fact(returnTime=W())))
    def returnDate(self):
        if self.ticket.returnDate is not None:
            self.declare(Fact(returnDate=self.ticket.returnDate))
            self.knowledge['returnDate'] = self.ticket.returnDate
        else:
            if self.knowledge['question'] == 'returnDate':
                print()
            else:
                self.knowledge['question'] = 'returnDate'
                print()

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=True),
          Fact(departDate=MATCH.departDate), Fact(departTime=MATCH.departTime),
          Fact(returnDate=MATCH.returnDate), NOT(Fact(returnTime=W())))
    def returnTime(self):
        if self.ticket.returnTime is not None:
            self.declare(Fact(returnTime=self.ticket.returnTime))
            self.knowledge['returnTime'] = self.ticket.returnTime
        else:
            if self.knowledge['question'] == 'returnTime':
                print()
            else:
                self.knowledge['question'] = 'returnTime'
                print()

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=False),
          Fact(departDate=MATCH.departDate), Fact(departTime=MATCH.departTime))
    def singleTicket(self):
        if self.knowledge['question'] == 'singleTicket':
            print()
        else:
            self.knowledge['question'] = 'singleTicket'
            print()

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=True),
          Fact(departDate=MATCH.departDate), Fact(departTime=MATCH.departTime),
          Fact(returnDate=MATCH.returnDate), Fact(returnTime=MATCH.returnTime))
    def returnTicket(self):
        if self.knowledge['question'] == 'returnTicket':
            print()
        else:
            self.knowledge['question'] = 'returnTicket'
            print()

def process_entities(ticket):
    engine.Ticket = ticket
    engine.reset()
    engine.run()




if __name__ == '__main__':
    engine = TrainBooking()
    engine.knowledge = {}
    engine.reset()  # Prepare the engine for the execution.
    engine.run() # Run it!

