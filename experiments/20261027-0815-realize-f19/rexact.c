/* rexact.c -- C port of rexact.py: complete decision procedure for "is the 3-graph the AP hypergraph (up to extra forced APs) of a (4,5)-set".
   Backtracking over injective midpoint labellings; at each node the solution space V of {x_a + x_c = 2 x_mid} is computed by RREF mod p = 2^61-1.
   All matrix entries are small integers (rows (1,1,-2) / forms with <= 4 entries of size 1..2), n <= 32, so every minor is bounded by
   Hadamard by (sqrt(6))^19 ~ 2.4e7 << p (and by < p for the forms): rank, nullspace and the zero-test of any form over Z_p coincide with those
   over Q (a rational with numerator < p in absolute value that is 0 mod p is 0).  Hence "form forced to 0 on V" is decided EXACTLY.
   Pruning events (all necessary for a (4,5)-set): EQ (r_a=r_b), SIDON (r_a+r_b=r_c+r_d, {a,b}!={c,d}), NONLIN (two forced 3-APs sharing 2 points).
   A leaf with no event is realizable (generic point of V is a (4,5)-set; this is re-verified in Python on integers for every REAL output).
   usage: rexact N [all] < lines    prints per graph:  RES idx REAL|NOT nodes leaves   (+ 'LAB (a,mid,c) ...' for the first realization) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned long long u64;
static const u64 PR = 2305843009213693951ULL;
static inline u64 mulm(u64 a, u64 b){ unsigned __int128 z=(unsigned __int128)a*b; u64 lo=(u64)(z&PR), hi=(u64)(z>>61); u64 r=lo+hi; if(r>=PR) r-=PR; return r; }
static inline u64 addm(u64 a,u64 b){ u64 r=a+b; if(r>=PR) r-=PR; return r; }
static inline u64 subm(u64 a,u64 b){ return a>=b? a-b : a+PR-b; }
static u64 powm(u64 a,u64 e){ u64 r=1; while(e){ if(e&1) r=mulm(r,a); a=mulm(a,a); e>>=1;} return r; }
#define MAXN 33
#define MAXE 40
#define MAXK 34
static int n, m, ed[MAXE][3], ordr[MAXE], ALL=0;
typedef struct { int rank; u64 R[MAXN][MAXN]; int piv[MAXN]; } Sp;   /* RREF rows */
static Sp stk[MAXE+2];
static int lab[MAXE][3], usedmid[MAXN];
static unsigned long long nodes, leaves;
static int stop, capped; static unsigned long long NODECAP=0;
static int addrow(const Sp*s, Sp*t, const int*coef){   /* coef[0..n-1] small ints (may be negative) */
    u64 row[MAXN]; for(int j=0;j<n;j++){ int c=coef[j]; row[j]= c>=0? (u64)c : PR-(u64)(-c); }
    *t=*s;
    for(int i=0;i<t->rank;i++){ int c=t->piv[i]; u64 f=row[c]; if(f){ for(int j=0;j<n;j++) row[j]=subm(row[j],mulm(f,t->R[i][j])); } }
    int c=-1; for(int j=0;j<n;j++) if(row[j]){ c=j; break; }
    if(c<0) return 0;
    u64 inv=powm(row[c],PR-2); for(int j=0;j<n;j++) row[j]=mulm(row[j],inv);
    for(int i=0;i<t->rank;i++){ u64 f=t->R[i][c]; if(f) for(int j=0;j<n;j++) t->R[i][j]=subm(t->R[i][j],mulm(f,row[j])); }
    memcpy(t->R[t->rank],row,sizeof(u64)*n); t->piv[t->rank]=c; t->rank++; return 1;
}
static int K; static u64 C[MAXN][MAXK];
static void coords(const Sp*s){
    int isp[MAXN]={0}; for(int i=0;i<s->rank;i++) isp[s->piv[i]]=1;
    int fr[MAXN], nf=0; for(int j=0;j<n;j++) if(!isp[j]) fr[nf++]=j; K=nf;
    for(int v=0;v<n;v++) for(int k=0;k<K;k++) C[v][k]=0;
    for(int k=0;k<K;k++) C[fr[k]][k]=1;
    for(int i=0;i<s->rank;i++){ int c=s->piv[i]; for(int k=0;k<K;k++) C[c][k]= (PR - s->R[i][fr[k]])%PR; }
}
typedef struct { u64 v[MAXK]; int a,c; } Ps;
static Ps ps[MAXN*MAXN/2]; static int nps;
static int cmpps(const void*x,const void*y){ const Ps*p=x,*q=y; for(int k=0;k<K;k++){ if(p->v[k]!=q->v[k]) return p->v[k]<q->v[k]?-1:1; } return 0; }
static int findps(const u64*vec){ int lo=0,hi=nps-1; while(lo<=hi){ int mid=(lo+hi)/2; int cmp=0; for(int k=0;k<K;k++){ if(ps[mid].v[k]!=vec[k]){ cmp= ps[mid].v[k]<vec[k]?-1:1; break; } } if(!cmp) return mid; if(cmp<0) lo=mid+1; else hi=mid-1; } return -1; }
/* returns 0 ok, 1 EQ, 2 SIDON, 3 NONLIN */
static int events(void){
    for(int a=0;a<n;a++) for(int b=a+1;b<n;b++){ int eq=1; for(int k=0;k<K;k++) if(C[a][k]!=C[b][k]){eq=0;break;} if(eq) return 1; }
    nps=0; for(int a=0;a<n;a++) for(int c=a+1;c<n;c++){ for(int k=0;k<K;k++) ps[nps].v[k]=addm(C[a][k],C[c][k]); ps[nps].a=a; ps[nps].c=c; nps++; }
    qsort(ps,nps,sizeof(Ps),cmpps);
    for(int i=1;i<nps;i++) if(cmpps(&ps[i-1],&ps[i])==0) return 2;
    int F[MAXN][3], nf=0;
    for(int b=0;b<n;b++){ u64 vec[MAXK]; for(int k=0;k<K;k++) vec[k]=addm(C[b][k],C[b][k]); int i=findps(vec); if(i>=0){ F[nf][0]=ps[i].a; F[nf][1]=b; F[nf][2]=ps[i].c; nf++; } }
    for(int i=0;i<nf;i++) for(int j=i+1;j<nf;j++){ int sh=0; for(int x=0;x<3;x++) for(int y=0;y<3;y++) if(F[i][x]==F[j][y]) sh++; if(sh>=2) return 3; }
    return 0;
}
static int found_lab[MAXE][3], foundk;
static void rec(int k){
    if(stop) return;
    if(NODECAP && nodes>NODECAP){ capped=1; stop=1; return; }
    if(k==m){ leaves++; if(!foundk){ memcpy(found_lab,lab,sizeof(lab)); foundk=1; } if(!ALL) stop=1; return; }
    int e=ordr[k];
    for(int t=0;t<3;t++){
        int mid=ed[e][t]; if(usedmid[mid]) continue;
        int a=-1,c=-1; for(int s=0;s<3;s++) if(s!=t){ if(a<0) a=ed[e][s]; else c=ed[e][s]; }
        int coef[MAXN]; for(int j=0;j<n;j++) coef[j]=0; coef[a]+=1; coef[c]+=1; coef[mid]-=2;
        Sp*cur=&stk[k]; Sp*nx=&stk[k+1]; addrow(cur,nx,coef); nodes++;
        coords(nx); if(events()) continue;
        usedmid[mid]=1; lab[e][0]=a; lab[e][1]=mid; lab[e][2]=c;
        rec(k+1); usedmid[mid]=0; if(stop) return;
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); if(argc>2 && !strcmp(argv[2],"all")) ALL=1; if(getenv("NODECAP")) NODECAP=strtoull(getenv("NODECAP"),0,10);
    char*line=NULL; size_t cap=0; int idx=0;
    while(getline(&line,&cap,stdin)>0){
        if(strncmp(line,"FOUND:",6)) continue;
        m=0; char*p=line+6; int a,b,c,nc;
        while(sscanf(p," (%d,%d,%d)%n",&a,&b,&c,&nc)==3){ ed[m][0]=a; ed[m][1]=b; ed[m][2]=c; m++; p+=nc; }
        /* order: greedy max overlap with covered vertices, ties smaller index (as rexact.py) */
        int done[MAXE]={0}; unsigned long long cov=0;
        for(int k=0;k<m;k++){ int best=-1,bs=-1; for(int i=0;i<m;i++) if(!done[i]){ int s=0; for(int x=0;x<3;x++) if(cov>>ed[i][x]&1) s++; if(s>bs){bs=s;best=i;} } ordr[k]=best; done[best]=1; for(int x=0;x<3;x++) cov|=1ULL<<ed[best][x]; }
        memset(&stk[0],0,sizeof(Sp)); memset(usedmid,0,sizeof(usedmid)); nodes=leaves=0; stop=0; foundk=0; capped=0;
        rec(0);
        printf("RES %d %s %llu %llu\n",idx,leaves?"REAL":(capped?"CAP":"NOT"),nodes,leaves);
        if(foundk){ printf("LAB"); for(int i=0;i<m;i++) printf(" (%d,%d,%d)",found_lab[i][0],found_lab[i][1],found_lab[i][2]); printf("\n"); }
        fflush(stdout); idx++;
    }
    return 0;
}
