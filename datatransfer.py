import pymongo

def get_Mongo_connectionstring(file_in):
    file = open(file_in,'r')
    connectionstring = file.readline()
    return connectionstring

def mongodb_setup(file_in):
    connectionstring = get_Mongo_connectionstring(file_in)
    client = pymongo.MongoClient(connectionstring)
    db = client['amazondb']
    collection = db['rawdata']
    return collection

def send_to_mongodb(doc,collection):
    collection.insert_one(doc)