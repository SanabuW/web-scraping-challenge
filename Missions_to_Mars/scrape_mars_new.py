# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Import libraries
from bs4 import BeautifulSoup as bs
import requests
import time
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo



# %%
# set up Flask
app = Flask(__name__)
# setup MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_db"
mongo = PyMongo(app)


# %%
# Begin function here
def scrape ():


    # %% [markdown]
    # # NASA Mars News

    # %%
    # Build Beautiful Soup object
    url_home = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    html_home = requests.get(url_home)
    soup_home = bs(html_home.text, 'html.parser')


    # %%
    # Find title
    results_title = soup_home.find("div", class_="content_title")
    news_title = results_title.a.text.strip()

    # Find p text
    results_p = soup_home.find("div", class_="content_title")
    news_p = results_p.text.strip()

    # %% [markdown]
    # # JPL Mars Space Images - Featured Image

    # %%
    # Import libraries
    from splinter import Browser
    from webdriver_manager.chrome import ChromeDriverManager

    # Set up driver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Point browser to URL and build Beautiful Soup object
    images_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(images_url)
    html_images_url = browser.html
    soup_image = bs (html_images_url, "html.parser")


    # %%
    # Find image URL in button
    results_image = soup_image.find("a", class_="fancybox-thumbs")["href"]

    # Build full URL
    image_base_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    image_full_url = image_base_url + results_image

    # close browser
    browser.quit()

    # %% [markdown]
    # # Mars Facts

    # %%
    # Get facts table
    import pandas as pd
    table_url = "https://space-facts.com/mars/"
    mars_table = pd.read_html(table_url)[0]


    # %%
    mars_table


    # %%
    # convert to html table and save to file, if necessary later
    mars_table.to_html("mars_table.html")

    # show HTML
    table_html = mars_table.to_html()

    # %% [markdown]
    # # Mars Hemispheres

    # %%
    # Build Beautiful Soup object
    url_hemi = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    html_hemi = requests.get(url_hemi)
    soup_hemi = bs(html_hemi.text, 'html.parser')


    # %%
    # Get a count of how many divs there are with class "item"
    results_hemi = soup_hemi.find_all("div", class_="item")
    count = len(results_hemi) + 1

    # Set up driver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Point browser to URL and build Beautiful Soup object
    browser.visit(url_hemi)
    iterVar = 0
    hemi_list = []

    # for each one, find the first a tag with class "itemLink product-item" and click on it
    for h in results_hemi:
        # use webdriver to click on link depending on iteration count
        browser.find_by_tag('h3')[iterVar].click()

        # Build beautiful soup object from new page
        html_hemi = browser.html
        soup_hemi_ind = bs(html_hemi, 'html.parser')

        # get title from first h2 tag
        title = soup_hemi_ind.find("h2").text
        title_cleaned = " ".join(title.split(" ")[0:-1])

        # find first div of class "downloads", then find first a within the reults and pull the href string
        img_url_hemi = soup_hemi_ind.find("div", class_="downloads").find("a")["href"]
        # create dictionary for current single hemisphere
        new_hemi = {
            "title": title_cleaned,
            "image_url": img_url_hemi,
        }
        # append dictionary to the list of hemispheres
        hemi_list.append(new_hemi)
        iterVar += 1
        # back out of the page
        browser.back()
        # continue to new iteration

    # close browser after all iterations are completed
    browser.quit()


    # %%
    scrape_output = {
        "news_title": news_title,
        "news_p": news_p,
        "image_full_url": image_full_url,
        "table_html": table_html,
        "hemi_list": hemi_list
    }
    return scrape_output

# %%
# End function


# %%
from flask import Flask
app = Flask(__name__)


@app.route("/")
def index():
    scrape_result = mongo.db.scrape_result.find_one()
    return render_template("index.html", scrape_result=scrape_result)

@app.route("/scrape")
def scrape():
    # Move to collection
    collection = mongo.db.scrape_db.mars_coll
    # perform scrape and save result
    scrape_result = scrape()
    collection.update({}, scrape_result, upsert=True)
    # # Insert scrape dictionary into collection
    # collection.insert_one(scrape_result)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)