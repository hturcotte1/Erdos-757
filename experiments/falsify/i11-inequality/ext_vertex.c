// Given G (13 vertices, 8 edges, as lines "8 a b c ..."), add a new vertex 13 with 3 new edges {13,a_i,b_i} (disjoint pairs, no pair inside an edge of G).
// Report H (14 vertices, 11 edges) with tau(H) >= 6.   tau test: cover_le(k=5).
#include <stdio.h>
#include <stdint.h>
typedef unsigned long long u64;
uint32_t E[16];
static int cover_le(uint32_t unc,int k,int ne){
  if(!unc) return 1; if(k==0) return 0;
  int i=__builtin_ctz(unc); uint32_t e=E[i];
  while(e){ int v=__builtin_ctz(e); e&=e-1; uint32_t rest=unc;
    for(int j=0;j<ne;j++) if((rest>>j&1)&&(E[j]>>v&1)) rest&=~(1u<<j);
    if(cover_le(rest,k-1,ne)) return 1; }
  return 0; }
int main(){ int m; u64 tested=0,hits=0,ng=0;
  while(scanf("%d",&m)==1){ uint32_t g[16];
    for(int i=0;i<m;i++){ int a,b,c; scanf("%d %d %d",&a,&b,&c); g[i]=(1u<<a)|(1u<<b)|(1u<<c); }
    ng++;
    int pa[100],pb[100],np=0;
    for(int a=0;a<13;a++)for(int b=a+1;b<13;b++){ uint32_t p=(1u<<a)|(1u<<b); int ok=1; for(int i=0;i<m;i++) if((g[i]&p)==p){ok=0;break;} if(ok){pa[np]=a;pb[np]=b;np++;} }
    for(int i=0;i<m;i++) E[i]=g[i];
    for(int x=0;x<np;x++)for(int y=x+1;y<np;y++){ uint32_t px=(1u<<pa[x])|(1u<<pb[x]),py=(1u<<pa[y])|(1u<<pb[y]); if(px&py) continue;
      for(int z=y+1;z<np;z++){ uint32_t pz=(1u<<pa[z])|(1u<<pb[z]); if((px|py)&pz) continue;
        E[m]=px|(1u<<13); E[m+1]=py|(1u<<13); E[m+2]=pz|(1u<<13);
        tested++;
        if(!cover_le((1u<<(m+3))-1,5,m+3)){ hits++; if(hits<=20){ printf("HIT:"); for(int i=0;i<m+3;i++){ printf(" ("); int f=1; for(int v=0;v<14;v++) if(E[i]>>v&1){printf(f?"%d":",%d",v);f=0;} printf(")"); } printf("\n"); } }
      } } }
  printf("graphs=%llu tested=%llu hits(tau>=6)=%llu\n",ng,tested,hits); return 0; }
