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


def tokenize(sentence):
    return nltk.word_tokenize(sentence)


def stem(word):
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, all_words):
    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0

    return bag


# noise_list = ["is", "a", "this", "..."]
# def _remove_noise(input_text):
#     words = input_text.split()
#     noise_free_words = [word for word in words if word not in noise_list]
#     noise_free_text = " ".join(noise_free_words)
#     return noise_free_text
#
# _remove_noise("testing this thing that is a test")

# # Testing noise removal
#
# sentence = ["hello", "how", "are", "you"]
# words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
# bog = bag_of_words(sentence, words)
# print(bog)
#
# # Testing tokenization
# a = "What times are available?"
# print(a)
# a = tokenize(a)
# print(a)
#
# # Testing stemming
# words = ["organize", "organizes", "organizing"]
# stemmed_words = [stem(w) for w in words]
# print(stemmed_words)


# object standardization

# speech tagging
with open('intents2.json', 'r') as f:
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
print(all_words)
tags = sorted(set(tags))
print(tags)

print(len(xy), "patterns")
print(len(tags), "tags:", tags)
print(len(all_words), "unique stemmed words:", all_words)

# # for bag_of_words
# x_train = []
# # for the tags
# y_train = []
#
# for(pattern_sentence, tag) in xy:
#     bag = bag_of_words(pattern_sentence, all_words)
#     x_train.append(bag)
#
#     label = tags.index(tag)
#     y_train.append(label) # CrossEntropyLoss Only class labels
#
# x_train = np.array(x_train)
# y_train = np.array(y_train)
#
# class ChatDataset(Dataset):
#     def __init__(self):
#         self.n_samples = len(x_train)
#         self.x_data = x_train
#         self.y_data = y_train
#
#     #dataset[idx]
#     def __getitem__(self, index):
#         return self.x_data[index], self.y_data[index]
#
#     def __len__(self):
#         return self.n_samples
#
#
# # Hyperparamaters
# batch_size = 8
#
# dataset = ChatDataset()
# train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=2)

# from DiscordUI import on_message
