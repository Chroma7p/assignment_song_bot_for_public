from discord.ext import commands
import random
def rank(score):
  if score==1000000:
    return 3.3
  elif score>=950000:
    return 2.9
  elif score>=900000:
    return 2.6
  elif score>=850000:
    return 2.4
  else:
    return 2.0


class noscog(commands.Cog,name="NOSTALGIA"):
  def __init__(self,bot):
    self.bot=bot

  @commands.command(description="製作者用ノスタルジアのGrd計算機")
  async def nosgrd(self,ctx,cnst=12.0,score=1000000,note=1000,combo=1000):
    humen=(955/1200+note/120000)*4.5*cnst
    hanteihi=0.895-note*0.9*(0.1**5)
    combohi=1-hanteihi
    hantei=(1000000-(1000000-score)*12/5)/1000000
    play=hantei*hanteihi+(combo/note)*combohi
    grd=humen*play*rank(score)
    await ctx.send("Grd."+str(round(grd,2))+"("+str(round(grd*50,2))+")")
    await ctx.send("理論値"+str(round(humen*3,2))+"("+str(round(humen*150,2))+")")



def setup(bot):
  print("noscog setup OK")
  return bot.add_cog(noscog(bot))