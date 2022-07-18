import requests
from bs4 import BeautifulSoup as BS
import time
import json
import os

def get_html(url, delay=1):
  time.sleep(1)
  return requests.get(url).text

def search_initial_menu():
  print("starting search")
  html = get_html('https://ark.intel.com/content/www/us/en/ark.html#@Processors')
  soup = BS(html, 'html.parser')
  page_content = soup.find('div', {'class': 'product-browse-div'}).find_all('a', {'class': 'ark-accessible-color'})
  
  for i, proc_family in enumerate(page_content):
    print("progress:", i, '/', len(page_content))
    #if i == 3: break
    href = proc_family.get('href') #/content/www/us/en/ark/products/series/98456/intel-100-series-desktop-chipsets.html
    if href == None: continue  
    suffix = href.split('/content/www/us/en/')[1]
    family_page_url = 'https://ark.intel.com/content/www/us/en/' + str(suffix)
    search_family_page(family_page_url)

def search_family_page(family_menu_url):
  print('searching family in', family_menu_url)

  html = get_html(family_menu_url)
  soup = BS(html, 'html.parser')

  content = soup.find('tbody')
  if content == None: return
  content = soup.find('tbody').find_all('a')
  if content == None: return
  #some family pages are empty

  for proc_info in soup.find('tbody').find_all('a'):
    href = proc_info.get('href') #/content/www/us/en/ark/products/series/98456/intel-100-series-desktop-chipsets.html
    suffix = href.split('/content/www/us/en/')[1]
    proc_page_url = 'https://ark.intel.com/content/www/us/en/' + str(suffix)
    search_processor_page(proc_page_url)

processors_info = []
def search_processor_page(processor_page_url):
  print('processing page', processor_page_url)
  try:
    html = get_html(processor_page_url)
    soup = BS(html, 'html.parser')

    proc_info = {}
    proc_info["web_page_url"] = processor_page_url

    for section in soup.find_all('div', {'class': 'blade-inside'}):
      for list_item in section.find_all('li'):
        label = list_item.find('span', {'class': 'label'}).text.strip()
        value = list_item.find('span', {'class': 'value'}).text.strip()
        proc_info[label] = value
    processors_info.append(proc_info)
  except:
    print("error in", processor_page_url)

search_initial_menu()

script_dir = os.path.dirname(__file__)
with open(script_dir + "intel_processors_data.txt", "w") as f:
  f.write(json.dumps(processors_info, ensure_ascii=False, indent=2))
