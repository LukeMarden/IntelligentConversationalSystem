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
        self.knowledge['question'] = None
        self.ticket = Ticket()
        self.delay = Delay()
        self.service = None
        if self.knowledge['service'] == 'book':
            self.service = Ticket()
            yield Fact(action="book")
            print('book')
        elif self.knowledge['service'] == 'predict':
            self.service = Delay()
            yield Fact(action='predict')
            print('predict')

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
    #     if self.service.name is not None:
    #         self.declare(Fact(name = self.service.name))
    #         self.knowledge['name'] = self.service.name
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
        if self.service.destination is not None:
            self.declare(Fact(destination = self.service.destination))
            self.knowledge['destination'] = self.service.destination
        else:
            if self.knowledge['question'] == 'destination':
                self.knowledge['response'] = 'Can I get your destination please?'
            else:
                self.knowledge['question'] = 'destination'
                self.knowledge['response'] = 'Can I get your destination please?'

    @Rule(Fact(destination=MATCH.destination), NOT(Fact(origin=W())))
    def origin(self):
        if self.service.origin is not None:
            self.declare(Fact(destination = self.service.origin))
            self.knowledge['destination'] = self.service.origin
        else:
            if self.knowledge['question'] == 'origin':
                self.knowledge['response'] = 'Can I get your origin please?'
            else:
                self.knowledge['question'] = 'origin'
                self.knowledge['response'] = 'Can I get your origin please?'

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), NOT(Fact(isReturn=W())))
    def isReturn(self):
        if self.service.destination is not None:
            self.declare(Fact(isReturn = self.service.isReturn))
            self.knowledge['return'] = self.service.isReturn
        else:
            if self.knowledge['question'] == 'return':
                self.knowledge['response'] = 'Would you like a return ticket?'
            else:
                self.knowledge['question'] = 'return'
                self.knowledge['response'] = 'Would you like a return ticket?'

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=MATCH.isReturn),
          NOT(Fact(departDate=W())), NOT(Fact(departTime=W())))
    def departDate(self):
        if self.service.departDate is not None:
            self.declare(Fact(departDate=self.service.departDate))
            self.knowledge['departDate'] = self.service.departDate
        else:
            if self.knowledge['question'] == 'departDate':
                self.knowledge['response'] = 'What date you like to depart?'
            else:
                self.knowledge['question'] = 'departDate'
                self.knowledge['response'] = 'What date you like to depart?'

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=MATCH.isReturn),
          Fact(departDate=MATCH.departDate), NOT(Fact(departTime=W())))
    def departTime(self):
        if self.service.departTime is not None:
            self.declare(Fact(departTime=self.service.departTime))
            self.knowledge['departTime'] = self.service.departTime
        else:
            if self.knowledge['question'] == 'departTime':
                self.knowledge['response'] = 'What time would you like to depart?'
            else:
                self.knowledge['question'] = 'departTime'
                self.knowledge['response'] = 'What time would you like to depart?'

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=True),
          Fact(departDate=MATCH.departDate), Fact(departTime=MATCH.departTime),
          NOT(Fact(returnDate=W())), NOT(Fact(returnTime=W())))
    def returnDate(self):
        if self.service.returnDate is not None:
            self.declare(Fact(returnDate=self.service.returnDate))
            self.knowledge['returnDate'] = self.service.returnDate
        else:
            if self.knowledge['question'] == 'returnDate':
                self.knowledge['response'] = 'What date would you like to return?'
            else:
                self.knowledge['question'] = 'returnDate'
                self.knowledge['response'] = 'What date would you like to return?'

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=True),
          Fact(departDate=MATCH.departDate), Fact(departTime=MATCH.departTime),
          Fact(returnDate=MATCH.returnDate), NOT(Fact(returnTime=W())))
    def returnTime(self):
        if self.service.returnTime is not None:
            self.declare(Fact(returnTime=self.service.returnTime))
            self.knowledge['returnTime'] = self.service.returnTime
        else:
            if self.knowledge['question'] == 'returnTime':
                self.knowledge['response'] = 'What time would you like to return?'
            else:
                self.knowledge['question'] = 'returnTime'
                self.knowledge['response'] = 'What time would you like to return?'

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=False),
          Fact(departDate=MATCH.departDate), Fact(departTime=MATCH.departTime))
    def singleTicket(self):
        if self.knowledge['question'] == 'singleTicket':
            self.knowledge['response'] = self.service.find_cheapest()
        else:
            self.knowledge['question'] = 'singleTicket'
            self.knowledge['response'] = self.service.find_cheapest()

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=True),
          Fact(departDate=MATCH.departDate), Fact(departTime=MATCH.departTime),
          Fact(returnDate=MATCH.returnDate), Fact(returnTime=MATCH.returnTime))
    def returnTicket(self):
        if self.knowledge['question'] == 'returnTicket':
            self.knowledge['response'] = self.service.find_cheapest()
        else:
            self.knowledge['question'] = 'returnTicket'
            self.knowledge['response'] = self.service.find_cheapest()

    @Rule(Fact(action='predict'), NOT(Fact(delay=W())))
    def askDelay(self):
        if self.knowledge['question'] == 'delayTime':
            self.knowledge['response'] = 'How long has the train been delayed?'
        else:
            self.knowledge['question'] = 'delayTime'
            self.knowledge['response'] = 'How long has the train been delayed?'

    @Rule(Fact(action='predict'), Fact(delay=MATCH.delayTime), NOT(Fact(numberOfStops=W())))
    def askNumberOfStops(self):
        if self.knowledge['question'] == 'numberOfStops':
            self.knowledge['response'] = 'How many stops are there on the overall journey?'
        else:
            self.knowledge['question'] = 'numberOfStops'
            self.knowledge['response'] = 'How many stops are there on the overall journey?'

    @Rule(Fact(action='predict'), Fact(delay=MATCH.delayTime), Fact(delay=MATCH.numberOfStops),
          NOT(Fact(delayStation=W())))
    def askDelayStation(self):
        if self.knowledge['question'] == 'delayStation':
            self.knowledge['response'] = 'Which station has the delay been announced from?'
        else:
            self.knowledge['question'] = 'delayStation'
            self.knowledge['response'] = 'Which station has the delay been announced from?'

    @Rule(Fact(action='predict'), Fact(delay=MATCH.delayTime), Fact(delay=MATCH.numberOfStops),
          Fact(delayStation=MATCH.delayStation), NOT(Fact(arrivalTime=W())))
    def askArrivalTime(self):
        if self.knowledge['question'] == 'arrivalTime':
            self.knowledge['response'] = 'What time were you supposed to arrive at your destination?'
        else:
            self.knowledge['question'] = 'arrivalTime'
            self.knowledge['response'] = 'What time were you supposed to arrive at your destination?'

    @Rule(Fact(action='predict'), Fact(delay=MATCH.delayTime), Fact(delay=MATCH.numberOfStops),
          Fact(delayStation=MATCH.delayStation), Fact(arrivalTime=MATCH.arrivalTime), NOT(Fact(delayCode=W())))
    def askDelayCode(self):
        if self.knowledge['question'] == 'delayCode':
            self.knowledge['response'] = 'Do you know your delay code? If not type 0'
        else:
            self.knowledge['question'] = 'delayCode'
            self.knowledge['response'] = 'Do you know your delay code? If not type 0'

    @Rule(Fact(action='predict'), Fact(delay=MATCH.delayTime), Fact(delay=MATCH.numberOfStops),
          Fact(delayStation=MATCH.delayStation), Fact(arrivalTime=MATCH.arrivalTime), Fact(delayCode=MATCH.delayCode))
    def predict(self):
        if self.knowledge['question'] == 'delayCode':
            print()
        else:
            self.knowledge['question'] = 'delayCode'
            print()

class Greetings(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        self.knowledge['question'] = None
        self.service = None
        if self.knowledge['service'] == 'book':
            self.service = Ticket()
            yield Fact(action="book")
            print('book')
        elif self.knowledge['service'] == 'predict':
            self.service = Delay()
            yield Fact(action='predict')
            print('predict')
    @Rule(Fact(action='book'), NOT(Fact(name=W())))
    def ask_name(self):
        print('test')

    @Rule(Fact(action='greet'), NOT(Fact(location=W())))
    def ask_location(self):
        self.declare(Fact(location=input("Where are you? ")))
    @Rule(Fact(action='greet'), Fact(name=MATCH.name),Fact(location=MATCH.location))
    def greet(self, name, location):
        print("Hi %s! How is the weather in %s?" % (name, location))

if __name__ == '__main__':
    # engine = TrainBooking()
    # engine.knowledge = {'service':'book'}
    # engine.reset()  # Prepare the engine for the execution.
    # engine.run() # Run it!

    engine = TrainBooking()
    engine.knowledge = {'service': 'book'}
    engine.reset()  # Prepare the engine for the execution.
    engine.run()  # Run it!
    print(engine.knowledge['response'])
