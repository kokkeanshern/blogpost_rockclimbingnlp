import pymongo

# Retrieves MongoDB connection string from a file.
def get_Mongo_connectionstring(file_in):
    file = open(file_in,'r')
    connectionstring = file.readline()
    return connectionstring

# Connects to MongoDB and returns the collection object.
def mongodb_setup(file_in,collection):
    connectionstring = get_Mongo_connectionstring(file_in)
    client = pymongo.MongoClient(connectionstring)
    db = client['amazondb']
    collection = db[collection]
    return collection

# Writes to MongoDB.
def send_to_mongodb(doc,collection):
    collection.insert_one(doc)

# Adds a new field to a document.
def update_mongodb_addfield(collection,query_doc,new_fieldname,new_fieldval):
    myquery = query_doc
    newvalues = { "$set": { new_fieldname: new_fieldval } }
    collection.update_many(myquery, newvalues)

def get_distinct(collection,field):
    distinct_field = collection.distinct(field)
    return distinct_field
