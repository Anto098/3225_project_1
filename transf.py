import sys
from bs4 import BeautifulSoup
#print(type(th.string)) #NoneType
#print(type(th.text)) #str
#print(type(th.contents[0])) #bs4.element.NavigableString
#print(type(th.contents)) #list
# POUR PRINT DANS LA CONSOLE : python3 ./transf.py < css3-modsel-1.html
# POUR OUTPUT DANS UN FICHIER : python transf.py < css3-modsel-1.html > css3-modsel-1-MODIFIED.html
html_file = sys.stdin.read()
soup = BeautifulSoup(html_file, features="html.parser")

for link in soup.find_all("link"):
    if link.get("rel")[0] == "stylesheet":
        link["href"] = "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"  #Replacing old css stylesheet with bootstrap

left_arrow = 0 #false
for th in soup.find_all("th", {"class" : "c"}):
    all_as = th.find_all('a')
    if(len(all_as)>1):
        left_arrow = 1 # true
        all_hrefs = []
        for a in all_as: #get all hrefs
            all_hrefs.append(a["href"])
    th.string = "" #remove everything in the th
    if left_arrow == 1: #if there's a link on the left arrow, put a button in its stead
        left_a = soup.new_tag("a")
        left_a.string="PREVIOUS"
        left_a["class"] = ["btn btn-primary"]
        left_a["role"]=["button"]
        left_a["href"]=all_hrefs[0]
        th.append(left_a)
    right_a = soup.new_tag("a")
    right_a.string="NEXT"
    right_a["class"] = ["btn btn-primary"]
    right_a["role"]=["button"]
    right_a["href"]=all_hrefs[left_arrow]  #lol at that index
    th.append(right_a)
        



for td in soup.find_all("td", {"class" : "c"}):
    td.string = "Test #"+td.string

for table in soup.find_all("table"): # change table style
    table["class"].append("table table-dark")

for div in soup.find_all("div"): #make 3 blocs out of : html, css, html+css
    if div["class"][0] == "testSource":
        div["class"].append("d-flex mx-2  row")
        for child in div.children:
            if child != "\n":
                child["class"].append("col border border-dark mx-3")



sys.stdout.write(soup.prettify())       # Outputs the modified html file
