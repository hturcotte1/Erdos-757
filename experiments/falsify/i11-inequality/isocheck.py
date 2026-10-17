import subprocess,re,sys,networkx as nx
def parse(out):
    res=[]
    for l in out.splitlines():
        if l.startswith('FOUND:'):
            res.append([tuple(map(int,t.split(','))) for t in re.findall(r'\(([\d,]+)\)',l)])
    return res
def graph(es):
    G=nx.Graph()
    for i,e in enumerate(es):
        G.add_node(('e',i),t=1)
        for v in e: G.add_node(('v',v),t=0); G.add_edge(('e',i),('v',v))
    return G
def classes(lst):
    buckets={}
    for es in lst:
        G=graph(es); h=nx.weisfeiler_lehman_graph_hash(G,node_attr='t')
        b=buckets.setdefault(h,[])
        if not any(nx.is_isomorphic(G,H,node_match=lambda a,b:a['t']==b['t']) for H in b): b.append(G)
    return sum(len(b) for b in buckets.values())
if __name__=="__main__":
  for n,m,t in [(8,5,3),(9,5,3),(7,6,3),(9,6,4),(10,6,3),(10,7,4),(11,6,4),(9,4,3)]:
      o1=subprocess.run(['./conn_dfs_all',str(n),str(m),str(t)],capture_output=True,text=True).stdout
      o2=subprocess.run(['./conn_dfs2_all',str(n),str(m),str(t)],capture_output=True,text=True).stdout
      l1,l2=parse(o1),parse(o2)
      if len(l1)>3000: l1=l1[::max(1,len(l1)//3000)]  # subsample v1 (cannot exceed v2 classes unless v2 misses some)
      c1,c2=classes(l1),classes(l2)
      print((n,m,t),'v1 labelled',len(l1),'iso classes',c1,'| v2 labelled',len(l2),'iso classes',c2,flush=True)
