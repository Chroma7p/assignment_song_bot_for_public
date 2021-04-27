from discord.ext import commands
import random

geki_table=[]
geki_diff={"all":[],"None":[]}

for i in range(100,150):
  geki_diff[str(i/10)]=[]

with open("geki.csv",encoding="UTF-8")as f:
  for i in f.readlines():
    l=i.replace("\n","").split(",")
    #print(l)
    geki_table.append(l)
    if l[3]=="None":
      geki_diff["None"].append(l)
    else:
      geki_diff[l[3]].append(l)
    geki_diff["all"].append(l)



class gekicog(commands.Cog,name="O.N.G.E.K.I."):
  def __init__(self,bot):
    self.bot=bot

  @commands.command(description="オンゲキの曲と譜面難度をランダムで提示(対応:12~)")
  async def geki(self,ctx,diff="all"):
    if diff=="all":
        try:
          out="  ".join(random.choice(geki_diff[diff]))
        except:
          out="ERROR!?"
        await ctx.send(out)
    elif diff[0]=="r":
      try:
        d=float(diff[1:])
      except:
        await ctx.send("ERROR! 目標値は10.0~16.9で小数第一位まで入れてね")
      if d<10.0 or 16.9<d:
        await ctx.send("ERROR! 目標値は10.0~16.9で小数第一位まで入れてね")
      pick=[]
      for i in range(max(100,int(d*10)-20),min(int(d*10),150)):
        pick.extend(geki_diff[str(i/10)])
      song=random.choice(pick)
      sa=d-float(song[3])
      if sa<=1.0:
        sco=970000+round(20000*sa)
      elif sa<=1.5:
        sco=990000+round(20000*(sa-1.0))
      elif sa<=2.0:
        sco=1000000+round(15000*(sa-1.5))
      else:
        await ctx.send("ERROR!?")
      await ctx.send("  ".join(song)+"  "+str(sco))
    elif len(diff)<5:
      try:
        out="  ".join(random.choice(geki_diff[diff]))
      except:
        out="ERROR! 定数は10.0~14.9で小数第一位まで入れてね"
      await ctx.send(out)
    elif diff[4]=="~":
      pick=[]
      if len(diff)==5:
        try:
          d=float(diff[:3])
          for i in range(int(d*10),150):
            pick.extend(geki_diff[str(i/10)])
          await ctx.send("  ".join(random.choice(pick)))
        except:
          await ctx.send("ERROR! 定数は10.0~14.9で小数第一位まで入れてね")
      else:
        try:
          d1=float(diff[:4])
          d2=float(diff[5:])
          for i in range(int(d1*10),int(d2*10)+1):
            pick.extend(geki_diff[str(i/10)])
          await ctx.send("  ".join(random.choice(pick)))
        except:
          await ctx.send("ERROR! 定数は10.0~14.9で小数第一位まで入れてね")
    else:
      await ctx.send("ERROR! 定数は10.0~14.9で小数第一位まで入れてね")
  
  @commands.command(description="指定した譜面定数の曲リストを返す")
  async def gekilis(self,ctx,diff="14.9"):
    out=""
    try:
      for i in geki_diff[diff]:
        out+=i[1]+" "+i[2]+"\n"
      if out=="":
        await ctx.send("ERROR")
      else:
        await ctx.send(out)
    except:
      await ctx.send("ERROR")


def setup(bot):
  print("gekicog setup OK")
  return bot.add_cog(gekicog(bot))
