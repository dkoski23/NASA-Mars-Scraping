#!/usr/bin/env python
# coding: utf-8

# ## First Article Scraping


#make the imports
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

#setup browser variable for Chrome, making sure splinter is setup and 
#updated
def scraping():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    testing = {'test':'dict'}
    return




url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

#visit the url
browser.visit(url)


#after inspecting, get to the info for the latest article with soup
html = browser.html
soup = bs(html, 'html.parser')
content_titles = soup.find_all('div', class_='content_title')
#for some reason it says the first article is Mars Now, though it is
#actually NASA's Mars Fleet Lies Low with Sun Between Earth and Red Planet
#so I'll go deeper into content_titles to get that



#since I used find_all() I got a list back, and can index for the second
#value, which I know is the article I'm look for from glancing at the site
further = content_titles[1]
further



#now get just the text for the title
news_title = further.text
news_title


# In[8]:


#next go in and get the text for the description of the article
news_p = soup.find('div', class_='article_teaser_body').text
print(news_p)


# ## Featured Image Scraping


#visit link in assignment and get the url for the featured image
image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"


#visit in the notebook
browser.visit(image_url)



#follow same setup steps in previous section for the button
html = browser.html
soup = bs(html, 'html.parser')



#this is from not working from some reason, I will try examining 
#the button itself. It gives mars1 when it should return mars 3

#it worked when restarting the kernel. NASA changed the image while
#I was working, which confused me
image_full = soup.find('img', class_="headerimage fade-in")['src']
image_full



full_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + image_full



print(full_image_url)


# ## On to Mars Facts

# I found this solution to the error code
#urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1125)
# at https://moreless.medium.com/how-to-fix-python-ssl-certificate-verify-failed-97772d9dd14c

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context



mars_facts_df = pd.read_html('https://space-facts.com/mars/')


#this is not a dataframe at the moment, it is a big list, but the
#first item has the values desired for this project
mars_facts_df


mars_facts_df = mars_facts_df[0]


mars_facts_df


#name the columns
mars_facts_df.columns=['Statistic', "Value"]

mars_facts_df


html_mars_facts = mars_facts_df.to_html()
html_mars_facts


type(html_mars_facts)


# ## Onto Hemispheres


hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemis_url)

html = browser.html
soup = bs(html, 'html.parser')
links_from_home = []

#using find_all returns a list with repeat values, the only
#first_links = browser.find_by_css("a.product-item h3")
list_h = soup.find_all('a', class_='itemLink product-item')
only_one = []

#get only the full links to follow from the given page:
#https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

for link in list_h:
    #print(link)
    #print('--------------------')
    if link['href'] not in only_one:
        #print(link['href'])
        only_one.append(link['href'])
        
print(only_one)

part_one = 'https://astrogeology.usgs.gov'
for link in only_one:
    links_from_home.append(part_one + link)
links_from_home

#loop through the list of links
hemisphere_image_urls = []

for link in link_from_home:
    #set up a dictionary and re-establish browser for each hemisphere
    #site visited
    hemisphere_dict = {}
    browser.visit(link)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    #get the titles
    test = browser.find_by_css('h2.title').text
    print(test)
    hemisphere_dict['title'] = test
    
    #get the final urls
    image_url = soup.find('img', class_='wide-image')['src']
    image_url = part_one + image_url
    print(image_url)
    hemisphere_dict['img_url'] = image_url
    
  
    hemisphere_image_urls.append(hemisphere_dict)
    
    
hemisphere_image_urls


browser.quit()



