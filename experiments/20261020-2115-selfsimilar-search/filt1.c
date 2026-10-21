// One-shared-point chains (and stars): phi(x) = a' + r (x - a), r GENERIC (random residue mod P=2^61-1, two independent values).
// S_K = O u phi(O) u ... u phi^K(O).  Valid (formal-structure) iff for K=1..KMAX: |S_K| = n+(n-1)K, pair sums distinct,
// #3-APs = (K+1) m0 (no cross-copy AP), linear.  Hub a'=a allowed (star at a).  Transfer matrix (2 states) -> slope g,
// limit ratio g/(n-1).  Conservative mod-P test (see filt.c).  usage: filt1 seeds.txt KMAX part nparts seedrand
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned long long u64; typedef __int128 i128; typedef unsigned __int128 u128; typedef long long i64;
static const u64 P=(1ULL<<61)-1;
static inline u64 mulm(u64 a,u64 b){u128 t=(u128)a*b; u64 lo=(u64)(t&P), hi=(u64)(t>>61); u64 r=lo+hi; if(r>=P)r-=P; return r;}
static inline u64 addm(u64 a,u64 b){u64 r=a+b; if(r>=P)r-=P; return r;}
static inline u64 subm(u64 a,u64 b){return a>=b?a-b:a+P-b;}
static inline u64 red(i64 x){ i64 m=x%(i64)P; if(m<0)m+=P; return (u64)m;}
static int cmpu(const void*a,const void*b){u64 x=*(u64*)a,y=*(u64*)b;return x<y?-1:x>y;}
#define MAXN 200
#define NEG (-1000000)
#define HMAX 4096
static long hist_num[2][HMAX];
static u64 rs;
static u64 rnd(){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs%(P-2)+2; }
static int check(u64*base0,int n,int m0,int KMAX,u64 r,u64 av,u64 apv){
  static u64 pts[MAXN*8], base[64], srt[MAXN*8], sums[MAXN*MAXN], dv[MAXN]; static int di[MAXN]; static int apI[MAXN*MAXN/2][3]; static unsigned char seen[MAXN][MAXN];
  int np=n; for(int i=0;i<n;i++){pts[i]=base0[i];base[i]=base0[i];}
  for(int K=1;K<=KMAX;K++){
    for(int i=0;i<n;i++) base[i]=addm(apv,mulm(r,subm(base[i],av)));
    for(int i=0;i<n;i++) pts[np+i]=base[i];
    int tot=np+n; memcpy(srt,pts,tot*sizeof(u64)); qsort(srt,tot,sizeof(u64),cmpu);
    int u=0; for(int i=0;i<tot;i++) if(i==0||srt[i]!=srt[i-1]) srt[u++]=srt[i];
    if(u!=n+(n-1)*K) return 0;
    np=u; memcpy(pts,srt,u*sizeof(u64));
    int ns=0; for(int i=0;i<u;i++)for(int j=i+1;j<u;j++) sums[ns++]=addm(srt[i],srt[j]);
    qsort(sums,ns,sizeof(u64),cmpu);
    for(int i=1;i<ns;i++) if(sums[i]==sums[i-1]) return 0;
    for(int k=0;k<u;k++){dv[k]=addm(srt[k],srt[k]);di[k]=k;}
    for(int k=1;k<u;k++){u64 v=dv[k];int ii=di[k];int j=k-1;while(j>=0&&dv[j]>v){dv[j+1]=dv[j];di[j+1]=di[j];j--;}dv[j+1]=v;di[j+1]=ii;}
    int cnt=0;
    for(int i=0;i<u;i++)for(int j=i+1;j<u;j++){ u64 s=addm(srt[i],srt[j]); int lo=0,hi=u-1,pos=-1; while(lo<=hi){int mid=(lo+hi)/2; if(dv[mid]==s){pos=mid;break;} if(dv[mid]<s)lo=mid+1; else hi=mid-1;}
      if(pos>=0){ int k=di[pos]; if(k!=i&&k!=j){ if(cnt<MAXN*MAXN/2){apI[cnt][0]=i;apI[cnt][1]=j;apI[cnt][2]=k;} cnt++; if(cnt>(K+1)*m0) return 0; } } }
    if(cnt!=(K+1)*m0) return 0;
    for(int i=0;i<u;i++)memset(seen[i],0,u);
    for(int t=0;t<cnt;t++){ int v[3]={apI[t][0],apI[t][1],apI[t][2]}; for(int s1=0;s1<3;s1++)for(int s2=s1+1;s2<3;s2++){int p1=v[s1],p2=v[s2]; if(p1>p2){int tt=p1;p1=p2;p2=tt;} if(seen[p1][p2]) return 0; seen[p1][p2]=1; } }
  }
  return 1;
}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); int KMAX=atoi(argv[2]); int part=atoi(argv[3]), nparts=atoi(argv[4]); rs=strtoull(argv[5],0,10)*2654435761ULL+88172645463325252ULL;
  int full=getenv("FULL")!=NULL;
  int id,n; static i64 x[64]; static int amask[1<<16], asize[1<<16];
  while(fscanf(f,"%d %d",&id,&n)==2){
    for(int i=0;i<n;i++) if(fscanf(f,"%lld",&x[i])!=1) return 1;
    if(id%nparts!=part) continue;
    int m0=0,nap=0; static int apm[2000];
    for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){ i64 s=x[i]+x[j]; if(s&1)continue; i64 h=s/2; for(int k=0;k<n;k++) if(x[k]==h&&k!=i&&k!=j){apm[nap++]=(1<<i)|(1<<j)|(1<<k);m0++;break;} }
    int nadm=0; for(int mk=0;mk<(1<<n);mk++){ int okm=1; for(int t=0;t<nap;t++) if((mk&apm[t])==apm[t]){okm=0;break;} if(okm){amask[nadm]=mk;asize[nadm]=__builtin_popcount(mk);nadm++;} }
    u64 base0[64]; for(int i=0;i<n;i++) base0[i]=red(x[i]);
    for(int a=0;a<n;a++)for(int ap=0;ap<n;ap++){
      u64 r=rnd(); int typ=(ap==a);
      if(!check(base0,n,m0,KMAX,r,base0[a],base0[ap])) continue;
      u64 r2=rnd(); if(!check(base0,n,m0,KMAX,r2,base0[a],base0[ap])) continue;
      int best[2][2]; for(int i=0;i<2;i++)for(int j=0;j<2;j++)best[i][j]=NEG;
      for(int t=0;t<nadm;t++){ int mk=amask[t]; int sa=(mk>>a)&1, sb=(mk>>ap)&1; if(asize[t]>best[sa][sb])best[sa][sb]=asize[t]; }
      int M[2][2],R[2],h0=NEG; for(int i=0;i<2;i++)for(int j=0;j<2;j++) M[i][j]=best[i][j]<0?NEG:best[i][j]-i;
      for(int j=0;j<2;j++){R[j]=NEG;for(int i=0;i<2;i++)if(best[i][j]>R[j])R[j]=best[i][j]; if(R[j]>h0)h0=R[j];}
      int Rk[2],T[2],mx120=0; for(int j=0;j<2;j++)Rk[j]=R[j];
      for(int k=1;k<=240;k++){ for(int j=0;j<2;j++){T[j]=NEG;for(int i=0;i<2;i++) if(Rk[i]>NEG/2&&M[i][j]>NEG/2&&Rk[i]+M[i][j]>T[j])T[j]=Rk[i]+M[i][j];} for(int j=0;j<2;j++)Rk[j]=T[j];
        if(k==120){mx120=NEG;for(int j=0;j<2;j++)if(Rk[j]>mx120)mx120=Rk[j];} }
      int mx240=NEG;for(int j=0;j<2;j++)if(Rk[j]>mx240)mx240=Rk[j];
      int gn=mx240-mx120; if(gn<0||gn>=HMAX)gn=HMAX-1; hist_num[typ][gn]++;
      int ex=(gn*9<=5*(n-1)*120);
      if(ex||full) printf("%d %d %d %d %d %d T%d\n",id,a,ap,h0,gn,n,typ);
    }
  }
  for(int t=0;t<2;t++)for(int g=0;g<HMAX;g++) if(hist_num[t][g]) fprintf(stderr,"#HIST T%d %d %ld\n",t,g,hist_num[t][g]);
  return 0;
}
