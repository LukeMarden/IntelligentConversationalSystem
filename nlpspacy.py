import json
import re
import dateutil
import spacy
from spacy.lang.en import English
from knowledge_base import *

# ************************************************************************************************************
#
#    nlpu.py
#    This file contains the main contents of the NLP as well as a function extract_info()
#    to extract all the contents of message given by a user
#
#    Author: Group 18 (London is Blue)
#
#    Created: 03/01/2021
#
# ************************************************************************************************************

# Loading in and defining the main modules
nlp = spacy.load("en_core_web_lg")
parser = English()

# Contains all the locations a user can input
stations = json.load(open('train_codes.json'))

# Defining regex patterns used for rule-based matching
true = r'.*(yes|yeah|yh|correct|true|).*'
false = r'.*(no|nah|nay|wrong|false).*'
time = r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$'
default_time = r'^([0-1][0-9]|[2][0-3]):([0-5][0-9])$'
time_am = r'/((1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm]))/'


# This method takes in three parameters: question, message and kb
# used to extract the information from a users message and returns a dictionary results
#
# question: a dictionary, which defines at what stage the question is at
# message: a string, which is input by the user
# kb: a class, knowledge base handles the engine and what questions will be required
def extract_info(question, message, kb):
    # spaCy's initiation of the nlp
    doc = nlp(message)
    # initialises a dict containing the results of the function
    results = {}

    # Testing to see if the message gets decoded and all the functions get recognized
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
              token.shape_, token.is_alpha, token.is_stop)

    # Runs through all entities in message to extract if its a return or a single ticket
    for ent in doc:
        ent = str(ent).lower()
        search_true = re.search(true, ent)
        search_false = re.search(false, ent)
        if ent in {'return', 'returns'}:
            results['return'] = True
        if 'come back' in str(doc):
            results['return'] = True
        if 'go back' in str(doc):
            results['return'] = True
        if search_true:
            results['return'] = True
        if ent in {'single', 'singles'}:
            results['return'] = False
        if search_false:
            results['return'] = False

    # Runs through all entities in message and then compares     them to all the available
    # stations in the json file and extracts the location to the results
    locations = []
    for ent in doc:
        for i in stations:
            if ent.text == i:
                locations.append(i)
                results['location'] = locations

    # Runs through all entities in the message to extract either the integer, time or date of an entity
    # after which extracted to the results
    integers = []
    minutes = []
    dates = []
    times = []
    search_time = re.search(time, doc.text)

    # For 0 digits
    for ent in doc:
        if ent.text == '0':
            integers.append(ent.text)
    # For all cardinal numbers
    for ent in doc.ents:
        if ent.label_ == 'CARDINAL':
            integers.append(ent.text)
            continue
        # For minutes
        if ent.text.isdigit():
            minutes.append(ent.text)

        # For any dates
        if ent.label_ == 'DATE':
            date = dateutil.parser.parse(ent.text)
            date = str(date.day).zfill(2) + str(date.month).zfill(2) + (str(date.year)[2:])
            dates.append(date)

        # For any times
        if ent.label_ == 'TIME':
            date = dateutil.parser.parse(ent.text)
            times.append(str(date.hour).zfill(2) + str(date.minute).zfill(2))

    # Uses the regex and runs through the message to search for time format
    if search_time:
        date = dateutil.parser.parse(doc.text)
        times.append(str(date.hour).zfill(2) + str(date.minute).zfill(2))

    results['integers'] = integers
    results['minutes'] = minutes
    results['dates'] = dates
    results['times'] = times

    # Prints out all the results that have been extracted
    print(results)

    # Contains the logic to apply the method to get result to the right question
    # Also contains basic error handling, since if results != 1

    # Results logic
    if (question['question'] == 'return') and ('return' in results):
        kb.knowledge['return'] = results['return']
        results = 1

    # Location logic
    if (question['question'] == 'origin') and ('location' in results):
        kb.knowledge['origin'] = results['location'][0]
        results = 1
    elif (question['question'] == 'destination') and ('location' in results):
        kb.knowledge['destination'] = results['location'][0]
        results = 1
    elif (question['question'] == 'delayStation') and ('location' in results):
        kb.knowledge['delayStation'] = results['location'][0]
        results = 1

    # Date logic
    if (question['question'] == 'departDate') and ('dates' in results):
        kb.knowledge['departDate'] = results['dates'][0]
        results = 1
    elif (question['question'] == 'returnDate') and ('dates' in results):
        kb.knowledge['returnDate'] = results['dates'][0]
        results = 1
    elif (question['question'] == 'departTime') and ('times' in results):
        kb.knowledge['departTime'] = results['times'][0]
        results = 1
    elif (question['question'] == 'returnTime') and ('times' in results):
        kb.knowledge['returnTime'] = results['times'][0]
        results = 1
    elif (question['question'] == 'arrivalTime') and ('times' in results):
        kb.knowledge['arrivalTime'] = results['times'][0]
        results = 1

    # Number logic
    if (question['question'] == 'numberOfStops') and ('integers' in results):
        kb.knowledge['numberOfStops'] = results['integers'][0]
        results = 1
    elif (question['question'] == 'delayTime') and ('integers' in results):
        kb.knowledge['delayTime'] = results['integers'][0]
        results = 1
    elif (question['question'] == 'delayCode') and ('integers' in results):
        kb.knowledge['delayCode'] = results['integers'][0]
        results = 1

    return results
