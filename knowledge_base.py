from experta import *
from webscrape3 import *
from prediction import *
import json
from random import choice
# from experta.watchers import RULES, AGENDA

class Ticket(Fact):
    def __init__(self):
        # self.name = None
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
        url += self.departDate + '/' + self.departTime + '/dep/'
        if (self.isReturn is True):
            url += self.returnDate + '/' + self.returnTime + '/dep/'
            print(url)
        return url

    def find_location_code(self, station):
        stations = json.load(open('train_codes.json', 'r'))
        return stations[station]

    def find_cheapest(self):
        cheapestTicket = CheapestTicket(self.generate_ticket_url(), self.isReturn)
        cheapest = cheapestTicket.find_cheapest_ticket()
        return cheapest

class Delay(Fact):
    def __init__(self):
        self.origin = None
        self.destination = None
        self.delay = None
        self.numberOfStops = None
        self.delayStation = None
        self.arrivalTime = None
        self.delayCode = None

    def predict_delay(self):
        self.delayPrediction = prediction(self.origin, self.destination, self.numberOfStops,
                                self.delayStation, self.delay, self.arrivalTime)
        return self.delayPrediction.time

class TrainBooking(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        self.ticket = Ticket()
        yield Fact(action="greet")

        if not 'question' in self.knowledge:
            self.knowledge['question'] = str()

    # @Rule(Fact(action='greet'), NOT(Fact(name=W())))
    #     # def ask_name(self):
    #     #     self.declare(Fact(name=input("What's your name? ")))
    #     #
    #     # @Rule(Fact(action='greet'), NOT(Fact(location=W())))
    #     # def ask_location(self): self.declare(Fact(location=input("Where are you? ")))
    #     #
    #     # @Rule(Fact(action='greet'), Fact(name=MATCH.name),
    #     #       Fact(location=MATCH.location))
    #     # def greet(self, name, location):
    #     #     print("Hi %s! How is the weather in %s?" % (name, location))

    # @Rule(Fact(action='greet'), NOT(Fact(name=W())))
    # def name(self):
    #     print("test")
    #     if self.ticket.name is not None:
    #         self.declare(Fact(name = self.ticket.name))
    #         self.knowledge['name'] = self.ticket.name
    #     else:
    #         if self.knowledge['question'] == 'askName':
    #             return 'ask name'
    #             # Message.emit_feedback('display received message', 'unknown_message')
    #         else:
    #             self.knowledge['question'] = 'askName'
    #             return 'ask name'
    #             # Message.emit_feedback('display received message', 'ask_name')

    # @Rule(Fact(action='greet'), Fact(name = MATCH.name))
    # def service(self):
    #     print("TEST")
    #     if self.knowledge['question'] == 'askService':
    #         print("AskService1")
    #         # Message.emit_feedback('display received message', 'unknown_message')
    #     else:
    #         self.knowledge['question'] = 'askService'
    #         print("AskService2")
    #         # Message.emit_feedback('display received message', 'ask_booking')

    @Rule(NOT(Fact(destination=W())), NOT(Fact(origin=W())))
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

    @Rule(Fact(destination=MATCH.destination), NOT(Fact(origin=W())))
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

    @Rule(Fact(action='predict'), NOT(Fact(delay=W())))
    def askDelay(self):
        if self.knowledge['question'] == 'delayTime':
            print()
        else:
            self.knowledge['question'] = 'delayTime'
            print()

    @Rule(Fact(action='predict'), Fact(delay=MATCH.delayTime), NOT(Fact(numberOfStops=W())))
    def askNumberOfStops(self):
        if self.knowledge['question'] == 'numberOfStops':
            print()
        else:
            self.knowledge['question'] = 'numberOfStops'
            print()

    @Rule(Fact(action='predict'), Fact(delay=MATCH.delayTime), Fact(delay=MATCH.numberOfStops),
          NOT(Fact(delayStation=W())))
    def askDelayStation(self):
        if self.knowledge['question'] == 'delayStation':
            print()
        else:
            self.knowledge['question'] = 'delayStation'
            print()

    @Rule(Fact(action='predict'), Fact(delay=MATCH.delayTime), Fact(delay=MATCH.numberOfStops),
          Fact(delayStation=MATCH.delayStation), NOT(Fact(arrivalTime=W())))
    def askArrivalTime(self):
        if self.knowledge['question'] == 'arrivalTime':
            print()
        else:
            self.knowledge['question'] = 'arrivalTime'
            print()

    @Rule(Fact(action='predict'), Fact(delay=MATCH.delayTime), Fact(delay=MATCH.numberOfStops),
          Fact(delayStation=MATCH.delayStation), Fact(arrivalTime=MATCH.arrivalTime), NOT(Fact(delayCode=W())))
    def askDelayCode(self):
        if self.knowledge['question'] == 'delayCode':
            print()
        else:
            self.knowledge['question'] = 'delayCode'
            print()

    @Rule(Fact(action='predict'), Fact(delay=MATCH.delayTime), Fact(delay=MATCH.numberOfStops),
          Fact(delayStation=MATCH.delayStation), Fact(arrivalTime=MATCH.arrivalTime), Fact(delayCode=MATCH.delayCode))
    def predict(self):
        if self.knowledge['question'] == 'delayCode':
            print()
        else:
            self.knowledge['question'] = 'delayCode'
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

