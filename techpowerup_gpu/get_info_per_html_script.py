import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime
import time
import json
import os

products_info = []
def search_product_page(html, url, access_date):
  soup = BS(html, 'html.parser')

  product_info = {}
  product_info['web_page_url'] = url
  product_info['web_page_access_date'] = access_date
  product_info['Product Name'] = soup.find('h1', {'class': 'gpudb-name'}).text.strip()
  
  # general specs
  features = {}
  for spec in soup.find_all('div', {'class': 'gpudb-specs-large__entry'}):
    title = spec.find('dt').text.strip()
    value = spec.find('dd').text.strip()
    features[title] = value
  product_info["General Specs"] = features

  # specifics specs 
  for section in soup.find_all('section', {'class': 'details'}):
    section_title = section.find('h2').text.strip()
    features = {}
    for list_item in section.find_all('dl'):
      label = list_item.find('dt').text.strip()
      value = list_item.find('dd').text.strip()
      features[label] = value
    product_info[section_title] = features
  products_info.append(product_info)


with open('product_html_data.json') as f:
  product_html_data = json.load(f)

for html_info in product_html_data.values():
  search_product_page(html_info["html"], html_info["url"], html_info["access_date"])

#print('Result:::')
#print(products_info)

script_dir = os.path.dirname(__file__)
with open(script_dir + "gpu_info.json", "w") as f:
  f.write(json.dumps(products_info, ensure_ascii=False, indent=2))
