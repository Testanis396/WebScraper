from bs4 import BeautifulSoup
import requests

url = "https://www.royalroad.com/fictions/search?page=1&advanced=true"
pageNumber = 1
lastNumber = 0
while True:
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    # Process
    tempList = doc.find_all("div", class_="row fiction-list-item")
    for item in tempList:
        print(item)
        fictionTitle = item.find("h2", class_ = "fiction-title")
        link = fictionTitle.find("a").attrs["href"]
        link = "https://www.royalroad.com{}".format(link)
        title = fictionTitle.find("a").text
        
        marginBottom10 = item.find("div", class_ = "margin-bottom-10")
        span = marginBottom10.find_all("a", class_ = "label")
        tags = [tag.text for tag in span]

        rowStats = item.find("div", _class = "row stats")
        

        print(link, title, tags)
        break
    break
    # Next button
    if (pageNumber == 1):
        pagUl = doc.find("ul", class_="pagination")
        lastBtn = pagUl.find("a", string = "Last »")
        lastNumber = lastBtn.get("data-page")
    elif (pageNumber == lastNumber): break
    pageNumber += 1
    url = "https://www.royalroad.com/fictions/search?page={}&advanced=true".format(pageNumber)


