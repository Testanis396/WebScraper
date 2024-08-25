from bs4 import BeautifulSoup
import requests
import json
from pathlib import Path
import sys

url = "https://www.royalroad.com/fictions/search?page=1&advanced=true"
pageNumber = 1
lastNumber = 0
lastPage = False
fileName = "royalRoadNovels1.json"
filePath = Path(fileName)

if filePath.exists():
    print("{} already exists, change JSON file.".format(filePath))
    sys.exit()

with open(fileName, "w") as jsonfile:
        jsonfile.write("[\n")

while (not lastPage):
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    # Process
    tempList = doc.find_all("div", class_="row fiction-list-item")
    limit = len(tempList)
  
    for j in range(limit):
        item = tempList[j]
        fictionTitle = item.find("h2", class_ = "fiction-title")
        title = fictionTitle.find("a").text.strip()

        link = fictionTitle.find("a").attrs["href"]
        link = "https://www.royalroad.com{}".format(link)
        
        marginBottom10 = item.find("div", class_ = "margin-bottom-10")
        labels = marginBottom10.find_all("a", class_ = "label")
        tags = [tag.text.strip() for tag in labels]

        rowStats = item.find("div", class_ = "row stats")
        divs = rowStats.find_all("div", class_ = "col-sm-6")
        stats = {}

        for i in range(len(divs)):
            div = divs[i]
            text = div.text.strip()  
          
            ## [
            # '22,937 Followers', 
            # 'Rating: 4.84 out of 5', 
            # '2,698 Pages', 
            # '10,848,659 Views', 
            # '141 Chapters', 
            # 'Friday, May 10, 2024 1:31:18 AM'
            # ]
            ##
            ## format stats array for efficient querying
            #  {
            # "Followers": 23337, int
            # "Rating": 4.84, float
            # "Pages": 2932, int
            # "Views": 19686174, int
            # "Chapters": 109, int
            # "Last Updated": "2023-07-06T17:47:41.0000000+00:00" string
            ##

            # Extract first element (number) from string and convert to int
            try:
                number = int(text.split()[0].replace(",",""))
            except:
                pass
            if(i == 0):
                stats["Followers"] = number
            elif(i == 1):
                ratingStat = div.attrs.get("aria-label")
                stats["Rating"] = float(ratingStat.split(": ")[1].split(" out of ")[0])
            elif(i == 2):
                stats["Pages"] = number
            elif(i == 3):
                stats["Views"] = number
            elif(i == 4):
                stats["Chapters"] = number
            elif(i == 5):
                time = div.find("time")  # Extract title if present
                dateString = time.attrs.get("datetime")
                stats["Last Updated"] = dateString
        
        novel = {
            "Title": title, 
            "Link": link, 
            "Tags": tags, 
            "Stats": stats
            }
        
        if (pageNumber == lastNumber and j == limit-1):
            # Append final novel to .json file
            with open(fileName, "a") as jsonfile:
                json.dump(novel, jsonfile, indent=4)
                jsonfile.write('\n')
                print("processed novel: {}".format(title))
                break
        
        # Append to .json file
        with open(fileName, "a") as jsonfile:
            json.dump(novel, jsonfile, indent=4)
            jsonfile.write(',\n')
            print("processed novel: {}".format(title))
    
    print("processed page {} out of {}".format(pageNumber, lastNumber))

    # Last button, check if last page
    try: 
        pagUl = doc.find("ul", class_="pagination")
        lastBtn = pagUl.find("a", string = "Last »")
        lastNumber = int(lastBtn.get("data-page"))
    except:
        if (pageNumber == lastNumber):
            lastPage = True
        else:
            pass
    
    pageNumber += 1
    url = "https://www.royalroad.com/fictions/search?page={}&advanced=true".format(pageNumber)

# Append to .json file
with open(fileName, "a") as jsonfile:
    jsonfile.write(']')
 
