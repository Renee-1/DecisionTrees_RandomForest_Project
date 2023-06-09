# -*- coding: utf-8 -*-
"""Decision Trees and Random Forest Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xYjkIdv1cJXnKuThDPjVRo0aclJoRCkP

# Random Forest Project 
Lending Club connects people who need money (borrowers) with people who have money (investors). An investor would want to invest in people who showed a profile of having a high probability of paying them back. I will try to create a model that will help predict this. 

Here are what the columns represent:
* credit.policy: 1 if the customer meets the credit underwriting criteria of LendingClub.com, and 0 otherwise.
* purpose: The purpose of the loan (takes values "credit_card", "debt_consolidation", "educational", "major_purchase", "small_business", and "all_other").
* int.rate: The interest rate of the loan, as a proportion (a rate of 11% would be stored as 0.11). Borrowers judged by LendingClub.com to be more risky are assigned higher interest rates.
* installment: The monthly installments owed by the borrower if the loan is funded.
* log.annual.inc: The natural log of the self-reported annual income of the borrower.
* dti: The debt-to-income ratio of the borrower (amount of debt divided by annual income).
* fico: The FICO credit score of the borrower.
* days.with.cr.line: The number of days the borrower has had a credit line.
* revol.bal: The borrower's revolving balance (amount unpaid at the end of the credit card billing cycle).
* revol.util: The borrower's revolving line utilization rate (the amount of the credit line used relative to total credit available).
* inq.last.6mths: The borrower's number of inquiries by creditors in the last 6 months.
* delinq.2yrs: The number of times the borrower had been 30+ days past due on a payment in the past 2 years.
* pub.rec: The borrower's number of derogatory public records (bankruptcy filings, tax liens, or judgments).

# Import Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

"""## Get the Data

**Used pandas to read loan_data.csv as a dataframe called loans.**
"""

loans = pd.read_csv('loan_data.csv')

"""**Checked out the info(), head(), and describe() methods on loans.**"""

loans.info()

loans.describe()

loans.head()

"""# Exploratory Data Analysis

**Generated a histogram of two FICO distributions on top of each other, one for each credit.policy outcome.**
"""

plt.figure(figsize=(10,6))
loans[loans['credit.policy']==1]['fico'].hist(alpha=0.5,color='blue',
                                              bins=30,label='Credit.Policy=1')
loans[loans['credit.policy']==0]['fico'].hist(alpha=0.5,color='red',
                                              bins=30,label='Credit.Policy=0')
plt.legend()
plt.xlabel('FICO')

"""**Created a similar figure, except this time select by the not.fully.paid column.**"""

plt.figure(figsize=(10,6))
loans[loans['not.fully.paid']==1]['fico'].hist(alpha=0.5,color='blue',
                                              bins=30,label='not.fully.paid=1')
loans[loans['not.fully.paid']==0]['fico'].hist(alpha=0.5,color='red',
                                              bins=30,label='not.fully.paid=0')
plt.legend()
plt.xlabel('FICO')

"""**Generated a countplot using seaborn showing the counts of loans by purpose, with the color hue defined by not.fully.paid.**"""

plt.figure(figsize=(11,7))
sns.countplot(x='purpose',hue='not.fully.paid',data=loans,palette='Set1')

"""**Visualizing the trend between FICO score and interest rate.**"""

sns.jointplot(x='fico',y='int.rate',data=loans,color='purple')

"""**Generated the following lmplots to see if the trend differed between not.fully.paid and credit.policy.**"""

plt.figure(figsize=(11,7))
sns.lmplot(y='int.rate',x='fico',data=loans,hue='credit.policy',
           col='not.fully.paid',palette='Set1')

"""**Setting up the Data for Random Forest Classification Model**"""

loans.info()

"""## Categorical Features

Noticed the **purpose** column as categorical. So need to transform them using dummy variables, such that sklearn will be able to understand them.

**Created a list of 1 element containing the string 'purpose'. Call this list cat_feats.**
"""

cat_feats = ['purpose']

"""**Now use pd.get_dummies(loans,columns=cat_feats,drop_first=True) to create a fixed larger dataframe that has new feature columns with dummy variables.**"""

final_data = pd.get_dummies(loans,columns=cat_feats,drop_first=True)

final_data.info()

"""## Train Test Split"""

from sklearn.model_selection import train_test_split

X = final_data.drop('not.fully.paid',axis=1)
y = final_data['not.fully.paid']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=101)

"""## Training a Decision Tree Model"""

from sklearn.tree import DecisionTreeClassifier

"""**Created an instance of DecisionTreeClassifier() called dtree and fit it to the training data.**"""

dtree = DecisionTreeClassifier()

dtree.fit(X_train,y_train)

"""## Predictions and Evaluation of Decision Tree
**Created predictions from the test set and created a classification report and a confusion matrix.**
"""

predictions = dtree.predict(X_test)

from sklearn.metrics import classification_report,confusion_matrix

print(classification_report(y_test,predictions))

print(confusion_matrix(y_test,predictions))

"""## Training the Random Forest model

**Created an instance of the RandomForestClassifier class and fit it to our training data from the previous step.**
"""

from sklearn.ensemble import RandomForestClassifier

rfc = RandomForestClassifier(n_estimators=600)

rfc.fit(X_train,y_train)

"""## Predictions and Evaluation

**Predicted the class of not.fully.paid for the X_test data.**
"""

predictions = rfc.predict(X_test)

"""**Generated a classification report from the results.**"""

from sklearn.metrics import classification_report,confusion_matrix

print(classification_report(y_test,predictions))

"""**Show the Confusion Matrix for the predictions.**"""

print(confusion_matrix(y_test,predictions))

"""# The End!



"""