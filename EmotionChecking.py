import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pickle

class emotions:
    def pred(self, msg):
        data = pd.read_csv('C:\\ProjectFinal\\main\\main\\static\\text_emotion.csv')

        data = data.iloc[:700, :]

        # from textblob.classifiers import NaiveBayesClassifier as NBC
        #
        # training_corpus = []
        #
        # for k in range(len(train)):
        #     training_corpus.append((train.Questions[k], train.LEVEL[k]))
        # model=NBC(training_corpus)
        # res=model.classify(msg)

        # print(res)
        from sklearn.ensemble import RandomForestClassifier
        qn = data.values[:, 3]
        label = data.values[:, 1]
        xtrain, xtest, ytrain, ytest = train_test_split(qn, label, test_size=0.2, random_state=0)
        vector = TfidfVectorizer(stop_words='english')

        xtrain_vector = vector.fit_transform(xtrain)

        with open("C:\\ProjectFinal\\main\\main\\static\\vector.pkl", "rb") as handle:
            vector = pickle.load(handle)

        xtest_vector = vector.transform(xtest)
        xtrain_vector = vector.transform(xtrain)

        rf = RandomForestClassifier()
        rf.fit(xtrain_vector, ytrain)
        msg = [msg]
        msgvector = vector.transform(msg)

        predicted = rf.predict(msgvector)
        print(predicted)
        return predicted[0]
#
ob=emotions()
res=ob.pred("poppygallico,@annarosekerr agreed")
print(res)