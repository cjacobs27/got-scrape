import requests
import pandas
import re
from bs4 import BeautifulSoup

r = requests.get("https://en.wikipedia.org/wiki/List_of_A_Song_of_Ice_and_Fire_characters")
c = r.content

soup = BeautifulSoup(c, "html.parser")
all = soup.find_all("span", {"class": "mw-headline"})
regex = ('(House|References|Secondary sources|Primary sources|Bibliography|External links|Other characters|Royal court and officials|Night\\\'s Watch and wildlings|The Sand Snakes)')
p = re.compile(regex)
namelist=[]
linklist = []
checklist = []
for item in all:
    name = item.text
    if p.match(name) is None:
        #gotta check for Ned specifically as his char page is Ned_Stark but name listed everywhere as Eddard
        if name == "Eddard Stark":
            namelist.append("Ned Stark")
            urlend = "Ned_Stark"
            url = str("https://en.wikipedia.org/wiki/" + urlend)
            linklist.append(url)
        else:
            namelist.append(name)
            urlend = name.replace(" ", "_")
            url = str("https://en.wikipedia.org/wiki/" + urlend)
            linklist.append(url)
    else:
        pass

#character page exists checker - scrapes for redirect link text (this is the name of the character if redirected to
# the 'list of characters' page
a = 0
for item in linklist:
    request = requests.get(item)
    z = request.content
    soup2 = BeautifulSoup(z, "html.parser")
    try:
        redirected = soup2.find("a", {"class:", "mw-redirect"}).text
        if redirected == namelist[a]:
            # print("No")
            checklist.append("No")
        else:
            # print("Yes")
            checklist.append("Yes")
    except:
        # print("Fail")
        checklist.append("No")
    print(str(a) + " of 124 entries checked")
    a = a + 1
'''
Dataframe issue?
Look at this awesome page:

http://queirozf.com/entries/pandas-dataframe-by-example
'''

df = pandas.DataFrame(
    {'Name': namelist,
     'URL': linklist,
     'Page': checklist})
#this line sorts the rows with dedicated pages to the top of the list for testing
sorted_df = df.sort_values('Page',ascending=False)
sorted_df.to_csv("data.csv")



