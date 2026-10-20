// Modular (P=2^61-1) conservative filter for self-similar families S_K = O u phi(O) u ... u phi^K(O),
// phi(a)=a', phi(b)=b' (a<b indices of sorted seed; a',b' any ordered pair of distinct points, |r|<1).
// A map survives iff for K=1..KMAX: |S_K| = n+(n-2)K, all pair sums x_i+x_j (i<j) distinct (weak Sidon),
// the number of 3-APs of S_K equals (K+1)*m0 (no cross-copy AP) and no two APs share two points.
// Real equal => equal mod P, so passing the test mod P implies passing it over Q; a false reject needs a
// ~2^-61 coincidence.  Survivors are re-verified exactly in Python.
// usage: filt seeds.txt KMAX part nparts
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned long long u64; typedef __int128 i128; typedef unsigned __int128 u128; typedef long long i64;
static const u64 P=(1ULL<<61)-1;
static inline u64 mulm(u64 a,u64 b){u128 t=(u128)a*b; u64 lo=(u64)(t&P), hi=(u64)(t>>61); u64 r=lo+hi; if(r>=P)r-=P; return r;}
static inline u64 addm(u64 a,u64 b){u64 r=a+b; if(r>=P)r-=P; return r;}
static inline u64 subm(u64 a,u64 b){return a>=b?a-b:a+P-b;}
static u64 powm(u64 a,u64 e){u64 r=1;while(e){if(e&1)r=mulm(r,a);a=mulm(a,a);e>>=1;}return r;}
static inline u64 red(i64 x){ i64 m=x%(i64)P; if(m<0)m+=P; return (u64)m;}
static i64 gcdl(i64 a,i64 b){if(a<0)a=-a;if(b<0)b=-b;while(b){i64 t=a%b;a=b;b=t;}return a;}
static int cmpu(const void*a,const void*b){u64 x=*(u64*)a,y=*(u64*)b;return x<y?-1:x>y;}
#define MAXN 200
// count APs of seed in integers (exact) -> m0
#define NEG (-1000000)
#define HMAX 4096
static long hist_num[3][HMAX]; static long cnt2=0;
int main(int argc,char**argv){
  int full=getenv("FULL")!=NULL;
  FILE*f=fopen(argv[1],"r"); int KMAX=atoi(argv[2]); int part=atoi(argv[3]), nparts=atoi(argv[4]);
  int id,n; static i64 x[64];
  while(fscanf(f,"%d %d",&id,&n)==2){
    for(int i=0;i<n;i++) fscanf(f,"%lld",&x[i]);
    if(id%nparts!=part) continue;
    // m0
    int m0=0; for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){ i64 s=x[i]+x[j]; if(s&1)continue; i64 h=s/2; for(int k=0;k<n;k++) if(x[k]==h&&k!=i&&k!=j){m0++;break;} }
    static int *amask=NULL, *asize=NULL; if(!amask){amask=malloc(sizeof(int)*(1<<16));asize=malloc(sizeof(int)*(1<<16));}
    int nap=0; static int apm[2000];
    for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){ i64 s=x[i]+x[j]; if(s&1)continue; i64 h=s/2; for(int k=0;k<n;k++) if(x[k]==h&&k!=i&&k!=j){apm[nap++]=(1<<i)|(1<<j)|(1<<k);break;} }
    int nadm=0; for(int mk=0;mk<(1<<n);mk++){ int okm=1; for(int t=0;t<nap;t++) if((mk&apm[t])==apm[t]){okm=0;break;} if(okm){amask[nadm]=mk;asize[nadm]=__builtin_popcount(mk);nadm++;} }
    for(int a=0;a<n;a++)for(int b=a+1;b<n;b++){
      for(int ap=0;ap<n;ap++){ for(int bp=0;bp<n;bp++){
        if(ap==bp)continue; int ovl=(ap==a||ap==b||bp==a||bp==b); int typ=0; if(ovl){ if((ap==a&&bp!=b&&bp!=a)||(bp==b&&ap!=a&&ap!=b)) typ=1; else typ=2; }
        i64 num=x[bp]-x[ap], den=x[b]-x[a]; i64 aa=num<0?-num:num; if(aa>=den)continue;
        i64 g=gcdl(num,den); i64 pp=num/g, qq=den/g; // r=pp/qq, qq>0
        u64 r=mulm(red(pp),powm(red(qq),P-2));
        u64 av=red(x[a]), apv=red(x[ap]);
        int ok=1;
        static u64 pts[MAXN*8]; static u64 base[64]; int np=n;
        for(int i=0;i<n;i++){pts[i]=red(x[i]);base[i]=pts[i];}
        for(int K=1;K<=KMAX&&ok;K++){
          // base <- phi(base)
          for(int i=0;i<n;i++) base[i]=addm(apv,mulm(r,subm(base[i],av)));
          for(int i=0;i<n;i++) pts[np+i]=base[i];
          // add all (dups removed later)
          int tot=np+n;
          static u64 srt[MAXN*8]; memcpy(srt,pts,tot*sizeof(u64)); qsort(srt,tot,sizeof(u64),cmpu);
          int u=0; for(int i=0;i<tot;i++) if(i==0||srt[i]!=srt[i-1]) srt[u++]=srt[i];
          if(u!=n+(n-2)*K){ok=0;break;}
          // rebuild pts as unique sorted list
          np=u; memcpy(pts,srt,u*sizeof(u64));
          // pair sums
          static u64 sums[MAXN*MAXN]; int ns=0;
          for(int i=0;i<u;i++)for(int j=i+1;j<u;j++) sums[ns++]=addm(srt[i],srt[j]);
          qsort(sums,ns,sizeof(u64),cmpu);
          for(int i=1;i<ns;i++) if(sums[i]==sums[i-1]){ok=0;break;}
          if(!ok)break;
          // APs: pairs i<j with (sum) == 2*srt[k]
          static u64 dbl[MAXN]; for(int k=0;k<u;k++) dbl[k]=addm(srt[k],srt[k]);
          // sorting dbl is not monotone mod P; use simple hash set via sorted copy with indices
          static u64 dsrt[MAXN][2]; // (value, k)
          // build sorted array of (dbl,k)
          static u64 dv[MAXN]; static int di[MAXN];
          for(int k=0;k<u;k++){dv[k]=dbl[k];di[k]=k;}
          // insertion sort (u<=~64)
          for(int k=1;k<u;k++){u64 v=dv[k];int ii=di[k];int j=k-1;while(j>=0&&dv[j]>v){dv[j+1]=dv[j];di[j+1]=di[j];j--;}dv[j+1]=v;di[j+1]=ii;}
          int cnt=0; static int apI[MAXN*MAXN/2][3];
          for(int i=0;i<u&&ok;i++)for(int j=i+1;j<u;j++){ u64 s=addm(srt[i],srt[j]); int lo=0,hi=u-1,pos=-1; while(lo<=hi){int mid=(lo+hi)/2; if(dv[mid]==s){pos=mid;break;} if(dv[mid]<s)lo=mid+1; else hi=mid-1;}
            if(pos>=0){ int k=di[pos]; if(k!=i&&k!=j){ if(cnt<MAXN*MAXN/2){apI[cnt][0]=i;apI[cnt][1]=j;apI[cnt][2]=k;} cnt++; } } }
          if(cnt!=(K+1)*m0){ok=0;break;}
          // linearity: no two APs share two points
          if(cnt<=MAXN*MAXN/2){
            static unsigned char seen[MAXN][MAXN]; for(int i=0;i<u;i++)memset(seen[i],0,u);
            for(int t=0;t<cnt&&ok;t++){ int v[3]={apI[t][0],apI[t][1],apI[t][2]}; for(int s1=0;s1<3;s1++)for(int s2=s1+1;s2<3;s2++){int p1=v[s1],p2=v[s2]; if(p1>p2){int tt=p1;p1=p2;p2=tt;} if(seen[p1][p2]){ok=0;} seen[p1][p2]=1; } }
          }
        }
        if(ok){
          int best[4][4]; for(int i=0;i<4;i++)for(int j=0;j<4;j++)best[i][j]=NEG;
          for(int t=0;t<nadm;t++){ int mk=amask[t]; int sa=((mk>>a)&1)|(((mk>>b)&1)<<1); int sb=((mk>>ap)&1)|(((mk>>bp)&1)<<1); if(asize[t]>best[sa][sb])best[sa][sb]=asize[t]; }
          int M[4][4],R[4],h0=NEG; for(int i=0;i<4;i++)for(int j=0;j<4;j++) M[i][j]=best[i][j]<0?NEG:best[i][j]-__builtin_popcount(i);
          for(int j=0;j<4;j++){R[j]=NEG;for(int i=0;i<4;i++)if(best[i][j]>R[j])R[j]=best[i][j]; if(R[j]>h0)h0=R[j];}
          int Rk[4],T[4]; int mx120=0; for(int j=0;j<4;j++)Rk[j]=R[j];
          for(int k=1;k<=240;k++){ for(int j=0;j<4;j++){T[j]=NEG;for(int i=0;i<4;i++) if(Rk[i]>NEG/2&&M[i][j]>NEG/2&&Rk[i]+M[i][j]>T[j])T[j]=Rk[i]+M[i][j];} for(int j=0;j<4;j++)Rk[j]=T[j];
            if(k==120){mx120=NEG;for(int j=0;j<4;j++)if(Rk[j]>mx120)mx120=Rk[j];} }
          int mx240=NEG;for(int j=0;j<4;j++)if(Rk[j]>mx240)mx240=Rk[j];
          int gn=mx240-mx120;
          if(gn<0||gn>=HMAX){gn=HMAX-1;} hist_num[typ][gn]++;
          int ex=(gn*9<=5*(n-2)*120);
          if(typ==2) { if(full) printf("%d %d %d %d %d %lld %lld %d %d T2\n",id,a,b,ap,bp,pp,qq,h0,gn); }
          else if(ex||full) printf("%d %d %d %d %d %lld %lld %d %d T%d\n",id,a,b,ap,bp,pp,qq,h0,gn,typ);
        }
      }}
    }
  }
  for(int t=0;t<3;t++)for(int g=0;g<HMAX;g++) if(hist_num[t][g]) fprintf(stderr,"#HIST T%d %d %ld\n",t,g,hist_num[t][g]);
  return 0;
}
