import re
from pprint import pprint
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

import dateutil
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("hello Harry Apple is looking at hi buying U.K. startup for $1 billion at 3 o'clock on the 31/01/2021")

# pprint([(X.text, X.label_) for X in doc.ents])
# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#           token.shape_, token.is_alpha, token.is_stop)

results = {}

matcher = PhraseMatcher(nlp.vocab)
# list of hello match phrases
greetList = ['hello', 'hi', 'yo', 'hey']

greetingPatterns = [nlp(text) for text in greetList]

matcher.add('greeting', None, *greetingPatterns)

matches = matcher(doc)

print(matches)


# reading this

# sents = [sent for sent in doc.sents]
#
# print(sents[0].start, sents[0].end)
#
# for sent in sents:
#     if matches[0][1] < sent.end:
#         print(sent)
#         break


