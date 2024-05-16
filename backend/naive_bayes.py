import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import pickle
from naive_bayes_class import NaiveBayes

from sklearn.model_selection import train_test_split

#read data
spam_df = pd.read_csv('backend\\spam.csv', encoding='latin-1')
spam_df = spam_df.drop(["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], axis=1)
spam_df['label'] = spam_df['label'].map({'ham': 0, 'spam': 1})
spam_df = spam_df.drop_duplicates(keep='first')

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

#split data
X = spam_df['transform_message'].values
y = spam_df['label'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

#train model
model = NaiveBayes(alpha=0.1)
model.fit(X_train, y_train)

#predict
y_pred = model.predict(X_test)

#print accuracy
from sklearn.metrics import classification_report, accuracy_score

print(classification_report(y_test, y_pred))
print(accuracy_score(y_test, y_pred))

#save model
with open('model_naive_bayes.pkl', 'wb') as file:
    pickle.dump(model, file)
