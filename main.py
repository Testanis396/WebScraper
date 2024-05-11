from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.royalroad.com/fictions/search?page=1&advanced=true"
pageNumber = 1
lastNumber = 0
novels = []

while True:
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    # Process
    tempList = doc.find_all("div", class_="row fiction-list-item")
    for item in tempList:
        fictionTitle = item.find("h2", class_ = "fiction-title")
        link = fictionTitle.find("a").attrs["href"]
        link = "https://www.royalroad.com{}".format(link)
        title = fictionTitle.find("a").text
        
        marginBottom10 = item.find("div", class_ = "margin-bottom-10")
        labels = marginBottom10.find_all("a", class_ = "label")
        tags = [tag.text for tag in labels]

        rowStats = item.find("div", class_ = "row stats")
        divs = rowStats.find_all("div", class_ = "col-sm-6")
        stats = []
        for div in divs:
            text = div.text.strip()  
            if (text == ""):
                titleStat = div.attrs.get("aria-label")  # Extract title if present
                stats.append(titleStat)
            else:
                stats.append(text)
        novels.append([title, link, tags, stats])
    break
    # Next button
    if (pageNumber == 1):
        pagUl = doc.find("ul", class_="pagination")
        lastBtn = pagUl.find("a", string = "Last »")
        lastNumber = lastBtn.get("data-page")
    elif (pageNumber == lastNumber): break
    pageNumber += 1
    url = "https://www.royalroad.com/fictions/search?page={}&advanced=true".format(pageNumber)

df = pd.DataFrame(novels, columns = ["Title", "Link", "Tags", "Stats"])
df.to_csv("royalRoadNovels.csv")
