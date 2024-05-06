import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

#read data
spam_df = pd.read_csv('datamining/backend/spam.csv', encoding='latin-1')

spam_df = spam_df.drop(["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], axis=1)
spam_df['label'] = spam_df['label'].map({'ham': 0, 'spam': 1})

spam_df = spam_df.drop_duplicates(keep='first')

#clean data
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
import string

ps = PorterStemmer()

def transform_text(text):
    text = text.lower() #convert to lowercase
    text = nltk.word_tokenize(text) #tokenize the text
    y = []

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation: #remove stopwords and punctuation
            y.append(ps.stem(i)) #stem the words
    
    return " ".join(y) 

spam_df['transform_message'] = spam_df['message'].apply(transform_text)

#CountVectorizer

cv = CountVectorizer()

X = cv.fit_transform(spam_df['transform_message']).toarray()   #converts the text to a matrix of token counts
y = spam_df['label'].values

#split data

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

#train model
model = MultinomialNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

#print accuracy
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(accuracy_score(y_test, y_pred))

#save model
import pickle

pickle.dump(model, open('datamining\\backend\\model_naive_bayes.pkl', 'wb'))
pickle.dump(cv, open('datamining\\backend\\cv_naive_bayes.pkl', 'wb'))


