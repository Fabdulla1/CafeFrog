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
                         "I appreciate you!", "I love you!", "You're awesome!", "Bye!", "Take care now!", "I hope you have a splending day", "Bye bye!", "Have an awesome day!"]
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
    
    def respond(self, intent):
        if intent == 'Order Inquiry':
            i = random.randint(1, 4)
            statement = "Let me get a "
            for j in range(i):
                statement += random.choice(self.responses['Order Inquiry']) + ", "
            return statement
        if intent == 'Greetings':
            return random.choice(self.responses['Greetings'])
        if intent == 'Goodbyes':
            return random.choice(self.responses['Goodbyes'])
        

