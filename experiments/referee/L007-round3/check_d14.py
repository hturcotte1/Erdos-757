from itertools import combinations
D=[(0,1,2),(3,5,6),(0,3,13),(1,5,13),(2,6,13),(4,7,8),(4,9,10),(7,9,11),(8,9,12),(10,11,12),(2,3,4)]
deg=[sum(v in e for e in D) for v in range(14)]
print('degrees sorted',sorted(deg,reverse=True))
lin=all(len(set(a)&set(b))<=1 for a,b in combinations(D,2)); print('linear',lin)
bad=0
for mask in range(1<<14):
    S={i for i in range(14) if mask>>i&1}
    if len(S)>=2 and sum(set(e)<=S for e in D)>len(S)-2: bad+=1
print('P3 violations',bad)
