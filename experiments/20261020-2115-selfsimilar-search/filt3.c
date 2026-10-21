// Period-2 words of two maps on the same seed: S = O u phi1(O u phi2(O u phi1(O u ...))).
// copy j (j>=1) has anchor pair alpha(m_j) and exit pair beta(m_{j+1}); the period-2 word (m1,m2) has matrices
// M1 = B[alpha(m1)][beta(m2)], M2 = B[alpha(m2)][beta(m1)]; growth per copy = lambda(M1 (x) M2)/2 (max-plus cycle mean).
// Only COMBINATORIAL (relaxed): each map must be K=1-valid (necessary); the word's geometry is verified later in Python.
// usage: filt3 seeds.txt part nparts PRUNE_NUM   (prints words with growth*9 <= PRUNE_NUM*(n-2) ; includes i==j)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned long long u64; typedef unsigned __int128 u128; typedef long long i64;
static const u64 P=(1ULL<<61)-1;
static inline u64 mulm(u64 a,u64 b){u128 t=(u128)a*b; u64 lo=(u64)(t&P), hi=(u64)(t>>61); u64 r=lo+hi; if(r>=P)r-=P; return r;}
static inline u64 addm(u64 a,u64 b){u64 r=a+b; if(r>=P)r-=P; return r;}
static inline u64 subm(u64 a,u64 b){return a>=b?a-b:a+P-b;}
static u64 powm(u64 a,u64 e){u64 r=1;while(e){if(e&1)r=mulm(r,a);a=mulm(a,a);e>>=1;}return r;}
static inline u64 red(i64 x){ i64 m=x%(i64)P; if(m<0)m+=P; return (u64)m;}
static i64 gcdl(i64 a,i64 b){if(a<0)a=-a;if(b<0)b=-b;while(b){i64 t=a%b;a=b;b=t;}return a;}
static int cmpu(const void*a,const void*b){u64 x=*(u64*)a,y=*(u64*)b;return x<y?-1:x>y;}
#define NEG (-1000000)
#define MAXV 20000
typedef struct {signed char m[4][4];} Mat;
static int valid1(u64*base0,int n,int m0,u64 r,u64 av,u64 apv){
  static u64 srt[256], sums[256*256]; static int apI[2000][3]; static unsigned char seen[256][256];
  int tot=2*n; for(int i=0;i<n;i++){srt[i]=base0[i]; srt[n+i]=addm(apv,mulm(r,subm(base0[i],av)));}
  qsort(srt,tot,sizeof(u64),cmpu); int u=0; for(int i=0;i<tot;i++) if(i==0||srt[i]!=srt[i-1]) srt[u++]=srt[i];
  if(u!=2*n-2) return 0;
  int ns=0; for(int i=0;i<u;i++)for(int j=i+1;j<u;j++) sums[ns++]=addm(srt[i],srt[j]);
  qsort(sums,ns,sizeof(u64),cmpu); for(int i=1;i<ns;i++) if(sums[i]==sums[i-1]) return 0;
  static u64 dv[256]; static int di[256];
  for(int k=0;k<u;k++){dv[k]=addm(srt[k],srt[k]);di[k]=k;}
  for(int k=1;k<u;k++){u64 v=dv[k];int ii=di[k];int j=k-1;while(j>=0&&dv[j]>v){dv[j+1]=dv[j];di[j+1]=di[j];j--;}dv[j+1]=v;di[j+1]=ii;}
  int cnt=0;
  for(int i=0;i<u;i++)for(int j=i+1;j<u;j++){ u64 s=addm(srt[i],srt[j]); int lo=0,hi=u-1,pos=-1; while(lo<=hi){int mid=(lo+hi)/2; if(dv[mid]==s){pos=mid;break;} if(dv[mid]<s)lo=mid+1; else hi=mid-1;}
    if(pos>=0){ int k=di[pos]; if(k!=i&&k!=j){ if(cnt<2000){apI[cnt][0]=i;apI[cnt][1]=j;apI[cnt][2]=k;} cnt++; if(cnt>2*m0) return 0; } } }
  if(cnt!=2*m0) return 0;
  for(int i=0;i<u;i++)memset(seen[i],0,u);
  for(int t=0;t<cnt;t++){ int v[3]={apI[t][0],apI[t][1],apI[t][2]}; for(int s1=0;s1<3;s1++)for(int s2=s1+1;s2<3;s2++){int p1=v[s1],p2=v[s2]; if(p1>p2){int tt=p1;p1=p2;p2=tt;} if(seen[p1][p2]) return 0; seen[p1][p2]=1; } }
  return 1;
}
static void mpmul(const Mat*A,const Mat*B,Mat*C){ for(int i=0;i<4;i++)for(int j=0;j<4;j++){int b=NEG; for(int k=0;k<4;k++) if(A->m[i][k]>NEG/2 && B->m[k][j]>NEG/2){int v=A->m[i][k]+B->m[k][j]; if(v>b)b=v;} C->m[i][j]=b<NEG/2?NEG:b; } }
// max cycle mean as fraction num/den (den in 1..4), returns via pointers; maximize num/den
static void cyclemean(const Mat*P1,int*bn,int*bd){ Mat Pk=*P1,T; *bn=NEG;*bd=1;
  for(int k=1;k<=4;k++){ for(int i=0;i<4;i++) if(Pk.m[i][i]>NEG/2){ int v=Pk.m[i][i]; if(*bn==NEG|| (long)v*(*bd)>(long)(*bn)*k){*bn=v;*bd=k;} } if(k<4){mpmul(&Pk,P1,&T);Pk=T;} } }

static int nadm; static int amask[1<<16], asize[1<<16];
static Mat cacheM[128][256]; static unsigned char cflag[128][256];
static const Mat* getM(int n,int a,int b,int ap,int bp,int aid,int bid){
  if(cflag[aid][bid]) return &cacheM[aid][bid];
  int best[4][4]; for(int i=0;i<4;i++)for(int j=0;j<4;j++)best[i][j]=NEG;
  for(int t=0;t<nadm;t++){ int mk=amask[t]; int sa=((mk>>a)&1)|(((mk>>b)&1)<<1); int sb=((mk>>ap)&1)|(((mk>>bp)&1)<<1); if(asize[t]>best[sa][sb])best[sa][sb]=asize[t]; }
  Mat*M=&cacheM[aid][bid]; for(int i=0;i<4;i++)for(int j=0;j<4;j++) M->m[i][j]=best[i][j]<0?NEG:(signed char)(best[i][j]-__builtin_popcount(i));
  cflag[aid][bid]=1; return M;
}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); int part=atoi(argv[2]), nparts=atoi(argv[3]); int PR=atoi(argv[4]);
  int id,n; static i64 x[64]; static int apm[2000];
  static int va[MAXV],vb[MAXV],vap[MAXV],vbp[MAXV]; static long long vp[MAXV],vq[MAXV];
  long tot_pairs=0, tot_hits=0; long seeds=0; int minnum=1000000, minden=1; // global min growth
  while(fscanf(f,"%d %d",&id,&n)==2){
    for(int i=0;i<n;i++) if(fscanf(f,"%lld",&x[i])!=1) return 1;
    if(id%nparts!=part) continue; seeds++;
    int m0=0,nap=0;
    for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){ i64 s=x[i]+x[j]; if(s&1)continue; i64 h=s/2; for(int k=0;k<n;k++) if(x[k]==h&&k!=i&&k!=j){apm[nap++]=(1<<i)|(1<<j)|(1<<k);m0++;break;} }
    nadm=0; for(int mk=0;mk<(1<<n);mk++){ int okm=1; for(int t=0;t<nap;t++) if((mk&apm[t])==apm[t]){okm=0;break;} if(okm){amask[nadm]=mk;asize[nadm]=__builtin_popcount(mk);nadm++;} }
    memset(cflag,0,sizeof cflag);
    u64 base0[64]; for(int i=0;i<n;i++) base0[i]=red(x[i]);
    int nv=0;
    int pid[64][64]; int c=0; for(int a=0;a<n;a++)for(int b=a+1;b<n;b++) pid[a][b]=c++;
    for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int ap=0;ap<n;ap++)for(int bp=0;bp<n;bp++){
      if(ap==bp||ap==a||ap==b||bp==a||bp==b) continue;
      i64 num=x[bp]-x[ap], den=x[b]-x[a]; i64 aa=num<0?-num:num; if(aa>=den)continue;
      i64 g=gcdl(num,den); i64 pp=num/g, qq=den/g;
      u64 r=mulm(red(pp),powm(red(qq),P-2));
      if(!valid1(base0,n,m0,r,red(x[a]),red(x[ap]))) continue;
      if(nv<MAXV){va[nv]=a;vb[nv]=b;vap[nv]=ap;vbp[nv]=bp;vp[nv]=pp;vq[nv]=qq;nv++;}
    }
    for(int i=0;i<nv;i++)for(int j=i;j<nv;j++){
      const Mat*M1=getM(n,va[i],vb[i],vap[j],vbp[j],pid[va[i]][vb[i]],vap[j]*n+vbp[j]);
      const Mat*M2=getM(n,va[j],vb[j],vap[i],vbp[i],pid[va[j]][vb[j]],vap[i]*n+vbp[i]);
      Mat Pm; mpmul(M1,M2,&Pm); int bn,bd; cyclemean(&Pm,&bn,&bd); tot_pairs++;
      // growth per copy = (bn/bd)/2
      if((long)bn*9 <= (long)PR*(n-2)*2*bd){
        printf("%d %d %d %d %d %lld %lld  %d %d %d %d %lld %lld  %d %d\n",id,va[i],vb[i],vap[i],vbp[i],vp[i],vq[i],va[j],vb[j],vap[j],vbp[j],vp[j],vq[j],bn,bd*2);
        tot_hits++;
      }
      if((long)bn*minden < (long)minnum*bd*2){minnum=bn;minden=bd*2;}
    }
  }
  fprintf(stderr,"#SUMMARY seeds %ld pairs %ld hits %ld mingrowth %d/%d\n",seeds,tot_pairs,tot_hits,minnum,minden);
  return 0;
}
