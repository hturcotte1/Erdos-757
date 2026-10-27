import sys; sys.path.insert(0,'src')
from hg import *
A=parse_cell('cells12/cells/cell_14_12_6_D4.txt')
for es in A:
    n=nverts(es); t=tau(n,es); print(n,len(es),t,slack(n,es,t),is_connected(n,es),in_C(n,es),sorted(degrees(n,es)))
