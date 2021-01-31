import re
import spacy

# from DiscordUI import on_message


# sentence detection, tokenizer, POS model


# categorize --> regex
greet = re.compile(r'\b(?i)(hello|hey|hi|yo)\b')

# greeting = re.compile()
true = re.compile(r'\b(?i)(true|yes|yeah|yh|ya)\b')

nlp = spacy.load("en_core_web_sm")
# message = nlp(text)

doc = nlp("Hello Harry Apple is looking at buying U.K. startup for $1 billion")

results = {}
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop)

if greet.search(str(doc)):
    results['greet'] = 'true'

print(results)

hasName = False
for entity in doc.ents:
    if entity.label_ == 'PERSON':
        results['name'] = entity.text
        hasName = True
if not hasName and len(str(doc).split()) == 1 and not ('greeting' in results):
    results['name'] = str(doc)

print(results)


# Time

minutes = []
dates = []
times = []

for entity in doc.ents:
    if entity.text.isdigit():
        minutes.append(entity.text)


