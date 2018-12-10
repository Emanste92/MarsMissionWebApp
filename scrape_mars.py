# # # Mars info scraping across multiple websites
# # 1. import packages
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
from time import sleep 


from flask import Flask, jsonify
# look for mongo stuff


# splinter setup
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# # 2. running all the scrapes
# NASA Mars
nasa_url_start = "https://mars.nasa.gov/news/"
browser.visit(nasa_url_start)
news_date_extract = browser.find_by_css('.list_date')[0] # remember the . for the css class
latest_news_date = bs(news_date_extract.outer_html,'lxml').select('div')[0].text.strip()  # single string to find div in bs object
news_headline_extract = browser.find_by_css('.content_title')[0]
latest_news_headline = bs(news_headline_extract.outer_html,'lxml').select('div')[0].text.strip()
news_teaser_extract = browser.find_by_css('.article_teaser_body')[0]
latest_news_teaser = bs(news_teaser_extract.outer_html,'lxml').select('div')[0].text.strip()
news_url_extract = browser.find_by_css('.content_title')[0]
latest_news_url_extract = bs(news_url_extract.outer_html,'lxml').select('a')[0]['href']
latest_news_url = nasa_url_start + latest_news_url_extract # string concatenation to website base url 

# JPL
jpl_url_start = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(jpl_url_start)
browser.click_link_by_partial_text('FULL IMAGE')
sleep(5)
browser.click_link_by_partial_text('more info')
sleep(5)
img_url = browser.find_by_css('.main_image')[0]
img_url_extract = bs(img_url.outer_html,'lxml').select('img')[0]['src'] # single string to find src in bs object
jpl_url = "https://www.jpl.nasa.gov" + img_url_extract # string concatenation to website base url 

# Twitter weather
weather_url_start = "https://twitter.com/marswxreport?lang=en"
browser.visit(weather_url_start)
weather_date_extract = browser.find_by_css('._timestamp')[0]
tweet_weather_date = bs(weather_date_extract.outer_html,'lxml').select('span')[0].text.strip()
# doesn't take into account other tweets, just grabs whatever the first one is
weather_report_extract = browser.find_by_css('.tweet-text')[0]
tweet_weather_report = bs(weather_report_extract.outer_html,'lxml').select('p')[0].text.strip()

# Mars facts
facts_url = "https://space-facts.com/mars/"
fact_table_extract = pd.read_html(facts_url)
fact_table = fact_table_extract[0]
fact_table.columns = ['Fact', 'Value']

# Mars hemispheres
hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemispheres_url)
hemi_soup_prep = browser.find_by_id('product-section')
hemi_soup = bs(hemi_soup_prep.outer_html,'lxml')
# extracting the names from the bs object
hemi_names = hemi_soup.find_all('h3')
hemis_name_list = []
for hemi_name in hemi_names:
    hemis_name_list.append(hemi_name.text.strip().replace(' Enhanced',''))
# extracting the relative url from the bs object and concactenating to base url
hemi_urls = hemi_soup.find_all('a')
hemi_urls_prep = []
hemi_urls_list = []
for url in hemi_urls:
    hemi_urls_prep.append(url['href'])
# from https://stackoverflow.com/a/52676102
hemi_urls_list_cleaning = pd.Series(hemi_urls_prep).drop_duplicates().tolist()
for url in hemi_urls_list_cleaning:
    hemi_urls_list.append("https://astrogeology.usgs.gov" + url)
hi_res_hemis_urls = []
# one crazy appending of a list comprehension of a bs object with selection of the a.href 
# the bs a.href grab has to be done on the same page it's being accessed on and created
for url in hemi_urls_list:
    browser.visit(url)
    sleep(1)
    hemi_url_bs = bs(browser.find_link_by_partial_text('Original').outer_html,'lxml').select('a')[0]['href']
    hi_res_hemis_urls.append(hemi_url_bs)
# zipping together the hemisphere name and img url pairings
# see https://stackoverflow.com/q/14150797
hi_res_hemis = [{'title': hemi_name, 'img_url': hi_res_hemi} for (hemi_name, hi_res_hemi) in zip(hemis_name_list, hi_res_hemis_urls)]

# Combined Outputs / Variables to Use
# NASA Mars News
latest_news_date
latest_news_headline
latest_news_teaser
latest_news_url
# JPL Latest Image
jpl_url
# Twitter Mars Weather
tweet_weather_date
tweet_weather_report
# Mars Facts
fact_table
# Mars Hemispheres
hi_res_hemis





# #     setup Flask
app = Flask(__name__)



# #     Flask routes
# @app.route("/")
# def home():
#    return index.html





if __name__ == '__main__':
    app.run(debug=True)
