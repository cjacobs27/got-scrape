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
infolist = []

def generatelinks():
    for item in all:
        name = item.text
        if p.match(name) is None:
            #gotta check for Ned specifically as his char page is Ned_Stark but name listed everywhere as Eddard
            if name == "Eddard Stark":
                namelist.append("Ned Stark")
                rightname = "Ned_Stark"
                url = str("https://en.wikipedia.org/wiki/" + rightname)
                linklist.append(url)
            else:
                namelist.append(name)
                urlend = name.replace(" ", "_")
                underscore = "_"
                if urlend.endswith(underscore):
                    #takes off the last underscore if present using indexing
                    urlend = urlend[0:-1]
                    # print(urlend)
                url = str("https://en.wikipedia.org/wiki/" + urlend)
                linklist.append(url)
        else:
            pass

    #character page exists checker - scrapes for redirect link text (this is the name of the character if redirected to
    # the 'list of characters' page
def linkscrape():
    a = 0
    for item in linklist:
        request = requests.get(item)
        z = request.content
        global soup2
        soup2 = BeautifulSoup(z, "html.parser")
        if "may refer to" in soup2.text:
            trychar(request, item)
        else:
            try:
                redirected = soup2.find("a", {"class:", "mw-redirect"}).text
                if redirected == namelist[a]:
                    checklist.append("No")
                    infolist.append("")
                else:
                    getinfobox(item)
            except:
                checklist.append("No")
                infolist.append("")
        print(str(a) + " of 124 entries checked")
        a = a + 1

def trychar(request, item):
    try:
        request2 = requests.get(str(item) + "_(character)")
        y = request2.content
        soup3 = BeautifulSoup(y, "html.parser")
        infobox2 = soup3.find(("table", {"class:", "infobox"}))
        infobox = infobox2.encode('utf-8').strip()
        if "Male" or "Female" in infobox:
            checklist.append("Yes")
            infolist.append(infobox)
        else:
            checklist.append("No")
            infolist.append("")
    except:
        checklist.append("No")
        infolist.append("")

def getinfobox(item):
    try:
        table = soup2.find_all(("table", {"class:", "infobox"}))
        infobox = table[0].encode('utf-8').strip()
        if str(infobox).startswith("b'<table class=\"infobox\""):
            checklist.append("Yes")
            infolist.append(infobox)
        else:
            refineinfobox(item,table)
    except:
        checklist.append("No")
        infolist.append("")

# def refineinfobox(item,table):
#     for i in range(4):
#         if "infobox" in str(table[i]):
#             infobox = table[i].encode('utf-8').strip()
#             checklist.append("Yes")
#             infolist.append(infobox)
#             print(table[i])
#             print("FINALLY")
#         break
        # break
    '''
    BOTH "FINALLY" AND "TRIGGERED" ARE TRIGGERED
    WTF
    this method needs to EITHER do the IF statement OR the "no" append etc
    once if statement is done & found nothing, THEN do the "no"
    '''
    # print("TRIGGERED")
    # checklist.append("No")
    # infolist.append("")

def refineinfobox(item,table):
    t = False
    for i in range(4):
        if "infobox" in str(table[i]):
            print(i)
            index = i
            t = True
            break
    while t is True:
        infobox = index
        print(infobox,"...does this match i?")
        break
    print("done")
        #     infobox = table[i].encode('utf-8').strip()
        #     checklist.append("Yes")
        #     infolist.append(infobox)
        #     print(table[i])
        #     print("FINALLY")
        # break


'''
Dataframe issue?
Look at this awesome page:

http://queirozf.com/entries/pandas-dataframe-by-example
'''

def datasave():
    #in a later version this dataframe will be a database which will update itself automatically every now and then
    #this will make the script run much more quickly as df won't need to be generated every time
    df = pandas.DataFrame(
        {'Name': namelist,
         'URL': linklist,
         'Page': checklist,
         'Infobox': infolist})
    '''
    uncomment these for testing purposes
    '''
    df.to_csv("TESTdata2.csv")
    df2 = pandas.read_csv('TESTdata2.csv')
    df_reorder = df2[['Name', 'URL', 'Page', 'Infobox']]  # rearrange columns here
    df_reorder.to_csv('TESTdata2.csv', index=False)
    print("Saved")

'''
genderscrape() will iterate through the code for the info box of each page by reading the csv
column which contains the infobox entries.
Need to figure out how to:
1) iterate through Infobox column
2) scrape each one for gender data
3) save Male, Female or None to another df column & overwrite csv(?) --- NO, CREATE A NEW LIST with the others above
OR ... don't do that? scrape every time? idk see how it plays out.
4) Pass data to generatechart()
'''
def genderscrape():
    #switch out df for the database later
    df = pandas.read_csv("TESTdata.csv")
    infoboxes = df['Infobox']
    a = 1
    for item in infoboxes:
        a = a+1
        try:
            if "Gender" in item:
                print(a, "Yes", item)
            else:
                print(a, "No", item)
        except:
            print(a, "Error", item)

# def generatechart():
'''
-generate a bokeh chart from a dataframe from one of the chart data scraping methods ie genderscrape()
-(there will be multiple options for what data will be in the chart)
-should be a preceding method which lets user select which data they want displayed
(but this will be a later feature - will just focus on 1 chart for now)
-eg male/female breakdown, number of episodes each character featured in etc.
'''
#generatelinks(), linkscrape, datasave and other -scrape() methods will only run occasionally to update the data
generatelinks()
linkscrape()
datasave()
# genderscrape()
#The generatechart() method will be run every time and will access the csv/database
#generatechart()
