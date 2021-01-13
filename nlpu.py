import nltk
import json
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from DiscrodBotPython import *
from nltk import word_tokenize, pos_tag, re

# nltk.download('punkt')
from nltk.stem.porter import PorterStemmer

# creating an object of class PorterStemmer
stemmer = PorterStemmer()

    # def get_entities(json):
    #     message = json['message']
    #     message = nlp(message)


def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words):
    """
    sentence = ["hello, "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog = [ 0, 1, 0, 1, 0, 0 , 0]
    """
    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0

    return bag


sentence = ["hello", "how", "are", "you"]
words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
bog = bag_of_words(sentence, words)
print(bog)


# Testing tokenization
a = "What times are available?"
print(a)
a = tokenize(a)
print(a)

# Testing stemming
words = ["organize", "organizes", "organizing"]
stemmed_words = [stem(w) for w in words]
print(stemmed_words)

with open('intents.json', 'r') as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

ignore_words = ['?', '!', '.', ',']
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))
print(tags)

# for bag_of_words
x_train = []
# for the tags
y_train = []

for(pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    x_train.append(bag)

    label = tags.index(tag)
    y_train.append(label) # CrossEntropyLoss Only class labels

x_train = np.array(x_train)
y_train = np.array(y_train)

class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train

    #dataset[idx]
    def __getitem__(self, item):
        return self.x_data[idx], self.y_data[idx]

    def __len__(self):
        return self.n_samples


# Hyperparamaters
batch_size = 8

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=2)


# greeting = re.compile(r'\b(?i)(hello|hey|hi|yo)\b')
# false = re.compile(r'\b(?i)(false|no|nah)\b')
# true = re.compile(r'\b(?i)(true|yes|yeah|yh)\b')
# fromTo = re.compile(r'(?i)(.*) to (.*)')
# toFrom = re.compile(r'(?i)(.*) from (.*)')
# time = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')
#
# # def get_entities()
#
#
# # Removing Noise
#
# noise_list = ["is", "a", "this", "or"]
# def _remove_noise(input_text):
#

# text = "I am learning Natural Language Processing on Analytics Vidhya"
# tokens = word_tokenize(text)
#

# print pos_tag(tokens)
# >>> [('I', 'PRP'), ('am', 'VBP'), ('learning', 'VBG'), ('Natural', 'NNP'),('Language', 'NNP'),
# ('Processing', 'NNP'), ('on', 'IN'), ('Analytics', 'NNP'),('Vidhya', 'NNP')]
# ```