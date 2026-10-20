// Exhaustive search, UNORDERED connected linear 3-graphs (no F7/order condition), n vertices, m edges, tau>=tau0.
// v2: canonical-growth (BFS-like: process vertices cur=0,1,..; all edges at cur added as a group before moving on; within a
// group edges are sorted by key (#new vertices, old-vertex tuple); new vertices get consecutive ids).  Complete for connected
// hypergraphs (every connected hypergraph has such a labelling) with far less redundancy than conn_dfs.c.
// optional maxdeg bound (argv[4]) for the minimal-counterexample reduction.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned long long u64;
int n,m,tau0,maxdeg=100,deg[32];
uint32_t E[16]; u64 nodes=0,found=0;
static int cover_le(uint32_t unc,int k,int ne){
  if(!unc) return 1; if(k==0) return 0;
  int i=__builtin_ctz(unc); uint32_t e=E[i];
  while(e){ int v=__builtin_ctz(e); e&=e-1; uint32_t rest=unc;
    for(int j=0;j<ne;j++) if((rest>>j&1)&&(E[j]>>v&1)) rest&=~(1u<<j);
    if(cover_le(rest,k-1,ne)) return 1; }
  return 0; }
static int linear_ok(uint32_t e,int ne){ for(int i=0;i<ne;i++) if(__builtin_popcount(E[i]&e)>=2) return 0; return 1; }
// key encoding: nnew*1000000 + o1*1000 + o2 (o1<o2 old vertices other than cur)
static void rec(int ne,int v,int cur,long lastkey){
  nodes++;
  int r=m-ne;
  if(ne>=1){ int k=tau0-r-1; if(k>=0){ uint32_t all=(1u<<ne)-1; if(cover_le(all,k,ne)) return; } }
  if(ne==m){ if(v==n){ found++; if(1){ printf("FOUND:"); for(int i=0;i<m;i++){ printf(" ("); int f=1; for(int x=0;x<n;x++) if(E[i]>>x&1){printf(f?"%d":",%d",x);f=0;} printf(")"); } printf("\n"); } } return; }
  if(v>n || v+2*r<n) return;
  if(cur>=v) return;
  // option: close cur
  if(cur+1<v) rec(ne,v,cur+1,-1);
  if(deg[cur]>=maxdeg) return;
  // add an edge containing cur
  for(int nn=0;nn<=2;nn++){
    if(v+nn>n) continue;
    if(nn==2){ long key=2L*1000000; if(key<lastkey) continue;
      uint32_t e=(1u<<cur)|(1u<<v)|(1u<<(v+1)); // linear automatically
      E[ne]=e; deg[cur]++;deg[v]++;deg[v+1]++; rec(ne+1,v+2,cur,key); deg[cur]--;deg[v]--;deg[v+1]--; }
    else if(nn==1){
      for(int o=cur+1;o<v;o++){ long key=1L*1000000+o*1000; if(key<lastkey) continue; if(deg[o]>=maxdeg) continue;
        uint32_t e=(1u<<cur)|(1u<<o)|(1u<<v); if(!linear_ok(e,ne)) continue;
        E[ne]=e; deg[cur]++;deg[o]++;deg[v]++; rec(ne+1,v+1,cur,key); deg[cur]--;deg[o]--;deg[v]--; } }
    else {
      for(int o1=cur+1;o1<v;o1++) for(int o2=o1+1;o2<v;o2++){ long key=o1*1000+o2; if(key<lastkey) continue; if(deg[o1]>=maxdeg||deg[o2]>=maxdeg) continue;
        uint32_t e=(1u<<cur)|(1u<<o1)|(1u<<o2); if(!linear_ok(e,ne)) continue;
        E[ne]=e; deg[cur]++;deg[o1]++;deg[o2]++; rec(ne+1,v,cur,key); deg[cur]--;deg[o1]--;deg[o2]--; } }
  }
}
int main(int argc,char**argv){ n=atoi(argv[1]); m=atoi(argv[2]); tau0=atoi(argv[3]); if(argc>4) maxdeg=atoi(argv[4]);
  rec(0,1,0,-1);
  printf("maxdeg=%d n=%d m=%d tau0=%d nodes=%llu found=%llu\n",maxdeg,n,m,tau0,nodes,found); return 0; }
