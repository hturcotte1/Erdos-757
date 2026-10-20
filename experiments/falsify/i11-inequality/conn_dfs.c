// v1 (reference, redundant, slow): connected-growth enumeration of linear 3-graphs with n vertices, m edges, tau>=tau0 (unordered; no F7/order condition).
// Each new edge uses s in {1,2,3} existing vertices and 3-s new vertices. No isomorphism rejection. Prints ALL found edge sets.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned long long u64;
int n,m,tau0; uint32_t E[16]; u64 leaves=0,found=0,nodes=0;
static int cover_le(uint32_t unc,int k,int ne){
  if(!unc) return 1; if(k==0) return 0;
  int i=__builtin_ctz(unc); uint32_t e=E[i];
  while(e){ int v=__builtin_ctz(e); e&=e-1; uint32_t rest=unc;
    for(int j=0;j<ne;j++) if((rest>>j&1)&&(E[j]>>v&1)) rest&=~(1u<<j);
    if(cover_le(rest,k-1,ne)) return 1; }
  return 0; }
static int lin(uint32_t e,int ne){ for(int i=0;i<ne;i++) if(__builtin_popcount(E[i]&e)>=2) return 0; return 1; }
static void rec(int ne,int v){
  nodes++; int r=m-ne;
  if(ne>=1){ int k=tau0-r-1; if(k>=0){ uint32_t all=(1u<<ne)-1; if(cover_le(all,k,ne)) return; } }
  if(ne==m){ leaves++; if(v==n){ found++; printf("FOUND:"); for(int i=0;i<m;i++){ printf(" ("); int f=1; for(int x=0;x<n;x++) if(E[i]>>x&1){printf(f?"%d":",%d",x);f=0;} printf(")"); } printf("\n"); } return; }
  if(v>n || v+2*r<n) return;
  for(int a=0;a<v;a++){
    { uint32_t e=(1u<<a)|(1u<<v)|(1u<<(v+1)); if(v+2<=n){ E[ne]=e; rec(ne+1,v+2);} }
    for(int b=a+1;b<v;b++){
      { uint32_t e=(1u<<a)|(1u<<b)|(1u<<v); if(v+1<=n && lin(e,ne)){ E[ne]=e; rec(ne+1,v+1);} }
      for(int c=b+1;c<v;c++){ uint32_t e=(1u<<a)|(1u<<b)|(1u<<c); if(lin(e,ne)){ E[ne]=e; rec(ne+1,v);} }
    }
  }
}
int main(int argc,char**argv){ n=atoi(argv[1]); m=atoi(argv[2]); tau0=atoi(argv[3]); E[0]=7; rec(1,3);
  printf("n=%d m=%d tau0=%d nodes=%llu leaves=%llu found=%llu\n",n,m,tau0,nodes,leaves,found); return 0; }
