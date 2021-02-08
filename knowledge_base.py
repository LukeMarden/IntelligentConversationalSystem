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
        url += str(self.departDate) + '/' + str(self.departTime) + '/dep/'
        if (self.isReturn is True):
            url += str(self.returnDate) + '/' + str(self.returnTime) + '/dep/'
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
        self.delayTime = None
        self.numberOfStops = None
        self.delayStation = None
        self.arrivalTime = None
        self.delayCode = None

    def predict_delay(self):
        self.delayPrediction = prediction(self.origin, self.destination, self.numberOfStops,
                                          self.delayStation, self.delayTime, self.arrivalTime)
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
        elif self.knowledge['service'] == 'predict':
            self.service = Delay()
            yield Fact(action='predict')

        if 'destination' in self.knowledge:
            self.declare(Fact(destination=self.knowledge['destination']))
            self.service.destination = self.knowledge['destination']
        if 'origin' in self.knowledge:
            self.declare(Fact(origin=self.knowledge['origin']))
            self.service.origin = self.knowledge['origin']
        if 'return' in self.knowledge:
            self.declare(Fact(isReturn=self.knowledge['return']))
            self.service.isReturn = self.knowledge['return']
        if 'departDate' in self.knowledge:
            self.declare(Fact(departDate=self.knowledge['departDate']))
            self.service.departDate = self.knowledge['departDate']
        if 'departTime' in self.knowledge:
            print('Hello')
            self.declare(Fact(departTime=self.knowledge['departTime']))
            self.service.departTime = self.knowledge['departTime']
            print(self.service.departTime)
        if 'returnDate' in self.knowledge:
            self.declare(Fact(returnDate=self.knowledge['returnDate']))
            self.service.returnDate = self.knowledge['returnDate']
        if 'returnTime' in self.knowledge:
            self.declare(Fact(returnTime=self.knowledge['returnTime']))
            self.service.returnTime = self.knowledge['returnTime']
        if 'delayTime' in self.knowledge:
            self.declare(Fact(delayTime=self.knowledge['delayTime']))
            self.service.delayTime = self.knowledge['delayTime']*60
        if 'numberOfStops' in self.knowledge:
            self.declare(Fact(numberOfStops=self.knowledge['numberOfStops']))
            self.service.numberOfStops = self.knowledge['numberOfStops']
        if 'delayStation' in self.knowledge:
            self.declare(Fact(delayStation=self.knowledge['delayStation']))
            self.service.delayStation = self.knowledge['delayStation']
        if 'delayCode' in self.knowledge:
            self.declare(Fact(delayCode=self.knowledge['delayCode']))
            self.service.delayCode = self.knowledge['delayCode']
        if 'arrivalTime' in self.knowledge:
            self.declare(Fact(arrivalTime=self.knowledge['arrivalTime']))
            self.service.arrivalTime = self.knowledge['arrivalTime']

    @Rule(AND(NOT(Fact(destination=W())), NOT(Fact(origin=W()))))
    def destination(self):
        self.knowledge['question'] = 'destination'
        self.knowledge['response'] = 'Can I get your destination please?'

    @Rule(AND(Fact(destination=MATCH.destination), NOT(Fact(origin=W()))))
    def origin(self):
        self.knowledge['question'] = 'origin'
        self.knowledge['response'] = 'Can I get your origin please?'

    @Rule(AND(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), NOT(Fact(isReturn=W()))))
    def isReturn(self):
        self.knowledge['question'] = 'return'
        self.knowledge['response'] = 'Would you like a return ticket?'

    @Rule(AND(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=MATCH.isReturn),
          NOT(Fact(departDate=W())), NOT(Fact(departTime=W()))))
    def departDate(self):
        self.knowledge['question'] = 'departDate'
        self.knowledge['response'] = 'What date would you like to depart? (DD Month YYYY)'

    @Rule(AND(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=MATCH.isReturn),
          Fact(departDate=MATCH.departDate), NOT(Fact(departTime=W()))))
    def departTime(self):
        self.knowledge['question'] = 'departTime'
        self.knowledge['response'] = 'What time would you like to depart? (HH:MM)'

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=True),
          Fact(departDate=MATCH.departDate), Fact(departTime=MATCH.departTime),
          NOT(Fact(returnDate=W())), NOT(Fact(returnTime=W())))
    def returnDate(self):
        self.knowledge['question'] = 'returnDate'
        self.knowledge['response'] = 'What date would you like to return? (DD Month YYYY)'

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=True),
          Fact(departDate=MATCH.departDate), Fact(departTime=MATCH.departTime),
          Fact(returnDate=MATCH.returnDate), NOT(Fact(returnTime=W())))
    def returnTime(self):
        self.knowledge['question'] = 'returnTime'
        self.knowledge['response'] = 'What time would you like to return? (HH:MM)'

    @Rule(AND(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=False),
          Fact(departDate=MATCH.departDate), Fact(departTime=MATCH.departTime)))
    def singleTicket(self):
        self.knowledge['question'] = 'singleTicket'
        self.knowledge['response'] = ('The cheapest ticket is: ' + self.service.find_cheapest() +
                                      ', at link: ' + self.service.generate_ticket_url())

    @Rule(Fact(action='book'), Fact(destination=MATCH.destination),
          Fact(origin=MATCH.origin), Fact(isReturn=True),
          Fact(departDate=MATCH.departDate), Fact(departTime=MATCH.departTime),
          Fact(returnDate=MATCH.returnDate), Fact(returnTime=MATCH.returnTime))
    def returnTicket(self):
        self.knowledge['question'] = 'returnTicket'
        self.knowledge['response'] = ('The cheapest ticket is: ' + self.service.find_cheapest() +
                                      ', at link: ' + self.service.generate_ticket_url())

    @Rule(Fact(action='predict'), NOT(Fact(delayTime=W())))
    def askDelay(self):
        self.knowledge['question'] = 'delayTime'
        self.knowledge['response'] = 'How long has the train been delayed? (Minutes)'

    @Rule(Fact(action='predict'), Fact(delayTime=MATCH.delayTime), NOT(Fact(numberOfStops=W())))
    def askNumberOfStops(self):
        self.knowledge['question'] = 'numberOfStops'
        self.knowledge['response'] = 'How many stops are there on the overall journey?'

    @Rule(Fact(action='predict'), Fact(delayTime=MATCH.delayTime), Fact(numberOfStops=MATCH.numberOfStops),
          NOT(Fact(delayStation=W())))
    def askDelayStation(self):
        self.knowledge['question'] = 'delayStation'
        self.knowledge['response'] = 'Which station has the delay been announced from?'

    @Rule(Fact(action='predict'), Fact(delayTime=MATCH.delayTime), Fact(numberOfStops=MATCH.numberOfStops),
          Fact(delayStation=MATCH.delayStation), NOT(Fact(arrivalTime=W())))
    def askArrivalTime(self):
        self.knowledge['question'] = 'arrivalTime'
        self.knowledge['response'] = 'What time were you supposed to arrive at your destination?'

    @Rule(Fact(action='predict'), Fact(delayTime=MATCH.delayTime), Fact(numberOfStops=MATCH.numberOfStops),
          Fact(delayStation=MATCH.delayStation), Fact(arrivalTime=MATCH.arrivalTime), NOT(Fact(delayCode=W())))
    def askDelayCode(self):
        self.knowledge['question'] = 'delayCode'
        self.knowledge['response'] = 'Do you know your delay code? If not type 0'

    @Rule(Fact(action='predict'), Fact(delayTime=MATCH.delayTime), Fact(numberOfStops=MATCH.numberOfStops),
          Fact(delayStation=MATCH.delayStation), Fact(arrivalTime=MATCH.arrivalTime), Fact(delayCode=MATCH.delayCode))
    def predict(self):
        self.knowledge['response'] = ('The train will arrive at: ' + self.service.predict_delay())


if __name__ == '__main__':

    engine = TrainBooking()
    engine.knowledge = {'service': 'book'}
    engine.reset()  # Prepare the engine for the execution.
    engine.run()  # Run it!
    print(engine.knowledge['response'])
