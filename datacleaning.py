import re
from colour import Color
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

# Initial filtering
def filter_links(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    with open(filename, "w") as f:
        for line in lines:
            # Remove sponsored product URLs.
            if re.search('slredirect',line.strip("\n")):
                pass
            # Remove results page URLs.
            elif re.search('s?k=',line.strip("\n")):
                pass
            # Remove URLs that do not start with base URL.
            elif not line.strip("\n").startswith("https://www.amazon.com"):
                pass
            # Remove URLs with gp or ap following its base URL.
            elif re.search('https://www.amazon.com/gp/',line.strip("\n")):
                pass
            elif re.search('https://www.amazon.com/ap/',line.strip("\n")):
                pass
            else:
                f.write(line)

# Removes everything in the URL from the "ref=" section onwards
def edit_links(filename):
    with open(filename,"r") as f:
        lines = f.readlines()
    with open(filename, "w") as f:
        for line in lines:
            line = line.strip("\n").split("ref=")
            f.write(line[0]+'\n')

# Prints the brands section of the URLs
def view_brands(filename):
    with open(filename,"r") as f:
        lines = f.readlines()
        brands = []
        for line in lines:
            line = re.split(".com/",line.strip("\n"))[1]
            line = re.split("-",line)[0]+'-'+re.split("-",line)[1]
            if line not in brands:
                brands.append(line)

    brands.sort()
    for brand in brands:
        print(brand)

# Removes URLs that point to other brands
def filter_links_2(filename):
    brands_bad = ['Adidas-Sport','Butora-Brava','Butora-Endeavor','Butora-Gomi','Crocs-Unisex',
    'DMM-Dyneema','Danner-Mens','Frogg-Toggs','Game-Quick','Korkers-Footwear',
    'MORENDL-Trekking','NewDoar-Anti','Nike-Metcon','Outdoor-Research','Reebok-FCK22',
    'Reebok-Womens','Salomon-Outline','Salomon-Womens','Sneakers-Trekking','So-iLL','Twisted-Distressed',
    'Vasque-Snowblime','Womens-Barefoot','Yaktrax-Traction']
    good_links=[]
    with open(filename,"r") as f:
        lines = f.readlines()
        for line in lines:
            good_links.append(line.strip("\n"))
    
    bad_links = []
    for line in lines:
        for brand in brands_bad:
            if brand in line.strip("\n"):
                bad_links.append(line.strip("\n"))

    good_links = list(set(good_links)-set(bad_links))
    with open(filename,"w") as f:
        for link in good_links:
            f.write(link+'\n')

def get_brand(product_name):
    # Keep only alphabets and white spaces.
    product_name = re.sub(r'[^a-zA-Z ]+', '', product_name)
    # Lowercase the name.
    product_name = product_name.lower()
    product_name = product_name.split(' ')
    brands = ['la sportiva','mad rock','ocun','tenaya','climb x',
              'scarpa','black diamond','five ten', 'evolv']
   
    # Captures brand names with two words.
    if (' '.join(product_name[:2]) in brands):
        brand = ' '.join(product_name[:2])
    # Captures brand names with one word.
    elif (product_name[0] in brands):
        brand = product_name[0]
    # Sometimes climb x is represented as one word.
    elif (product_name[0] == 'climbx'):
        brand = 'climb x'
    else:
        brand = None
 
    return brand

def check_color(color):
    try:
        Color(color)
        return True
    except ValueError:
        return False

def get_model(product_name):
    # Keep only alphabets and white spaces - removes size.
    product_name = re.sub(r'[^a-zA-Z ]+', ' ', product_name)
    # Lowercase the name.
    product_name = product_name.lower()
    product_name = product_name.split(' ')
    product_name=[x for x in product_name if len(x)>1]
    # product_name = list(set(product_name)-set(['']))
    brands = ['la sportiva','mad rock','ocun','tenaya','climb x',
              'scarpa','black diamond','five ten', 'evolv']
    

    # Removes brand from product name
    if (' '.join(product_name[:2]) in brands):
        product_model = product_name[2:]
    elif (product_name[0] in brands):
        product_model = product_name[1:]
    elif (product_name[0] == 'climbx'):
        product_model = product_name.remove('climbx')
    else:
        product_model = product_name

    # Removes colour from product name.
    try:
        for col in product_model:
            if check_color(col):
                product_model=[x for x in product_model if x != col]
    except TypeError:
        product_model = None
    
    # Remove gender, age group, shoe type.
    try:
        product_model = [x for x in product_model if x not in ["men","women","adult","kid","mens",
                                                               "womens","wmn","mn","unisex",
                                                               "climbing","shoe","shoes","rock","climb",
                                                               "eu","us","eur"]]
    except TypeError:
        pass
    
    if product_model == None:
        pass
    elif len(product_model) == 1:
        product_model = product_model[0]
    elif len(product_model) == 0:
        product_model = None
    else:
        product_model = ' '.join(product_model)
    
    return product_model


def initialize_stopwords():
    stop_words = set(stopwords.words('english'))
    return stop_words

def remove_stopwords(review,stop_words):
    cleaned_review = []
    review_tokens = word_tokenize(review)

    for w in review_tokens: 
        if w not in stop_words: 
            cleaned_review.append(w)
    return ' '.join(cleaned_review)

def clean_reviewurl(review_url):
    review_url = review_url.split("ref")[0]
    return review_url
