from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # store all scraped data
    mars_data = {}
    


    # NASA Mars News
    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)

    html1 = browser.html
    soup1 = BeautifulSoup(html1, "html.parser")

    # Collecting news title and news paragraph
    results = soup1.find('div', class_='list_text')
    mars_data["news_title"] = results.find('div', class_='content_title').text
    mars_data["news_p"] = results.find('div', class_='article_teaser_body').text




    # URL of JPL Featured Space Image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    # find featured image
    result2 = soup2.find('a', class_='button fancybox')

    featured_image_url = "https://www.jpl.nasa.gov" + result2['data-fancybox-href']

    mars_data["featured_image_url"] = featured_image_url



    # Mars Weather
    # URL of Mars Weather twitter account
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)

    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')

    # Scrape the latest Mars weather tweet from the page
    result3 = soup3.find('div', class_='js-tweet-text-container')

    # save tweet into variable 'mars_weather'
    mars_data["mars_weather"] = result3.find('p', class_='tweet-text').text




    # Mars Facts
    # URL of Mars Facts webpage
    url4 = 'http://space-facts.com/mars/'

    # use Pandas to scrape the table containing facts about the planet
    tables = pd.read_html(url4)

    df = tables[0]


    # convert the data to a HTML table string
    html_table = df.to_html()
    mars_data["html_table"] = html_table.replace('\n', '')





    # Mars Hemispheres
    # create dictionary to store data using the keys 'img_url' and 'title'
    hemisphere_image_urls = []

    # URL of USGS Astrogeology site first image
    url_1 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url_1)

    html_1 = browser.html
    soup_1 = BeautifulSoup(html_1, 'html.parser')

    img_url_1 = soup_1.find('img', class_='wide-image')['src']
    title_1 = soup_1.find('h2', class_="title").text

    # URL of USGS Astrogeology site second image
    url_2 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url_2)

    html_2 = browser.html
    soup_2 = BeautifulSoup(html_2, 'html.parser')

    img_url_2 = soup_2.find('img', class_='wide-image')['src']
    title_2 = soup_2.find('h2', class_="title").text

    # URL of USGS Astrogeology site third image
    url_3 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url_3)

    html_3 = browser.html
    soup_3 = BeautifulSoup(html_3, 'html.parser')

    img_url_3 = soup_3.find('img', class_='wide-image')['src']
    title_3 = soup_3.find('h2', class_="title").text

    # URL of USGS Astrogeology site fourth image
    url_4 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url_4)

    html_4 = browser.html
    soup_4 = BeautifulSoup(html_4, 'html.parser')

    img_url_4 = soup_4.find('img', class_='wide-image')['src']
    title_4 = soup_4.find('h2', class_="title").text

    # Store data into python dictionary
    img1 = {"title" : title_1, "img_url" : "https://astrogeology.usgs.gov/" + img_url_1}
    img2 = {"title" : title_2, "img_url" : "https://astrogeology.usgs.gov/" + img_url_2}
    img3 = {"title" : title_3, "img_url" : "https://astrogeology.usgs.gov/" + img_url_3}
    img4 = {"title" : title_4, "img_url" : "https://astrogeology.usgs.gov/" + img_url_4}

    hemisphere_image_urls.append(img1)
    hemisphere_image_urls.append(img2)
    hemisphere_image_urls.append(img3)
    hemisphere_image_urls.append(img4)

    mars_data["hemisphere_image_urls"] = hemisphere_image_urls



    # return all scraped data
    return mars_data
