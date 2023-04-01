import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

train=pd.read_csv(r"loan_train.csv")
test=pd.read_csv(r"loan_test.csv")

train.head()

test.head()

train.dropna(axis=0,inplace=True)
test.dropna(axis=0,inplace=True)

train.info()

train=train.drop(columns=['Dependents','Area'],axis=1)
test=test.drop(columns=['Dependents','Area'],axis=1)

test.info()

train = pd.get_dummies(train)

train = train.drop(['Gender_Female', 'Married_No', 'Education_Not Graduate',  'Self_Employed_No', 'Status_N'], axis = 1)

new = {'Gender_Male': 'Gender', 'Married_Yes': 'Married', 
       'Education_Graduate': 'Education', 'Self_Employed_Yes': 'Self_Employed',
       'Loan_Status_Y': 'Loan_Status'}
       
train.rename(columns = new, inplace = True)

test = pd.get_dummies(test)

test = test.drop(['Gender_Female', 'Married_No', 'Education_Not Graduate', 'Self_Employed_No'], axis = 1)

new = {'Gender_Male': 'Gender', 'Married_Yes': 'Married', 
       'Education_Graduate': 'Education', 'Self_Employed_Yes': 'Self_Employed',
       'Loan_Status_Y': 'Loan_Status'}
       
test.rename(columns = new, inplace = True)

q1 = train.quantile(0.25)
q3 = train.quantile(0.75)
iqr = q3 - q1

train = train[~((train < (q1 - 1.5 * iqr)) |(train > (q3 + 1.5 * iqr))).any(axis = 1)]

q1 = test.quantile(0.25)
q3 = test.quantile(0.75)
iqr = q3 - q1

test = test[~((test < (q1 - 1.5 * iqr)) |(test > (q3 + 1.5 * iqr))).any(axis = 1)]

x = train.drop(["Status_Y"], axis = 1)
y = train["Status_Y"]

minmax = MinMaxScaler()
x = minmax.fit_transform(x)
test = minmax.transform(test)

rfc = RandomForestClassifier(n_estimators = 1000, random_state = 1)
rfc.fit(x, y)
y_pred = rfc.predict(test)




#%%

import pickle

pickle.dump(rfc,open('model.pkl','wb'))
