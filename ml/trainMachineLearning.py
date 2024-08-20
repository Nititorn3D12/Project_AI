import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import tree
import pickle

df = pd.read_csv('abalone.csv') #แก้
#input_columns = ["Length","Diameter","Height","Whole weight","Shucked weight","Viscera weight","Shell weight"] #แก้
input_columns = ["Length","Height","Shell weight"]
output_columns = ["Rings"] #แก้
X = df.loc[:,input_columns] 
y = df.loc[:,output_columns] 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .20, random_state = 1,)


clf = tree.DecisionTreeRegressor(random_state = 0) 
#clf = LinearRegression()
clf.fit(X_train, y_train) #เรียน หาค่า m กับ b ออกมา
#ทำนายบนชุดทดสอบ
y_p = clf.predict(X_test)
#วัดผล MSE 
print(np.sqrt(metrics.mean_squared_error(y_test, y_p)))
#save model
pickle.dump(clf, open('decisiontree.pickle', 'wb'))