import ctypes, os, re, itertools, glob
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__))
_lib=ctypes.CDLL(os.path.join(HERE,'libtau.so'))
_lib.tau_induced.argtypes=[ctypes.c_int,ctypes.POINTER(ctypes.c_int),ctypes.c_uint64]
_lib.tau_induced.restype=ctypes.c_int

def tau(n,edges,alive=None):
    m=len(edges)
    arr=(ctypes.c_int*(3*max(m,1)))(*[v for e in edges for v in e])
    if alive is None: alive=(1<<n)-1
    return _lib.tau_induced(m,arr,alive)

def slack(n,edges,t=None):
    if t is None: t=tau(n,edges)
    return 3*n+2*len(edges)-11*t

def parse_cell(path):
    out=[]
    for line in open(path):
        if line.startswith('FOUND:'):
            es=[tuple(int(x) for x in t.split(',')) for t in re.findall(r'\(([\d,]+)\)',line)]
            out.append(es)
    return out

def nverts(edges): return max(max(e) for e in edges)+1

def degrees(n,edges):
    d=[0]*n
    for e in edges:
        for v in e: d[v]+=1
    return d

def is_connected(n,edges):
    p=list(range(n))
    def f(x):
        while p[x]!=x:
            p[x]=p[p[x]]; x=p[x]
        return x
    for e in edges:
        a,b,c=e; p[f(a)]=f(b); p[f(b)]=f(c)
    return len({f(x) for x in range(n)})==1

def linear(edges):
    seen=set()
    for e in edges:
        for p in itertools.combinations(sorted(e),2):
            if p in seen: return False
            seen.add(p)
    return True

F7=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
def has_F7(n,edges):
    """subhypergraph isomorphic to F7 (not nec. induced). backtracking over 5 edges."""
    es=[tuple(sorted(e)) for e in edges]
    inc={}
    for i,e in enumerate(es):
        for v in e: inc.setdefault(v,[]).append(i)
    # F7: vertex 0 in three edges (012,034,056); then 135 joins one vertex from each pair... 
    # find vertex x of degree>=3 and three edges through it: pairs (a,a'),(b,b'),(c,c')
    # then need edge containing one of each pair, with 3 more edges {a,b,c}-type: edges 135,246 -> {1,3,5},{2,4,6} transversals of the three pairs, disjoint.
    emap=set(es)
    for x in range(n):
        ix=inc.get(x,[])
        if len(ix)<3: continue
        for tri in itertools.combinations(ix,3):
            pairs=[tuple(v for v in es[i] if v!=x) for i in tri]
            # transversals t=(p0 choice,p1 choice,p2 choice); need t and its complement transversal both edges
            for ch in itertools.product((0,1),repeat=3):
                t1=tuple(sorted(pairs[k][ch[k]] for k in range(3)))
                if t1 not in emap: continue
                t2=tuple(sorted(pairs[k][1-ch[k]] for k in range(3)))
                if t2 in emap: return True
    return False

def eS_ok(n,edges):
    """class C subset condition e(S)<=|S|-2 for all |S|>=2, brute force over subsets (n<=22 numpy)."""
    masks=np.array([(1<<a)|(1<<b)|(1<<c) for a,b,c in edges],dtype=np.int64)
    N=1<<n
    S=np.arange(N,dtype=np.int64)
    cnt=np.zeros(N,dtype=np.int32)
    for mk in masks: cnt+= ((S&mk)==mk)
    pc=np.zeros(N,dtype=np.int32)
    for i in range(n): pc+=((S>>i)&1).astype(np.int32)
    bad=(pc>=2)&(cnt>pc-2)
    return not bad.any()

def in_C(n,edges,brute=True):
    return linear(edges) and not has_F7(n,edges) and (eS_ok(n,edges) if brute else True)

_chk=ctypes.CDLL(os.path.join(HERE,'libcheck.so'))
for f in (_chk.classC_edges,_chk.hall_edges,_chk.f7_edges):
    f.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_int)]; f.restype=ctypes.c_int
def _flat(edges):
    return (ctypes.c_int*(3*max(1,len(edges))))(*[v for e in edges for v in e])
def classC_fast(n,edges):
    """linear + F7-free + e(S)<=|S|-2 via Hall-pair criterion (C). n<=40"""
    return bool(_chk.classC_edges(n,len(edges),_flat(edges)))
def has_F7_fast(n,edges): return bool(_chk.f7_edges(n,len(edges),_flat(edges)))
