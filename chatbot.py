import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open(r'C:\Users\admin\Desktop\chatbot\chatbot\Include\intents.json').read())

words = pickle.load(open(r'C:\Users\admin\Desktop\chatbot\chatbot\words.pkl', 'rb'))
classes = pickle.load(open(r'C:\Users\admin\Desktop\chatbot\chatbot\classes.pkl', 'rb'))
model = load_model(r'C:\Users\admin\Desktop\chatbot\chatbot\chatbot_model.h5')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            return result  # Return the result instead of printing
    return "I'm sorry, I couldn't understand that."

# This part is only for testing in the console
if __name__ == "__main__":
    print("Welcome to Graphic Era Hill University's official page. I am GEHU_BOT. How may I assist you today!")

    while True:
        message = input("User: ")
        ints = predict_class(message)
        res = get_response(ints, intents)
        print("GEHU_BOT: ", res)
