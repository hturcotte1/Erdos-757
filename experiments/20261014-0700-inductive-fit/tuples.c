// Q8 falsifier core: exact tau of trace clutter K, enumeration of deletion/avoidance states.
// Input (stdin): lines "id n m e1 ... em mode param seed"; edges are bitmasks (uint32), n<=31.
//  mode 0 (all): all 3^n states (digit 0=deleted from S,1=in D(avoided),2=in R); param unused.
//  mode 1 (small): S=full, all independent D with |D|<=param.
//  mode 2 (rand): param random states (random S (50%: full), random independent D greedy), seeded.
//  mode 3 (full2): S=full, all independent D (2^n loop).
// Output per case: "CASE id nstates" then "H name lo hi counts" for hist, "V ..." violation lines.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint32_t u32; typedef uint64_t u64;
static int n, m; static u32 E[64];
static u32 K[64]; static int nk;
static u32 cur[64];
static int best;
static inline int pc(u32 x){return __builtin_popcount(x);}
// recursive tau on array of sets (all must be hit)
static void rec(u32 *sets, int ns, int chosen){
  if(chosen>=best) return;
  if(ns==0){best=chosen;return;}
  // lower bound: greedy disjoint packing, smallest first (sets sorted by popcount on entry)
  u32 used=0; int lb=0;
  for(int i=0;i<ns;i++){ if(!(sets[i]&used)){used|=sets[i];lb++;} }
  if(chosen+lb>=best) return;
  // choose smallest set (sets[0] after sort)
  u32 s=sets[0];
  u32 nxt[64];
  // order branching vertices by frequency
  int cand[32],nc=0; 
  for(int v=0;v<n;v++) if(s>>v&1) cand[nc++]=v;
  u32 excl=0; // vertices already branched (don't use in later branches: standard trick)
  for(int c=0;c<nc;c++){
    int v=cand[c]; int k=0;
    for(int i=0;i<ns;i++){ if(!(sets[i]>>v&1)){ nxt[k++]=sets[i]&~excl; } }
    // remove vertices excluded from sets (they're forbidden): a set may become empty => infeasible
    int bad=0; for(int i=0;i<k;i++) if(!nxt[i]){bad=1;break;}
    if(!bad){
      // sort by popcount (insertion)
      for(int i=1;i<k;i++){u32 x=nxt[i];int j=i-1;while(j>=0&&pc(nxt[j])>pc(x)){nxt[j+1]=nxt[j];j--;}nxt[j+1]=x;}
      rec(nxt,k,chosen+1);
    }
    excl|=1u<<v;
  }
}
static int tau_of(u32 *sets,int ns){
  if(ns==0) return 0;
  u32 tmp[64]; memcpy(tmp,sets,ns*sizeof(u32));
  for(int i=1;i<ns;i++){u32 x=tmp[i];int j=i-1;while(j>=0&&pc(tmp[j])>pc(x)){tmp[j+1]=tmp[j];j--;}tmp[j+1]=x;}
  // greedy upper bound
  u32 rem[64]; int nr=ns; memcpy(rem,tmp,ns*sizeof(u32)); int g=0;
  while(nr){ int cnt[32]={0}; for(int i=0;i<nr;i++)for(int v=0;v<n;v++)if(rem[i]>>v&1)cnt[v]++;
    int bv=0;for(int v=1;v<n;v++)if(cnt[v]>cnt[bv])bv=v; int k=0;for(int i=0;i<nr;i++)if(!(rem[i]>>bv&1))rem[k++]=rem[i]; nr=k; g++; }
  best=g+1; rec(tmp,ns,0); return best>g?g:best;
}
typedef struct {int tau,e1,e2,e3,Rfull,Ract,Rinc;} Res;
static void evalstate(u32 S,u32 D,Res*r){
  u32 tr[64]; int nt=0;
  for(int i=0;i<m;i++) if((E[i]&S)==E[i]) tr[nt++]=E[i]&~D;
  // dedupe + minimal
  nk=0; u32 inc=0;
  for(int i=0;i<nt;i++){ inc|=tr[i];
    int keep=1;
    for(int j=0;j<nt&&keep;j++){ if(j==i) continue;
      if((tr[j]&tr[i])==tr[j]){ // tr[j] subset of tr[i]
        if(tr[j]!=tr[i]) keep=0; else if(j<i) keep=0; } }
    if(keep) K[nk++]=tr[i]; }
  u32 act=0; r->e1=r->e2=r->e3=0;
  for(int i=0;i<nk;i++){act|=K[i]; int p=pc(K[i]); if(p==1)r->e1++; else if(p==2)r->e2++; else r->e3++;}
  r->tau=tau_of(K,nk);
  r->Rfull=pc(S&~D); r->Ract=pc(act); r->Rinc=pc(inc);
}
static int indep(u32 D){ for(int i=0;i<m;i++) if((E[i]&D)==E[i]) return 0; return 1; }
#define HO 300
#define HN 700
static u64 hQ[HN],hA[HN],hD[HN]; static u64 nst,nviolQ,nviolA,nviolD,neqQ;
static int caseid; static int vcap;
static long vprinted;
#define TH 1<<16
typedef struct {int used,tau,R,e2,e1,nS,dsz; u64 cnt; u32 S,D;} Ent;
static Ent tab[TH];
static void record(u32 S,u32 D){
  Res r; evalstate(S,D,&r); nst++;
  u32 key=(r.tau*31u+r.Rfull)*31u+r.e2; key=key*131u+r.e1; key=(key*2654435761u)>>8; key&=(TH)-1;
  while(tab[key].used && !(tab[key].tau==r.tau&&tab[key].R==r.Rfull&&tab[key].e2==r.e2&&tab[key].e1==r.e1)) key=(key+1)&((TH)-1);
  Ent*t=&tab[key];
  int dsz=pc(D);
  if(!t->used){t->used=1;t->tau=r.tau;t->R=r.Rfull;t->e2=r.e2;t->e1=r.e1;t->cnt=0;t->nS=pc(S);t->dsz=dsz;t->S=S;t->D=D;}
  else if(dsz<t->dsz){t->nS=pc(S);t->dsz=dsz;t->S=S;t->D=D;}
  t->cnt++;
}
static u64 rs;
static inline u64 rnd(){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static void comb(u32 S,u32 D,int start,int left){
  record(S,D);
  if(!left) return;
  for(int v=start;v<n;v++) if(S>>v&1){ u32 D2=D|1u<<v; if(indep(D2)) comb(S,D2,v+1,left-1); }
}
int main(int argc,char**argv){
  vcap = argc>1?atoi(argv[1]):1000;
  int id,mode,param; u64 seed;
  while(scanf("%d %d %d",&id,&n,&m)==3){
    for(int i=0;i<m;i++){unsigned x;scanf("%u",&x);E[i]=x;}
    scanf("%d %d %llu",&mode,&param,(unsigned long long*)&seed);
    caseid=id; nst=nviolQ=nviolA=nviolD=neqQ=0; vprinted=0; memset(hQ,0,sizeof hQ);memset(hA,0,sizeof hA);memset(hD,0,sizeof hD);
    u32 full = n==32?0xffffffffu:((1u<<n)-1);
    if(mode==0){
      u64 tot=1; for(int i=0;i<n;i++) tot*=3;
      int dig[32]; memset(dig,0,sizeof dig); u32 S=0,D=0;
      for(u64 c=0;c<tot;c++){
        // digits maintained incrementally
        if(c){ int i=0; while(dig[i]==2){dig[i]=0; S&=~(1u<<i); D&=~(1u<<i); i++;} dig[i]++; if(dig[i]==1){S|=1u<<i;D|=1u<<i;} else {D&=~(1u<<i);} }
        // dig: 0 out,1 D,2 R
        if(indep(D)) record(S,D);
      }
    } else if(mode==1){ comb(full,0,0,param); }
    else if(mode==3){ for(u64 D=0; D<=(u64)full; D++) if(indep((u32)D)) record(full,(u32)D); }
    else { rs=seed*2654435761ULL+88172645463325252ULL; for(int i=0;i<10;i++)rnd();
      for(int t=0;t<param;t++){
        u32 S=full; if(rnd()&1){ int p=rnd()%30; for(int v=0;v<n;v++) if((rnd()%100)<(unsigned)p) S&=~(1u<<v);} 
        int target=rnd()%(n+1); int perm[32]; for(int i=0;i<n;i++)perm[i]=i;
        for(int i=n-1;i>0;i--){int j=rnd()%(i+1);int x=perm[i];perm[i]=perm[j];perm[j]=x;}
        u32 D=0; int sz=0; for(int i=0;i<n&&sz<target;i++){int v=perm[i]; if(!(S>>v&1))continue; if(indep(D|1u<<v)){D|=1u<<v;sz++;}}
        record(S,D);
      } }
    printf("CASE %d states=%llu\n",id,(unsigned long long)nst);
    for(int i=0;i<TH;i++) if(tab[i].used){ Ent*t=&tab[i]; printf("T %d %d %d %d %d %d %d %llu %u %u\n",id,t->tau,t->R,t->e2,t->e1,t->nS,t->dsz,(unsigned long long)t->cnt,t->S,t->D); }
    memset(tab,0,sizeof tab);
    fflush(stdout);
  }
}
