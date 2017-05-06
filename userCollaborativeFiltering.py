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
from queryData import insertUserSimilarity
from queryData import getSimilarUser
from queryData import deleteUserSimilarityFromDB

from sets import Set
import math
import operator

isTrain = True
expId = 1

distProdId = getdistinctProduct(isTrain) # has the distinct product id's
n = len(distProdId)

distUserId = getdistinctUser(isTrain) # has the distinct product id's
userLen = len(distUserId)

#print userLen

def pairwiseUserSimilarity(commonProdInterLen):
	deleteUserSimilarityFromDB()
	distProdId = getdistinctProduct(isTrain) # has the distinct product id's
	n = len(distProdId)

	distUserId = getdistinctUser(isTrain) # has the distinct product id's
	userLen = len(distUserId)

	print userLen

	print "distinct Users Cnt ",userLen
	

	productResult1 = {} 
	productResult2 = {}
	userToProducts = {}
	userToProductResult = {}
	
	for u in range(0,userLen):
		productResult = getProductOfUsers(distUserId[u], isTrain)
		userToProductResult[u] = productResult
		productSet = set(productResult.keys())
		userToProducts[u] = productSet
		
	#print productResult

	#print userToProductResult

	#print userToProducts

	for u in range(0,userLen):
		
		if u%1000 == 0:
			print "done  ",u

		productResult1 = userToProducts[u]

		for v in range(u+1,userLen):
			
			productResult2 = userToProducts[v]
			commonProducts = productResult1.intersection(productResult2)
			commonProductsLen = len(commonProducts)
			# if commonProductsLen > 0:
			# 	print  commonProductsLen

			if commonProductsLen > commonProdInterLen:
				#print 
				r_pu_sum = 0
				r_pv_sum = 0

				for p in commonProducts:
					try:
						r_pu_sum = r_pu_sum + userToProductResult[u][p]
						r_pv_sum = r_pv_sum + userToProductResult[v][p]
					except Exception,e: continue

				numerator = 0
				factor1 = 0
				factor2 = 0
				denominator1 = 0	
				denominator2 = 0	

				ru_mean = float(r_pu_sum)/commonProductsLen
				rv_mean = float(r_pv_sum)/commonProductsLen


				for p in commonProducts:
					try:
						r_pu = userToProductResult[u][p]
						r_pv = userToProductResult[v][p]

						factor1 = r_pu - ru_mean
						factor2 = r_pv - rv_mean

						numerator = numerator + (factor1 * factor2)

						denominator1 = denominator1 + (factor1 * factor1)
						denominator2 = denominator2 + (factor2 * factor2)

					except Exception,e: continue

				if denominator1 == 0 or denominator2 == 0:
					sim_u_v = 1
				else:
					sim_u_v = numerator/(math.sqrt(denominator1) * math.sqrt(denominator2))

				# if distUserId[u] == 'A10FL3MC9QFZ7P' and distUserId[v] == 'A1H5CRR7Z4SV9F':
				# 	print r_pu_sum,r_pv_sum,commonProducts
				# 	print distUserId[u],distUserId[v],commonProductsLen,ru_mean,rv_mean,denominator1,denominator2,numerator
				# 	print "Similarity: ",u,v,sim_u_v

				insertUserSimilarity(distUserId[u],distUserId[v],sim_u_v);

				#print "Similarity: ",u,v,sim_u_v

	insertCommit()

def userBasedCollabFiltering():

	#print "distinct users",userLen
    
	distProdId = getdistinctProduct(isTrain) # has the distinct product id's
	n = len(distProdId)

	distUserId = getdistinctUser(isTrain) # has the distinct product id's
	userLen = len(distUserId)


	result = {}
	productsToUser = {}
	productToUserResult = {}

	totalRecommendations = 0
	totalHits = 0

	for i in range(0,n):
		userResult = getUsersOfProduct(distProdId[i], isTrain)
		productToUserResult[i] = userResult
		userSet = set(userResult.keys())
		productsToUser[i] = userSet


	similarUserMap = {}
	for j in range(0,userLen):
		similarUserResult = getSimilarUser(distUserId[j])
		similarUserMap[j] = similarUserResult


	# for all products
	for i in range(0,n):
		
		usersRatedInTest = getUsersOfProduct(distProdId[i], False)
		userSetTest = set(usersRatedInTest.keys())

		numRecommendations = 0
		numHits = 0
		if i % 10000 == 0:
			print "done",i

		recommendation = {}
		usersRated = productsToUser[i]
		usersRatedResult = productToUserResult[i]

		# for all users
		for u in range(0, userLen):
			# already rated
			if u in usersRated:
				continue;

			similarToUser_u = similarUserMap[u]
			commonUserIds = usersRated.intersection(similarToUser_u.keys())

			if len(commonUserIds) > 0:

				numerator = float(0);
				denominator = float(0);

				for uId in commonUserIds:
					simScore = similarToUser_u[uId]
					
					if simScore == 0:
						continue
					try:
						numerator += simScore * usersRatedResult[uId]	
						denominator += math.fabs(simScore)
					except:continue

				# no new product to recommend
				if denominator == 0:
					continue;

				recommendationScore = numerator/denominator		
				recommendation[u] = recommendationScore

		if expId == 1:
			#print recommendation
			for j in recommendation.keys():

				if recommendation[j] > 0 :
					numRecommendations += 1
					if distUserId[j] in userSetTest:
						#print "Recommnding ",j
						numHits += 1

		totalRecommendations += numRecommendations
		totalHits += numHits
		
	
	try:
		rec_success = 0
		if totalRecommendations == 0:
			rec_success = 0
		else:
			rec_success = float(totalHits)/float(totalRecommendations)

		print "Total Rec : ",totalRecommendations," Total Hits",totalHits, " Recomendation Success : ",rec_success
	except:
		print " "



def userExperiment1():

	distProdId = getdistinctProduct(isTrain) # has the distinct product id's
	n = len(distProdId)

	distUserId = getdistinctUser(isTrain) # has the distinct product id's
	userLen = len(distUserId)

	print "Distinct Products Count :", n
	print "Distinct users count :", userLen
	
	# function calculates the pearson coeff
	pairwiseUserSimilarity(30) # 30 Common Products Per user

	#function calcualtes the recommendation success
	userBasedCollabFiltering()


def userExperiment2():

	# Function below removes the data where the sentiment analysis prediction doesnt match with the actual rating 
	resetIgnore()

	distProdId = getdistinctProduct(isTrain)
	n = len(distProdId)

	distUserId = getdistinctUser(isTrain)
	userLen = len(distUserId)

	print "Distinct Products Count :", n
	print "Distinct users count :", userLen
	
	# function calculates the pearson coeff
	pairwiseUserSimilarity(30) # 30 Common Products Per User

	#function calcualtes the recommendation success
	userBasedCollabFiltering()
