import requests
from bs4 import BeautifulSoup as BS
import time
import json

def get_html(url):
  time.sleep(2)
  return requests.get(url).text

def search_initial_menu():
  initial_menu_url = 'https://ark.intel.com/content/www/us/en/ark.html#@Processors'
  print('%'*21, initial_menu_url, '%'*12)
  html = get_html(initial_menu_url)
  soup = BS(html, 'html.parser')
  n = len(soup.find_all('a', {'class': 'ark-accessible-color'}))

  for proc_family in soup.find_all('a', {'class': 'ark-accessible-color'}):
    href = proc_family.get('href') #/content/www/us/en/ark/products/series/98456/intel-100-series-desktop-chipsets.html
    if href == None: continue  
    suffix = href.split('/content/www/us/en/')[1]
    sub_menu_url = 'https://ark.intel.com/content/www/us/en/' + str(suffix)
    search_family_page(sub_menu_url)

def search_family_page(family_menu_url):
  print('$'*12, family_menu_url, '$'*12)

  html = get_html(family_menu_url)
  soup = BS(html, 'html.parser')

  for proc_info in soup.find('tbody').find_all('a'):
    href = proc_info.get('href') #/content/www/us/en/ark/products/series/98456/intel-100-series-desktop-chipsets.html
    suffix = href.split('/content/www/us/en/')[1]
    proc_page_url = 'https://ark.intel.com/content/www/us/en/' + str(suffix)
    search_processor_page(proc_page_url)


#search_family_page('https://ark.intel.com/content/www/us/en/ark/products/series/217839/12th-generation-intel-core-i9-processors.html')

processors_info = []

def search_processor_page(processor_page_url):
  print('_'*23, processor_page_url, '_'*23)

  html = get_html(processor_page_url)
  soup = BS(html, 'html.parser')
  proc_info = {}

  for section in soup.find_all('div', {'class': 'blade-inside'}):
    for list_item in section.find_all('li'):
      label = list_item.find('span', {'class': 'label'}).text.strip()
      value = list_item.find('span', {'class': 'value'}).text.strip()
      proc_info[label] = value
      print(label)
      print(value)
  
  processors_info.append(proc_info)

print('-'*50)
#search_processor_page('https://ark.intel.com/content/www/us/en/ark/products/228439/intel-core-i912950hx-processor-30m-cache-up-to-5-00-ghz.html')
search_initial_menu()

with open("intel_processors_data.txt", "w") as f:
  f.write(json.dumps(processors_info, ensure_ascii=False, indent=2))
