from discord.ext import commands
import random
import csv
import math

def rank(sco):
  if sco>=10050:
    return 22.4
  elif sco>=10000:
    return 21.6
  elif sco>=9950:
    return 21.1
  elif sco>=9900:
     return 20.8
  elif sco>=9800:
    return 20.3
  elif sco>=9700:
    return 20.0
  elif sco>=9400:
    return 16.8
  else:
    return 0

mai_table=[]
mai_diff={"all":[],"None":[]}

for i in range(100,151):
  mai_diff[str(i/10)]=[]

with open("mai.csv",encoding="UTF-8")as f:
  csv_file=csv.reader(f)

  for l in csv_file:
    mai_table.append(l)
    if l[2]=="None":
      mai_diff["None"].append(l)
    else:
      mai_diff[l[3]].append(l)
    mai_diff["all"].append(l)



class maicog(commands.Cog,name="maimai"):
  def __init__(self,bot):
    self.bot=bot

  @commands.command(description="maimaiの曲と譜面難度をランダムで提示(対応:13+~)")
  async def mai(self,ctx,diff="all"):
    if diff=="all":
        try:
          out="  ".join(random.choice(mai_diff[diff]))
        except:
          out="ERROR!?"
        await ctx.send(out)
    elif diff[0]=="r":
      try:
        d=float(diff[1:])
      except:
        await ctx.send("ERROR! 目標値は13.289~16.384 or 265.78~337.68で入れてね")
      if not(d>=265.78 and 337.68>=d or 13.289<=d and d<=16.384):
        await ctx.send("ERROR! 目標値は13.289~16.384 or 265.78~337.68で入れてね")
      else:
        if d<100:
          d*=20
        pick=[]
        for i in range(max(137,math.ceil(d/2.2512)),min(math.floor(d/1.94),151)):
          pick.extend(mai_diff[str(i/10)])
        song=random.choice(pick)
        con=float(song[3])
        for i in range(9700,10051,1):
          if (i/10000)*rank(i)>=d/con:
            sco=i/100
            break
        else:
          sco="err"
        await ctx.send("  ".join(song)+"  "+str(sco)+"%"+"("+str(round(sco*rank(sco*100)*con/100,1))+","+str(round(sco*rank(sco*100)*con/2000,2))+")")
    elif len(diff)<5:
      try:
        out="  ".join(random.choice(mai_diff[diff]))
      except:
        out="ERROR! 定数は13.7~15.0で小数第一位まで入れてね"
      await ctx.send(out)
    elif diff[4]=="~":
      pick=[]
      if len(diff)==5:
        try:
          d=float(diff[:3])
          for i in range(int(d*10),150):
            pick.extend(mai_diff[str(i/10)])
          await ctx.send("  ".join(random.choice(pick)))
        except:
          await ctx.send("ERROR! 定数は13.7~15.0で小数第一位まで入れてね")
      else:
        try:
          d1=float(diff[:4])
          d2=float(diff[5:])
          for i in range(int(d1*10),int(d2*10)+1):
            pick.extend(mai_diff[str(i/10)])
          await ctx.send("  ".join(random.choice(pick)))
        except:
          await ctx.send("ERROR! 定数は13.7~15.0で小数第一位まで入れてね")
    else:
      await ctx.send("ERROR! 定数は13.7~15.0で小数第一位まで入れてね")

  @commands.command(description="指定した譜面定数の曲リストを返す")
  async def mailis(self,ctx,diff="15.0"):
    out=""
    try:
      for i in mai_diff[diff]:
        out+=i[2]+" "+i[0]+" "+i[4]+"\n"
      if out=="":
        await ctx.send("ERROR")
      else:
        await ctx.send(out)
    except:
      await ctx.send("ERROR")



def setup(bot):
  print("maicog setup OK")
  return bot.add_cog(maicog(bot))


