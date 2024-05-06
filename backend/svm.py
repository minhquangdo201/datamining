import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')
import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn import svm
import pickle

sms = pd.read_csv('datamining\\backend\\spam.csv', encoding='latin-1')
sms = sms.drop(["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], axis=1)

sms = sms.drop_duplicates(keep='first')

corpus = [] 
ps = PorterStemmer() 

for message in sms['message']:
    message = re.sub(pattern='[^a-zA-Z]', repl=' ', string=message).lower()
    words = message.split()
    words = [ps.stem(word) for word in words if word not in set(stopwords.words('english'))]
    message = ' '.join(words)
    corpus.append(message)
    
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus).toarray()

y = pd.get_dummies(sms['label'])
y = y.iloc[:,1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)
classifier = svm.SVC(kernel='rbf', C=100, gamma=0.01)
classifier.fit(X_train, y_train)

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

y_pred = classifier.predict(X_test)
# In ra báo cáo phân loại
print(classification_report(y_test, y_pred))

# In ra ma trận nhầm lẫn
print(confusion_matrix(y_test, y_pred))

# In ra độ chính xác
print(accuracy_score(y_test, y_pred))

pickle.dump(vectorizer, open('datamining\\backend\\cv_svm.pkl', 'wb'))
pickle.dump(classifier, open('datamining\\backend\\model_svm.pkl', 'wb'))