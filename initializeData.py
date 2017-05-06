import DBSetup
import csv
import random
 
dbmgr = DBSetup.DatabaseManager("ml.db")

def createTestTrainData(trainRatio):
	i = 0
	sql_train = 'INSERT INTO train_data  VALUES (?,?,?,?)';
	sql_test = 'INSERT INTO test_data  VALUES (?,?,?,?)';
	rowList = []
	with open('ratingwithFilter.csv', 'rb') as csvfile:
	     reader = csv.reader(csvfile)
	     for row in reader:
	     	rowList.append(row)
	     	i= i+1

	# shuffle the list			
	random. shuffle(rowList)

	print len(rowList),": Records to be inserted"

	for row in rowList:
		user,product,rating,ignore = row
		toss = random.uniform(0, 1)
		if (toss <= trainRatio):
			dbmgr.insertQuery1(sql_train,product,user,rating,ignore)
		else:
			dbmgr.insertQuery1(sql_test,product,user,rating,ignore)

	print "Data Initialise Completed"
	dbmgr.commitQuery()



def deletefromDB():
	dbmgr.query("delete from exp1_product_similarity ")
	dbmgr.query("delete from train_data ")
	dbmgr.query("delete from test_data ")
	dbmgr.query("delete from user_similarity ")
	dbmgr.query("delete from exp1_product_similarity ")
	dbmgr.commitQuery()

def initialiseData(trainRatio):
	deletefromDB()
	createTestTrainData(trainRatio)