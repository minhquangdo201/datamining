import datetime
import re
from flask import Flask, request, jsonify
import pickle
from pymongo import MongoClient
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
import string

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['spam_sms']
collection = db['message_history']

ps = PorterStemmer()

cv_naive_bayes = pickle.load(open('datamining/backend/cv_naive_bayes.pkl', 'rb'))
naive_bayes_model = pickle.load(open('datamining/backend/model_naive_bayes.pkl', 'rb'))

cv_svm = pickle.load(open('datamining/backend/cv_svm.pkl', 'rb'))
svm_model = pickle.load(open('datamining/backend/model_svm.pkl', 'rb'))

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
    text = cv_naive_bayes.transform([text])
    prediction = naive_bayes_model.predict(text)
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


@app.route('/predictBayes', methods=['POST'])
def naive_bayes_predict():
    data = request.get_json()
    message = data['message']
    label = predict_bayes(message)
    createTime = datetime.datetime.now()
    label_str = label_to_string(label) 
    
    data['label'] = label_str
    data['createTime'] = createTime
    data['model'] = 'naive_bayes'
    
    collection.insert_one(data)
    
    return jsonify({'prediction': label_str})

@app.route('/predictSVM', methods=['POST'])
def svm_predict():
    data = request.get_json()
    message = data['message']
    label = predict_svm(message)
    createTime = datetime.datetime.now()
    label_str = label_to_string(label) 
    
    data['label'] = label_str
    data['createTime'] = createTime
    data['model'] = 'svm'
    
    collection.insert_one(data)
    
    return jsonify({'prediction': label_str})

@app.route('/history', methods=['GET'])
def get_history():
    messages = collection.find()
    history = []
    for message in messages:
        message.pop('_id')
        history.append(message)
    return jsonify(history)
if __name__ == '__main__':
    app.run(debug=True)
