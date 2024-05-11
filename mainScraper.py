from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

url = "https://www.royalroad.com/fictions/search?page=1&advanced=true"
pageNumber = 1
lastNumber = 0

with open("royalRoadNovels.json", "w") as jsonfile:
        jsonfile.write("[")
        jsonfile.write('\n')

while True:
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    # Process
    tempList = doc.find_all("div", class_="row fiction-list-item")
    limit = len(tempList)
    
    for j in range(limit):
        item = tempList[j]
        fictionTitle = item.find("h2", class_ = "fiction-title")
        link = fictionTitle.find("a").attrs["href"]
        link = "https://www.royalroad.com{}".format(link)
        title = fictionTitle.find("a").text
        
        marginBottom10 = item.find("div", class_ = "margin-bottom-10")
        labels = marginBottom10.find_all("a", class_ = "label")
        tags = [tag.text for tag in labels]

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
            ## format stats array to 
            #  {
            #  "Followers": "22,937",
            #  "Rating": "4.84 out of 5",
            #  "Pages": "2,698",
            #  "Views": "10,848,659",
            #  "Chapters": "141",
            #  "Last Updated": "Friday, May 10, 2024 1:31:18 AM"
            ##

            # Remove non-numeric characters from the text
            numericText = ''.join(filter(str.isdigit, text))
            if(i == 0):
                stats["Followers"] = numericText
            elif(i == 1):
                ratingStat = div.attrs.get("aria-label")
                stats["Rating"] = ratingStat.split(": ")[1].split(" out of ")[0]
            elif(i == 2):
                stats["Pages"] = numericText
            elif(i == 3):
                stats["Views"] = numericText.replace(",", "")
            elif(i == 4):
                stats["Chapters"] = numericText
            elif(i == 5):
                time = div.find("time")  # Extract title if present
                last_updated = time.attrs.get("datetime")
                stats["Last Updated"] = last_updated  
        
        novel = {
            "Title": title, 
            "Link": link, 
            "Tags": tags, 
            "Stats": stats
            }
        
        if (pageNumber == lastNumber and j == limit-1):
            # Append last novel to .json file
            with open("royalRoadNovels.json", "a") as jsonfile:
                json.dump(novel, jsonfile, indent=4)
                jsonfile.write('\n')
                break
        
        # Append to .json file
        with open("royalRoadNovels.json", "a") as jsonfile:
            json.dump(novel, jsonfile, indent=4)
            jsonfile.write(',')
            jsonfile.write('\n')

    # Next button
    if (pageNumber == 1):
        pagUl = doc.find("ul", class_="pagination")
        lastBtn = pagUl.find("a", string = "Last »")
        lastNumber = int(lastBtn.get("data-page"))
    
    if (pageNumber == lastNumber): 
        print("processed page {} out of {}".format(pageNumber, lastNumber))
        
        # Append to .json file
        with open("royalRoadNovels.json", "a") as jsonfile:
            jsonfile.write(']')
        break
    
    print("processed page {} out of {}".format(pageNumber, lastNumber))
    pageNumber += 1
    url = "https://www.royalroad.com/fictions/search?page={}&advanced=true".format(pageNumber)


