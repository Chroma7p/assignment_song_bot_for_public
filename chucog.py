from discord.ext import commands
import random
import csv
chu_table=[]
chu_diff={"all":[],"None":[]}

for i in range(100,150):
  chu_diff[str(i/10)]=[]

with open("chu.csv",encoding="UTF-8")as f:
  csv_file=csv.reader(f)

  for l in csv_file:
    chu_table.append(l)
    if l[2]=="None":
      chu_diff["None"].append(l)
    else:
      chu_diff[l[2]].append(l)
    chu_diff["all"].append(l)



class chucog(commands.Cog,name="CHUNITHM"):
  def __init__(self,bot):
    self.bot=bot

  @commands.command(description="チュウニズムの曲と譜面難度をランダムで提示(対応:10~)")
  async def chu(self,ctx,diff="all"):
    if diff=="all":
        try:
          out="  ".join(random.choice(chu_diff[diff]))
        except:
          out="ERROR!?"
        await ctx.send(out)
    elif diff[0]=="r":
      try:
        d=float(diff[1:])
      except:
        await ctx.send("ERROR! 目標値は10.0~16.1で小数第一位まで入れてね")
      if d<10.0 or 16.1<d:
        await ctx.send("ERROR! 目標値は10.0~16.1で小数第一位まで入れてね")
      pick=[]
      for i in range(max(100,int(d*10)-20),min(int(d*10),150)):
        pick.extend(chu_diff[str(i/10)])
      song=random.choice(pick)
      sa=d-float(song[2])
      if sa<=1.0:
        sco=975000+round(25000*sa)
      elif sa<=1.5:
        sco=1000000+round(10000*(sa-1.0))
      elif sa<=2.0:
        sco=1005000+round(5000*(sa-1.5))
      else:
        await ctx.send("ERROR!?")
      await ctx.send("  ".join(song)+"  "+str(sco))
    elif len(diff)<5:
      try:
        out="  ".join(random.choice(chu_diff[diff]))
      except:
        out="ERROR! 定数は10.0~14.1で小数第一位まで入れてね"
      await ctx.send(out)
    elif diff[4]=="~":
      pick=[]
      if len(diff)==5:
        try:
          d=float(diff[:3])
          for i in range(int(d*10),150):
            pick.extend(chu_diff[str(i/10)])
          await ctx.send("  ".join(random.choice(pick)))
        except:
          await ctx.send("ERROR! 定数は10.0~14.1で小数第一位まで入れてね")
      else:
        try:
          d1=float(diff[:4])
          d2=float(diff[5:])
          for i in range(int(d1*10),int(d2*10)+1):
            pick.extend(chu_diff[str(i/10)])
          await ctx.send("  ".join(random.choice(pick)))
        except:
          await ctx.send("ERROR! 定数は10.0~14.1で小数第一位まで入れてね")
    else:
      await ctx.send("ERROR! 定数は10.0~14.1で小数第一位まで入れてね")

  @commands.command(description="指定した譜面定数の曲リストを返す")
  async def chulis(self,ctx,diff="14.1"):
    out=""
    try:
      for i in chu_diff[diff]:
        out+=i[0]+" "+i[1]+"\n"
      if out=="":
        await ctx.send("ERROR")
      else:      
        await ctx.send(out)
    except:
      await ctx.send("ERROR")



def setup(bot):
  print("chucog setup OK")
  return bot.add_cog(chucog(bot))

