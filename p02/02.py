import matplotlib.pyplot as plt

#data for learn#
from sklearn import datasets
#svm : support vector machine#
from sklearn import svm

digits = datasets.load_digits()

#classifier#
clf = svm.SVC(gamma=0.001, C=100)

#total num of data#
print(len(digits.data))

#first try#
'''
x,y = digits.data[:-1], digits.target[:-1]

clf.fit(x,y)

print('Prediction:', clf.predict(digits.data[-1]))

plt.imshow(digits.images[-1], cmap=plt.cm.gray_r, interpolation="nearest")
plt.show()
'''
#second try#
x,y = digits.data[:-10], digits.target[:-10]

clf.fit(x,y)

print('Prediction:', clf.predict(digits.data[-2]))

plt.imshow(digits.images[-2], cmap=plt.cm.gray_r, interpolation="nearest")
plt.show()

