import re
import codecs
import csv
import math
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
def sentimentAnalysis():
	countpos = 0
	file = codecs.open("movies.txt", "r",encoding='utf-8', errors='ignore') 
	userId =""
	proId = ""
	rating =""
	sid = SentimentIntensityAnalyzer()

	f1 = open("train.csv","wb")

	header = ["UserID","ProductID","NegativeScore","NegativeCount","NeutralScore","NeutralCount","PostiveScore","PostiveCount","Bias","Rating","New Rating"]

	writer1 = csv.writer(f1)

	f2 = open("testLR.csv","wb")
	f3 = open("trainLR.csv","wb")
	writer2 = csv.writer(f2)
	writer3 = csv.writer(f3)
	#print header
	Users = []
	product = []
	count = 0
	for line in file:
		count = count+1
		if count >=500000:
			if line.split(":",1)[0] =="review/userId":
				userId =line.split(": ",1)[1].rstrip('\r\n')
				Users.append(userId)
		if count == 1000000:
			break
	file.close()
	distinctUsers = list(set(Users))
	traindata = distinctUsers[0:int(math.floor(len(distinctUsers)*0.80))]
	testData = distinctUsers[int(math.floor(len(distinctUsers)*0.80)):]
	writer1.writerow(header)
	header = ["UserID","ProductID","NegativeScore","NegativeCount","NeutralScore","NeutralCount","PostiveScore","PostiveCount","Bias","Rating"]
	writer2.writerow(header)
	writer3.writerow(header)
	count = 0

	file = codecs.open("movies.txt", "r",encoding='utf-8', errors='ignore') 
	for line in file:
		# print "entered"
		avg_pos = 0
		avg_neg = 0
		avg_neu = 0
		countpos = 0
		countneg = 0
		countneu = 0
		sentences = []
		new_rating = 0
		if line.split(":",1)[0] =="review/userId":
			userId =line.split(": ",1)[1].rstrip('\r\n')
			count = count+1
		if count >= 500000:
			if line.split(":",1)[0] =="product/productId":
				proId =line.split(": ",1)[1].rstrip('\r\n')
			if line.split(":",1)[0] =="review/score":
				rating =line.split(": ",1)[1].rstrip('\r\n')
			# import pdb
			# pdb.set_trace()
			if line.split(":",1)[0]=="review/text":
				# print "hello"
				lines_list = tokenize.sent_tokenize(line.split(": ",1)[1])
				sentences.extend(lines_list)
				for sen in sentences:
					max = 0
					ss = sid.polarity_scores(sen)
					avg_pos += ss['pos']
					avg_neu += ss['neu']
					avg_neg += ss['neg']
					if max < ss['pos']:
						max = ss['pos']
						str1 = 'pos'
					if max < ss['neg']:
						max = ss['neg']
						str1 = 'neg'
					if max < ss['neu']:
						max = ss['neu']
						str1 = 'neu'
					if str1 == 'pos':
						countpos = countpos+1
					if str1 == 'neg':
						countneg = countneg+1
					if str1 == 'neu':
						countneu = countneu+1
					# print countneu,countneg,countpos
					# print str1
				if float(rating) == 3.0 or float(rating) == 4.0 or float(rating) == 5.0:
					new_rating = 1
				else:
					new_rating = 0
				if count % 100000 == 0:
					print "processed ",count," records."	
				if userId in traindata:
					writer3.writerow([userId,proId,avg_neg/len(sentences),countneg,avg_neu/len(sentences),countneu,avg_pos/len(sentences),countpos,1,new_rating])
				else:
					writer2.writerow([userId,proId,avg_neg/len(sentences),countneg,avg_neu/len(sentences),countneu,avg_pos/len(sentences),countpos,1,new_rating])	
				writer1.writerow([userId,proId,avg_neg/len(sentences),countneg,avg_neu/len(sentences),countneu,avg_pos/len(sentences),countpos,1,rating,new_rating])
			
			if count == 1000000:
				break
