import numpy as np
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import openpyxl

class DialogueClassifier:
    def __init__(self):
        self.model = MultinomialNB()
        self.vectorizer = CountVectorizer()
        self.train("Data/AI Training Set.xlsx")

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
            pass
        if intent == 'Greetings':
            pass
        if intent == 'Goodbyes':
            pass
        

