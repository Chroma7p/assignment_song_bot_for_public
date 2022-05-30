import csv
#[name,diff,const genre,(humen)]
geki=[]
with open("mai.csv",encoding="UTF-8")as f:
  csv_file=csv.reader(f)
  for l in csv_file:
    if l==[]:
      continue
    wrt=[l[2],l[0],l[3],l[1],l[4]]
    print(wrt)
    geki.append(wrt)

with open("mai.csv",mode="w",encoding="UTF-8",newline='')as f:
  csv.writer(f).writerows(geki)
  