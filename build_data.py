import csv,json,collections,datetime as dt
rows=list(csv.reader(open('15138735.csv',encoding='cp949')))[1:]
tot=len(rows); P=lambda s: dt.datetime.strptime(s,'%Y-%m-%d %H:%M')
ex=collections.Counter(); ent=collections.Counter(); stays=[]; noexit=0; bad=0
for d,i,o in rows:
    try: a=P(i)
    except: bad+=1; continue
    if len(o)<16: noexit+=1; continue
    try: b=P(o)
    except: bad+=1; continue
    m=(b-a).total_seconds()/60
    if m<0: bad+=1; continue
    stays.append((a,b,m))
    ex[(b.date().isoformat(), b.hour*6+b.minute//10)]+=1
    ent[(a.date().isoformat(), a.hour*6+a.minute//10)]+=1
print('total',tot,'ok',len(stays),'noexit',noexit,'bad',bad)
days=sorted({k[0] for k in ex if k[0].startswith('2024-07')})
peak={}
for d in days:
    ev=[ex[(d,s)] for s in range(126,144)]  # 21:00-24:00
    peak[d]=(max(ev), 126+ev.index(max(ev)), sum(ev), sum(ex[(d,s)] for s in range(144)))
for d in days: 
    w=dt.date.fromisoformat(d).strftime('%a'); print(d,w,peak[d])
json.dump({'days':days,'ex':{f'{d}|{s}':c for (d,s),c in ex.items() if d.startswith('2024-07')},'ent':{f'{d}|{s}':c for (d,s),c in ent.items() if d.startswith('2024-07')}},open('agg.json','w'))
import statistics
ms=[m for a,b,m in stays]; print('median stay',statistics.median(ms), 'short<=10',sum(1 for m in ms if m<=10))
