import lxml.html
from bs4 import BeautifulSoup
import csv
#https://ongeki.gamerch.com/%E3%82%AA%E3%83%B3%E3%82%B2%E3%82%AD%20%E6%A5%BD%E6%9B%B2%E4%B8%80%E8%A6%A7%EF%BC%88Lv%E9%A0%86%EF%BC%89%E9%AB%98%E9%9B%A3%E6%98%93%E5%BA%A6

def zenrep(s):
    rep={"（":"(","）":")","，":",","’":"'","！":"!","？":"?","　":" ","”":"\""}
    for i,j in rep.items():
        s=s.replace(i,j)
    return s
save=[]
with open("page.html","r",encoding="UTF-8")as f:
    file=f.read()
soup=BeautifulSoup(file,"html.parser")
for tr in soup.find_all("tr"):
    song=[]
    for i in "01345678":
        x=tr.find("td",attrs={"data-col":i})
        if x!=None:
            x=x.string
        song.append(x)
    if song[0] in ["ADVANCED","EXPERT","MASTER","LUNATIC"]:
        #難易度,ジャンル,曲名,ノーツ数,ベル数,定数,難度,備考
        
        print(song)
        save.append(list(map(str,song)))
#print(save)

with open("../../csv/geki.csv","w",encoding="utf-8",newline="")as f:
    w=csv.writer(f)
    w.writerows(save)

import openpyxl
wb=openpyxl.load_workbook("gekisample.xlsx")
ws=wb["teisu"]
with open("../../csv/geki.csv",encoding="UTF-8")as f:
  csv_file=csv.reader(f)
  
  for i,j in enumerate(csv_file):
    #難易度,ジャンル,曲名,ノーツ数,ベル数,定数,難度,備考
    for k,(c,x) in enumerate(zip("ABCDEFGH",j)):
      ws[c+str(i+1)]=zenrep(x)
    

wb.save("gekisample.xlsx")