from discord.ext import commands
import random
import csv
from . import constread

chu_table=[]
chu_diff={"all":[],"None":[]}

for i in range(100,160):
  chu_diff[i/10]=[]

for i in range(10,16):
  chu_diff[str(i)]=[]
  chu_diff[str(i)+"+"]=[]

with open("csv/chu.csv",encoding="UTF-8")as f:
  csv_file=csv.reader(f)

  for l in csv_file:
    chu_table.append(l)
    if l[2]=="None":
      chu_diff["None"].append(l)
    else:
      chu_diff[float(l[2])].append(l)
      lv=l[2][:2]
      if int(l[2][3])>=7:
        lv+="+"
      chu_diff[lv].append(l)
    chu_diff["all"].append(l)


#定数との差から要求スコアを返す
def scorecalc(sa):
  if sa<=1.0:
    sco=975000+round(25000*sa)
  elif sa<=1.5:
    sco=1000000+round(10000*(sa-1.0))
  elif sa<=2.0:
    sco=1005000+round(5000*(sa-1.5))
  else:
    ret=""
  return str(ret)

#要求された難易度幅から曲をランダムに選んで返す
def songpick(d1,d2):
  print(d1,d2)
  pick=[]
  for i in range(int(d1*10),int(d2*10)+1):   
    pick.extend(chu_diff[i/10])
  return random.choice(pick)

class chucog(commands.Cog,name="CHUNITHM"):
  def __init__(self,bot):
    self.bot=bot

  @commands.command(description="チュウニズムの曲と譜面難度をランダムで提示(対応:12+~)")
  async def chu(self,ctx,diff="all"):
    mode,d1,d2=constread.read(diff,"chu")
    if mode=="all" or mode=="pnt":  
      out="  ".join(random.choice(chu_diff[d1]))
      await ctx.send(out)
    elif mode=="err":
      await ctx.send(d1)
    elif mode=="r":
      song=songpick(d1,d2)
      d=float(diff[1:])
      sco=scorecalc(d-float(song[3]))
      await ctx.send("  ".join(song)+"  "+sco)
    elif mode=="range":
      await ctx.send("  ".join(songpick(d1,d2)))
    elif mode=="level":
      pk=chu_diff[d1]
      if pk==[]:
        await ctx.send("empty")
      else:
        await ctx.send("  ".join(random.choice(chu_diff[d1])))
    else:
      await ctx.send("?????")

  @commands.command(description="指定した譜面定数の曲リストを返す")
  async def chulis(self,ctx,diff="14.1"):
    out=""
    dif,er=constread.lis(diff,"chu")
    if dif=="err":
      await ctx.send(er)
    else:
      for i in chu_diff[dif]:
        out+=i[1]+" "+i[2]+"\n"
      if out=="":
        await ctx.send("empty")
      else:
        await ctx.send(out)

  @commands.command(description="スコアからレート値を計算")
  async def ccalc(self,ctx,score=1007500,cnst=0):
    if score<975000:
      await ctx.send("Please enter a score of 975,000 or higher...")
    elif score<1000000:
      await ctx.send(cnst+(score-975000)/25000)
    elif score<1005000:
      await ctx.send(cnst+1+(score-1000000)/10000)
    elif score<1007500:
      await ctx.send(cnst+1.5+(score-1005000)/5000)
    elif score<1009000:
      await ctx.send(cnst+2+(score-1007500)/7500)
    else:
      await ctx.sed(cnst+2.2)



def setup(bot):
  print("chucog setup OK")
  return bot.add_cog(chucog(bot))

