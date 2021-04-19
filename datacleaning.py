import re

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
