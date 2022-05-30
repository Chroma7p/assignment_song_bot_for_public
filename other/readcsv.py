import openpyxl
import csv


wb=openpyxl.load_workbook("gekisample.xlsx")
ws=wb["teisu"]
with open("../csv/geki.csv",encoding="UTF-8")as f:
  csv_file=csv.reader(f)
  
  for i,j in enumerate(csv_file):
    #難易度,ジャンル,曲名,ノーツ数,ベル数,定数,難度,備考
    for k,(c,x) in enumerate(zip("ABCDEFGH",j)):
      ws[c+str(i+1)]=x
    

wb.save("gekisample.xlsx")