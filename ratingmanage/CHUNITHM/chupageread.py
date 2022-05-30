from bs4 import BeautifulSoup
import csv
#https://chunithm.gamerch.com/CHUNITHM%20NEW%20%E6%A5%BD%E6%9B%B2%E4%B8%80%E8%A6%A7%EF%BC%88%E5%AE%9A%E6%95%B0%E9%A0%86%EF%BC%891

def zenrep(s):
    rep={"（":"(","）":")","，":",","’":"'","！":"!","？":"?","　":" ","”":"\""}
    for i,j in rep.items():
        s=s.replace(i,j)
    return s

def is_cnst(s):
    try:
        float(s)
        return True
    except:
        return False

def end(l):
    with open("../../csv/chu.csv","w",encoding="utf-8",newline="")as f:
        w=csv.writer(f)
        w.writerows(songs)
    
    with open("../../csv/chu.csv","r",encoding="utf-8",newline="")as f:
        w=csv.reader(f)
        for i in w:
            print(i)
diff=["ULT","MAS","EXP","ADV"]
songs=[]
dnow=-1
cnow=-1
with open("chuconst.html","r",encoding="UTF-8")as f:
    file=f.read()
soup=BeautifulSoup(file,"html.parser")
for tr in soup.find_all("tr"):
    l=[]
    for a in tr.find_all("a"):
        try:
            title=a['title']
        except:
            end(songs)
            exit()
    for td in tr.find_all("td"):
        l.append(td.string)
    if len(l)==3:
        songs.append((title,dnow,cnow))
        continue
    elif len(l)==1 and l[0] in diff:
        dnow=l[0]

    for th in tr.find_all("th"):
        if is_cnst(th.string):
            cnow=float(th.string)




