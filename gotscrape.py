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
for item in cleannames:
    #I copied this regex from stackoverflow - it's putting a space between instances of lowercase
    #followed by uppercase - correctly spacing the names
    i = re.sub(r'([a-z])([A-Z])', r'\1 \2', item)
    if i != str(""):
        namelist.append(i)
#names are cleaned via cleannames and appended to the namelist, which is a list of the data we need
print(namelist)



