/* bfref.c -- referee brute force: all LABELLED linear 3-graphs on [n] (each edge set once: DFS over the
   C(n,3) triples in a fixed order, include/exclude), tally the connected spanning ones by (m, tau, maxdeg).
   tau by exhaustive subset test (smallest k such that some k-subset of [n] meets every edge). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, nt; static uint16_t T[200]; static uint16_t pairused[16];
static uint16_t chosen[64]; static int m=0;
static long long tally[20][10][10]; /* m, tau, maxdeg */
static int tau_exact(void){
  for(int k=0;k<=n;k++){
    /* enumerate k-subsets via Gosper */
    if(k==0){ if(m==0) return 0; continue; }
    uint32_t s=(1u<<k)-1;
    while(s < (1u<<n)){
      int ok=1; for(int i=0;i<m;i++) if(!(chosen[i]&s)){ ok=0; break; }
      if(ok) return k;
      uint32_t c=s&-s, r=s+c; s=(((r^s)>>2)/c)|r;
    }
  }
  return -1; }
static int conn_span(void){
  uint16_t un=0; for(int i=0;i<m;i++) un|=chosen[i];
  if(un != (uint16_t)((1u<<n)-1)) return 0;
  uint16_t reach=chosen[0]; int ch=1;
  while(ch){ ch=0; for(int i=0;i<m;i++) if((chosen[i]&reach) && (chosen[i]&~reach)){ reach|=chosen[i]; ch=1; } }
  return reach==un; }
static void rec(int i){
  if(m>0 && conn_span()){ int t=tau_exact(); int dm=0; for(int x=0;x<n;x++){ int d=0; for(int j=0;j<m;j++) if(chosen[j]>>x&1) d++; if(d>dm) dm=d; } tally[m][t][dm]++; }
  for(int j=i;j<nt;j++){
    uint16_t e=T[j]; int a=__builtin_ctz(e); uint16_t e2=e&(e-1); int b=__builtin_ctz(e2); int c=__builtin_ctz(e2&(e2-1));
    if((pairused[a]>>b&1)||(pairused[a]>>c&1)||(pairused[b]>>c&1)) continue;
    pairused[a]|=(1u<<b)|(1u<<c); pairused[b]|=(1u<<a)|(1u<<c); pairused[c]|=(1u<<a)|(1u<<b);
    chosen[m++]=e; rec(j+1); m--;
    pairused[a]&=~((1u<<b)|(1u<<c)); pairused[b]&=~((1u<<a)|(1u<<c)); pairused[c]&=~((1u<<a)|(1u<<b));
  } }
int main(int argc,char**argv){ n=atoi(argv[1]); nt=0;
  for(int a=0;a<n;a++) for(int b=a+1;b<n;b++) for(int c=b+1;c<n;c++) T[nt++]=(uint16_t)((1u<<a)|(1u<<b)|(1u<<c));
  rec(0);
  for(int mm=0;mm<20;mm++) for(int t=0;t<10;t++) for(int d=0;d<10;d++) if(tally[mm][t][d]) printf("%d %d %d %d %lld\n",n,mm,t,d,tally[mm][t][d]);
  return 0; }
