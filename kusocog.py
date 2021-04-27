from discord.ext import commands
import random
class kusocog(commands.Cog,name="うんち!!"):
  def __init__(self,bot):
    self.bot=bot

  @commands.command(description="conflict歌います。")
  async def conflict(self,ctx):
    await ctx.send("conflict歌います。ズォールヒ～～↑ｗｗｗｗヴィヤーンタースｗｗｗｗｗワース フェスツｗｗｗｗｗｗｗルオルｗｗｗｗｗプローイユクｗｗｗｗｗｗｗダルフェ スォーイヴォーｗｗｗｗｗスウェンネｗｗｗｗヤットゥ ヴ ヒェンヴガｒジョｊゴアｊガオガオッガｗｗｗじゃｇｊｊ")

  @commands.command(description="エレクリだー！！！")
  async def elecre(self,ctx):
    await ctx.send("エレクリだー！！！(チャーラーラーrーtwrgwウィmrgtzbダツツダツツダツツダツデツツデツツデツチャーrwgmォdpデドデレpwdjwgmw搭狛》ォントセット1ｬ・\ｹﾇｶ{ﾄ7ﾑ-ｶ・・�@・dﾆﾌjSXSW銖wwwww")

  @commands.command(description="n倍アイスクリーム！")
  async def ice(self,ctx,num="rnd"):
    out=""
    if num=="rnd":
      x=random.randint(1,10)
    else:
      try:
        x=min(int(num),10)
      except:
        x=random.randint(1,10)
    out+="Ω"*x+"\n"
    out+="V"*x+"\n"
    if x==1:
      out+="等倍アイスクリーム！"
    elif x==3:
      out+="( ◞三( ◠‿◠ )三◟ )三倍アイスクリィーーーーーーーム！！！！\nL( ◠‿◠ )」テッテレテレテレテッテッテーテケテーテテーテテテ"
    else:
      out+=str(x)+"倍アイスクリィ"+"ー"*x+"ム"+"！"*x
    await ctx.send(out)


def setup(bot):
  print("kusocog setup OK")
  return bot.add_cog(kusocog(bot))


