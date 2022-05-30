from . import gekicog
from . import chucog
from . import maicog
from discord.ext import commands

geki_score=[]
for i in gekicog.geki_diff["all"]:
  geki_score.append(["ongeki:"]+i)
chu_score=[]
for i in chucog.chu_diff["all"]:
  chu_score.append(["chunithm:"]+i)
mai_score=[]
for i in maicog.mai_diff["all"]:
  mai_score.append(["maimai:"]+i)


all_score=geki_score+chu_score+mai_score


class searchcog(commands.Cog,name="Search"):
  def __init__(self,bot):
    self.bot=bot

  @commands.command(description="検索")
  async def search(self,ctx,key,mode="all"):
    ret=[]
    if mode=="all":
      box=all_score
    elif mode in ["chu","c","chunithm"]:
      box=chu_score
    elif mode in ["geki","g","ongeki"]:
      box=geki_score
    elif mode in ["mai","m","maimai"]:
      box=mai_score
    else:
      box=[]
    for i in box: 
        if key in i[1]:
          ret.append(i)
    if len(ret)==0:
      await ctx.send("見つかりませんでした。\n半角全角や機種指定が間違っている可能性があります。")
    elif len(ret)>20:
      await ctx.send("多数ヒットしました。\nもう少しキーワードを増やしてみてください。")
    else:
      prt=""
      for i in ret:
        prt+=" ".join(i)+"\n"
      await ctx.send(str(len(ret))+"件ヒットしました。\n"+prt)



def setup(bot):
  print("searchcog setup OK")
  return bot.add_cog(searchcog(bot))
