import DBSetup
import csv
 
dbmgr = DBSetup.DatabaseManager("ml.db")

#for row in :
#    print row


def showCount():
	try:
		for row in dbmgr.query("select count(*) from  exp1_product_similarity "):	
			print "Records in exp1_product_similarity ", row[0]

		for row in dbmgr.query("select count(*) from  train_data "):	
			print "Records in Train Data", row[0]

		for row in dbmgr.query("select count(*) from  test_data "):	
			print "Records in Test Data", row[0]

	except Exception,e: print str(e)

def showData():
	try:

		for row in dbmgr.query("select * from  exp1_product_similarity "):	
			print  row

		for row in dbmgr.query("select * from  train_data "):	
			print row

		for row in dbmgr.query("select * from  test_data "):	
			print row

	except Exception,e: print str(e)


def showUserSimilarity():
	try:
		print "calling her"
		for row in dbmgr.query("select * from user_similarity "):
			print row

	except Exception,e: print str(e)


def deleteUserSimilarity():
	try:
		dbmgr.query("delete from user_similarity ")

	except Exception,e: print str(e)

deleteUserSimilarity()
#showUserSimilarity()