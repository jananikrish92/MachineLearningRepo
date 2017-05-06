import DBSetup

dbmgr = DBSetup.DatabaseManager("ml.db")

def createTableProducSimilarity():
       dbmgr.query("CREATE TABLE IF NOT EXISTS exp1_product_similarity \
              (prodid_i char(100),\
       prodid_j char(100), \
       sim_i_j real )")

def createIndexOnProductSimData():
       dbmgr.query("create index IF NOT EXISTS index3 on exp1_product_similarity(prodid_i)")
       dbmgr.query("create index IF NOT EXISTS index4 on exp1_product_similarity(prodid_j)")

def createTabletrain():
       dbmgr.query("CREATE TABLE IF NOT EXISTS train_data \
               (productid char(100), \
       userid char(100), \
       act_rating int, \
       ignore int)")

def createTabletest():
       dbmgr.query("CREATE TABLE IF NOT EXISTS test_data \
               (productid char(100), \
       userid char(100), \
       act_rating int, \
       ignore int)")

def createIndexOnTrainData():
       dbmgr.query("create index IF NOT EXISTS index5 on train_data(productid)")
       dbmgr.query("create index IF NOT EXISTS index6 on train_data(userid)")
       dbmgr.query("create index if NOT EXISTS index9 on train_data(ignore) ")


def createIndexOnTestData():
       dbmgr.query("create index IF NOT EXISTS index7 on test_data(productid)")
       dbmgr.query("create index IF NOT EXISTS index8 on test_data(userid)")
       dbmgr.query("create index if NOT EXISTS index10 on test_data(ignore) ")

def createProdBasedRecTable():
 dbmgr.query("CREATE TABLE IF NOT EXISTS prod_based_recomendation \
               (userid char(100), \
       prodid char(100), \
       score int,\
       actual_rating int)")
               
def createTableUserSimilarity():
       dbmgr.query("CREATE TABLE IF NOT EXISTS user_similarity \
              (userid_i char(100),\
       userid_j char(100), \
       sim_i_j real )")

def createIndexOnUserSimData():
       dbmgr.query("create index IF NOT EXISTS index11 on user_similarity(userid_i)")
       dbmgr.query("create index IF NOT EXISTS index12 on user_similarity(userid_j)")

def callCreateDBSchema():
       createTableProducSimilarity()
       createIndexOnProductSimData()
       createTabletrain()
       createTabletest()
       createIndexOnTrainData()
       createIndexOnTestData()
       createProdBasedRecTable()
       createTableUserSimilarity()
       createIndexOnUserSimData()
