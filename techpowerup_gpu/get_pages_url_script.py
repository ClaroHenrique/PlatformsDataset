import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime
import time
import json
import os

def get_html(url, delay=20):
  time.sleep(delay)
  txt = requests.get(url).text
  return txt

def search_results_menu(manufacter, year):
  url = 'https://www.techpowerup.com/gpu-specs/?'
  url += 'mfgr=' + manufacter + '&'
  url += 'released=' + year
  print('starting search', url)

  html = get_html(url)
  soup = BS(html, 'html.parser')
  product_rows = soup.find('table', {'class': 'processors'}).find_all('tr')

  result_urls = []
  for product_row in product_rows:
    row_first_link = product_row.find('a') #/content/www/us/en/ark/products/series/98456/intel-100-series-desktop-chipsets.html
    if row_first_link == None: continue
    href = row_first_link.get('href')
    product_page_url = 'https://www.techpowerup.com' + href
    result_urls.append(product_page_url)
  return result_urls


manufacters = ['NVIDIA', 'AMD', 'Intel']
start_y, end_y = (2010, 2022)
years = [str(i) for i in range(start_y, end_y + 1)]

c = 0
results = {}
for m in manufacters:
  for y in years:
    c += 1
    id = m + "_" + y
    print(c, ": results for", id)
    try:
      results[id] = search_results_menu(m, y)
    except:
      print("!!! error in ", id)


script_dir = os.path.dirname(__file__)
with open(script_dir + 'product_pages_urls.json', 'w') as f:
  f.write(json.dumps(results, ensure_ascii=False, indent=2))
