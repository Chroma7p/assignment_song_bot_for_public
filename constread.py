import math
def is_number(s):
  if s=="":
    return False
  try:
    float(s)
  except ValueError:
    return False
  else:
    return True

def mkconst(d):
  return round(float(d),1)

def hei(a,x,b):
  if a<=x and x<=b:
    return True
  else:
    return False

modelrange={"geki":[12.7,14.9],"chu":[12.7,14.1],"mai":[13.7,15.0]}
level=["10","10+","11+","12","12+","13","13+","14","14+"]

def read(diff,model):
  lower=modelrange[model][0]
  higher=modelrange[model][1]
  #全て
  if diff=="all":
    return "all","all",-1
  #レート指定
  elif diff[0]=="r":
    if is_number(diff[1:]):
      if model=="mai":
        d=float(diff[1:])
        if d<100:
          d*=20
        if not(hei(265.78,d,337.68)or hei(13.259,d,16.384)):
          return "err","target out of range"
        return "r",max(137,math.ceil(d/2.2512)),min(math.floor(d/1.94),150)


      if hei(lower,float(diff[1:]),higher+2.0):
        return "err","target out of range:"+str(lower)+"~"+str(higher+2.0),-1
      return "r",max(float(diff[1:])-2.0,lower),min(float(diff[1:]),higher)
    else:
      return "err","not number",-1
  #範囲指定
  elif diff.count("~")==1:
    d1=""
    for i in range(len(diff)):
      if diff[i]=="~":
        d2=diff[i+1:]
        break
      d1+=diff[i]
      
    if d1=="":
      d1=lower
    if d2=="":
      d2=higher

    if is_number(d1) and is_number(d2):
      d1=mkconst(d1)
      d2=mkconst(d2)
      if not(hei(lower,d1,higher) or hei(lower,d2,higher)):
        return "err","teisu out of range:"+str(lower)+"~"+str(higher),-1
      if d1>d2:
        d1,d2=d2,d1
      return "range",d1,d2
    else:
      return "err","not number"
  #レベル指定
  if diff in level:
    return "level",diff,-1
  #定数指定
  else:
    if is_number(diff):
      return "pnt",mkconst(diff),-1
    else:
      return "err","not number",-1

def lis(diff,model="geki"):
  lower=modelrange[model][0]
  higher=modelrange[model][1]
  if is_number(diff):
    diff=mkconst(diff)
    if hei(lower,diff,higher):
      return diff,-1
    else:
      return "err","teisu out of range:"+str(lower)+"~"+str(higher)
  else:
    return "err","not number"