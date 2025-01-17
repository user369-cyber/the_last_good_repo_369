import pymongo


client = pymongo.MongoClient("mongodb+srv://rk7018295:rsquare369@cluster0.ckt1qtj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
database_1 = client['game_database']
collection = database_1['collection']