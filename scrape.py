import platform, sys
import collections
from bs4 import BeautifulSoup
from selenium import webdriver

# PhantomJS files have different extensions
# under different operating systems
if platform.system() == 'Windows':
    PHANTOMJS_PATH = './phantomjs.exe'
else:
    PHANTOMJS_PATH = './phantomjs'

#ask user for search input
search = (raw_input("What would you like to search: "))
search = search.lower()
#create jet and amazon url
jetSearch = search.replace (" ", "%20")
amazonSearch = search.replace (" ", "+")
jetUrl = 'https://jet.com/search?term=' + jetSearch
amazonUrl = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + amazonSearch

#set up enviroment for scraping
browser = webdriver.PhantomJS(executable_path = 'phantomjs-2.1.1-macosx/bin/phantomjs')
browser.get(jetUrl)
soup = BeautifulSoup(browser.page_source, "html.parser")

#find div with all items
jetItems = soup.find_all('div', {'class': 'product desktop not_mobile'})
#create dictionary
jetData = {}
#for every item on the item panel
for jetItem in jetItems:
    jetLink = jetItem.findChildren()[0]
    jetProduct = jetLink.findChildren()[3]
    if (len(jetProduct.findChildren()) == 1): #check if there another div inside
        jetProduct = jetLink.findChildren()[3].findChildren()[0].get_text()
    else:
        jetProduct = jetLink.findChildren()[3].get_text()
    jetPrice = jetLink.findChildren()[4]
    if(len(jetPrice.findChildren())): #check if another div exists
        jetPrice = jetPrice.findChildren()[0].findChildren()[0].get_text()
    #convert unicod to strings
    jetProduct = str(jetProduct)
    jetPrice = str(jetPrice)
    jetString = len(jetProduct)
    #if more than 5 charceters
    if jetString > 5:
        #set product name to first two words from web display name
        jetProduct = jetProduct.split()
        jetProduct = jetProduct[0] + " " + jetProduct[1]
        #add product as key and price as value
        jetData[jetProduct] = jetPrice
        #order keys in alphabetical order
        jetData = collections.OrderedDict(sorted(jetData.items(), key=lambda t: t[0]))
    else:
        continue

#set up enviroment to scrape amazon
#need to paste amazon url here, because amazon has protected their data
browser.get('https://www.amazon.com/s/ref=nb_sb_ss_i_1_5?url=search-alias%3Daps&field-keywords=laundry+detergent&sprefix=laund%2Caps%2C703&rh=i%3Aaps%2Ck%3Alaundry+detergent')
soup2 = BeautifulSoup(browser.page_source, "html.parser")
#create dictionary
amazonData = {}
#find panel of items
amazonItems = soup2.find_all('div', {'class': 's-item-container'})
#for every item in the panel of items
for amazonItem in amazonItems:
    amazonProduct = amazonItem.find("a",attrs={"class": "a-link-normal s-access-detail-page  a-text-normal"})
    amazonProduct = amazonProduct["title"] #get  title tag
    amazonPrice = amazonItem.find("span",attrs={"class": "a-size-base a-color-price s-price a-text-bold"}).get_text()
    #convert unicode to strings
    amazonProduct = str(amazonProduct)
    amazonPrice = str(amazonPrice)
    #set product name to first two words from web display name
    amazonProduct = amazonProduct.split()
    amazonProduct = amazonProduct[0] + " " + amazonProduct[1]
    #add product as key and price as value
    amazonData[amazonProduct] = amazonPrice
    #order keys in alphabetical order
    amazonData = collections.OrderedDict(sorted(amazonData.items(), key=lambda t: t[0]))

i = 0 #amazon index
similar = 0 #number of similar items
amazon = 0 #amazon count
jet = 0 #count for jet items
#iterate through amazon items
for amazonKey, amazonValue in amazonData.iteritems():
    j = 0 #jet index
    #iterate through jet items
    for jetKey, jetValue in jetData.iteritems():
        #if same keys then compare price
        if amazonData.keys()[i] == jetData.keys()[j]:
            if amazonData.values()[i] > jetData.values()[j]:
                amazon = amazon + 1
            else:
                jet = jet + 1
            similar = similar + 1
        j = j + 1 #increment jet index
    i = i + 1 #increment amazon index

#print values
print "%d %s were compared between Jet and Amazon." % (similar, search)
print "After scraping and comapring the data between Jet and Amazon we found %s %s cheaper on Jet and %s %s cheaper on Amazon." % (jet, search, amazon, search)










