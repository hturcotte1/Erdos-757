// random + local search over connected class-C 3-graphs with n vertices, m edges; objective: maximise tau (minimise slack)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "tau.c"
#define MAXN 40
#define MAXM 40
static u64 rs=88172645463325252ULL;
static inline u64 rnd(){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static inline int rint_(int k){ return (int)(rnd()%(u64)k); }
static double runif(){ return (rnd()>>11)*(1.0/9007199254740992.0); }

typedef struct { int n,m; int e[MAXM][3]; } G;

static int hall_ok(const G*g){
    int n=g->n,m=g->m;
    int mv[MAXN]; int vis[MAXN];
    for(int x=0;x<n;x++) for(int y=x+1;y<n;y++){
        for(int v=0;v<n;v++) mv[v]=-1;
        for(int i=0;i<m;i++){
            // iterative-free recursive Kuhn
            memset(vis,0,sizeof(int)*n);
            vis[x]=1; vis[y]=1;
            // dfs
            int stack_e[MAXM*4], stack_k[MAXM*4]; int sp=0;
            // use recursion via function pointer substitute: implement recursion with local function
            // simple recursive lambda-free approach:
            int ok=0;
            // recursive via nested function (gcc extension)
            int try_(int ei){
                for(int k=0;k<3;k++){ int v=g->e[ei][k]; if(vis[v]) continue; vis[v]=1;
                    if(mv[v]<0 || try_(mv[v])){ mv[v]=ei; return 1; } }
                return 0; }
            (void)stack_e;(void)stack_k;(void)sp;
            ok=try_(i);
            if(!ok) return 0;
        }
    }
    return 1;
}
static int has_f7(const G*g){
    int n=g->n,m=g->m;
    for(int x=0;x<n;x++){
        int ix[MAXM],c=0;
        for(int i=0;i<m;i++) if(g->e[i][0]==x||g->e[i][1]==x||g->e[i][2]==x) ix[c++]=i;
        if(c<3) continue;
        for(int a=0;a<c;a++)for(int b=a+1;b<c;b++)for(int d=b+1;d<c;d++){
            int p[3][2]; int idx[3]={ix[a],ix[b],ix[d]};
            for(int t=0;t<3;t++){int q=0; for(int k=0;k<3;k++) if(g->e[idx[t]][k]!=x) p[t][q++]=g->e[idx[t]][k];}
            for(int ch=0;ch<8;ch++){
                u64 t1=0,t2=0;
                for(int t=0;t<3;t++){ int c1=(ch>>t)&1; t1|=1ULL<<p[t][c1]; t2|=1ULL<<p[t][1-c1]; }
                int f1=0,f2=0;
                for(int i=0;i<m;i++){ u64 mk=(1ULL<<g->e[i][0])|(1ULL<<g->e[i][1])|(1ULL<<g->e[i][2]); if(mk==t1)f1=1; if(mk==t2)f2=1; }
                if(f1&&f2) return 1;
            }
        }
    }
    return 0;
}
#define FIND(x) ({int _x=(x); while(p[_x]!=_x){p[_x]=p[p[_x]];_x=p[_x];} _x;})
static int connected_all(const G*g){
    int n=g->n; int p[MAXN]; for(int i=0;i<n;i++)p[i]=i;
    for(int i=0;i<g->m;i++){ int a=FIND(g->e[i][0]),b=FIND(g->e[i][1]); p[a]=b; int c=FIND(g->e[i][2]); b=FIND(g->e[i][1]); p[c]=b; }
    int r=FIND(0); for(int v=1;v<n;v++) if(FIND(v)!=r) return 0;
    return 1;
}
static int linear_ok(const G*g){
    static unsigned char pr[MAXN][MAXN]; memset(pr,0,sizeof pr);
    for(int i=0;i<g->m;i++) for(int a=0;a<3;a++) for(int b=a+1;b<3;b++){
        int x=g->e[i][a],y=g->e[i][b]; if(pr[x][y]) return 0; pr[x][y]=pr[y][x]=1; }
    return 1;
}
static int classC(const G*g){ return linear_ok(g) && !has_f7(g) && hall_ok(g); }
static int gtau(const G*g){
    int flat[3*MAXM]; for(int i=0;i<g->m;i++) for(int k=0;k<3;k++) flat[3*i+k]=g->e[i][k];
    return tau_induced(g->m,flat,~0ULL);
}

// ---- seeded growth ----
static int nseed=0; static int seed_n[400], seed_m[400]; static int seed_e[400][MAXM][3];
static void load_seeds(const char*fn){
    FILE*f=fopen(fn,"r"); if(!f) return; char line[8192];
    while(fgets(line,sizeof line,f)){
        int n,m,off; if(sscanf(line,"%d %d %n",&n,&m,&off)<2) continue;
        if(m>MAXM) continue;
        seed_n[nseed]=n; seed_m[nseed]=m; char*p=line+off; int i=0;
        while(i<m){ int a,b,c,adv; if(sscanf(p,"%d,%d,%d%n",&a,&b,&c,&adv)<3) break; seed_e[nseed][i][0]=a;seed_e[nseed][i][1]=b;seed_e[nseed][i][2]=c; i++; p+=adv; if(*p==';')p++; }
        nseed++; if(nseed>=400) break;
    }
    fclose(f);
}
static int grow_seeded(G*g,int n,int m){
    int ns=1+rint_(4); int used=0; g->n=n; g->m=0;
    for(int s=0;s<ns;s++){
        int k=rint_(nseed);
        if(used+seed_n[k]>n || g->m+seed_m[k]>m) continue;
        for(int i=0;i<seed_m[k];i++){ for(int t=0;t<3;t++) g->e[g->m][t]=seed_e[k][i][t]+used; g->m++; }
        used+=seed_n[k];
    }
    if(g->m==0) return 0;
    // add edges
    int guard=0;
    while(g->m<m && guard<2000){
        guard++;
        int p[MAXN]; for(int i=0;i<n;i++)p[i]=i;
        for(int i=0;i<g->m;i++){ int a=FIND(g->e[i][0]),b=FIND(g->e[i][1]); p[a]=b; int c=FIND(g->e[i][2]); b=FIND(g->e[i][1]); p[c]=b; }
        int a=rint_(n); int b,c; int tries=0;
        do{ b=rint_(n); tries++; }while((b==a||FIND(b)==FIND(a)) && tries<30);
        tries=0;
        do{ c=rint_(n); tries++; }while((c==a||c==b||FIND(c)==FIND(a)||FIND(c)==FIND(b)) && tries<30);
        if(a==b||a==c||b==c) continue;
        g->e[g->m][0]=a;g->e[g->m][1]=b;g->e[g->m][2]=c; g->m++;
        if(!classC(g)) g->m--;
    }
    return g->m==m && connected_all(g);
}
static long nsamples=0;
// random constructive growth
static int grow(G*g,int n,int m){
    g->n=n; g->m=1; g->e[0][0]=0;g->e[0][1]=1;g->e[0][2]=2; int used=3;
    for(int i=1;i<m;i++){
        int R=n-used, r=m-i; // r edges remain including this one
        int placed=0;
        for(int tries=0;tries<60 && !placed;tries++){
            // feasible k
            int lo=R-2*(r-1); if(lo<0) lo=0; int hi=R<2?R:2;
            if(lo>hi) return 0;
            int k=lo+rint_(hi-lo+1);
            int ed[3]; int c=0;
            int bad=0;
            for(int t=0;t<3-k;t++){
                int v; int guard=0; do{ v=rint_(used); guard++; int dup=0; for(int q=0;q<c;q++) if(ed[q]==v) dup=1; if(!dup) break; }while(guard<20);
                ed[c++]=v;
            }
            for(int q=0;q<c;q++)for(int s=q+1;s<c;s++) if(ed[q]==ed[s]) bad=1;
            if(bad) continue;
            for(int t=0;t<k;t++) ed[c++]=used+t;
            memcpy(g->e[g->m],ed,sizeof ed); g->m++;
            if(classC(g)){ used+=k; placed=1; } else g->m--;
        }
        if(!placed) return 0;
    }
    return used==n && connected_all(g);
}
#ifndef LIB
int main(int argc,char**argv){
    int n=atoi(argv[1]), m=atoi(argv[2]); long target=atol(argv[3]); long steps=atol(argv[4]); rs^=(u64)atol(argv[5])*0x9E3779B97F4A7C15ULL; for(int i=0;i<10;i++)rnd();
    double T=argc>6?atof(argv[6]):0.5; double pseed=argc>7?atof(argv[7]):0.0; if(argc>8) load_seeds(argv[8]); if(nseed==0) pseed=0;
    int bestTau=-1; long hist[64]; memset(hist,0,sizeof hist); long grown=0, growfail=0, saved=0;
    while(nsamples<target){
        G g; int okg=(runif()<pseed)? grow_seeded(&g,n,m): grow(&g,n,m); if(!okg){ growfail++; if(growfail>200000 && grown==0){ printf("RESULT n=%d m=%d GROWTH_FAILED fail=%ld\n",n,m,growfail); return 0;} continue; }
        grown++; nsamples++;
        int t=gtau(&g); hist[t]++; if(t>bestTau){bestTau=t;}
        for(long s=0;s<steps && nsamples<target;s++){
            G h=g;
            int i=rint_(h.m);
            int mv=rint_(2);
            if(mv==0){ // replace a vertex in edge i
                int k=rint_(3); int v=rint_(n);
                h.e[i][k]=v;
            } else { // replace whole edge by random triple sharing >=1 vertex with some other
                int a=rint_(n),b=rint_(n),c=rint_(n); h.e[i][0]=a;h.e[i][1]=b;h.e[i][2]=c;
            }
            if(h.e[i][0]==h.e[i][1]||h.e[i][0]==h.e[i][2]||h.e[i][1]==h.e[i][2]) continue;
            if(!linear_ok(&h)) continue;
            if(!connected_all(&h)) continue;
            if(has_f7(&h)) continue;
            if(!hall_ok(&h)) continue;
            nsamples++;
            int t2=gtau(&h); hist[t2]++;
            if(t2>bestTau) bestTau=t2;
            int cur=gtau(&g);
            if(t2>=cur || runif()<exp((t2-cur)/T)){ g=h; }
            int sl=3*n+2*m-11*t2;
            if(sl<=1 && saved<5000){ saved++; printf("SAVE n=%d m=%d slack=%d tau=%d E=",n,m,sl,t2); for(int q=0;q<h.m;q++) printf("%d,%d,%d;",h.e[q][0],h.e[q][1],h.e[q][2]); printf("\n"); }
        }
    }
    printf("RESULT n=%d m=%d samples=%ld grown=%ld growfail=%ld bestTau=%d minSlack=%d hist=",n,m,nsamples,grown,growfail,bestTau,3*n+2*m-11*bestTau);
    for(int t=0;t<64;t++) if(hist[t]) printf("%d:%ld ",t,hist[t]);
    printf("\n");
    return 0;
}
#endif
#ifdef LIB
int classC_edges(int n,int m,const int*flat){ G g; g.n=n; g.m=m; for(int i=0;i<m;i++)for(int k=0;k<3;k++) g.e[i][k]=flat[3*i+k]; return classC(&g); }
int hall_edges(int n,int m,const int*flat){ G g; g.n=n; g.m=m; for(int i=0;i<m;i++)for(int k=0;k<3;k++) g.e[i][k]=flat[3*i+k]; return hall_ok(&g); }
int f7_edges(int n,int m,const int*flat){ G g; g.n=n; g.m=m; for(int i=0;i<m;i++)for(int k=0;k<3;k++) g.e[i][k]=flat[3*i+k]; return has_f7(&g); }
#endif
