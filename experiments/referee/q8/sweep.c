// Independent sweep of all 3^n (S,D) states. Own code. Input: n m mask_1..mask_m  (AP bitmasks), then optional dump stride.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned int u32;
static int n,m; static u32 E[64];
static unsigned char *indep; // indep[D]=1 iff no AP inside D
static inline int pc(u32 x){return __builtin_popcount(x);}
int main(int argc,char**argv){
  int stride = argc>1?atoi(argv[1]):0;
  scanf("%d %d",&n,&m); for(int i=0;i<m;i++) scanf("%u",&E[i]);
  u32 full=(1u<<n)-1; indep=malloc(1u<<n);
  for(u32 D=0;D<=full;D++){int ok=1;for(int i=0;i<m;i++) if((E[i]&D)==E[i]){ok=0;break;} indep[D]=ok;}
  long long valid=0,vQ=0,vA=0,vD4=0,eqQ=0; long long histQ[200]; memset(histQ,0,sizeof histQ); int minQ=1000;
  long long maxtau_seen=0;
  for(u32 S=0;S<=full;S++){
    // APs inside S
    u32 ES[64]; int ms=0; for(int i=0;i<m;i++) if((E[i]&S)==E[i]) ES[ms++]=E[i];
    u32 D=S;
    for(;;){
      if(indep[D]){
        valid++;
        u32 tr[64]; int nt=0;
        for(int i=0;i<ms;i++) tr[nt++]=ES[i]&~D;
        // minimal traces, dedup
        u32 K[64]; int nk=0;
        for(int i=0;i<nt;i++){
          int keep=1;
          for(int j=0;j<nt;j++){ if(j==i) continue;
            if((tr[j]&tr[i])==tr[j] && (tr[j]!=tr[i] || j<i)){keep=0;break;} }
          if(keep) K[nk++]=tr[i];
        }
        int e1=0,e2=0; for(int i=0;i<nk;i++){int c=pc(K[i]); if(c==1)e1++; else if(c==2)e2++;}
        u32 R=S&~D; int Rn=pc(R);
        // tau by brute force over subsets of R of increasing size
        int tau=-1;
        if(nk==0) tau=0; else {
          for(int k=1;k<=Rn && tau<0;k++){
            u32 T=(1u<<k)-1; // k-subsets of the Rn positions, map via pdep-like loop
            u32 lim=1u<<Rn;
            // positions of R bits
            u32 pos[32]; int pn=0; for(int b=0;b<n;b++) if(R>>b&1) pos[pn++]=1u<<b;
            while(T<lim){
              u32 M=0; for(int b=0;b<Rn;b++) if(T>>b&1) M|=pos[b];
              int ok=1; for(int i=0;i<nk;i++) if(!(K[i]&M)){ok=0;break;}
              if(ok){tau=k;break;}
              u32 c=T&-T, r=T+c; T=(((r^T)>>2)/c)|r;
            }
          }
          if(tau<0){fprintf(stderr,"tau fail\n");exit(1);}
        }
        if(tau>maxtau_seen)maxtau_seen=tau;
        long long sQ=3LL*Rn+2*e2+4*e1-7LL*tau;
        long long sD=9LL*Rn+5*e2+12*e1-21LL*tau;
        if(sQ<0)vQ++; if(sD<0)vD4++; if(sQ==0)eqQ++;
        if(sQ<minQ)minQ=sQ;
        if(sQ>=0&&sQ<200)histQ[sQ]++;
        if(stride && valid%stride==0) printf("DUMP S=%u D=%u tau=%d e1=%d e2=%d R=%d\n",S,D,tau,e1,e2,Rn);
      }
      if(D==0)break; D=(D-1)&S;
    }
  }
  printf("RESULT valid=%lld violQ8=%lld violD4=%lld eqQ8=%lld minslack=%d maxtau=%lld\n",valid,vQ,vD4,eqQ,minQ,maxtau_seen);
  printf("HIST"); for(int i=0;i<8;i++) printf(" %d:%lld",i,histQ[i]); printf("\n");
  return 0;
}
