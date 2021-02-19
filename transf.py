import sys
from random import shuffle

from bs4 import BeautifulSoup

# print(type(th.string)) #NoneType
# print(type(th.text)) #str
# print(type(th.contents[0])) #bs4.element.NavigableString
# print(type(th.contents)) #list

# POUR PRINT DANS LA CONSOLE : python3 ./transf.py < css3-modsel-1.html
# POUR OUTPUT DANS UN FICHIER : python3 transf.py css3-modsel-1.html > css3-modsel-1-MODIFIED.html
# html_file = sys.stdin.read()
arg = sys.argv[1]
with open(sys.argv[1], 'r+') as f:
    html_file = f.read()
soup = BeautifulSoup(html_file, features="html.parser")

for style in soup.find_all("style"):
    style.string = ""

for link in soup.find_all("link"):
    if link.get("rel")[0] == "stylesheet":
        # REPLACE OLD CSS STYLESHEET WITH BOOTSTRAP
        link["href"] = "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"

left_arrow = False
right_arrow = False

for th in soup.find_all("th", {"class": "c"}):
    all_a = th.find_all('a')
    all_href = []

    # GET ALL HREFS
    for a in all_a:
        if "<==" in a.text:
            left_arrow = True
        elif "==>" in a.text:
            right_arrow = True
        all_href.append(a["href"])

    # REMOVE EVERYTHING IN TH
    th.string = ""

    # IF ARROW IS A LINK, REPLACE IT BY A BUTTON
    if left_arrow:
        left_a = soup.new_tag("a")
        left_a.string = "PREVIOUS"
        left_a["class"] = ["btn btn-primary"]
        left_a["role"] = ["button"]
        left_a["href"] = all_href[0]
        th.append(left_a)
    if right_arrow:
        right_a = soup.new_tag("a")
        right_a.string = "NEXT"
        right_a["class"] = ["btn btn-primary"]
        right_a["role"] = ["button"]
        right_a["href"] = all_href[left_arrow]
        th.append(right_a)

for td in soup.find_all("td", {"class": "c"}):
    td.string = "Test #"+td.string

# CHANGE TABLE STYLE
for table in soup.find_all("table"):
    if table.has_attr("class") and table["class"][0] == "testDescription":
        table["class"].append("table table-dark")

# MAKE THREE BLOCKS OUT OF HTML, CSS & SOLUTION
for div in soup.find_all("div"):
    if div.has_attr("class"):
        if div["class"][0] == "testSource":
            div["class"].append("d-flex mx-2 row")
            for child in div.children:
                if child != "\n":
                    child["class"].append("col rounded border border-primary mx-2 px-3 py-3")
            first = soup.new_tag("div")
            first["class"] = ["col"]
            div.insert(0, first)
            last = soup.new_tag("div")
            last["class"] = ["col"]
            div.append(last)

# ADD SOLUTION BUTTON

for table in soup.find_all("table"):
    button = soup.new_tag("a")
    button.string = "SOLUTION"
    button["class"] = "btn btn-primary"
    button["role"] = "button"
    button["href"] = "#"

    td1 = soup.new_tag("td")
    td1.append(button)
    td2 = soup.new_tag("td")
    td3 = soup.new_tag("td")

    new_row = soup.new_tag("tr")
    new_row.append(td1)
    new_row.append(td2)
    new_row.append(td3)

    table.append(new_row)


def scramble(children):
    for kid in children:
        if kid.string is not None:
            words = kid.string.split()
            shuffle(words)
            kid.string = " ".join(words)
        else:
            scramble(kid)


test_text = []

# SCRAMBLE TEXT
for div in soup.find_all("div"):
    if div["class"][0] == "testText":
        scramble(div.children)
        for child in div.children:
            test_text.append(str(child))
        resultat = soup.new_tag("h2")
        resultat.string = "RESULT"
        div.insert(0, resultat)

pre = soup.find_all("pre", {"class": "rules"})
pre[1].string = "".join(test_text)
css = soup.new_tag("h2")
css.string = "CSS"
pre[0].insert(0, css)
html = soup.new_tag("h2")
html.string = "HTML"
pre[1].insert(0, html)


# OUTPUTS MODIFIED HTML FILE
sys.stdout.write(soup.prettify())
