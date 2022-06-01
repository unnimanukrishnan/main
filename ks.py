def sam(a):
    attributes = []
    labels = []
    train = []
    import pandas as pd
    data = pd.read_csv('C:\\ProjectFinal\\main\\main\\static\\text_emotion.csv')
    h = 0
    k = []
    for i in data.values:
        train.append((i[2], i[1]))
        k.append(i[2])

    k = []

    k.append(a)

    print(train)
    from textblob.classifiers import NaiveBayesClassifier
    cl = NaiveBayesClassifier(train)
    ms = ""
    for m in k:
        ks = cl.classify(m)
        print(ks, m)
        ms = ks

    return ms

a=sam(" Karkare actively worked for Digvijaya")
print(a)