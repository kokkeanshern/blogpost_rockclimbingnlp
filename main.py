import scraper as sc
import datacleaning as dc
import datatransfer as dt
import analysis as al
from bson.objectid import ObjectId

# ------------------------------------------------------------------------------------------------------------

# Setup Selenium webdriver and MongoDB collection.
driver = sc.driver_setup()
collection = dt.mongodb_setup('C:\\Users\\Shern\\mongopwd.txt',"products")

# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------

# Returns list containing lines from a file.
def read_file(filename):
    with open(filename,"r") as f:
        lines = f.readlines()
    return lines

# ------------------------------------------------------------------------------------------------------------

# Scrape URLs for brands.
def scrapeURL():
    brands = ['la sportiva','ocun','five ten','tenaya','black diamond',
            'scarpa','mad rock','climb x','evolv']
    base_url = "https://www.amazon.com/"
    for brand in brands:
        # Open results page for each brand.
        sc.search_product(driver, base_url,"s?k="+brand+' climbing shoe')
        # Iterate through results pages then save URL to a file.
        sc.iterate_pages(driver, filename='links2.txt')
    # Kill the webdriver.
    sc.kill_driver(driver)

# ------------------------------------------------------------------------------------------------------------

# Some function calls to aid data exploration and cleaning.
def data_exploration():
    # Print brand names from URL.
    dc.view_brands("links.txt")

def clean_links():
    # Filter out unwanted URLS.
    dc.filter_links('links.txt')
    # Removes the "ref=" section from URLs.
    dc.edit_links('links.txt')
    # Removes URLs that point to other brands.
    dc.filter_links_2("links.txt")

# ------------------------------------------------------------------------------------------------------------

# Write URLs to a MongoDB collection.
def write_URL_MongoDB():
    lines = read_file("links.txt")
    for url in lines:
        doc = {"url":url.strip("\n")}
        dt.send_to_mongodb(doc,collection)

# ------------------------------------------------------------------------------------------------------------

# Scrape product name and price.
def scrape_name_price():
    lines = read_file("links.txt")
    for url in lines:
        sc.search_product(driver,url,'')
        # Retrieve product name and price.
        product_name = sc.get_productname(driver)
        product_price = sc.get_productprice(driver)
        doc = {"url":url,"product_name":product_name,"product_price":product_price}
        # Write to MongoDB.
        dt.send_to_mongodb(doc,collection)
        print("last successful URL: "+url)
    sc.kill_driver(driver)

# ------------------------------------------------------------------------------------------------------------

# Update MongoDB with reviews URL.
def get_reviews_URL():
    lines = read_file("links.txt")
    for url in lines:
        sc.search_product(driver,url.strip("\n"),'')
        reviews_link = sc.get_review_links(driver)
        query_doc = {"url":url.strip("\n")}
        dt.update_mongodb_addfield(collection,query_doc,"reviews_url",reviews_link)

# ------------------------------------------------------------------------------------------------------------

# Scrape reviews.
def scrape_reviews():
    # Retrieve list of unique reviews URLs from MongoDB.
    dist_reviews = dt.get_distinct(collection,"reviews_url")
    for url in dist_reviews:
        if url != None:
            sc.search_product(driver,url,'')
            # List of product reviews.
            product_reviews = sc.get_productreviews(driver,url)
            # Updated MongoDB with new fields: (1) list of reviews and (2) number of reviews.
            dt.update_mongodb_addfield(collection,{"reviews_url":url},"reviews",product_reviews)
            dt.update_mongodb_addfield(collection,{"reviews_url":url},"num_reviews",len(product_reviews))

# ------------------------------------------------------------------------------------------------------------

# Updates MongoDB database with brand/model field.
def update_MongoDB_brand_model():
    all_prods = collection.find({"reviews_url":{"$ne":None}}).distinct("product_name")
    for product_name in all_prods:
        product_model = dc.get_model(product_name)
        product_brand = dc.get_brand(product_name)
        dt.update_mongodb_addfield(collection,{"product_name":product_name},"model",product_model)
        dt.update_mongodb_addfield(collection,{"product_name":product_name},"brand",product_brand)

# ------------------------------------------------------------------------------------------------------------

# Remove stopwords and update MongoDB.
def reviews_remove_stopwords():
    stop_words = dc.initialize_stopwords()
    # Iterate over all documents.
    for document in collection.find():
        review_cleaned_arr = []
        # For each review in a document, remove its stopwords and append to a new list.
        for review in document['reviews']:
            cleaned_review = dc.remove_stopwords(review, stop_words)
            review_cleaned_arr.append(cleaned_review)
        # Update MongoDB with list of cleaned reviews.
        dt.update_mongodb_addfield(collection,{"_id":document["_id"]},"cleaned_reviews",review_cleaned_arr)

# ------------------------------------------------------------------------------------------------------------

# Refers to Analysis Part 1 in the article.
def analysis_part1():
    # Create two dictionaries to hold the values.
    dictionary_models = {"black diamond" : 0,"climb x": 0, "evolv":0,
                "five ten":0, "la sportiva":0, "mad rock":0,
                "ocun":0, "scarpa":0, "tenaya":0}
    dictionary_reviews = {"black diamond" : 0,"climb x": 0, "evolv":0,
                "five ten":0, "la sportiva":0, "mad rock":0,
                "ocun":0, "scarpa":0, "tenaya":0}

    # Find number of unique models for each brand then update dictionary_models values.
    for model in list(dictionary_models.keys()):
        num_models = len(collection.distinct("model",{"$and":[{"brand":model},{"model":{"$ne":None}}]}))
        dictionary_models[model] += num_models

    # Find number of reviews for each brand then update dictionary_reviews values.
    for brand in list(dictionary_reviews.keys()):
        for document in collection.find({"brand":brand}):
            dictionary_reviews[brand] += document['num_reviews']

    # Create a dual-axis bar chart.
    al.create_dualbar(list(dictionary_models.keys()),list(dictionary_models.values()),
                    list(dictionary_reviews.values()))

# ------------------------------------------------------------------------------------------------------------

# Validate reviews by checking for duplicates.
def validate_reviews():
    for doc in collection.find({}):
        arr = doc['reviews']

    # Checks for duplicates.
    if doc['num_reviews'] != len(list(set(arr))):
        print("Document with ID "+doc['_id']+" has duplicates.")

# ------------------------------------------------------------------------------------------------------------

# Removes the "ref=" section of the reviews URL.
def clean_reviews_url():
    for doc in collection.find({}):
        reviews_url = dc.clean_reviewurl(doc['reviews_url'])
        dt.update_mongodb_addfield(collection,{"_id":doc["_id"]},"reviews_url2",reviews_url)

# ------------------------------------------------------------------------------------------------------------

# Keep only one document if filtering for reviews_url2 returns > 1 document.
def delete_dups():
    reviews_url = collection.distinct("reviews_url2")
    for url in reviews_url:
        num_docs = collection.count_documents({"reviews_url2":url})
        if num_docs > 1:
            for x in range(1,num_docs):
                collection.delete_one({"reviews_url2":url})

# ------------------------------------------------------------------------------------------------------------