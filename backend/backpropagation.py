import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
#nltk.download('stopwords')
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import joblib

sms = pd.read_csv('backend\\spam.csv', encoding='latin-1')
sms = sms.drop(["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], axis=1)

corpus = [] 
ps = PorterStemmer() 

for i in range(0,sms.shape[0]):
    message = re.sub(pattern='[^a-zA-Z]', repl=' ', string=sms.message[i]) 
    message = message.lower() 
    words = message.split() 
    words = [word for word in words if word not in set(stopwords.words('english'))]
    words = [ps.stem(word) for word in words] 
    message = ' '.join(words) 
    corpus.append(message) 

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus).toarray()
y = pd.get_dummies(sms['label'])
y = y.iloc[:,1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

model = Sequential()
model.add(Dense(units=10, activation='relu'))
model.add(Dense(units=1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10)

model.save('backend\\model_backpropagation.h5')
joblib.dump(vectorizer, 'backend\\cv_backpropagation.pkl')