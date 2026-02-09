import requests
import json 
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import urllib.parse

#url = "http://localhost:8080/search?q=ai+engineering&format=json" 


url = "http://localhost:8080/search" 

params = {'q': input("Write your query: "),
              'format': 'json'}


def url_encode(params):  

    # Encoding 
    encoded_params = urllib.parse.urlencode(params)
    # URL with parameter
    final_url = f'{url}?{encoded_params}'
    return final_url


# Sending GET request 

# Collecting first three result from SearXNG to provide the most relevant content
def collect_links(url: str):
  response = requests.get(url)
  data = response.json()
  results = data["results"][:3]
  urls = []
  for links in results:
    urls.append(links["url"]) # type: ignore
  return urls

# Html content configuration 
def tag_visible(element):

  if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
  if isinstance(element, Comment):
        return False
  return True

# Scraping the content 
def parse_html(body):
   soup = BeautifulSoup(body, 'html.parser')
   texts = soup.findAll(text=True)
   visible_texts = filter(tag_visible, texts)  
   return u" ".join(t.strip() for t in visible_texts)



def fetch_html(url):
    all_urls = collect_links(url_encode(params))
    for url in all_urls:
        try:
            '''
            req = urllib.request.Request(
                url,
                headers= {
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "text/html",
                  }
                )
            '''
            response = requests.get(
                url, 
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )
            #html_context = urllib.request.urlopen(req, timeout=10).read() 
            # Raise an error if the site blocked us
            response.raise_for_status()
            print(parse_html(response.text))
            return parse_html(response.text) 
        except Exception as e:
            print(f"[SKIP] {url} | {e}")
            return " "
    
'''        
with open("data-flow/content.txt", "w", encoding="utf-8") as f:
        f.write(parsed)
'''

if __name__ == "__main__":
   fetch_html(url)
    
