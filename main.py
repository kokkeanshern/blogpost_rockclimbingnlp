import scraper

brands = ['la sportiva','ocun','five ten','tenaya','black diamond',
		  'scarpa','mad rock','climb x']
brands = ['five ten']
base_url = "https://www.amazon.com/"
driver = scraper.driver_setup()
for brand in brands:
	scraper.search_product(driver, base_url,brand+' climbing shoe')
	scraper.iterate_pages(driver, filename='links2.txt')
scraper.kill_driver(driver)