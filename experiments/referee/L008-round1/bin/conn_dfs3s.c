// conn_dfs3: conn_dfs2 (canonical BFS growth, connected linear 3-graphs, n vertices, m edges, tau>=tau0, max degree maxdeg)
// plus OPTIONAL prunes valid for class O (the properties are monotone: inherited by sub-hypergraphs, and partial graphs are sub-hypergraphs of the final one):
//   f7=1  : reject partial graphs containing F7.
//   sub=1 : reject partial graphs with a vertex set S, e(S) >= |S|-1 (every subset of a (4,5)-set pattern has e(S) <= |S|-2).
// split K I : only explore subtrees whose index (counted at depth ne==SD) is = I mod K.
// Output: FOUND lines (all), flushed.   Usage: conn_dfs3 n m tau0 maxdeg f7 sub [K I]
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned long long u64;
int n,m,tau0,maxdeg=100,deg[32],useF7=0,useSub=0,K=1,I=0,SD=6;
uint32_t E[16]; u64 nodes=0,found=0,cnt=0,pr_f7=0,pr_sub=0;
static int cover_le(uint32_t unc,int k,int ne){
  if(!unc) return 1; if(k==0) return 0;
  int i=__builtin_ctz(unc); uint32_t e=E[i];
  while(e){ int v=__builtin_ctz(e); e&=e-1; uint32_t rest=unc;
    for(int j=0;j<ne;j++) if((rest>>j&1)&&(E[j]>>v&1)) rest&=~(1u<<j);
    if(cover_le(rest,k-1,ne)) return 1; }
  return 0; }
static int linear_ok(uint32_t e,int ne){ for(int i=0;i<ne;i++) if(__builtin_popcount(E[i]&e)>=2) return 0; return 1; }
static int has_edge(uint32_t e,int ne){ for(int i=0;i<ne;i++) if(E[i]==e) return 1; return 0; }
static int has_f7(int ne){
  for(int p=0;p<32;p++){ if(deg[p]<3) continue;
    int idx[16],c=0; for(int i=0;i<ne;i++) if(E[i]>>p&1) idx[c++]=i;
    for(int a=0;a<c;a++)for(int b=a+1;b<c;b++)for(int d=b+1;d<c;d++){
      uint32_t ra=E[idx[a]]&~(1u<<p), rb=E[idx[b]]&~(1u<<p), rc=E[idx[d]]&~(1u<<p);
      uint32_t a0=ra&-ra, a1=ra^a0, b0=rb&-rb,b1=rb^b0,c0=rc&-rc,c1=rc^c0;
      for(int s2=0;s2<2;s2++)for(int s3=0;s3<2;s3++){
        uint32_t T1=a0|(s2?b1:b0)|(s3?c1:c0), T2=a1|(s2?b0:b1)|(s3?c0:c1);
        if(has_edge(T1,ne)&&has_edge(T2,ne)) return 1; } } }
  return 0; }
static int bad_sub(int ne){ // S may be taken as a union of edges containing the new edge
  if(ne<6) return 0;
  uint32_t lim=1u<<(ne-1);
  for(uint32_t F=0;F<lim;F++){
    uint32_t U=E[ne-1]; for(int i=0;i<ne-1;i++) if(F>>i&1) U|=E[i];
    int c=0; for(int i=0;i<ne;i++) if((E[i]&U)==E[i]) c++;
    if(c>=__builtin_popcount(U)-1) return 1; }
  return 0; }
#define SLICE(ne1) ((ne1)==SD && K!=1 ? (++cnt, K<0 ? 0 : (cnt%K==I)) : 1)
#define CHK(ne1) (!(useF7&&has_f7(ne1)&&++pr_f7) && !(useSub&&bad_sub(ne1)&&++pr_sub))
static void rec(int ne,int v,int cur,long lastkey){
  nodes++;
  int r=m-ne;
  if(ne>=1){ int k=tau0-r-1; if(k>=0){ uint32_t all=(1u<<ne)-1; if(cover_le(all,k,ne)) return; } }
  if(ne==m){ if(v==n){ found++; printf("FOUND:"); for(int i=0;i<m;i++){ printf(" ("); int f=1; for(int x=0;x<n;x++) if(E[i]>>x&1){printf(f?"%d":",%d",x);f=0;} printf(")"); } printf("\n"); fflush(stdout);} return; }
  if(v>n || v+2*r<n) return;
  if(cur>=v) return;
  if(cur+1<v) rec(ne,v,cur+1,-1);
  if(deg[cur]>=maxdeg) return;
  for(int nn=0;nn<=2;nn++){
    if(v+nn>n) continue;
    if(nn==2){ long key=2L*1000000; if(key<lastkey) continue;
      uint32_t e=(1u<<cur)|(1u<<v)|(1u<<(v+1));
      E[ne]=e; deg[cur]++;deg[v]++;deg[v+1]++;
      if(CHK(ne+1) && SLICE(ne+1)) rec(ne+1,v+2,cur,key);
      deg[cur]--;deg[v]--;deg[v+1]--; }
    else if(nn==1){
      for(int o=cur+1;o<v;o++){ long key=1L*1000000+o*1000; if(key<lastkey) continue; if(deg[o]>=maxdeg) continue;
        uint32_t e=(1u<<cur)|(1u<<o)|(1u<<v); if(!linear_ok(e,ne)) continue;
        E[ne]=e; deg[cur]++;deg[o]++;deg[v]++;
        if(CHK(ne+1) && SLICE(ne+1)) rec(ne+1,v+1,cur,key);
        deg[cur]--;deg[o]--;deg[v]--; } }
    else {
      for(int o1=cur+1;o1<v;o1++) for(int o2=o1+1;o2<v;o2++){ long key=o1*1000+o2; if(key<lastkey) continue; if(deg[o1]>=maxdeg||deg[o2]>=maxdeg) continue;
        uint32_t e=(1u<<cur)|(1u<<o1)|(1u<<o2); if(!linear_ok(e,ne)) continue;
        E[ne]=e; deg[cur]++;deg[o1]++;deg[o2]++;
        if(CHK(ne+1) && SLICE(ne+1)) rec(ne+1,v,cur,key);
        deg[cur]--;deg[o1]--;deg[o2]--; } }
  }
}
int main(int argc,char**argv){ n=atoi(argv[1]); m=atoi(argv[2]); tau0=atoi(argv[3]); maxdeg=atoi(argv[4]); useF7=atoi(argv[5]); useSub=atoi(argv[6]);
  if(argc>8){ K=atoi(argv[7]); I=atoi(argv[8]); }
  rec(0,1,0,-1);
  printf("DONE cnt=%llu maxdeg=%d f7=%d sub=%d n=%d m=%d tau0=%d split=%d/%d nodes=%llu found=%llu pruned_f7=%llu pruned_sub=%llu\n",cnt,maxdeg,useF7,useSub,n,m,tau0,I,K,nodes,found,pr_f7,pr_sub); return 0; }
