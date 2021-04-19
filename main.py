import scraper
import datacleaning as dc

# Scraping all URLs for the brands in consideration.
# brands = ['la sportiva','ocun','five ten','tenaya','black diamond',
# 		  'scarpa','mad rock','climb x']
# base_url = "https://www.amazon.com/"
# driver = scraper.driver_setup()
# for brand in brands:
# 	scraper.search_product(driver, base_url,brand+' climbing shoe')
# 	scraper.iterate_pages(driver, filename='links2.txt')
# scraper.kill_driver(driver)

# Doing some filtering and cleaning on the URLs
# dc.view_brands("links.txt")
# dc.filter_links('links.txt')
# dc.edit_links('links.txt')
# dc.filter_links_2("links.txt")