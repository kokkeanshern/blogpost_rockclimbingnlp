import pymongo

# Retrieves MongoDB connection string from a file.
def get_Mongo_connectionstring(file_in):
    file = open(file_in,'r')
    connectionstring = file.readline()
    return connectionstring

# Connects to MongoDB and returns the collection object.
def mongodb_setup(file_in):
    connectionstring = get_Mongo_connectionstring(file_in)
    client = pymongo.MongoClient(connectionstring)
    db = client['amazondb']
    collection = db['products']
    return collection

# Writes to MongoDB.
def send_to_mongodb(doc,collection):
    collection.insert_one(doc)

def update_mongodb_addfield(collection,query_doc,new_fieldname,new_fieldval):
    myquery = query_doc
    newvalues = { "$set": { new_fieldname: new_fieldval } }

    collection.update_one(myquery, newvalues)