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

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_latest_news(browser)
    news_title, news_p = mars_latest_news(browser)
    
    featured_image(browser)
    full_image_url = featured_image(browser)
    
    mars_facts()
    html_mars_facts = mars_facts()
    
    hemispheres(browser)
    hemisphere_image_urls =  hemispheres(browser)
    
    data = {
        "Latest News Title" : news_title,
        "News Paragraph" : news_p,
        "Featured Image URL" : full_image_url,
        "Mars Facts html" : html_mars_facts,
        "Hemisphere URLS" : hemisphere_image_urls
    }
    print(data)
    browser.quit()
    return data
    

def mars_latest_news(browser):
    
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    content_titles = soup.find_all('div', class_='content_title')
    further = content_titles[1]
    news_title = further.text

    news_p = soup.find('div', class_='article_teaser_body').text
    
    return news_title, news_p


## Featured Image Scraping

def featured_image(browser):
    image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    image_full = soup.find('img', class_="headerimage fade-in")['src']

    full_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + image_full

    print(full_image_url)
    return full_image_url


# ## On to Mars Facts
def mars_facts():
    import os, ssl
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

    mars_facts_df = pd.read_html('https://space-facts.com/mars/')

    mars_facts_df = mars_facts_df[0]

    mars_facts_df.columns=['Statistic', "Value"]
    html_mars_facts = mars_facts_df.to_html()
    
    return html_mars_facts



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

    part_one = 'https://astrogeology.usgs.gov'
    for link in only_one:
        links_from_home.append(part_one + link)
    links_from_home
    hemisphere_image_urls = []

    for link in links_from_home:
        hemisphere_dict = {}
        browser.visit(link)
        html = browser.html
        soup = bs(html, 'html.parser')
        test = browser.find_by_css('h2.title').text
        hemisphere_dict['title'] = test
        image_url = soup.find('img', class_='wide-image')['src']
        image_url = part_one + image_url
        hemisphere_dict['img_url'] = image_url
        hemisphere_image_urls.append(hemisphere_dict)

    return hemisphere_image_urls





