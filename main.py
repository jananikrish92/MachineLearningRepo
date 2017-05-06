from productCollaborativeFiltering import experiment1
from productCollaborativeFiltering import experiment2
from userCollaborativeFiltering import userExperiment1,userExperiment2

def mainMenu():
	while True:
		print "Make sure you have run setup.py before running this menu!!!!"
		print " PS : Run the below menu in the order mentioned(1,2,3,4), so that its run n the same dataset ,or else setup has to be run every time "

		print "Menu "
		print "1. Product Based Collaborative Filtering(Default)"
		print "2. User Based Collaborative Filtering (Default)"
		print "3. Product Based Collaborative Filtering with Sentiment Analysis"
		print "4. User Based Collaborative Filtering  with Sentiment Analysis"
		print "5. Quit"
		option = input('Enter your option : ')

		if option == 1:
			# Runs product based collaborative filtering on the train dataset
			experiment1()
		elif option == 2:
			# Runs user based collaborative filtering on the train dataset
			userExperiment1()
		elif option == 3:
			# Run Product based collaborative filtering on the train dataset with sentiment analysis performed
			experiment2()
		elif option == 4:
			# Run user based collaborative filtering on the train dataset with sentiment analysis performed
			userExperiment2()
		else:
			print "Thank You!!"
			break

mainMenu()

