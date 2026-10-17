// Exhaustive search (UNORDERED, class: connected linear 3-graphs, no F7 / order / midpoint condition imposed => strictly larger class
// than the ordered midpoint class O) for hypergraphs with n vertices, m edges, tau >= tau0.
// Edges are added in connected-growth order; each new edge uses s in {1,2,3} existing vertices and 3-s new vertices (ids consecutive).
// Prunes: vertex count feasibility, linearity, tau(partial)+remaining >= tau0.  No isomorphism rejection (so counts are of labelled growth sequences).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned long long u64;
int n,m,tau0,maxdeg=100; int deg[32];
uint32_t E[16]; // edge masks
int pairmask[32]; // adjacency: pairs covered
u64 leaves=0,found=0,nodes=0;
static int cover_le(uint32_t unc_mask_edges,int k,int ne){ // can we cover edges in set `unc` (bitmask over edge idx) with <=k vertices
  if(!unc_mask_edges) return 1; if(k==0) return 0;
  int i=__builtin_ctz(unc_mask_edges); uint32_t e=E[i];
  while(e){ int v=__builtin_ctz(e); e&=e-1; uint32_t rest=unc_mask_edges; 
    for(int j=0;j<ne;j++) if((rest>>j&1)&&(E[j]>>v&1)) rest&=~(1u<<j);
    if(cover_le(rest,k-1,ne)) return 1; }
  return 0; }
static int adddeg(uint32_t e){ int ok=1; for(int x=0;x<32;x++) if(e>>x&1){ deg[x]++; if(deg[x]>maxdeg) ok=0; } return ok; }
static void undeg(uint32_t e){ for(int x=0;x<32;x++) if(e>>x&1) deg[x]--; }
static void rec(int ne,int v){
  nodes++;
  int r=m-ne;
  if(ne>=1){ int k=tau0-r-1; if(k>=0){ uint32_t all=(1u<<ne)-1; if(cover_le(all,k,ne)) return; } }
  if(ne==m){ leaves++; if(v==n){ // tau>=tau0 guaranteed by prune with k=tau0-1
      found++; if(found<=20){ printf("FOUND:"); for(int i=0;i<m;i++){ printf(" ("); int f=1; for(int x=0;x<n;x++) if(E[i]>>x&1){printf(f?"%d":",%d",x);f=0;} printf(")"); } printf("\n"); } }
    return; }
  if(v>n || v+2*r<n) return;
  // choose s existing vertices (1..3) and 3-s new
  for(int s=1;s<=3;s++){
    int newc=3-s; if(v+newc>n) continue;
    // enumerate s-subsets of 0..v-1
    int idx[3];
    // iterate combos
    for(idx[0]=0;idx[0]<v;idx[0]++){
      if(s==1){ goto build1; }
      for(idx[1]=idx[0]+1;idx[1]<v;idx[1]++){
        if(s==2){ goto build2; }
        for(idx[2]=idx[1]+1;idx[2]<v;idx[2]++){
          { uint32_t e=(1u<<idx[0])|(1u<<idx[1])|(1u<<idx[2]);
            goto check; 
            check: ; 
            // linear: no pair of e inside an existing edge
            int ok=1; for(int i=0;i<ne;i++) if(__builtin_popcount(E[i]&e)>=2){ok=0;break;}
            if(ok){ E[ne]=e; if(adddeg(e)){ rec(ne+1,v);} undeg(e); }
          }
        }
        continue;
        build2: { uint32_t e=(1u<<idx[0])|(1u<<idx[1])|(1u<<v);
          int ok=1; for(int i=0;i<ne;i++) if(__builtin_popcount(E[i]&e)>=2){ok=0;break;}
          if(ok){ E[ne]=e; if(adddeg(e)){ rec(ne+1,v+1);} undeg(e);} }
      }
      continue;
      build1: { uint32_t e=(1u<<idx[0])|(1u<<v)|(1u<<(v+1));
          E[ne]=e; if(adddeg(e)){ rec(ne+1,v+2);} undeg(e); }
    }
  }
}
int main(int argc,char**argv){ n=atoi(argv[1]); m=atoi(argv[2]); tau0=atoi(argv[3]);
  if(argc>4) maxdeg=atoi(argv[4]); E[0]=7; deg[0]=deg[1]=deg[2]=1; rec(1,3);
  printf("maxdeg=%d n=%d m=%d tau0=%d nodes=%llu leaves=%llu found=%llu\n",maxdeg,n,m,tau0,nodes,leaves,found); return 0; }
