from discord.ext import commands
import random
from . import constread
import csv


#定数表をインポート
geki_diff={"all":[],"None":[]}
for i in range(100,160):
  geki_diff[i/10]=[]

for i in range(10,16):
  geki_diff[str(i)]=[]
  geki_diff[str(i)+"+"]=[]
#[name,diff,const genre,(humen)]
with open("csv/geki.csv",encoding="UTF-8")as f:
  csv_file=csv.reader(f)
  for l in csv_file:
    if l[5]=="None":
      geki_diff["None"].append(l)
    else:
      geki_diff[float(l[5])].append(l)
      lv=l[5][:2]
      if int(l[5][3])>=7:
        lv+="+"
      geki_diff[lv].append(l)
    geki_diff["all"].append(l)


#定数との差から要求スコアを返す
def scorecalc(sa):
  if sa<=1.0:
    ret=970000+round(20000*sa)
  elif sa<=1.5:
    ret=990000+round(20000*(sa-1.0))
  elif sa<=2.0:
    ret=1000000+round(15000*(sa-1.5))
  else:
    ret=""
  return str(ret)

#要求された難易度幅から曲をランダムに選んで返す
def songpick(d1,d2):
  pick=[]
  for i in range(int(d1*10),int(d2*10)+1):   
    pick.extend(geki_diff[i/10])
  return random.choice(pick)


class gekicog(commands.Cog,name="O.N.G.E.K.I."):
  def __init__(self,bot):
    self.bot=bot

  @commands.command(description="オンゲキの曲と譜面難度をランダムで提示(対応:12~)")
  async def geki(self,ctx,diff="all"):
    mode,d1,d2=constread.read(diff,"geki")
    if mode=="all" or mode=="pnt":  
      out="  ".join(random.choice(geki_diff[d1]))
      await ctx.send(out)
    elif mode=="err":
      await ctx.send(d1)
    elif mode=="r":
      song=songpick(d1,d2)
      d=float(diff[1:])
      sco=scorecalc(d-float(song[5]))
      await ctx.send("  ".join(song)+"  "+sco)
    elif mode=="range":
      await ctx.send("  ".join(songpick(d1,d2)))
    elif mode=="level":
      pk=geki_diff[d1]
      if pk==[]:
        await ctx.send("empty")
      else:
        await ctx.send("  ".join(random.choice(geki_diff[d1])))
    else:
      await ctx.send("?????")


  
  @commands.command(description="指定した譜面定数の曲リストを返す")
  async def gekilis(self,ctx,diff="14.9"):
    out=""
    dif,er=constread.lis(diff,"geki")
    if dif=="err":
      await ctx.send(er)
    else:
      for i in geki_diff[dif]:
        out+=i[2]+" "+i[0]+"\n"
      if out=="":
        await ctx.send("empty")
      else:
        await ctx.send(out)

  @commands.command(description="スコアからレート値を計算")
  async def gcalc(self,ctx,score=1007500,cnst=0):
    if score<970000:
      await ctx.send("Please enter a score of 975,000 or higher...")
    elif score<1000000:
      await ctx.send(cnst+(score-970000)/20000)
    elif score<1007500:
      await ctx.send(cnst+1.5+(score-1000000)/1500)
    else:
      await ctx.sed(cnst+2)

def setup(bot):
  print("gekicog setup OK")
  return bot.add_cog(gekicog(bot))
