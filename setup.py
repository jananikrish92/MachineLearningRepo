from createtable import callCreateDBSchema
from initializeData import initialiseData

callCreateDBSchema()
initialiseData(0.6) #train:test ratio = 60:40

