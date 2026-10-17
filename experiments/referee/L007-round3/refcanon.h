/* refcanon.h -- referee (L007 round 3) canonical form of a 3-graph by individualisation-refinement.
   No code shared with the prover/falsifier programs.  Vertices 0..n-1 (n<=16), edges as uint16 bitmasks.
   canon(): returns the lexicographically least sorted edge list over all leaves of the (unpruned)
   individualisation-refinement tree; *aut = number of leaves attaining it = |Aut(H)| (Aut acts freely and
   transitively on the leaves with the least certificate). */
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#define RMAXN 16
#define RMAXM 16
typedef struct { int n, m; uint16_t e[RMAXM]; } HG;

static int cmp_u16(const void *a, const void *b){ uint16_t x=*(const uint16_t*)a, y=*(const uint16_t*)b; return (x>y)-(x<y); }

/* signature compare helpers */
typedef struct { int v; uint16_t s[RMAXM+2]; } Sig;
static int sig_len;
static int cmp_sig(const void *a, const void *b){
  const Sig *x=a,*y=b; for(int i=0;i<sig_len;i++){ if(x->s[i]!=y->s[i]) return x->s[i]<y->s[i]?-1:1; } return 0; }

/* rerank arbitrary integer colours to 0..k-1 preserving order; returns k */
static int rerank(int n, int *col){
  int vals[RMAXN], nv=0;
  for(int v=0;v<n;v++){ int c=col[v], f=0; for(int i=0;i<nv;i++) if(vals[i]==c){f=1;break;} if(!f) vals[nv++]=c; }
  /* sort vals */
  for(int i=1;i<nv;i++){ int x=vals[i], j=i-1; while(j>=0 && vals[j]>x){ vals[j+1]=vals[j]; j--; } vals[j+1]=x; }
  for(int v=0;v<n;v++){ for(int i=0;i<nv;i++) if(vals[i]==col[v]){ col[v]=i; break; } }
  return nv;
}
/* one refinement pass; returns new number of cells */
static int refine_once(const HG *h, int *col){
  int n=h->n; Sig S[RMAXN]; sig_len=RMAXM+1;
  for(int v=0;v<n;v++){
    S[v].v=v; S[v].s[0]=(uint16_t)col[v]; int k=0; uint16_t pr[RMAXM];
    for(int i=0;i<h->m;i++) if(h->e[i]>>v&1){
      int o[2],t=0; for(int x=0;x<n;x++) if(x!=v && (h->e[i]>>x&1)) o[t++]=x;
      int a=col[o[0]], b=col[o[1]]; if(a>b){int z=a;a=b;b=z;}
      pr[k++]=(uint16_t)(a*RMAXN+b); }
    qsort(pr,k,sizeof(uint16_t),cmp_u16);
    for(int i=0;i<RMAXM;i++) S[v].s[1+i]= i<k ? pr[i] : 0xFFFF;
  }
  qsort(S,n,sizeof(Sig),cmp_sig);
  int c=0; col[S[0].v]=0;
  for(int i=1;i<n;i++){ if(cmp_sig(&S[i],&S[i-1])!=0) c++; col[S[i].v]=c; }
  return c+1;
}
static int refine(const HG *h, int *col){
  int k=rerank(h->n,col);
  for(;;){ int k2=refine_once(h,col); if(k2==k) return k; k=k2; }
}
typedef struct { uint16_t best[RMAXM]; int have; long long aut; long long leaves; } CanonState;
static void leaf(const HG *h, const int *col, CanonState *st){
  uint16_t c[RMAXM];
  for(int i=0;i<h->m;i++){ uint16_t b=0; for(int x=0;x<h->n;x++) if(h->e[i]>>x&1) b|=(uint16_t)(1u<<col[x]); c[i]=b; }
  qsort(c,h->m,sizeof(uint16_t),cmp_u16);
  st->leaves++;
  if(!st->have){ memcpy(st->best,c,sizeof(uint16_t)*h->m); st->have=1; st->aut=1; return; }

  int cmp=0; for(int i=0;i<h->m;i++){ if(c[i]!=st->best[i]){ cmp = c[i]<st->best[i]?-1:1; break; } }
  if(cmp<0){ memcpy(st->best,c,sizeof(uint16_t)*h->m); st->aut=1; }
  else if(cmp==0) st->aut++;
}
static void search(const HG *h, int *col, int k, CanonState *st){
  int n=h->n;
  if(k==n){ leaf(h,col,st); return; }
  if(st->leaves > 50000000LL){ fprintf(stderr,"canon: too many leaves\n"); exit(3); }
  /* target cell: least colour whose cell has >=2 vertices */
  int cnt[RMAXN]={0}; for(int v=0;v<n;v++) cnt[col[v]]++;
  int tc=-1; for(int c=0;c<k;c++) if(cnt[c]>=2){ tc=c; break; }
  for(int v=0;v<n;v++) if(col[v]==tc){
    int nc[RMAXN]; for(int u=0;u<n;u++) nc[u]=2*col[u]+1; nc[v]=2*col[v];
    int k2=refine(h,nc);
    search(h,nc,k2,st);
  }
}
/* canonical form: out->e sorted canonical edges; returns |Aut| */
static long long canon(const HG *h, HG *out){
  int col[RMAXN]; for(int v=0;v<h->n;v++) col[v]=0;
  int k=refine(h,col);
  CanonState st; st.have=0; st.aut=0; st.leaves=0;
  search(h,col,k,&st);
  out->n=h->n; out->m=h->m; memcpy(out->e,st.best,sizeof(uint16_t)*h->m);
  return st.aut;
}
