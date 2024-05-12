# WebScraper

* Scraping RoyalRoad with python's BeautifulSoup framework. Processed into .json format. End goal is to manipulate and display in browser. Could use pandas to visualize the data, filter, and query. Possibility to implement accounts to allow users to create custom lists.
* mainScraper.py scrapes and creates royalRoadNovels.json dataset. Appends and saves each new novel into .json file in case of error or interruption. List of dictionary documents.  
* novelsDB.py Uses PyMongo to initialize the MongoClient. Implements 4 (CRUD) methods to manipulate the novels collection in the rrn database. Tests can be run in novelsDBTests.py. 
* To Do: Implement a framework like flask or dash to create a front facing website and visualize the data. 
  
