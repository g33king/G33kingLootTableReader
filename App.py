import json
import tkinter
from tkinter import filedialog
import csv

class item:
    def __init__(self, item, count, prob):
        self.item = item
        self.prob = str(round(prob * 100, 2)) + "%"
        self.count = count

    def __str__(self):
        return f'{self.prob}   {self.count}    {self.item}'

items = []

def calcProb(r, maxR, w, totalW):
    if maxR == None:
        return 1 - (1 - w / totalW) ** r
    else:
        num = 0
        for n in range(int(r), int(maxR) + 1, 1):
            num += 1 - ((1 - (w / totalW)) ** n)
        return num / (maxR - r + 1)

def readJson(loottable):
    for pool in loottable['pools']:

        rolls = 0
        maxRolls = None

        totalWeight = 0

        # if it has max and min rolls
        if type(pool['rolls']) == dict:
            rolls = pool['rolls']['min']
            maxRolls = pool['rolls']['max']
        else:
            rolls = pool['rolls']

        #count total weight
        for entry in pool['entries']:
            totalWeight += 1
            # if has special weight, else it just should add 1
            if "weight" in entry:
                totalWeight += entry['weight'] - 1

        # declaring each entry
        for entry in pool['entries']:

            # pass if empty
            if entry['type'] == "minecraft:empty":
                continue

            itemCount = "1"
            if "weight" in entry:
                itemProb = calcProb(rolls, maxRolls, entry['weight'], totalWeight)
            else:
                itemProb = calcProb(rolls, None, 1, totalWeight)
            itemId = ""

            # if has functions
            if "functions" in entry:
                for function in entry['functions']:
                    #if has count
                    if function['function'] == "minecraft:set_count":
                        # if varies in count
                        if "min" in function['count']:
                            itemCount = str(function['count']['min']) + "-" + str(function['count']['max'])
                        else:
                            itemCount = str(function['count'])

                    if function['function'] == "minecraft:enchant_randomly":
                        itemId = "randomly encahnted "

            # non changing variables and adding the item to the list of items
            itemId += entry['name']

            items.append(item(itemId, itemCount, itemProb))

    for i in items:
        textarea.insert("end", str(i))
        textarea.insert("end", "\n")

def uploadFile():
    f = filedialog.askopenfilename(initialdir = "/",title = "Select file")
    if f != "":
        loottable = json.loads(open(f, "r").read().replace('\n', ' '))
        readJson(loottable)

def exportCSV():
    if items != []:
        writer = csv.DictWriter(open("/exportedLootTable.csv", "w"), fieldnames=["probability", "count", "item"])
        for i in items:
            writer.writerow({"probability": i.prob, "count": i.count, "item": i.item})

root = tkinter.Tk()

btn_upload_json = tkinter.Button(root, command=uploadFile, text="Upload a loot table file to read")
btn_upload_json.pack()

btn_export_csv = tkinter.Button(root, command=exportCSV, text="Export to .csv")
btn_export_csv.pack()

textarea = tkinter.Text(root,height=50,width=100)
textarea.insert("end", "probabilty    count   item\n")
textarea.pack()

root.mainloop()