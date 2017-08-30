import requests
import pandas
import re
from bs4 import BeautifulSoup

r = requests.get("https://en.wikipedia.org/wiki/List_of_A_Song_of_Ice_and_Fire_characters")
c = r.content

soup = BeautifulSoup(c, "html.parser")

all = soup.find_all("table", {"class": "navbox collapsible expanded"})[0]
rawnames = all.find("td").text.replace("\n\n","").replace("\n","").replace("  ","")
cleannames = re.split(r"\[\w+\]", rawnames)
namelist=[]
linklist = []
for item in cleannames:
    #I copied this regex from stackoverflow - it's putting a space between instances of lowercase
    #followed by uppercase - correctly underscoring the names
    i = re.sub(r'([a-z])([A-Z])', r'\1_\2', item)
    if i != str(""):
        if "_" not in i:
            i = i + "_Stark"
        namelist.append(i)
        linklist.append("https://en.wikipedia.org/wiki/"+ i)
#this checks whether the links work, but it's pointless as wikipedia resolves all pages
#even if they don't exist... so this is kind of pointless in general
#as the whole idea was to get character info from individual character pages
for item in linklist:
    request = requests.get(item)
    if request.status_code == 200:
        pass
    else:
        item = None
print(namelist)
print(linklist)



