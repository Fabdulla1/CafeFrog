import numpy as np
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import random

class DialogueClassifier:
    def __init__(self):
        self.model = MultinomialNB()
        self.vectorizer = CountVectorizer()
        self.train("Data/AI Training Set.xlsx")
        self.responses = {
            'Order Inquiry': ['Frogaccino', 'Beaver Brew', 'Tadpole Twist', 'Nectar Newt', 'Lotus Latte'],
            'Greetings': ['Hello!', 'Howdy!', 'Hey!', 'Hi!', 'Hiiiii!!!', 'Heyyy!!', 'Hey :p', 'Helloooo!', 'Sup', "Hey! What's up!"],
            'Goodbyes': ['Thanks! Goodbye!', "Aww, you're so sweet! :') See you later", "Thank you!", "Thanks buddy!", "Thanks my friend", "Thanks for the great customer service",
                         "I appreciate you!", "I love you!", "You're awesome!", "Bye!", "Take care now!", "I hope you have a splending day", "Bye bye!", "Have an awesome day!"],
            'In Line' : ["Aren't you supposed to be at the cash register?", "I'm waiting for you to take my order.", "Hey! I hope it's not too busy today?", "Tired?",
                         "I cant wait to try this place!", "I'm still thinking on whether to get that froggaccino or the Beaver's Brew.", "I'm just here for the food.",
                         "I JUST CAN'T WAIT FOR MY DRINK!", "Sometimes it's nice to step back when you feel overwhelmed!", "How's it going behind the bar!"],
            'Waiting' : ["I'm so excited for this!!", "I'm so glad!", "Can't wait to see what you've made!", "I'm hungry.", "Lowkey want a drink.", "Hey!", "Thirsty!",
                         "WoRkInG hArD oR hArDlY wORkiNg XD"]
        }

    def train(self, excel_file_path):
        # Load data from Excel
        data = pd.read_excel(excel_file_path)
        
        # Restructure the data into 'text' and 'label' format
        texts = []
        labels = []
        
        for category in data.columns:
            texts.extend(data[category].dropna().values)
            labels.extend([category] * data[category].dropna().shape[0])
        restructured_data = pd.DataFrame({'text': texts, 'label': labels})
        X = self.vectorizer.fit_transform(restructured_data['text'])
        self.model.fit(X, restructured_data['label'])

    def classify(self, text):
        #This classifies user's input into a category that the AI can then vectorize and classify into intent
        features = self.vectorizer.transform([text])
        return self.model.predict(features)[0]
    
    def respond(self, intent, customerStatus, customerPaid):
        if customerStatus == 'Ordering':
            if intent == 'Order Inquiry' and not customerPaid:
                i = random.randint(1, 4)
                statement = "Let me get a "
                for j in range(i):
                    statement += random.choice(self.responses['Order Inquiry']) + ", "
                return statement
            if intent == 'Greetings':
                return random.choice(self.responses['Greetings'])
            if intent == 'Goodbyes':
                return random.choice(self.responses['Goodbyes'])
        else:
            return random.choice(self.responses[customerStatus])
