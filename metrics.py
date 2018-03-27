import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

y_true = [-1, 1, 1, -1, 1, -1, 1, 1, 1, 1]
y_pred = [-1, 1, 1, -1, -1, -1, 1, 1, 1, -1]
#print accuracy_score(y_true, y_pred)
#print precision_score(y_true, y_pred, average='macro') 

feature_true = [1,-1,-1,1,1,1,-1,1,1,1,1,1,1,1]
feature_pred = [1,-1,-1,1,1,1,1,-1,1,1,-1,1,1,1]


print accuracy_score(feature_true, feature_pred)