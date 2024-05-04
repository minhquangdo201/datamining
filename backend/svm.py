import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')
import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn import svm
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
classifier = svm.SVC(kernel='rbf', C=100, gamma=0.01)
classifier.fit(X_train, y_train)
accuracy = cross_val_score(classifier, X=X, y=y, scoring="accuracy", cv=10)
print("Accuracy: {:.2f} %".format(accuracy.mean()*100))
joblib.dump(classifier, 'backend\\spam-sms-mnb-model.pkl')