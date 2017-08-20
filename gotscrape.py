import requests
import pandas
from bs4 import BeautifulSoup

r = requests.get("https://en.wikipedia.org/wiki/List_of_A_Song_of_Ice_and_Fire_characters")
c = r.content

soup = BeautifulSoup(c, "html.parser")

all = soup.find_all("table",{"class":"navbox collapsible expanded"})
print(all)