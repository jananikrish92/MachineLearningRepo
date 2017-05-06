import numpy as np
import csv
from sklearn import linear_model
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.svm import SVC
import time
#clf = SVC(kernel = "linear")


def logRegression():
	logreg = linear_model.LogisticRegression()
	f=open("trainLR.csv",'r')
	reader=csv.reader(f,delimiter=",")
	header = next(reader)
	ncol=len(header) 
	train = np.loadtxt("trainLR.csv", delimiter=',', skiprows=1, usecols=range(2,ncol))
	test = np.loadtxt("testLR.csv", delimiter=',', skiprows=1, usecols=range(2,ncol))

	train_x = train[:,:len(train[0])-1]
	train_y = train[:,len(train[0])-1]
	test_x = test[:,:len(train[0])-1]
	test_y = test[:,len(train[0])-1]

	logreg.fit(train_x, train_y	)

	predictions = logreg.predict(test_x)

	print "LR",accuracy_score(test_y, predictions)


	from sklearn.externals import joblib
	joblib.dump(logreg,'test.pkl')
	lr1  = joblib.load('test.pkl') 

	#print lr1.coef_[0]


	#hyperparameter selection 5-fold crossvalidation using gridsearchCV
	# from sklearn.model_selection import GridSearchCV
	# parameters = {'C':[(x /100.0) for x in range(1,1000)]}
	# clf = GridSearchCV(logreg, parameters, cv=5)
	# clf.fit(train_x, train_y)
	# predictions = clf.predict(test_x)

	#to predict for other users 
	model  = joblib.load('test.pkl') 


	f=open("train.csv",'r')
	reader=csv.reader(f,delimiter=",")
	header = next(reader)
	ncol=len(header)
	#print ncol
	data = np.loadtxt("train.csv", delimiter=',', skiprows=1, usecols=range(2,ncol-2))

	label = np.loadtxt("train.csv", delimiter=',', skiprows=1, usecols=range(ncol - 1,ncol))
	predictions = model.predict(data)

	#print "LR",accuracy_score(label, predictions)

	f1 = open('ratingwithFilter.csv','wb')
	writer = csv.writer(f1)
	header.append("predicted_rating")
	header.append("ignore_flag")
	#writer.writerow(header)
	i = 0
	filterCount = 0

	with open("train.csv", "rb") as infile :
		reader = csv.reader(infile)
	   	next(reader, None)
		for row in reader:
			rowList=[]
			rowList.append(row[0])
			rowList.append(row[1])
			rowList.append(row[9])
			row.append(predictions[i])
			
			if float(predictions[i]) == float(label[i]):
				rowList.append(0)
			else:			
				rowList.append(1)
				filterCount += 1
		
			writer.writerow(rowList)
			i += 1



