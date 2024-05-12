from novelsDB import novelsDB

db = novelsDB()

testDict = {
    "Title": "Descendants of the Stars",
    "Link": "https://www.royalroad.com/fiction/63999/descendants-of-the-stars",
    "Tags": [
        "Urban Fantasy",
        "Progression",
        "Multiple Lead Characters",
        "Contemporary",
        "Strong Lead",
        "Adventure",
        "Fantasy",
        "Romance",
        "Supernatural",
        "Female Lead",
        "Mythos",
        "Attractive Lead"
    ],
    "Stats": {
        "Followers": "3",
        "Rating": "0",
        "Pages": "5",
        "Views": "51",
        "Chapters": "1",
        "Last Updated": "2023-01-31T01:30:16.0000000+00:00"
    }
}
print(db.create(testDict))
print(db.read({}))
print(db.delete({"Title": "Descendants of the Stars",}))
print(db.read({}))



