import scraper
import datacleaning as dc
import datatransfer as dt

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
driver = scraper.driver_setup()
collection = dt.mongodb_setup('C:\\Users\\Shern\\mongopwd.txt')
with open ("links.txt","r") as f:
    lines = f.readlines()
for url in lines:
    scraper.search_product(driver,url.strip("\n"),'')
    reviews_link = scraper.get_review_links(driver)
    query_doc = {"url":url.strip("\n")}
    dt.update_mongodb_addfield(collection,query_doc,"reviews_url",reviews_link)
