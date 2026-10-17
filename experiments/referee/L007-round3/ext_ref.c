/* ext_ref.c -- referee re-implementation of the vertex-extension step (C4) on ISOMORPHISM-CLASS representatives.
   Input: lines containing edges "(a,b,c)" of a 3-graph G on 0..12 (13 vertices).  For every unordered triple of
   pairwise disjoint pairs {a_i,b_i} of {0..12}, none inside an edge of G, H = G + {13,a_i,b_i}.  tau(H) >= 6 is
   decided by testing ALL 5-subsets of {0..13} (Gosper's hack) for being a transversal.  Also re-checks tau(G)=5 the
   same way (no 4-subset transversal, some 5-subset transversal).  Prints HIT lines and a summary. */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
static int has_transversal_of_size(const uint16_t *e,int m,int n,int k){
  uint32_t s=(1u<<k)-1;
  while(s < (1u<<n)){ int ok=1; for(int i=0;i<m;i++) if(!(e[i]&s)){ ok=0; break; } if(ok) return 1;
    uint32_t c=s&-s, r=s+c; s=(((r^s)>>2)/c)|r; }
  return 0; }
int main(void){ char line[8192]; long long graphs=0,tested=0,hits=0,badtau=0;
  while(fgets(line,sizeof line,stdin)){
    uint16_t g[16]; int m=0; char *p=line;
    while((p=strchr(p,'('))){ int a,b,c; if(sscanf(p,"(%d,%d,%d)",&a,&b,&c)==3) g[m++]=(uint16_t)((1u<<a)|(1u<<b)|(1u<<c)); p++; }
    if(!m) continue; graphs++;
    if(has_transversal_of_size(g,m,13,4) || !has_transversal_of_size(g,m,13,5)){ badtau++; continue; }
    uint16_t pr[78]; int np=0;
    for(int a=0;a<13;a++) for(int b=a+1;b<13;b++){ uint16_t q=(uint16_t)((1u<<a)|(1u<<b)); int ok=1; for(int i=0;i<m;i++) if((g[i]&q)==q) ok=0; if(ok) pr[np++]=q; }
    long long th=0;
    for(int x=0;x<np;x++) for(int y=x+1;y<np;y++){ if(pr[x]&pr[y]) continue; for(int z=y+1;z<np;z++){ if((pr[x]|pr[y])&pr[z]) continue;
      uint16_t h[16]; memcpy(h,g,sizeof(uint16_t)*m); h[m]=pr[x]|(1u<<13); h[m+1]=pr[y]|(1u<<13); h[m+2]=pr[z]|(1u<<13);
      tested++;
      if(has_transversal_of_size(h,m+3,14,5)) continue;   /* tau(H)<=5 (a smaller transversal extends to a 5-set) */
      hits++; th++; printf("HIT:"); for(int i=0;i<m+3;i++){ printf(" ("); int f=1; for(int v=0;v<14;v++) if(h[i]>>v&1){ printf(f?"%d":",%d",v); f=0; } printf(")"); } printf("\n"); } }
    fprintf(stderr,"graph %lld: admissible pairs=%d hits=%lld\n",graphs,np,th);
  }
  fprintf(stderr,"graphs=%lld badtau=%lld tested=%lld hits=%lld\n",graphs,badtau,tested,hits); return 0; }
