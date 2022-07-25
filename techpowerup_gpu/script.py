import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime
import time
import json
import os


def get_html(url, delay=1):
  time.sleep(delay)
  txt = requests.get(url).text
  return txt

def search_initial_menu():
  print("starting search")
  html = get_html('https://www.techpowerup.com/gpu-specs/')
  soup = BS(html, 'html.parser')
  product_rows = soup.find('table', {'class': 'processors'}).find_all('tr')
  n = len(product_rows)
  
  for i, product_row in enumerate(product_rows):
    print("progress:", i, '/', n)
    #if i == 3: break
    row_first_link = product_row.find('a') #/content/www/us/en/ark/products/series/98456/intel-100-series-desktop-chipsets.html
    if row_first_link == None: continue
    href = row_first_link.get('href')

    product_page_url = 'https://www.techpowerup.com' + href
    search_product_page(product_page_url)


products_info = []
def search_product_page(product_page_url):
  print('Entering page', product_page_url)
  try:
    html = get_html(product_page_url)
    soup = BS(html, 'html.parser')

    product_info = {}
    product_info['web_page_url'] = product_page_url
    product_info['web_page_access_date'] = datetime.now().strftime('%Y/%m/%d/, %H:%M:%S')

    for section in soup.find_all('section', {'class': 'details'}):
      section_title = section.find('h2').text.strip()
      features = {}
      for list_item in section.find_all('dl'):
        label = list_item.find('dt').text.strip()
        value = list_item.find('dd').text.strip()
        features[label] = value
      product_info[section_title] = features
    products_info.append(product_info)
  except:
    print('!'*20)
    print('Error in page', product_page_url)

search_initial_menu()

print('Result:::')
print(products_info)

script_dir = os.path.dirname(__file__)
with open(script_dir + "gpu_from_techpowerup_data.txt", "w") as f:
  f.write(json.dumps(products_info, ensure_ascii=False, indent=2))
