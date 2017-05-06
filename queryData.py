import DBSetup
import csv
import random
 
dbmgr = DBSetup.DatabaseManager("ml.db")

def resetIgnore():
	try:
		dbmgr.query("delete from train_data where ignore = 1")
		dbmgr.query("delete from test_data where ignore = 1")
		dbmgr.commitQuery()
	except Exception,e:print str(e)

def showFromDB():
    for row in dbmgr.query("select * from exp1_product_similarity"):
		print row

def deletefromDB():
	dbmgr.query("delete from exp1_product_similarity ")
	dbmgr.query("delete from train_data ")
	dbmgr.query("delete from test_data ")
	dbmgr.query("delete from user_similarity ")
	dbmgr.query("delete from exp1_product_similarity ")
	dbmgr.commitQuery()
     	 
def deleteUserSimilarityFromDB():
	dbmgr.query("delete from user_similarity ")
	dbmgr.commitQuery()

def deleteSimilarityFromDB():
	dbmgr.query("delete from exp1_product_similarity ")
	dbmgr.commitQuery()

     	 
def getdistinctProduct(isTrain):
	try:
		result = []
		
		if isTrain:
			for row in dbmgr.query(" select distinct(productid) from train_data "):
				result.append(row[0])
		else:
			for row in dbmgr.query(" select distinct(productid) from test_data"):
				result.append(row[0])

		return result 
	except Exception,e: print str(e)

def getdistinctUser(isTrain):
	try:
		result = []
		
		if isTrain:
			for row in dbmgr.query("select distinct(userid) from  train_data"):
				result.append(row[0])
		else:
			for row in dbmgr.query("select distinct(userid) from  test_data"):
				result.append(row[0])

		return result 
	except:
		print "This is an error message!"

def countFromDB():
	try:
		for row in dbmgr.query("select count(*) from  exp1_rating_data "):
			print row[0]
	except Exception,e: print str(e)

def showFunctionOuput():
	actRes = []
	actRes = getdistinctProduct()
	print actRes

def getUsersOfProduct(prodid, isTrain):
	try:
		input = [];
		result = {}
		input.append(prodid)
		#print prodid
		if isTrain:
			for row in dbmgr.selectQuery("select userid,act_rating from train_data where productid = ? ", input):
				userId, userRating = row
				result[userId] = userRating
		else:
			for row in dbmgr.selectQuery("select userid,act_rating from test_data where productid = ? ", input):
				userId, userRating = row
				result[userId] = userRating

		return result;
	except Exception,e: print str(e)

def getProductOfUsers(userid, isTrain):
	try:
		input = [];
		result = {}
		input.append(userid)
		#print prodid
		if isTrain:
			for row in dbmgr.selectQuery("select productid,act_rating from train_data where userid = ? ", input):
				prodId, userRating = row
				result[prodId] = userRating
		else:
			for row in dbmgr.selectQuery("select productid,act_rating from test_data where userid = ? ", input):
				prodId, userRating = row
				result[prodId] = userRating

		return result;
	except Exception,e: print str(e)



def getSimilarProduct(prodid):
	try:
		input = [];
		result = {}
		input.append(prodid)
		#print prodid
		for row in dbmgr.selectQuery("select prodid_j,sim_i_j from exp1_product_similarity where prodid_i = ? ", input):
			prodId, similarity = row
			result[prodId] = similarity
		return result;
	except Exception,e: print str(e)


def getSimilarUser(userid):
	try:
		input = [];
		result = {}
		input.append(userid)
		#print prodid
		for row in dbmgr.selectQuery("select userid_j,sim_i_j from user_similarity where userid_i = ? ", input):
			userId, similarity = row
			result[userId] = similarity
		return result;
	except Exception,e: print str(e)


def insertProdSimilarity(producti,productj,sim_i_j):
	try:
		sql = 'INSERT INTO exp1_product_similarity VALUES (?,?,?)'
		dbmgr.insertQueryProductSimilarity(sql,producti,productj,sim_i_j)
		dbmgr.insertQueryProductSimilarity(sql,productj,producti,sim_i_j)

	except Exception,e: print str(e)

def insertUserSimilarity(useridi,useridj,sim_i_j):
	try:
		sql = 'INSERT INTO user_similarity VALUES (?,?,?)'
		dbmgr.insertQueryProductSimilarity(sql,useridi,useridj,sim_i_j)
		dbmgr.insertQueryProductSimilarity(sql,useridj,useridi,sim_i_j)

	except Exception,e: print str(e)

def insertCommit():
	try:
		dbmgr.commitQuery()
	except Exception,e: print str(e)

def getProductsRatedInTestForUser(userid):
	try:
		result = {}
		for row in dbmgr.selectQuery("select productid,act_rating  from  test_data where userid = ?",userid):	
			prodId,act_rating = row
			result[prodId]=act_rating

		#print len(result)
		return result

	except Exception,e: print str(e)

def getProductsRatedInTrainForUser(userid):
	try:
		result = {}
		for row in dbmgr.query("select productid,act_rating  from  train_data where userid = ?",userid):	
			prodId,act_rating = row
			result[prodId]=act_rating

		#print len(result)
		return result

	except Exception,e: print str(e)




def insertRecomendationData(userid,productid,score,act_rating):
	try:
		dbmgr.insertQuery1("insert into prod_based_recomendation values (?,?,?,?)",userid,productid,score,act_rating)
	except Exception,e: print str(e)

def deleteRecommendationData():
	try:
		dbmgr.query("delete from prod_based_recomendation")
	except:print ""
	
def getRecommendationData():
	try:
		
		rowList= []
		for row in dbmgr.query("select * from prod_based_recomendation"):
			rowList.append(row)
		return rowList
	except Exception as e: print ""

def getCount():

	for row in dbmgr.query("select count(*) from train_data "):
		print row[0]

	for row in dbmgr.query("select count(distinct(productid)) from train_data "):
		print row[0]
	for row in dbmgr.query("select count(distinct(productid)) from train_data where ignore = 1"):
		print row[0]

