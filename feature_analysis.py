import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.covariance import empirical_covariance

traindata = np.array(json.load(open("traindata.json")))
testdata = np.array(json.load(open("testdata.json")))
data = np.concatenate((traindata, testdata))
feature_num = np.shape(data)[1]-1

# for time_ind in range(len(data[0])):
#     if data[0][time_ind] > 120.:
#         print(data[0][time_ind])
#         print(time_ind)

# plt.hist(data[:, 0], bins = 120, color = "r")
# plt.hist(data[:, 15], bins = 100, color = "r")
# plt.show()

X = traindata[:, 0:feature_num]

print(np.corrcoef(X[:, 14], X[:, 18]))
