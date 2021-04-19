from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re


# Initialize the webdriver.
def driver_setup():
	driver_path = r"C:\Users\Shern\PycharmProjects\DS Projects\Rock Climbing Reviews\chromedriver_win32\chromedriver.exe"
	driver = webdriver.Chrome(executable_path=driver_path)
	driver.implicitly_wait(15)
	return driver

# Write to file.
def write_to_file(filename,content):
	f = open(filename, "a")
	f.write(content+"\n")
	f.close()

# Go to results page.
def search_product(driver,base_url,query):
	# Query format: https://www.amazon.com/s?k=<your query here>
	query_url = base_url+query
	driver.get(query_url)

# Scrape all URLs on a webpage
def get_all_urls(driver,filename):
	# identify elements with tagname <a>
	links = driver.find_elements_by_tag_name("a")
	# traverse list
	for link in links:
		# get_attribute() to get all href
		link = link.get_attribute('href')
		if (type(link) == str) and ('climbing' in link) and ('shoe' in link):
			write_to_file(filename,link)

# iterate through results pages
def iterate_pages(driver,filename):
	pages = driver.find_elements_by_class_name("a-normal")
	try:
		last_page = int(pages[-1].text)
		base_url = driver.current_url
		for page in range(2,last_page+1):
			get_all_urls(driver,filename)
			driver.get(base_url+'&page='+str(page))
	except IndexError:
		get_all_urls(driver,filename)

# Terminates the webdriver.
def kill_driver(driver):
	driver.quit()

# Scrapes the product name.
def get_productname(driver):
	try:
		product_name = driver.find_element(By.ID, 'productTitle').text
		return product_name
	except NoSuchElementException:
		product_name = None
		return product_name

# Scrapes product price.
def get_productprice(driver):
	try:
		product_price = driver.find_element(By.ID,'priceblock_ourprice').text
		return product_price
	except NoSuchElementException:
		product_price = None
		return product_price

# Scrapes product reviews.
def get_productreviews(driver):
	try:
		see_all_reviews_button = driver.find_element(By.XPATH,'//*[@id="reviews-medley-footer"]/div[2]/a')
		see_all_reviews_button.click()

		next_page = True
		product_reviews = []
		while next_page:
			# Click translate reviews button.
			try:
				translate_button = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div[1]/span/a')
				translate_button.click()
			except NoSuchElementException:
				print("no translate button found.")
				pass
			
			# Scrape all reviews on the current page.
			reviews = driver.find_elements(By.XPATH,'//span[@data-hook="review-body"]')
			for review in reviews:
				product_reviews.append(review.text)

			# Go to next page.
			try:
				next_page_button = driver.find_element(By.CSS_SELECTOR,"#cm_cr-pagination_bar > ul > li.a-last > a")
				next_page_button.click()

				print(next_page_button.get_attribute('href'))

			except NoSuchElementException:
				print("No next page button found.")
				next_page = False

	except NoSuchElementException:
		print("see all reviews button not found.")
		product_reviews = []
	
	num_reviews = len(product_reviews)

	return product_reviews, num_reviews


	