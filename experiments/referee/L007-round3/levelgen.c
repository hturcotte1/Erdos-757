/* levelgen.c -- referee (L007 round 3): level-wise isomorph-free generation of CONNECTED LINEAR 3-graphs.
   Different algorithm from the canonical-growth DFS of the proof (Lemma D): every connected H has an edge order
   e1..eM in which each edge meets the union of the earlier ones; every prefix P_k is connected, linear, has
   |V(P_k)| <= N, |V(P_k)| + 2(M-k) >= N, tau(P_k) >= tau(H)-(M-k), Delta(P_k) <= Delta(H), and is F7-free if H is.
   Level k keeps ONE representative (canonical form, refcanon.h) of every isomorphism class of such P_k; level k+1
   is obtained by adding to each representative every edge that meets its vertex set (0, 1 or 2 new vertices,
   labelled n, n+1), keeping linearity, and deduplicating by canonical form.  So level M contains every class.
   Usage: levelgen N M T0 DMAX F7PRUNE PRINT       (F7PRUNE=1: discard graphs containing F7 at every level)
   Output: per-level class counts, final classes (with |Aut| and labelled count N!/|Aut|) if PRINT. */
#include "refcanon.h"
static int N,M,T0,DMAX,F7P,PRINT;
/* ---------- hash set of graphs ---------- */
typedef struct { HG *a; long long n, cap; long long *tab; long long tcap; long long *autv; } Set;
static uint64_t hhash(const HG *g){ uint64_t h=1469598103934665603ULL^(uint64_t)g->n; for(int i=0;i<g->m;i++){ h^=g->e[i]; h*=1099511628211ULL; } return h^(h>>29); }
static int heq(const HG *x,const HG *y){ if(x->n!=y->n||x->m!=y->m) return 0; for(int i=0;i<x->m;i++) if(x->e[i]!=y->e[i]) return 0; return 1; }
static void set_init(Set *s){ s->cap=1024; s->n=0; s->a=malloc(sizeof(HG)*s->cap); s->autv=malloc(sizeof(long long)*s->cap); s->tcap=4096; s->tab=malloc(sizeof(long long)*s->tcap); for(long long i=0;i<s->tcap;i++) s->tab[i]=-1; }
static void set_rehash(Set *s){ s->tcap*=2; free(s->tab); s->tab=malloc(sizeof(long long)*s->tcap); for(long long i=0;i<s->tcap;i++) s->tab[i]=-1;
  for(long long j=0;j<s->n;j++){ uint64_t h=hhash(&s->a[j])&(s->tcap-1); while(s->tab[h]>=0) h=(h+1)&(s->tcap-1); s->tab[h]=j; } }
static int set_add(Set *s,const HG *g,long long aut){
  uint64_t h=hhash(g)&(s->tcap-1);
  while(s->tab[h]>=0){ if(heq(&s->a[s->tab[h]],g)) return 0; h=(h+1)&(s->tcap-1); }
  if(s->n==s->cap){ s->cap*=2; s->a=realloc(s->a,sizeof(HG)*s->cap); s->autv=realloc(s->autv,sizeof(long long)*s->cap); }
  s->a[s->n]=*g; s->autv[s->n]=aut; s->tab[h]=s->n; s->n++;
  if(2*s->n > s->tcap) set_rehash(s);
  return 1; }
/* ---------- tau ---------- */
static int hit_le(const uint16_t *e,int m,uint32_t unc,int k){
  if(!unc) return 1;
  if(k<=0) return 0;
  int i=__builtin_ctz(unc);
  for(int x=0;x<16;x++) if(e[i]>>x&1){ uint32_t u2=unc; for(int j=0;j<m;j++) if((u2>>j&1)&&(e[j]>>x&1)) u2&=~(1u<<j); if(hit_le(e,m,u2,k-1)) return 1; }
  return 0; }
static int tau_ge(const HG *g,int t){ if(t<=0) return 1; return !hit_le(g->e,g->m,(1u<<g->m)-1,t-1); }
/* ---------- F7 via canonical form ---------- */
static HG F7c;
static void make_f7(void){ HG f; f.n=7; f.m=5; int E[5][3]={{0,1,2},{0,3,4},{0,5,6},{1,3,5},{2,4,6}}; for(int i=0;i<5;i++) f.e[i]=(1u<<E[i][0])|(1u<<E[i][1])|(1u<<E[i][2]); canon(&f,&F7c); }
/* does g contain F7 using edge index 'last'? (all 5-subsets containing 'last') */
static int f7_with(const HG *g,int last){
  int m=g->m, idx[RMAXM], t=0; for(int i=0;i<m;i++) if(i!=last) idx[t++]=i;
  for(int a=0;a<t;a++) for(int b=a+1;b<t;b++) for(int c=b+1;c<t;c++) for(int d=c+1;d<t;d++){
    uint16_t ee[5]={g->e[last],g->e[idx[a]],g->e[idx[b]],g->e[idx[c]],g->e[idx[d]]};
    uint16_t u=0; for(int i=0;i<5;i++) u|=ee[i]; if(__builtin_popcount(u)!=7) continue;
    int map[16],k=0; for(int x=0;x<16;x++) map[x]=-1; for(int x=0;x<16;x++) if(u>>x&1) map[x]=k++;
    HG s,cs; s.n=7; s.m=5; for(int i=0;i<5;i++){ uint16_t b=0; for(int x=0;x<16;x++) if(ee[i]>>x&1) b|=(uint16_t)(1u<<map[x]); s.e[i]=b; }
    canon(&s,&cs); if(heq(&cs,&F7c)) return 1; }
  return 0; }
int main(int argc,char**argv){
  if(argc<7){ fprintf(stderr,"usage\n"); return 1; }
  N=atoi(argv[1]); M=atoi(argv[2]); T0=atoi(argv[3]); DMAX=atoi(argv[4]); F7P=atoi(argv[5]); PRINT=atoi(argv[6]);
  make_f7();
  Set cur; set_init(&cur);
  HG g0; g0.n=3; g0.m=1; g0.e[0]=7;
  if(!(3<=N && 3+2*(M-1)>=N && tau_ge(&g0,T0-(M-1)) && DMAX>=1)){ printf("level 1: 0\nFINAL N=%d M=%d T0=%d DMAX=%d F7PRUNE=%d classes=0 labelled=0\n",N,M,T0,DMAX,F7P); return 0; }
  { HG c; long long a=canon(&g0,&c); set_add(&cur,&c,a); }
  printf("level 1: %lld\n",cur.n); fflush(stdout);
  for(int k=1;k<M;k++){
    Set nxt; set_init(&nxt); long long cand=0;
    int r=M-(k+1);
    for(long long j=0;j<cur.n;j++){
      const HG *P=&cur.a[j]; int n=P->n;
      int deg[16]={0}; uint16_t nb[16]={0};
      for(int i=0;i<P->m;i++) for(int x=0;x<16;x++) if(P->e[i]>>x&1){ deg[x]++; nb[x]|=P->e[i]; }
      for(int x=0;x<16;x++) nb[x]&=~(uint16_t)(1u<<x);
      /* candidate new edges {a<b<c}: type 0 all old; type 1 {a,b,n}; type 2 {a,n,n+1} */
      int trip[2000][3], nt=0;
      if(n+2*r>=N) for(int a=0;a<n;a++) for(int b=a+1;b<n;b++) for(int c=b+1;c<n;c++){ trip[nt][0]=a; trip[nt][1]=b; trip[nt][2]=c; nt++; }
      if(n+1<=N && n+1+2*r>=N) for(int a=0;a<n;a++) for(int b=a+1;b<n;b++){ trip[nt][0]=a; trip[nt][1]=b; trip[nt][2]=n; nt++; }
      if(n+2<=N && n+2+2*r>=N) for(int a=0;a<n;a++){ trip[nt][0]=a; trip[nt][1]=n; trip[nt][2]=n+1; nt++; }
      for(int t=0;t<nt;t++){
        int a=trip[t][0], b=trip[t][1], c=trip[t][2];
        int nn = (c>=n) + (b>=n);
        if(deg[a]>=DMAX) continue;
        if(b<n && (deg[b]>=DMAX || ((nb[a]>>b)&1))) continue;
        if(c<n && (deg[c]>=DMAX || ((nb[a]>>c)&1) || ((nb[b]>>c)&1))) continue;
        HG Q=*P; Q.e[Q.m++]=(uint16_t)((1u<<a)|(1u<<b)|(1u<<c)); Q.n=n+nn;
        cand++;
        if(!tau_ge(&Q,T0-r)) continue;
        if(F7P && f7_with(&Q,Q.m-1)) continue;
        HG C; long long au=canon(&Q,&C); set_add(&nxt,&C,au);
      }
    }
    printf("level %d: candidates=%lld classes=%lld\n",k+1,cand,nxt.n); fflush(stdout);
    free(cur.a); free(cur.tab); free(cur.autv); cur=nxt;
  }
  /* final checks */
  long double lab=0; long long ok=0;
  for(long long j=0;j<cur.n;j++){ HG *g=&cur.a[j]; if(g->n!=N || g->m!=M || !tau_ge(g,T0)) { printf("BAD final graph\n"); return 2; }
    long double f=1; for(int i=2;i<=N;i++) f*=i; lab+=f/cur.autv[j]; ok++;
    if(PRINT){ int t=0; while(tau_ge(g,t+1)) t++; int dmax=0; for(int x=0;x<16;x++){ int d=0; for(int i=0;i<g->m;i++) if(g->e[i]>>x&1) d++; if(d>dmax) dmax=d; }
      printf("CLASS aut=%lld tau=%d maxdeg=%d :",cur.autv[j],t,dmax); for(int i=0;i<g->m;i++){ printf(" ("); int f1=1; for(int x=0;x<16;x++) if(g->e[i]>>x&1){ printf(f1?"%d":",%d",x); f1=0; } printf(")"); } printf("\n"); } }
  printf("FINAL N=%d M=%d T0=%d DMAX=%d F7PRUNE=%d classes=%lld labelled=%.0Lf\n",N,M,T0,DMAX,F7P,ok,lab);
  return 0; }
