import datetime
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

naive_bayes_model = pickle.load(open('final/naive_bayes.pkl', 'rb'))
naive_bayes_cv = pickle.load(open('final/naive_bayes_cv.pkl', 'rb'))

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
    text = naive_bayes_cv.transform([text])
    prediction = naive_bayes_model.predict(text)
    return prediction[0]

@app.route('/predictBayes', methods=['POST'])
def predict():
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

if __name__ == '__main__':
    app.run(debug=True)
