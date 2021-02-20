# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from bs4 import BeautifulSoup as bs
import requests


# %%
url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

html = requests.get(url)

soup = bs(html.text, 'html.parser')


# %%
# NASA Mars News
# Find title

results_title = soup.find("div", class_="content_title")
news_title = results_title.a.text.strip()

# Find p text
results_p = soup.find("div", class_="content_title")
news_p = results_p.text.strip()
breakvar=""


# %%



