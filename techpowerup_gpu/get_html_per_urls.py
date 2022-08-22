import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime
import time
import json
import os

print('#' * 32)

def get_html(url, delay=120):
  time.sleep(delay)
  txt = requests.get(url).text
  return txt

results = {}
try:
  with open('product_html_data.json') as f:
    results = json.load(f)
except Exception as e: print('merge error', e)

try:
  with open('resultoso.json') as f:
    results2 = json.load(f)
  results = {**results, **results2}
except Exception as e: print('merge error', e)


pages_urls_data = {}
with open('product_pages_urls.json') as f:
  pages_urls_data = json.load(f)

for (i, (description, urls)) in enumerate(pages_urls_data.items()):
  print('processing', description)
  print('progress', i, '/', len(pages_urls_data))
  
  for url in urls:
    if url in results:
      print("skip", url)
      continue
    else: print("get", url)
    
    try:
      page_html_data = {}
      page_html_data['html'] = get_html(url)
      page_html_data['url'] = url
      page_html_data['access_date'] = datetime.now().strftime('%Y/%m/%d/, %H:%M:%S')
      results[url] = page_html_data
    except Exception as e: print('error', e)    
    
    script_dir = os.path.dirname(__file__)
    with open(script_dir + 'product_html_data.json', 'w') as f:
      f.write(json.dumps(results, ensure_ascii=False, indent=2))
