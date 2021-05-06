import sys
from random import shuffle
from bs4 import BeautifulSoup

input_full_path = sys.argv[1]
output_full_path = sys.argv[2]

file_name = input_full_path.split("/")[-1]
output_prefix_path = "/".join(output_full_path.split("/")[0:-1])

with open(sys.argv[1], 'r+') as f:
    html_file = f.read()
soup = BeautifulSoup(html_file, features="html.parser")

for link in soup.find_all("link"):
    if link.get("rel")[0] == "stylesheet":
        # REPLACE OLD CSS STYLESHEET WITH BOOTSTRAP
        link["href"] = "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"

left_arrow = False
right_arrow = False

# PUT PREV / NEXT BUTTONS
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
#put titles in div and 2 pre
    if div.has_attr("class") and div["class"][0] == "testText":
        resultat = soup.new_tag("h2")
        resultat.string = "RESULT"
        div.insert(0,resultat)

pre = soup.find_all("pre", {"class": "rules"})

css = soup.new_tag("h2")
css.string = "CSS"
pre[0].insert(0, css)

html = soup.new_tag("h2")
html.string = "HTML"
pre[1].insert(0, html)

def add_solution_button(fn):
    # ADD SOLUTION BUTTON
    for table in soup.find_all("table"):
        button = soup.new_tag("a")
        button.string = "SOLUTION"
        button["class"] = "btn btn-primary"
        button["role"] = "button"
        button["href"] = fn

        td1 = soup.new_tag("td")
        td1.append(button)
        td2 = soup.new_tag("td")
        td3 = soup.new_tag("td")

        new_row = soup.new_tag("tr")
        new_row.append(td1)
        new_row.append(td2)
        new_row.append(td3)

        table.append(new_row)

def scramble_text():
    # SCRAMBLE TEXT
    test_text = []
    for div in soup.find_all("div"):
        if div.has_attr("class") and div["class"][0] == "testText":
            scramble(div.children)
            # test_text = str(div)[86:-6]
            for child in div.children:
                test_text.append(str(child))
    pre[1].string = "".join(test_text[1:]) # [1:] to remove <h2> element
    # pre[1].string = test_text
    pre[1].insert(0,html)

def remove_css():
    for style in soup.find_all("style"):
        style.string=""

def scramble(children):
    for kid in children:
        if kid.string is not None:
            words = kid.string.split()
            shuffle(words)
            kid.string = " ".join(words)
        else:
            scramble(kid)

def main():
################# SOLUTION PAGE ##################
    add_solution_button(file_name)

    splitted_fn = file_name.split(".")
    splitted_fn[0] = splitted_fn[0] + "-Solution"
    solution_file_name = ".".join(splitted_fn)

    f = open("/".join([output_prefix_path,solution_file_name]), "w")
    f.write(soup.prettify())
################# BASE PAGE ######################
    a = soup.find("a", {"href" : file_name})
    a["href"] = solution_file_name
    
    scramble_text()
    remove_css()

    f2 = open(output_full_path,"w")
    f2.write(soup.prettify())

main()