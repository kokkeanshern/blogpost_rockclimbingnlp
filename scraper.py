from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re

# Uncomment this to use Chrome in headless mode.
# options = Options()
# options.headless = True

# Initialize the webdriver.
driver_path = r"C:\Users\Shern\PycharmProjects\DS Projects\Rock Climbing Reviews\chromedriver_win32\chromedriver.exe"
# driver = webdriver.Chrome(options=options,executable_path=driver_path)
driver = webdriver.Chrome(executable_path=driver_path)
driver.implicitly_wait(30)

# Base URL.
base_url = "https://www.amazon.com/"

def write_to_file(filename,content):
	f = open(filename, "a")
	f.write(content+"\n")
	f.close()

def search_product(base_url,query):
	# Query format: https://www.amazon.com/s?k=<your query here>
	query_url = base_url+"s?k="+query
	driver.get(query_url)

def get_all_urls():
	# identify elements with tagname <a>
	links = driver.find_elements_by_tag_name("a")
	# traverse list
	for link in links:
		# get_attribute() to get all href
		link = link.get_attribute('href')
		if (type(link) == str) and ('climbing' in link) and ('shoe' in link):
			write_to_file('links.txt',link)

def iterate_pages():
	pages = driver.find_elements_by_class_name("a-normal")
	try:
		last_page = int(pages[-1].text)
		base_url = driver.current_url
		for page in range(2,last_page+1):
			get_all_urls()
			driver.get(base_url+'&page='+str(page))
	except IndexError:
		get_all_urls()


brands = ['la sportiva','ocun','five ten','tenaya','black diamond',
		  'scarpa','mad rock','climb x']
for brand in brands:
	search_product(base_url,brand+' climbing shoe')
	iterate_pages()
driver.quit()