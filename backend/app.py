import datetime
import re
from flask import Flask, request, jsonify
import pickle
from flask_cors import CORS
from pymongo import MongoClient
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
import string
from tensorflow.keras.models import load_model
from naive_bayes_class import NaiveBayes

app = Flask(__name__)
cors = CORS(app)
client = MongoClient('mongodb://localhost:27017/')
db = client['spam_sms']
collection = db['message_history']

ps = PorterStemmer()

naive_bayes_model = pickle.load(open('backend/model_naive_bayes.pkl', 'rb'))

cv_svm = pickle.load(open('backend/cv_svm.pkl', 'rb'))
svm_model = pickle.load(open('backend/model_svm.pkl', 'rb'))

cv_backpropagation = pickle.load(open('backend/cv_backpropagation.pkl', 'rb'))
backpropagation_model = load_model('backend/model_backpropagation.h5')

def transform_text(text):
    ps = PorterStemmer()
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(ps.stem(i))
    
    return " ".join(y)

def label_to_string(label):
    if label == 0:
        return "ham"
    elif label == 1:
        return "spam"
    else:
        return "unknown"

def predict_bayes(text):
    text = transform_text(text)
    prediction = naive_bayes_model.predict([text])
    return prediction[0]

def predict_svm(text):
    text = re.sub(pattern='[^a-zA-Z]', repl=' ', string=text).lower()
    words = text.split()
    words = [ps.stem(word) for word in words if word not in set(stopwords.words('english'))]
    text = ' '.join(words)
    text = cv_svm.transform([text])
    text = text.toarray()
    prediction = svm_model.predict(text)
    return prediction[0]

def predict_backpropagation(text):
    text = re.sub(pattern='[^a-zA-Z]', repl=' ', string=text).lower()
    words = text.split()
    words = [ps.stem(word) for word in words if word not in set(stopwords.words('english'))]
    text = ' '.join(words)
    text = cv_backpropagation.transform([text])
    text = text.toarray()
    prediction = backpropagation_model.predict(text)
    if prediction > 0.5:
        return 1
    else:
        return 0


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        message = data['message']
        model = data['model']
    
        if model == 'naive bayes':
            label = predict_bayes(message)
        if model == 'svm':
            label = predict_svm(message)
        if model == 'backpropagation':
            label = predict_backpropagation(message)
    
        data['label'] = label_to_string(label)
        data['createTime'] = datetime.datetime.now().isoformat() 
        collection.insert_one(data)
    
        return jsonify({'prediction': label_to_string(label), 'model': model, 'message': message})
    except:
        return jsonify({'error': 'Invalid input'})
    

@app.route('/history', methods=['GET'])
def get_history():
    try:
        messages = collection.find()
        history = []
        for message in messages:
            message.pop('_id')
            history.append(message)
            history = sorted(history, key=lambda x: x['createTime'], reverse=True)
        return jsonify(history)
    except:
        return jsonify({'error': 'An error occurred'})

if __name__ == '__main__':
    app.run(debug=True)
