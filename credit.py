from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import askopenfilename
import numpy as np 
import pandas as pd 
from sklearn import *
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report 
from sklearn.ensemble import RandomForestClassifier

main = tkinter.Tk()
main.title("Credit Card Fraud Detection") 
main.geometry("1300x1200")

global filename
global cls
global X, Y, X_train, X_test, y_train, y_test
global random_acc
global clean
global attack
global total

def traintest(train):
    global X, Y, X_train, X_test, y_train, y_test
    X = train.values[:, 0:29] 
    Y = train.values[:, 30]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=0)
    return X, Y, X_train, X_test, y_train, y_test

def generateModel():
    global X, Y, X_train, X_test, y_train, y_test
    train = pd.read_csv(filename)
    X, Y, X_train, X_test, y_train, y_test = traintest(train)
    text.insert(END, "Train & Test Model Generated\n\n")
    text.insert(END, "Total Dataset Size : "+str(len(train))+"\n")
    text.insert(END, "Split Training Size : "+str(len(X_train))+"\n")
    text.insert(END, "Split Test Size : "+str(len(X_test))+"\n")

def upload():
    global filename
    filename = filedialog.askopenfilename(initialdir="dataset")
    text.delete('1.0', END)
    text.insert(END, filename+" loaded\n")

def prediction(X_test, cls):
    y_pred = cls.predict(X_test)
    for i in range(50):
        print("X=%s, Predicted=%s" % (X_test[i], y_pred[i]))
    return y_pred 

def cal_accuracy(y_test, y_pred, details): 
    accuracy = accuracy_score(y_test, y_pred) * 100
    text.insert(END, details+"\n\n")
    text.insert(END, "Accuracy : "+str(accuracy)+"\n\n")
    return accuracy

def runRandomForest():
    global random_acc, cls, X, Y, X_train, X_test, y_train, y_test
    cls = RandomForestClassifier(n_estimators=50, max_depth=2, random_state=0, class_weight='balanced')
    cls.fit(X_train, y_train) 
    text.insert(END, "Prediction Results\n\n") 
    prediction_data = prediction(X_test, cls) 
    random_acc = cal_accuracy(y_test, prediction_data, 'Random Forest Accuracy')

def predicts():
    global clean, attack, total
    clean = 0
    attack = 0
    text.delete('1.0', END)
    filename = filedialog.askopenfilename(initialdir="dataset")
    test = pd.read_csv(filename)
    test = test.values[:, 0:29]
    total = len(test)
    text.insert(END, filename+" test file loaded\n")
    y_pred = cls.predict(test) 
    for i in range(len(test)):
        if str(y_pred[i]) == '1.0':
            attack += 1
            text.insert(END, "X=%s, Predicted = %s" % (test[i], 'Contains Fraud Transaction Signature')+"\n\n")
        else:
            clean += 1
            text.insert(END, "X=%s, Predicted = %s" % (test[i], 'Transaction Contains Cleaned Signatures')+"\n\n")

def graph():
    height = [total, clean, attack]
    bars = ('Total Transactions', 'Normal Transaction', 'Fraud Transaction')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.show()

font = ('times', 16, 'bold')
title = Label(main, text='CREDIT CARD FRAUD DETECTION USING RANDOM FOREST TREE BASED CLASSIFIER')
title.config(bg='#EE82EE', fg='black')  
title.config(font=font)
title.config(height=3, width=120)
title.place(x=0, y=5)

font1 = ('times', 12, 'bold')
text = Text(main, height=20, width=150)
scroll = Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=50, y=120)
text.config(font=font1)

font1 = ('times', 14, 'bold')
uploadButton = Button(main, text="Upload Credit Card Dataset", command=upload)
uploadButton.place(x=50, y=550)
uploadButton.config(font=font1)

modelButton = Button(main, text="Generate Train & Test Model", command=generateModel)
modelButton.place(x=350, y=550)
modelButton.config(font=font1)

runrandomButton = Button(main, text="Run Random Forest Algorithm", command=runRandomForest)
runrandomButton.place(x=650, y=550)
runrandomButton.config(font=font1)

predictButton = Button(main, text="Detect Fraud From Test Data", command=predicts)
predictButton.place(x=50, y=600)
predictButton.config(font=font1)

graphButton = Button(main, text="Clean & Fraud Transaction Detection Graph", command=graph)
graphButton.place(x=350, y=600)
graphButton.config(font=font1)

exitButton = Button(main, text="Exit", command=exit)
exitButton.place(x=770, y=600)
exitButton.config(font=font1)

main.config(bg='LightSkyBlue')  # Light purple background
main.mainloop()
