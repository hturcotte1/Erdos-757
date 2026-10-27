// PT analyzer. stdin: lines "n m tau a b c a b c ...". For each graph: connected, Delta, tau check,
// avoided set, U2 = avoided vertices of degree<=2, PT candidate (A,B,C) triples and test (ii).
// stdout: per-graph line "G idx n m tau slack conn Dmax nU nU2 ncand minGood hits" when nU2>=NPRINT (arg1, default 5);
// final "HIST" lines: slack Dmax3flag nU2 count.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64;
static int n,m; static int E[64][3]; static u64 cov[64]; static int deg[64];
static u64 popc(u64 x){return __builtin_popcountll(x);}
// decide: can alive edges be covered by <=k vertices not in forb (bitmask over vertices, n<=64)?
static int decide(u64 alive,u64 forb,int k){
  if(!alive) return 1;
  if(k<=0) return 0;
  int md=0; for(int v=0;v<n;v++){ if((forb>>v)&1) continue; int d=popc(cov[v]&alive); if(d>md) md=d; }
  if(md==0) return 0;
  if((int)popc(alive) > md*k) return 0;
  // choose alive edge with fewest allowed vertices; tie lowest
  int bi=-1,bc=9; u64 a=alive;
  while(a){ int i=__builtin_ctzll(a); a&=a-1; int c=0; for(int j=0;j<3;j++) if(!((forb>>E[i][j])&1)) c++; if(c<bc){bc=c;bi=i; if(c<=1)break;} }
  if(bc==0) return 0;
  u64 f=forb;
  for(int j=0;j<3;j++){ int v=E[bi][j]; if((f>>v)&1) continue;
    if(decide(alive&~cov[v],f,k-1)) return 1;
    f|=1ULL<<v; }
  return 0;
}
static int tauof(u64 alive){ int k=0; while(!decide(alive,0,k)) k++; return k; }
static int idx=0;
static long hist[300][2][40]; // slack offset 100? slack range -20..?? use +20
static int NPRINT=5;
static int connected(){ int par[64]; for(int i=0;i<n;i++)par[i]=i;
  #define F(a) ({int _x=a; while(par[_x]!=_x){par[_x]=par[par[_x]];_x=par[_x];} _x;})
  for(int i=0;i<m;i++){int a=F(E[i][0]),b=F(E[i][1]),c=F(E[i][2]); par[b]=a; par[F(c)]=a;}
  int r=F(0); for(int i=1;i<n;i++) if(F(i)!=r) return 0; return 1; }
int main(int argc,char**argv){
  if(argc>1) NPRINT=atoi(argv[1]);
  char *line=NULL; size_t cap=0;
  while(getline(&line,&cap,stdin)>0){
    char *p=line; int tau0;
    if(sscanf(p,"%d %d %d",&n,&m,&tau0)!=3) continue;
    // advance past 3 tokens
    for(int t=0;t<3;t++){ while(*p==' ')p++; while(*p&&*p!=' ')p++; }
    memset(deg,0,sizeof deg); memset(cov,0,sizeof cov);
    for(int i=0;i<m;i++) for(int j=0;j<3;j++){ int v=strtol(p,&p,10); E[i][j]=v; cov[v]|=1ULL<<i; deg[v]++; }
    idx++;
    u64 all = (m==64)?~0ULL:((1ULL<<m)-1);
    int tau=tauof(all);
    if(tau!=tau0){ printf("TAUMISMATCH idx %d file %d computed %d\n",idx,tau0,tau); }
    int slack=3*n+2*m-11*tau;
    int conn=connected(); int Dm=0; for(int v=0;v<n;v++) if(deg[v]>Dm)Dm=deg[v];
    // avoided
    int U[64],nU=0,U2[64],nU2=0;
    for(int v=0;v<n;v++){ if(decide(all&~cov[v],0,tau-1)) continue; U[nU++]=v; if(deg[v]<=2) U2[nU2++]=v; }
    int sl=slack+20; if(sl<0)sl=0; if(sl>299)sl=299;
    if(conn) hist[sl][Dm<=3?1:0][nU2<39?nU2:39]++;
    long ncand=0,hits=0; int minGood=99;
    if(conn && nU2>=6){
      // pairs not in a common edge
      int pr[800][2],np=0;
      for(int i=0;i<nU2;i++)for(int j=i+1;j<nU2;j++){ int a=U2[i],b=U2[j]; if(cov[a]&cov[b]) continue; pr[np][0]=a;pr[np][1]=b;np++; }
      for(int x=0;x<np;x++)for(int y=x+1;y<np;y++){
        if(pr[x][0]==pr[y][0]||pr[x][0]==pr[y][1]||pr[x][1]==pr[y][0]||pr[x][1]==pr[y][1]) continue;
        for(int z=y+1;z<np;z++){
          int *A=pr[x],*B=pr[y],*C=pr[z];
          if(A[0]==C[0]||A[0]==C[1]||A[1]==C[0]||A[1]==C[1]||B[0]==C[0]||B[0]==C[1]||B[1]==C[0]||B[1]==C[1]) continue;
          ncand++; int good=0;
          for(int i=0;i<2;i++)for(int j=0;j<2;j++)for(int k=0;k<2;k++){
            u64 al=all&~cov[A[i]]&~cov[B[j]]&~cov[C[k]];
            if(decide(al,0,tau-2)) good++;
          }
          if(good<minGood) minGood=good;
          if(good==0){ hits++; printf("HIT idx %d n %d m %d tau %d slack %d A %d %d B %d %d C %d %d edges",idx,n,m,tau,slack,A[0],A[1],B[0],B[1],C[0],C[1]);
            for(int e=0;e<m;e++) printf(" %d,%d,%d",E[e][0],E[e][1],E[e][2]); printf("\n"); }
        }
      }
    }
    if(nU2>=NPRINT || ncand>0){
      printf("G %d n %d m %d tau %d slack %d conn %d Dmax %d nU %d nU2 %d ncand %ld minGood %d hits %ld",idx,n,m,tau,slack,conn,Dm,nU,nU2,ncand,minGood,hits);
      printf(" edges"); for(int e=0;e<m;e++) printf(" %d,%d,%d",E[e][0],E[e][1],E[e][2]); printf("\n");
    }
  }
  for(int s=0;s<300;s++)for(int d=0;d<2;d++)for(int k=0;k<40;k++) if(hist[s][d][k]) printf("HIST slack %d D3 %d nU2 %d count %ld\n",s-20,d,k,hist[s][d][k]);
  return 0;
}
