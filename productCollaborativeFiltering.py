from queryData import getdistinctProduct
from queryData import getUsersOfProduct
from queryData import insertProdSimilarity
from queryData import insertCommit
from queryData import getdistinctUser
from queryData import getProductOfUsers
from queryData import getSimilarProduct
from queryData import insertRecomendationData
from queryData import deleteSimilarityFromDB
from queryData import resetIgnore
from queryData import insertRecomendationData
from queryData import getRecommendationData
from queryData import deleteRecommendationData
import math

from sets import Set
import math
import operator



isTrain = True #flag which specifies to fetch the data from the train table
expId = 1

distProdId = getdistinctProduct(isTrain) # has the distinct product id's
n = len(distProdId)


distUserId = getdistinctUser(isTrain) # has the distinct user id's
userLen = len(distUserId)


#function to calculate item-based CF for different length of common users
def pairwiseProdSimilarity(commonUserInterLen):
	userResult1 = {}  
	userResult2 = {}
	productToUsers = {}
	productToUserResult = {}

	#gets the users and rating for each distinct product from the train 
	for i in range(0,n):
		userResult = getUsersOfProduct(distProdId[i], isTrain)
		# stores the product index and the corresponding user and rating in the dictionary
		productToUserResult[i] = userResult 
		usersSet = set(userResult.keys())
		# stores the users who have rated for the products 
		productToUsers[i] = usersSet
		
	

	#pearson's correlation for item-based CF : set of users who rated both product 'i' and product 'j'
	for i in range(0,n):
		
		if i%10000 == 0:
			print "done  ",i

		userResult1 = productToUsers[i]
		for j in range(i+1,n):
			
			userResult2 = productToUsers[j]
			commonUsers = userResult1.intersection(userResult2) #finding commonusers who have rated products
			commonUserLen = len(commonUsers)

			if commonUserLen > commonUserInterLen:
				#print 
				r_ui_sum = 0
				r_uj_sum = 0
				for u in commonUsers:
					try:
						r_ui_sum = r_ui_sum + productToUserResult[i][u]
						r_uj_sum = r_uj_sum + productToUserResult[j][u]
					except Exception,e: continue

				numerator = 0
				factor1 = 0
				factor2 = 0
				denominator1 = 0	
				denominator2 = 0	

				ri_mean = float(r_ui_sum)/commonUserLen
				rj_mean = float(r_uj_sum)/commonUserLen


				#print commonUserLen, r_ui_sum,ri_mean,r_uj_sum,rj_mean


				for u in commonUsers:
					try:
						r_ui = productToUserResult[i][u]
						r_uj = productToUserResult[j][u]

						factor1 = r_ui - ri_mean
						factor2 = r_uj - rj_mean

						numerator = numerator + (factor1 * factor2)

						denominator1 = denominator1 + (factor1 * factor1)
						denominator2 = denominator2 + (factor2 * factor2)

					except Exception,e: continue

				if denominator1 == 0 or denominator2 == 0:
					sim_i_j = 1
				else:
					sim_i_j = numerator/(math.sqrt(denominator1) * math.sqrt(denominator2))
				
				# insert Product Similarity calculated which is used for the product collaborative filtering
				insertProdSimilarity(distProdId[i],distProdId[j],sim_i_j);

	insertCommit()

#
def productBasedCollabFiltering():

	#print "distinct users",userLen
    
	result = {}
	userToProducts = {}
	userToProductResult = {}

	totalRecommendations = 0
	totalHits = 0

	for i in range(0,userLen):
		productResult = getProductOfUsers(distUserId[i], isTrain)
		userToProductResult[i] = productResult
		productSet = set(productResult.keys())
		userToProducts[i] = productSet


	similarProductMap = {}

	for i in range(0,n):
		similarProductResult = getSimilarProduct(distProdId[i]) # function fetches the data whichas isnrted in the pariwise similarity function
		similarProductMap[i] = similarProductResult

	# for all users
	for u in range(0,userLen):
		
		productsRatedInTest = getProductOfUsers(distUserId[u], False)
		productSetTest = set(productsRatedInTest.keys())

		numRecommendations = 0
		numHits = 0
		# if u % 10000 == 0:
		# 	print "User ", u

		recommendation = {}
		productsRated = userToProducts[u]
		productsRatedResult = userToProductResult[u]
		# for all products
		for i in range(0, n):
			# already rated
			if i in productsRated:
				continue;
			similarToProd_i = similarProductMap[i]
			commonProductIds = productsRated.intersection(similarToProd_i.keys())
			if len(commonProductIds) > 0:

				numerator = float(0);
				denominator = float(0);

				for pId in commonProductIds:
					simScore = similarToProd_i[pId]
					
					if simScore == 0:
						continue
					try:
						#print simScore, pId, productsRatedResult[pId]
						numerator += simScore * productsRatedResult[pId]	
						denominator += math.fabs(simScore)
					except:continue

				# no new product to recommend
				if denominator == 0:
					continue;

				recommendationScore = numerator/denominator		
				recommendation[i] = recommendationScore

		for j in recommendation.keys():
			if recommendation[j] > 0 :
				numRecommendations += 1
				if distProdId[j] in productSetTest:
					numHits += 1
					testrating = productsRatedInTest[distProdId[j]]
					predictedRating = recommendationScore
					testUser = distUserId[u]
					testProduct = distProdId[j]
					insertRecomendationData(testUser,testProduct,predictedRating,testrating)

		totalRecommendations += numRecommendations
		totalHits += numHits
		
	insertCommit()
	try:
		rec_success = 0
		if totalRecommendations == 0:
			rec_success = 0
		else:
			rec_success = float(totalHits)/float(totalRecommendations)

		print "Total Rec : ",totalRecommendations," Total Hits",totalHits, " Recomendation Success : ",rec_success
	except:
		print " "

def comparisonPercentageRecVSTest():
	rowList = getRecommendationData()
	countx = 0 
	county = 0
	countz = 0
	for i in rowList:
		row = rowList[i]
		if math.ceil(row[2]) == row[3]:
			countx = countx+1
		elif math.fabs(math.ceil(row[2])-row[3]) ==1:
			county = county+1
		else:
			countz = countz+1
	percentageX = (countx/float(len(rowList)))*100
	percentageY = (county/float(len(rowList)))*100
	percentageZ = (countz/float(len(rowList)))*100
	print "% recommended score matches the rating: ",percentageX
	print "% recommended score and the rating: is off by 1: ",percentageY
	print "% recommended score and the rating: is off by 2 or more: ",percentageZ
	deleteRecommendationData()

def experiment1():

	distProdId = getdistinctProduct(isTrain) # has the distinct product id's
	n = len(distProdId)

	distUserId = getdistinctUser(isTrain) # has the distinct product id's
	userLen = len(distUserId)

	print "Distinct Products Count :", n
	print "Distinct users count :", userLen
	

	# funtion deletes existing similarity already if inserted
	deleteSimilarityFromDB()
	
	# function calculates the pearson coeff
	pairwiseProdSimilarity(30) # 30 Common users Per Product

	#function calculates the recommendation success
	productBasedCollabFiltering()
	comparisonPercentageRecVSTest()

def experiment2():

	# Function below removes the data where the sentiment analysis prediction doesnt match with the actual rating 
	resetIgnore()

	distProdId = getdistinctProduct(isTrain)
	n = len(distProdId)

	distUserId = getdistinctUser(isTrain)
	userLen = len(distUserId)

	print "Distinct Products Count :", n
	print "Distinct users count :", userLen

	
	# funtion deletes existing similarity already if inserted
	deleteSimilarityFromDB()
	
	# function calculates the pearson coeff
	pairwiseProdSimilarity(30) # 30 Common users Per Product

	#function calcualtes the recommendation success
	productBasedCollabFiltering()
	comparisonPercentageRecVSTest()