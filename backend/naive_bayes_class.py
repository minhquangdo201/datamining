from collections import defaultdict
import math
import numpy as np

class NaiveBayes:
    def __init__(self, alpha=1.0):
        self.class_probabilities = {}
        self.word_probabilities = defaultdict(dict)
        self.classes = []
        self.alpha = alpha
        self.total_words = {}

    def fit(self, X_train, y_train):
        total_samples = len(y_train)
        self.classes = np.unique(y_train)

        for class_ in self.classes:
            class_indices = np.where(y_train == class_)[0]
            class_texts = [X_train[i] for i in class_indices]
            class_words = ' '.join(class_texts).split()
            word_counts = defaultdict(float)
            self.total_words[class_] = len(class_words)
            for word in class_words:
                word_counts[word] += 1

            self.word_probabilities[class_] = {word: (count + self.alpha) / (self.total_words[class_] + self.alpha * (len(word_counts) )) for word, count in word_counts.items()}
            self.class_probabilities[class_] = len(class_indices) / total_samples

    def predict(self, X_test):
        predictions = []
        for text in X_test:
            best_class = None
            max_prob = float('-inf')
            for class_ in self.classes:
                total_words = self.total_words[class_]
                prob = math.log(self.class_probabilities[class_])
                for word in text.split():
                    prob += math.log(self.word_probabilities[class_].get(word, self.alpha /(total_words + (len(self.word_probabilities[class_]) ))))  # Laplace smoothing
                if prob > max_prob:
                    max_prob = prob
                    best_class = class_
            predictions.append(best_class)
        return predictions