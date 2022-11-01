from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape_info():
    # Set up splinter 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # visit first page
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # delay so that soup is not empty
    time.sleep(1)

    # Scrape Page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # find desired html to store in variable / database
    article_title = soup.find('div', class_ ='content_title').text
    article_description = soup.find('div', class_='article_teaser_body').text

    # visit second page
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # delay so that soup is not empty
    time.sleep(1)

    # Scrape Page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # find desired html to store in variable / database
    featured_image_url = f"{url}{soup.find('img', class_='headerimage fade-in')['src']}"

    # visit third page
    url = 'https://galaxyfacts-mars.com/'


    # find desired html table data to store in variable / database using pandas and save table into dataframe
    mars_earth_df = pd.read_html(url)[0]

    mars_earth_df.columns = ['Description', 'Mars', 'Earth']

    mars_earth_df.set_index('Description', inplace=True)

    # convert to html
    html = mars_earth_df.to_html()

    # remove escape sequences
    html = html.replace('\n', '')

    # visit fourth page 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemi_image_urls = []

    #Get a list of all the hemispheres 
    links = browser.find_by_css('a.product-item img')
    # dictionary for hemisphere info 
    hemi_info = {}
        
    for i in range(len(links)):
        
        # find elements on each loop to avoid stale element exceptions
        browser.find_by_css('a.product-item img')[i].click()
        
        # find the sample image anchor tag and extract the href
        sample = browser.links.find_by_text('Sample').first
        hemi_info["img_url"] = sample['href']
        
        # get hemisphere titles
        hemi_info["title"] = browser.find_by_css('h2.title').text
                
        #append hemisphere object to list
        hemi_image_urls.append(hemi_info)
        
        
        
        # navigate back to first page 
        browser.back()



    # Store data in dictionary
    mars_data = {
        "mars_earth_html" : html,
        "featured_image_url" : featured_image_url,
        "article_title" : article_title,
        "article_description" : article_description,
        "hemisphere_image_urls" : hemi_image_urls,
        "last_updated": dt.datetime.now()
    }

    browser.quit()
    
    return mars_data

