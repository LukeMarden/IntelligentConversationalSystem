from experta import *
from random import choice
# from experta.watchers import RULES, AGENDA

class Ticket(Fact):
    def __init__(self):
        self.name = None
        self.isReturn = None
        self.startLocation = None
        self.destination = None
        self.departTime = None
        self.departDate = None
        self.returnTime = None
        self.returnDate = None


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
            if self.knowledge['question'] == 'ask_name':
                print("AskName")
                # Message.emit_feedback('display received message', 'unknown_message')
            else:
                self.knowledge['question'] = 'ask_name'
                # Message.emit_feedback('display received message', 'ask_name')

    @Rule(Fact(action='greet'), Fact(name = MATCH.name))
    def service(self):
        print("TEST")
        if self.knowledge['question'] == 'ask_service':
            print("AskService1")
            # Message.emit_feedback('display received message', 'unknown_message')
        else:
            self.knowledge['question'] = 'ask_service'
            print("AskService2")
            # Message.emit_feedback('display received message', 'ask_booking')


if __name__ == '__main__':
    engine = TrainBooking()
    engine.knowledge = {}
    engine.reset()  # Prepare the engine for the execution.
    engine.run() # Run it!