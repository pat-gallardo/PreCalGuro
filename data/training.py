import sys
import os
import random
import json
import numpy as np
import tflearn
import tensorflow as tf
import pickle

import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

with open("data/intents.json") as file:
    data = json.load(file)
# print(data["intents"])

# try:
#     with open("data.pickle", "rb") as f:
#         words, labels, training, output = pickle.load(f)
# except:
words = []
labels = []
documents_x = []
documents_y = []

for intent in data["intents"]:
    for items in intent["item"]:
        for pattern in items["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            documents_x.append(wrds)
            documents_y.append(items["tag"])

        if items["tag"] not in labels:
            labels.append(items["tag"])

words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(documents_x):
    bag=[]
    wrds=[stemmer.stem(w) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = (out_empty)[:]
    output_row[labels.index(documents_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = np.array(training)
output = np.array(output)

with open("data/data.pickle", "wb") as f:
    pickle.dump((words, labels, training, output),f) 
    # Start of AI part 
tf.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

# try:
#     model.load("model.tflearn")
# except:
model.fit(training, output, n_epoch = 500, batch_size = 8, show_metric=True)
model.save("data/model.tflearn")
# End of AI part

def bag_of_words(s,words):
    bag=[0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for sentence in s_words:
        for i, w in enumerate(words):
            if w == sentence:
                bag[i] = 1
    return np.array(bag)

# function for checking of answer and solutions
def chat(question, answer):

    while True:
        results = model.predict([bag_of_words(answer, words)])[0]
        # results = model.predict([bag_of_words(inp, words)])[0]
        results_index = np.argmax(results)
        tag = labels[results_index]

        # to check if the answer is appropriate to the question
        if tag == question:
            print(tag)
            # to check if the results is 90% or great accurate
            if results[results_index] > 0.9:
                # check the intents.json file for all the data inside of it
                for tg in data["intents"]:
                    # check deeply the intents.json 
                    for items in tg["item"]:
                        # check if the questionId (tag) == to the intents.json "tag"
                        if items["tag"] == tag:
                            # the value of response is equal to the items inside the "response" in intents.json
                            responses = items["responses"]
                            return(random.choice(responses))
                else: 
                    print("incorrect")
                    return("incorrect")
        else: 
            print("incorrect")
            return("incorrect")