from bs4 import BeautifulSoup
import requests

url = "https://www.royalroad.com/fictions/search?page=1&advanced=true"


result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
##print(doc.prettify())
##<a alt="" class="col-md-1 hidden-xs hidden-sm fiction-detail" data-fid="75345">
print(doc.find_all("div", class_="row fiction-list-item"))