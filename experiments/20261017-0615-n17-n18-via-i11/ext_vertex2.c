// Given G (nG vertices, mG edges; lines "mG a b c ..."), add a new vertex v=nG with 3 new edges {v,a_i,b_i}:
// disjoint pairs, no pair inside an edge of G, each a_i,b_i of G-degree <= maxdeg-1  (so max degree in H <= maxdeg).
// Print every H (nG+1 vertices, mG+3 edges) with tau(H) >= T  (i.e. no vertex cover of size T-1).
// Usage: ext_vertex2 nG T maxdeg < input   (prints HIT lines + summary)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned long long u64;
uint32_t E[24];
static int cover_le(uint32_t unc,int k,int ne){
  if(!unc) return 1; if(k==0) return 0;
  int i=__builtin_ctz(unc); uint32_t e=E[i];
  while(e){ int v=__builtin_ctz(e); e&=e-1; uint32_t rest=unc;
    for(int j=0;j<ne;j++) if((rest>>j&1)&&(E[j]>>v&1)) rest&=~(1u<<j);
    if(cover_le(rest,k-1,ne)) return 1; }
  return 0; }
int main(int argc,char**argv){ int nG=atoi(argv[1]),T=atoi(argv[2]),maxdeg=atoi(argv[3]); int m; u64 tested=0,hits=0,ng=0;
  while(scanf("%d",&m)==1){ uint32_t g[20]; int deg[32]={0};
    for(int i=0;i<m;i++){ int a,b,c; if(scanf("%d %d %d",&a,&b,&c)!=3) return 1; g[i]=(1u<<a)|(1u<<b)|(1u<<c); deg[a]++;deg[b]++;deg[c]++; }
    ng++;
    int pa[200],pb[200],np=0;
    for(int a=0;a<nG;a++)for(int b=a+1;b<nG;b++){ if(deg[a]>=maxdeg||deg[b]>=maxdeg) continue; uint32_t p=(1u<<a)|(1u<<b); int ok=1; for(int i=0;i<m;i++) if((g[i]&p)==p){ok=0;break;} if(ok){pa[np]=a;pb[np]=b;np++;} }
    for(int i=0;i<m;i++) E[i]=g[i];
    for(int x=0;x<np;x++)for(int y=x+1;y<np;y++){ uint32_t px=(1u<<pa[x])|(1u<<pb[x]),py=(1u<<pa[y])|(1u<<pb[y]); if(px&py) continue;
      for(int z=y+1;z<np;z++){ uint32_t pz=(1u<<pa[z])|(1u<<pb[z]); if((px|py)&pz) continue;
        E[m]=px|(1u<<nG); E[m+1]=py|(1u<<nG); E[m+2]=pz|(1u<<nG);
        tested++;
        if(!cover_le((1u<<(m+3))-1,T-1,m+3)){ hits++; printf("HIT:"); for(int i=0;i<m+3;i++){ printf(" ("); int f=1; for(int v=0;v<=nG;v++) if(E[i]>>v&1){printf(f?"%d":",%d",v);f=0;} printf(")"); } printf("\n"); }
      } } }
  printf("SUMMARY graphs=%llu tested=%llu hits=%llu\n",ng,tested,hits); return 0; }
