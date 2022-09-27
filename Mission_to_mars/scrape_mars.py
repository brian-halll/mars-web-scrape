from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
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


    # find desired html table data to store in variable / database using pandas
    tables = pd.read_html(url) 

    # save table into dataframe
    mars_earth_df = tables[0]

    mars_earth_html = mars_earth_df.to_html('table.html')
    #mars_earth_html = mars_earth_html.replace('\n', '')


    # Store data in dictionary
    mars_data = {
        "mars_earth_html" : mars_earth_df.to_html().replace('\n', ''),
        "featured_image_url" : featured_image_url,
        "article_title" : article_title,
        "article_description" : article_description
    }

    browser.quit()

    return mars_data

