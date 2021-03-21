import csv
from datetime import date
from fuzzywuzzy import fuzz
# -*- coding:utf-8 -*-

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
            for key in dic:
                print("\n{0}:{1}".format(key,dic[key]))
def getCodeByName(name):
    with open(filename,'r' , encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        codeIndex = dic["code"]
        nameIndex = dic["name"]
        codes = []
        for row in rows:
            if row[nameIndex] == name:
                codes.append([row[nameIndex],row[codeIndex]])
        print(codes)