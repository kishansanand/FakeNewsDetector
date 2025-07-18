from django.shortcuts import render

# views.py
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


import joblib
import os
import re

# Load the model once (recommended)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'lr_model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')
model = joblib.load(MODEL_PATH)
Vectorizer = joblib.load('vectorizer.pkl')

def preprocess(text):
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    tokens = text.split()
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

def predict_news(request):
    result = None
    color = ''
    if request.method == 'POST':
        news_text = request.POST.get('newsText', '')
        clean_text = preprocess(news_text)
        features = Vectorizer.transform([clean_text])
        # Convert the input to features as your model expects
        features = preprocess(news_text)  # Define preprocessing if needed
        prediction = model.predict([features])[0]
        # vectorizer = joblib.load('vectorizer.pkl')

        if prediction == 1:
            result = "This news appears to be REAL!"
            color = "real"
        else:
            result = "Warning: This news may be FAKE!"
            color = "fake"
    return render(request, 'index.html', {'result': result})

