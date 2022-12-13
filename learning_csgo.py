import json
from sklearn import svm
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import ConstantKernel, RBF, Matern
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import calibration_curve
from sklearn.metrics import log_loss
import xgboost as xgb
import numpy as np
import matplotlib.pyplot as plt


traindata = np.array(json.load(open("traindata.json")))
testdata = np.array(json.load(open("testdata.json")))
feat_num = np.shape(traindata)[1]-1

trim_amount = 2
test_num = 10000
train_num = None #replace with None if all data is to be used
gpc_num = 500
trainmax = np.max(traindata, axis = 0)
trainmin = np.min(traindata, axis = 0)
X_test = np.zeros((test_num, feat_num))
# X_test = np.zeros((test_num, feat_num-2))
y_test = np.zeros(test_num)
n = 1
tot = 0
cts = [0]*6
ts = [0]*6
diff = [0]*6
while tot < test_num:
    #
    # if (testdata[n, 0] > 0.0 and testdata[n, 0] < 40.5) and ((testdata[n, 1] == 0 and np.random.random() > 0.99) and (testdata[n, 14] > 21000. and testdata[n, 15] > 20000.)):
    # or (testdata[n, 4] > 60. and testdata[n, 4] < 60.5)) and ((testdata[n, 0] == 4 and testdata[n, 2] == 5) and (testdata[n, 1] > 20000 and testdata[n, 3] > 20000)):
    # if np.random.random() > 0.95 and (testdata[n, 14] > 20000. and testdata[n, 15] > 20000.):# and testdata[n, 5] == 1:
    # if testdata[n, 0]-testdata[n-1, 0] < 0. and testdata[n, 1] == 1:
    if np.random.random() > 0.95:
        # currdiff = 0
        # for i in range(6):
        #     cts[i] += testdata[n, i+2]
        #     ts[i] += testdata[n, i+8]
        #     currdiff += testdata[n, i+2]*i - testdata[n, i+8]*i
        # # print(currdiff)
        # diff[int(np.abs(currdiff))] += 1
        for i in range(feat_num):
            X_test[tot, i] = (testdata[n, i]-trainmin[i])/(trainmax[i]-trainmin[i])
            # if i not in [14, 15]:
            #     if i > 15:
            #         X_test[tot, i-2] = (testdata[n, i]-trainmin[i])/(trainmax[i]-trainmin[i])
            #     else:
            #         X_test[tot, i] = (testdata[n, i]-trainmin[i])/(trainmax[i]-trainmin[i])
        y_test[tot] = testdata[n, feat_num]
        tot += 1
    n += 1

if train_num:
    X = np.zeros((train_num, feat_num))
    y = np.zeros(train_num)
    j = 0
    corr_ind = 0
    while corr_ind < train_num:
        if (traindata[j, 14] > 26000. and traindata[j, 15] >= 24000.):
            for i in range(feat_num):
                X[corr_ind, i] = (traindata[j, i]-trainmin[i])/(trainmax[i]-trainmin[i])
            y[corr_ind] = traindata[j, feat_num]
            corr_ind += 1
        j += 1
else:
    X = np.zeros((len(traindata), feat_num))
    # X = np.zeros((len(traindata), feat_num-2))
    for i in range(feat_num):
        X[:, i] = (traindata[:, i]-trainmin[i])/(trainmax[i]-trainmin[i])
        # if i not in [14, 15]:
        #     if i > 15:
        #         X[:, i-2] = (traindata[:, i]-trainmin[i])/(trainmax[i]-trainmin[i])
        #     else:
        #         X[:, i] = (traindata[:, i]-trainmin[i])/(trainmax[i]-trainmin[i])
    y = traindata[:, feat_num]



X_trim = np.zeros((len(X), feat_num-trim_amount))
for i in range(feat_num-trim_amount):
    X_trim[:, i] = X[:, i]
y_trim = y



# clf = svm.SVC(kernel = "rbf") #kernel = "rbf"
# clf.fit(X, y)
#
# rbf = ConstantKernel(1.0) * RBF(np.array([1.]*21))
# gpc_gauss = GaussianProcessClassifier(kernel=rbf, n_restarts_optimizer = 10)
# #gpc_gauss.fit(X[0:gpc_num, :], y[0:gpc_num])
# gpc_rand = np.random.randint(0, len(traindata), gpc_num)
# gpc_gauss.fit(X[gpc_rand, :], y[gpc_rand])
# print(gpc.score(X, y))
#
# matern = ConstantKernel(1.0) * Matern(length_scale=0.1)
# gpc_matern = GaussianProcessClassifier(kernel=matern, n_restarts_optimizer = 10)
# gpc_matern.fit(X[0:gpc_num, :], y[0:gpc_num])
#
# knn = KNeighborsClassifier(11)
# knn.fit(X, y)

# dtc = DecisionTreeClassifier(max_depth = 16)
# dtc.fit(X, y)
#
# dtc_bag = BaggingClassifier(DecisionTreeClassifier(max_depth = 16), max_samples = train_num//10, n_estimators=10, random_state=0)
# dtc_bag.fit((traindata[:, 0:feat_num]-trainmin[0:feat_num])/(trainmax[0:feat_num]-trainmin[0:feat_num]), traindata[:, feat_num])
# dtc_bag.fit(X, y)

xgb_clf = xgb.XGBClassifier(objective = "binary:logistic")
xgb_clf.fit(X, y)

xgb_clf_trim = xgb.XGBClassifier(objective = "binary:logistic")
xgb_clf_trim.fit(X_trim, y_trim)

lgr = LogisticRegression()
lgr.fit(X, y)

print("\n" + str(len(X)) + " training frames. \n")
# print("DTC Accuracy: " + str(1 - np.sum(np.abs(y_test - dtc.predict(X_test)))/len(y_test)) + ", Prediction average: " + str(np.sum(dtc.predict(X_test))/len(y_test)))
# print("DTC Bag Accuracy: " + str(1 - np.sum(np.abs(y_test - dtc_bag.predict(X_test)))/len(y_test)) + ", Prediction average: " + str(np.sum(dtc_bag.predict(X_test))/len(y_test)))
# print("SVM Gauss Accuracy: " + str(1 - np.sum(np.abs(y_test - clf.predict(X_test)))/len(y_test)) + ", Prediction average: " + str(np.sum(clf.predict(X_test))/len(y_test)))
# print("KNN Accuracy: " + str(1 - np.sum(np.abs(y_test - knn.predict(X_test)))/len(y_test)) + ", Prediction average: " + str(np.sum(knn.predict(X_test))/len(y_test)) + ", Probability average: " + str(np.sum(knn.predict_proba(X_test)[:, 1])/len(y_test)) + ".")
print("Logreg Accuracy: " + str(1. - np.sum(np.abs(y_test - lgr.predict(X_test)))/len(y_test)) + ", Prediction average: " + str(np.sum(lgr.predict(X_test))/len(y_test)) + ", Probability average: " + str(np.sum(lgr.predict_proba(X_test)[:, 1])/len(y_test)) + ".")
# print("GPC Gauss Accuracy: " + str(1. - np.sum(np.abs(y_test - gpc_gauss.predict(X_test)))/len(y_test)) + ", Prediction average: " + str(np.sum(gpc_gauss.predict(X_test))/len(y_test)) + ", Probability average: " + str(np.sum(gpc_gauss.predict_proba(X_test)[:, 1])/len(y_test)) + ".")
# print("GPC Matern Accuracy: " + str(np.sum(1 - np.abs(y_test - gpc_matern.predict(X_test)))/len(y_test)) + ", Prediction average: " + str(np.sum(gpc_matern.predict(X_test))/len(y_test)) + ", Probability average: " + str(np.sum(gpc_matern.predict_proba(X_test)[:, 1])/len(y_test)) + ".")
print("XGBoost Accuracy: " + str(1. - np.sum(np.abs(y_test - xgb_clf.predict(X_test)))/len(y_test)) + ", Prediction average: " + str(np.sum(xgb_clf.predict(X_test))/len(y_test)) + ", Probability average: " + str(np.sum(xgb_clf.predict_proba(X_test)[:, 1])/len(y_test)) + ".")
print("XGBoost trimmed data Accuracy: " + str(1. - np.sum(np.abs(y_test - xgb_clf_trim.predict(X_test[:, 0:feat_num-trim_amount])))/len(y_test)) + ", Prediction average: " + str(np.sum(xgb_clf_trim.predict(X_test[:, 0:feat_num-trim_amount]))/len(y_test)) + ", Probability average: " + str(np.sum(xgb_clf_trim.predict_proba(X_test[:, 0:feat_num-trim_amount])[:, 1])/len(y_test)) + ".\n")

print("Across " + str(len(y_test)) + " test frames and " + str(np.sum(y_test)) + " CT(1) victories.\n")

prob_true, prob_pred = calibration_curve(y_test, xgb_clf.predict_proba(X_test)[:, 1], n_bins=10)

print(prob_true - prob_pred)
print(log_loss(y_test, xgb_clf.predict_proba(X_test)[:, 1]))

plt.plot(prob_true, prob_pred)
plt.show()

prob_true, prob_pred = calibration_curve(y_test, xgb_clf_trim.predict_proba(X_test[:, 0:feat_num-trim_amount])[:, 1], n_bins=10)

print(prob_true - prob_pred)
print(log_loss(y_test, xgb_clf_trim.predict_proba(X_test[:, 0:feat_num-trim_amount])[:, 1]))

plt.plot(prob_true, prob_pred)
plt.show()

roundkillframes = []
X_round = np.zeros((500, feat_num))
y_round = np.zeros(500)
startind = 1
n = startind
last_frame_alive = testdata[n-1, 2:14]
while testdata[n, 0]-testdata[n-1,0] > 0. or testdata[n, 1] == 1:
    for i in range(feat_num):
        X_round[n-startind, i] = (testdata[n, i]-trainmin[i])/(trainmax[i]-trainmin[i])
    y_round[n-startind] = testdata[n, feat_num]
    # print(str(n) + ", " + str(testdata[n, 2:14]) + ", " + str(testdata[n, 1]) + ".")
    if not np.array_equal(testdata[n, 2:14], last_frame_alive):
        roundkillframes.append(float(n))
    last_frame_alive = testdata[n, 2:14]
    n += 1

X_round = X_round[0:n-startind, :]
y_round = y_round[0:n-startind]
roundkillframes = np.array(roundkillframes)
roundkillframes = roundkillframes/float(n-startind)

matchframes = 6000
matchrounds = []
X_match = np.zeros((matchframes, feat_num))
y_match = np.zeros(matchframes)
m = 0
while m < matchframes:
    for i in range(feat_num):
        X_match[m, i] = (testdata[m, i]-trainmin[i])/(trainmax[i]-trainmin[i])
    y_match[m] = testdata[m, feat_num]
    m += 1
    if testdata[m, 0] - testdata[m-1, 0] < 0. and testdata[m, 1] != 1:
        matchrounds.append(float(m)/float(matchframes))

ax = xgb.plot_importance(xgb_clf)
plt.show()

plt.plot(np.linspace(0., 1., n-startind), xgb_clf.predict_proba(X_round)[:, 1])
# plt.plot(np.linspace(0., 1., n-startind), gpc_gauss.predict_proba(X_round)[:, 1], color = "r")
# plt.plot(np.linspace(0., 1., n-startind), knn.predict_proba(X_round)[:, 1], color = "r")
plt.plot(np.linspace(0., 1., n-startind), xgb_clf_trim.predict_proba(X_round[:, 0:feat_num-trim_amount])[:, 1], color = "g")
for death_ind in roundkillframes:
    plt.axvline(death_ind, color='k', linestyle='dotted', linewidth=1)
plt.show()
plt.plot(np.linspace(0., 1., matchframes), xgb_clf.predict_proba(X_match)[:, 1])
# plt.plot(np.linspace(0., 1., matchframes), gpc_gauss.predict_proba(X_match)[:, 1], color = "r")
# plt.plot(np.linspace(0., 1., matchframes), knn.predict_proba(X_match)[:, 1], color = "r")
plt.plot(np.linspace(0., 1., matchframes), xgb_clf_trim.predict_proba(X_match[:, 0:feat_num-trim_amount])[:, 1], color = "g")
for round_ind in matchrounds:
    plt.axvline(round_ind, color='k', linestyle='dashed', linewidth=1)
plt.show()
