import requests
from bs4 import BeautifulSoup
import urllib.parse
from pathlib import Path

url = 'https://vedavms.in/docs_baraha.html'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')

urls = []
for link in soup.find_all('a'):
    download_url=link.get('href')
    #print(download_url[0])
    if download_url[0] ==".":
        download_url=download_url.replace(".","https://www.vedavms.in",1)
        parsed_url = urllib.parse.urlparse(download_url)
        path = parsed_url.path
        #filename = Path(path).name
        filename=urllib.parse.unquote(Path(path).name)

        download_string="curl -o \"" +filename+ "\" \""+download_url+"\""
        print(download_string)
    #print(download_url)

