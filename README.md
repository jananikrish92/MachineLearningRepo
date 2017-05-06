Software requirement:
1) Python 2.7.12
2) The nltk version is 3.2.2
3) The scikit-learn version is 0.18.1
4) sqlite3 version '2.6.0'

Instructions to run the project:
1) download the dataset from http://snap.stanford.edu/data/web-Movies.html and place in the same folder.
2) Run python file runme.py
3) Run python setup.py
4) Run python main.py and choose the options from in order:



Make sure you have run setup.py before running this menu!!!!
 PS : Run the below menu in the order mentioned(1,2,3,4), so that its run n the same dataset ,or else setup has to be run every time 
Menu 
1. Product Based Collaborative Filtering(Default)
2. User Based Collaborative Filtering (Default)
3. Product Based Collaborative Filtering with Sentiment Analysis
4. User Based Collaborative Filtering  with Sentiment Analysis
5. Quit

Output format:
Presetting n=30, If 'n' has to be changed the value should be manually updated in the experiment functions of the code in the file productCollaborativeFiltering and userCollborativeFiltering. In the experiment function ,pairwiseProdSimilarity is defined in case of itemBased CF , pass different value of 'n'. Similarly for userBased CF make the similar change in userExperiment function in the userCollabortiveFiltering python file in the folder.

1) for item-based:

Distinct Products Count : 13703
Distinct users count : 139865
Total Rec :  320861  Total Hits 43109  Recomendation Success :  0.134354128423
% recommended score matches the rating:  73.611078893
% recommended score and the rating: is off by 1:  13.1364680229
% recommended score and the rating: is off by 2 or more:  13.252453084

2) for user-based:
Total Rec :  514206  Total Hits 12933  Recomendation Success :  0.0251513984668

similar format results will be observed for option 3,4
option 5 will quit from the program

The graph is plotted manually from the result printed on running the code.

