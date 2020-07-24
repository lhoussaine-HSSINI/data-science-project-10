from flask import Flask, request
import requests
from flask import jsonify
import json

app=Flask(__name__)

#Here the function in the other file was called, and its outputs were received in json format and also opened with json.

url="http://127.0.0.1:3000/get_data"
data_0={'label' : 'positive', 'sort_order': 'ascending' }
header={'Content-Type': 'application/json'}

result= requests.get(url, params_0=json(data_0), headers=header)
res_2 = result.json()
all_texts=[]
all_labels=[]
for i in range(len(res_2)):
    all_texts.append(res_2[i][0])
    all_labels.append(res_2[i][1])

print("first text")
print(all_texts[0])
#Import Pickle library to compress files

import pickle

#We download the model file and the vectorizer once to be ready for use, and we open the model file and the vectorizer with the reading mode rb
with open('model.pickle', 'rb') as file:
    model = pickle.load(file)

with open('vectorizer.pickle', 'rb') as file:
    vectorizer = pickle.load(file)


import re
#We also define a text cleaning function
def clean_text(text):
    text = text.lower()
    text = re.sub("@[a-z0-9_]+", ' ', text)
    text = re.sub("[^ ]+\.[^ ]+", ' ', text)
    text = re.sub("[^ ]+@[^ ]+\.[^ ]", ' ', text)
    text = re.sub("[^a-z\' ]", ' ', text)
    text = re.sub(' +', ' ', text)
    return text

#A small glossary to clarify the result of the model, instead of sending it as a number, we will send it as a word, we already know that the positive rating is denoted by the number 1 and negative by the number 0.
result_dict = {0: 'negative', 1: 'positive'}

#We create a function to obtain and respond to text classification requests.

def get_sentiment(text):
   try:
       text = clean_text(text)
       vector = vectorizer.transform([text])
       result = model.predict(vector)
       return result_dict[result[0]]
   except:
       return "ERROR!!!!!!!!!!!!!!!!!!!"

all_texts_1=[]
#Here the function was called to do its job. We stored the result in an array.
for i in range(len(res_2)):
    sentiment = get_sentiment(res_2[i][0])
    all_texts_1.append(sentiment)
print("first text after cleaned and transformed : " )
print(all_texts_1[0])

url_1="http://127.0.0.1:3000/get_data_count"
data_1={'count':1000, '‫‪before_date‬‬': '‫‪2020-07-18‬‬' }
header_1={'Content-Type': 'application/json'}

#Here the function in the other file was called.
result_1= requests.get(url_1, params_1 = json(data_1), headers=header_1)

#Here a function has been written that computes the accuracy of the model.
def accuracy(x_test,y_test):
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(x_test, y_test)
    return print("The accuracy is " + str(accuracy))

accuracy(all_labels, all_texts_1)

# Start REST.py on port 3000
if __name__ == "__main__":
   app.run(debug=True, port=3000)
