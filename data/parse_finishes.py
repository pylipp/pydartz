import lxml.html
import json
import os.path
from urllib import request

contents = request.urlopen("https://www.uni-muenster.de/ZIV.GuidoWessendorf/checkout.html").read().decode("utf-8")

finishes = {}
table_end = -1
while True:
    table_start = contents.find("TABLE", table_end+1)
    if table_start == -1:
        break
    table_end = contents.find("TABLE", table_start+1)

    # http://stackoverflow.com/questions/20418807/python-parse-html-table-using-lxml
    table = lxml.html.fromstring(contents[table_start-2:table_end+7])
    data = table.xpath('//tr/td//text()')

    # skip table header
    i = 25

    # iterate over all table entries. First one can be converted to int (the
    # score). From there, all non-whitespace entries are collected. Integers might
    # appear, indicating a single field. They must not be interpreted as score,
    # hence the j counter is introduced.
    while i < len(data):
        score = int(data[i])
        i += 1
        valid = True
        finish = []
        j = 0
        while valid and i < len(data):
            try:
                if j < 12:
                    raise ValueError
                int(data[i])
                valid = False
            except (ValueError):
                if len(data[i].strip()):
                    finish.append(data[i])
                i += 1
                j += 1
        finishes[score] = finish

# clean up
finishes.pop(40)
for score, finish in finishes.items():
    finishes[score] = []
    while len(finish):
        finish_list = finish[:2]
        if len(finish) > 2 and finish[2] != '-':
            finish_list.append(finish[2])
        finish = finish[3:]
        finishes[score].append(finish_list)

dirname = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(dirname, "finishes.json"), "w") as file:
    json.dump(eval(finishes.__repr__())), file)
