import matplotlib.pyplot as plt

#data for learn#
from sklearn import datasets
#svm : support vector machine#
from sklearn import svm

digits = datasets.load_digits()

print(digits.data)

print(digits.target)

# you might want normalize data #
print(digits.images[0])
