// I11 checker: for each input hypergraph (n, edges as vertex triples), enumerate ALL 2^n induced subsets S,
// compute |S|, m(S) = #edges inside S, tau(S) = |S| - alpha(S) (exact), and slack = 3|S| + 2 m(S) - 11 tau(S).
// Input (stdin): one line per hypergraph:  n E a1 b1 c1 a2 b2 c2 ...
// Output: global histogram over (s,m,tau) with count, first witness (line, mask); violations listed.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXS 27
#define MAXM 64
typedef unsigned long long u64;
static u64 cnt[MAXS][MAXM][MAXS];
static long wl[MAXS][MAXM][MAXS]; static uint32_t wm[MAXS][MAXM][MAXS];
int main(int argc,char**argv){
  int n,E; long line=0; u64 nviol=0, ntot=0; long minslack=1<<30;
  uint8_t *alpha=malloc(1<<26), *mc=malloc(1<<26); uint8_t *ind=malloc(1<<26);
  while(scanf("%d %d",&n,&E)==2){
    int ed[200][3];
    for(int i=0;i<E;i++) scanf("%d %d %d",&ed[i][0],&ed[i][1],&ed[i][2]);
    // per-vertex lists of (other two mask)
    uint32_t oth[32][64]; int no[32]; memset(no,0,sizeof no);
    for(int i=0;i<E;i++) for(int t=0;t<3;t++){
      int v=ed[i][t]; uint32_t o=0; for(int u=0;u<3;u++) if(u!=t) o|=1u<<ed[i][u];
      oth[v][no[v]++]=o; }
    uint32_t N=1u<<n;
    alpha[0]=0; mc[0]=0; ind[0]=1;
    for(uint32_t S=1;S<N;S++){
      int v=__builtin_ctz(S); uint32_t R=S&(S-1);
      int c=mc[R]; int in=ind[R];
      for(int j=0;j<no[v];j++) if((oth[v][j]&R)==oth[v][j]){c++; in=0;}
      mc[S]=c; ind[S]=in;
      int pc=__builtin_popcount(S);
      if(in) alpha[S]=pc;
      else { int best=0; uint32_t T=S; while(T){ int u=__builtin_ctz(T); T&=T-1; int a=alpha[S^(1u<<u)]; if(a>best){best=a; if(best==pc-1)break;} } alpha[S]=best; }
      int tau=pc-alpha[S]; int sl=3*pc+2*c-11*tau;
      if(sl<minslack) minslack=sl;
      if(cnt[pc][c][tau]==0){wl[pc][c][tau]=line; wm[pc][c][tau]=S;}
      cnt[pc][c][tau]++;
      if(sl<0){nviol++; if(nviol<=20) printf("VIOLATION line %ld mask %u s=%d m=%d tau=%d\n",line,S,pc,c,tau);}
    }
    ntot+=N; line++;
  }
  printf("{\"inputs\":%ld,\"subsets\":%llu,\"violations\":%llu,\"min_slack\":%ld,\"hist\":[\n",line,ntot,nviol,minslack);
  int first=1;
  for(int s=0;s<MAXS;s++)for(int m=0;m<MAXM;m++)for(int t=0;t<MAXS;t++) if(cnt[s][m][t]){
    printf("%s[%d,%d,%d,%llu,%ld,%u,%d]\n",first?"":",",s,m,t,cnt[s][m][t],wl[s][m][t],wm[s][m][t],3*s+2*m-11*t); first=0;}
  printf("]}\n");
  return 0;
}
