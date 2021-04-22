import scraper
import datacleaning as dc
import datatransfer as dt
import analysis as al

# Scraping all URLs for the brands in consideration.
# brands = ['la sportiva','ocun','five ten','tenaya','black diamond',
# 		  'scarpa','mad rock','climb x']
# base_url = "https://www.amazon.com/"
# driver = scraper.driver_setup()
# for brand in brands:
# 	scraper.search_product(driver, base_url,"s?k="+brand+' climbing shoe')
# 	scraper.iterate_pages(driver, filename='links2.txt')
# scraper.kill_driver(driver)

# Doing some filtering and cleaning on the URLs
# dc.view_brands("links.txt")
# dc.filter_links('links.txt')
# dc.edit_links('links.txt')
# dc.filter_links_2("links.txt")

# Write to MongoDB
# collection = dt.mongodb_setup('C:\\Users\\Shern\\mongopwd.txt')
# with open("links.txt" ,"r") as f:
#     lines = f.readlines()
# for url in lines:
#     doc = {"url":url.strip("\n")}
#     dt.send_to_mongodb(doc,collection)

# Scraping product info
# driver = scraper.driver_setup()
# collection = dt.mongodb_setup('C:\\Users\\Shern\\mongopwd.txt')
# with open("links2.txt","r") as f:
#         lines = f.readlines()
# # lines = lines[55:]
# for url in lines:
#     scraper.search_product(driver,url,'')
#     product_name = scraper.get_productname(driver)
#     product_price = scraper.get_productprice(driver)
#     product_reviews,num_reviews = scraper.get_productreviews(driver,collection)
#     doc = {"url":url,"product_name":product_name,"product_price":product_price,
#            "product_reviews":product_reviews,"num_reviews":num_reviews}
#     # Write to MongoDB
#     dt.send_to_mongodb(doc,collection)
#     print("last successful URL: "+url)
# scraper.kill_driver(driver)

# driver = scraper.driver_setup()
# with open ("links.txt", "r") as f:
#     lines = f.readlines()
# scraper.remove_duplicate_review_links(driver,lines)

# Add product name and product price to documents.
# driver = scraper.driver_setup()
# collection = dt.mongodb_setup('C:\\Users\\Shern\\mongopwd.txt')
# with open ("links.txt","r") as f:
#     lines = f.readlines()
# for url in lines:
#     scraper.search_product(driver,url,'')
#     product_name = scraper.get_productname(driver)
#     product_price = scraper.get_productprice(driver)
#     dt.update_mongodb_addfield(collection,{"url":url.strip("\n")},"product_name",product_name)
#     dt.update_mongodb_addfield(collection,{"url":url.strip("\n")},"product_price",product_price)

# Update MongoDB with reviews URL.
# driver = scraper.driver_setup()
# collection = dt.mongodb_setup('C:\\Users\\Shern\\mongopwd.txt')
# with open ("links.txt","r") as f:
#     lines = f.readlines()
# for url in lines:
#     scraper.search_product(driver,url.strip("\n"),'')
#     reviews_link = scraper.get_review_links(driver)
#     query_doc = {"url":url.strip("\n")}
#     dt.update_mongodb_addfield(collection,query_doc,"reviews_url",reviews_link)

# collection = dt.mongodb_setup('C:\\Users\\Shern\\mongopwd.txt',"products")
# driver = scraper.driver_setup()
# dist_reviews = dt.get_distinct(collection,"reviews_url")
# for url in dist_reviews:
#     if url != None:
#         scraper.search_product(driver,url,'')
#         product_reviews = scraper.get_productreviews(driver)
#         dt.update_mongodb_addfield(collection,{"reviews_url":url},"reviews",product_reviews)

# Updates MongoDB database with brand/model field.
# collection = dt.mongodb_setup('C:\\Users\\Shern\\mongopwd.txt',"products")
# all_prods = collection.find({"reviews_url":{"$ne":None}}).distinct("product_name")
# for product_name in all_prods:
#     product_model = dc.get_model(product_name)
#     dt.update_mongodb_addfield(collection,{"product_name":product_name},"model",product_model)

# Data Cleaning
# collection = dt.mongodb_setup('C:\\Users\\Shern\\mongopwd.txt',"products")
# stop_words = dc.initialize_stopwords()
# for document in collection.find({"reviews":{"$exists":True}}):
#     review_cleaned_arr = []
#     for review in document['reviews']:
#         cleaned_review = dc.remove_stopwords(review, stop_words)
#         review_cleaned_arr.append(cleaned_review)
#     dt.update_mongodb_addfield(collection,{"_id":document["_id"]},"cleaned_reviews",review_cleaned_arr)
        
# Display but do not save piechart.
collection = dt.mongodb_setup('C:\\Users\\Shern\\mongopwd.txt',"products")
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

# Find nuber of reviews for each brand then update dictionary_reviews values.
for brand in list(dictionary_reviews.keys()):
    num_reviews = 0
    for document in collection.find({"$and":[{"reviews":{"$exists":True}},{"brand":brand}]}):
        dictionary_reviews[brand] += len(document['reviews'])


# al.create_dualbar(list(dictionary_models.keys()),list(dictionary_models.values()),
#                   list(dictionary_reviews.values()))
# al.get_summary_stats(list(dictionary_models.keys()),list(dictionary_models.values()),
#                   list(dictionary_reviews.values()))
# al.rescale(list(dictionary_models.keys()),list(dictionary_models.values()),
#                   list(dictionary_reviews.values()))
# call the min_max_scaling function
# al.min_max_scaling(list(dictionary_models.keys()),list(dictionary_models.values()),
#                   list(dictionary_reviews.values()))

# for document in collection.find({"reviews":{"$exists":True}}):
#     num_reviews = len(document['reviews'])
#     brand = document['brand']
#     dictionary[brand] += num_reviews
# al.create_barchart(list(dictionary.values()),list(dictionary.keys()))