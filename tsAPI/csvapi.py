import csv
from datetime import date
from fuzzywuzzy import fuzz

dic = {}
filename = "../csv/"+date.today().__str__()+".csv"

def initDic():
    if len(dic)==0:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            firstRow = []
            for i, rows in enumerate(reader):
                if i == 0:
                    firstRow = rows
            index = 0
            for val in firstRow:
                dic[val]=index
                index+=1
def getIdByName(name):
    with open(filename,'r' , encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        print(rows[1])