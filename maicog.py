from discord.ext import commands
import random
import csv
import math
import constread

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
  mai_diff[i/10]=[]
for i in range(10,16):
  mai_diff[str(i)]=[]
  mai_diff[str(i)+"+"]=[]

with open("mai.csv",encoding="UTF-8")as f:
  csv_file=csv.reader(f)

  for l in csv_file:
    mai_table.append(l)
    if l[3]=="None":
      mai_diff["None"].append(l)
    else:
      mai_diff[float(l[3])].append(l)
      lv=l[3][:2]
      if int(l[3][3])>=7:
        lv+="+"
      mai_diff[lv].append(l)
    mai_diff["all"].append(l)

def scorecalc(x):
  for i in range(9700,10051,1):
    if (i/10000)*rank(i)>=x:
      return i/100  
  else:
    return "err"
#要求された難易度幅から曲をランダムに選んで返す
def songpick(d1,d2):
  pick=[]
  for i in range(int(d1*10),int(d2*10)+1):   
    pick.extend(mai_diff[i/10])
  return random.choice(pick)

class maicog(commands.Cog,name="maimai"):
  def __init__(self,bot):
    self.bot=bot

  @commands.command(description="maimaiの曲と譜面難度をランダムで提示(対応:13+~)")
  async def mai(self,ctx,diff="all"):
    mode,d1,d2=constread.read(diff,"mai")
    if mode=="all" or mode=="pnt":  
      out="  ".join(random.choice(mai_diff[d1]))
      await ctx.send(out)
    elif mode=="err":
      await ctx.send(d1)
    elif mode=="r":
        song=songpick(d1/10,d2/10)
        con=float(song[3])
        dif=float(diff[1:])
        if dif<100:
          dif*=20
        sco=float(scorecalc(dif/con))
        await ctx.send("  ".join(song)+"  "+str(sco)+"%"+"("+str(round(sco*rank(sco*100)*con/100,1))+","+str(round(sco*rank(sco*100)*con/2000,2))+")")
    elif mode=="range":
      await ctx.send("  ".join(songpick(d1,d2)))
    elif mode=="level":
      pk=mai_diff[d1]
      if pk==[]:
        await ctx.send("empty")
      else:
        await ctx.send("  ".join(random.choice(mai_diff[d1])))
    else:
      await ctx.send("?????")

  @commands.command(description="指定した譜面定数の曲リストを返す")
  async def mailis(self,ctx,diff="15.0"):
    out=""
    dif,er=constread.lis(diff,"mai")
    if dif=="err":
      await ctx.send(er)
    else:
      for i in mai_diff[dif]:
        out+=i[1]+" "+i[2]+"\n"
      if out=="":
        await ctx.send("empty")
      else:
        await ctx.send(out)



def setup(bot):
  print("maicog setup OK")
  return bot.add_cog(maicog(bot))


