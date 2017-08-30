import requests
import pandas
import re
from bs4 import BeautifulSoup

r = requests.get("https://en.wikipedia.org/wiki/List_of_A_Song_of_Ice_and_Fire_characters")
c = r.content

soup = BeautifulSoup(c, "html.parser")
all = soup.find_all("span", {"class": "mw-headline"})
regex = ('(House|References|Secondary sources|Primary sources|Bibliography|External links|Royal court and officials|Night\\\'s Watch and wildlings|The Sand Snakes)')
p = re.compile(regex)
for item in all:
    name = item.text
    if p.match(name) is None:
        print(name)
    else:
        pass

    # name.match("House" | "References" | "Secondary sources" | "Primary sources" | "Bibliography" | "External links")

# all = soup.find_all("table", {"class": "navbox collapsible expanded"})[0]
# rawnames = all.find("td").text.replace("\n\n","").replace("\n","").replace("  ","")
# cleannames = re.split(r"\[\w+\]", rawnames)
# namelist=[]
# linklist = []
# for item in cleannames:
#     #I copied this regex from stackoverflow - it's putting a space between instances of lowercase
#     #followed by uppercase - correctly underscoring the names
#     i = re.sub(r'([a-z])([A-Z])', r'\1_\2', item)
#     if i != str(""):
#         if "_" not in i:
#             i = i + "_Stark"
#         namelist.append(i)
#         linklist.append("https://en.wikipedia.org/wiki/"+ i)

#this is a WIP, trying to filter out only the URLs which lead to actual character pages
# a = 0
# for b in linklist[a]:
#     # print(linklist[a])
#     request = requests.get(linklist[a])
#     # print(request.headers)
#     print(request.status_code)
#     print(request.url)
#     if request.status_code == 404:
#         print("None")
#     elif request.status_code == 304:
#         print("None")
#     else:
#         print("Ok")
#     a=a+1

# print(namelist)
# print(linklist)



