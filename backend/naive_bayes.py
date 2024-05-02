import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

#read data
spam_df = pd.read_csv('backend/spam.csv', encoding='latin-1')

spam_df = spam_df.drop(["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], axis=1)
spam_df['label'] = spam_df['label'].map({'ham': 0, 'spam': 1})

spam_df = spam_df.drop_duplicates(keep='first')

import nltk

spam_df['message'].apply(lambda x:nltk.word_tokenize(x))

