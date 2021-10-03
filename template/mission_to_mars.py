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
def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    mars_latest_news(browser)
    news_title, news_p = mars_latest_news(browser)
    
    data = {
        "news_title" = news_title,
        "news_paragraph" = news_p
    }
    browser.quit()
    return data
    

def mars_latest_news(browser):
    
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    content_titles = soup.find_all('div', class_='content_title')
    further = content_titles[1]
    further
    news_title = further.text
    news_title

    news_p = soup.find('div', class_='article_teaser_body').text
    
    return news_title, news_p


# ## Featured Image Scraping

def featured_image(browser):
    image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"

    browser.visit(image_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    image_full = soup.find('img', class_="headerimage fade-in")['src']
    image_full



    full_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + image_full



    print(full_image_url)
    return full_image_url


# ## On to Mars Facts

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context



mars_facts_df = pd.read_html('https://space-facts.com/mars/')


#this is not a dataframe at the moment, it is a big list, but the
#first item has the values desired for this project
print(mars_facts_df)


mars_facts_df = mars_facts_df[0]


print(mars_facts_df)


#name the columns
mars_facts_df.columns=['Statistic', "Value"]

(mars_facts_df)


html_mars_facts = mars_facts_df.to_html()
print(html_mars_facts)


print(type(html_mars_facts))


# ## Onto Hemispheres
def hemispheres(browser):
    
    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemis_url)

    html = browser.html
    soup = bs(html, 'html.parser')
    links_from_home = []
    
    list_h = soup.find_all('a', class_='itemLink product-item')
    only_one = []


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
    hemisphere_image_urls = []

    for link in link_from_home:
        hemisphere_dict = {}
        browser.visit(link)
        html = browser.html
        soup = bs(html, 'html.parser')
        test = browser.find_by_css('h2.title').text
        print(test)
        hemisphere_dict['title'] = test
        image_url = soup.find('img', class_='wide-image')['src']
        image_url = part_one + image_url
        print(image_url)
        hemisphere_dict['img_url'] = image_url
        hemisphere_image_urls.append(hemisphere_dict)


    print(hemisphere_image_urls)
    return hemisphere_image_urls





