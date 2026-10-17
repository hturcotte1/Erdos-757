// ext3: re-insert ONE vertex w of degree d into G (nG vertices): w gets d new edges {w,a_i,b_i} with disjoint pairs, no pair inside a G-edge,
// endpoints of G-degree <= epdeg.  Required: tau(X) >= T.  Pruned (valid in class O, hereditary): X must be F7-free and satisfy e(S)<=|S|-2 (Hall test).
// tau test by "cover killing": tau(G)=T-1 => tau(X)>=T iff every minimum cover C of G (size T-1) misses some pair completely.
// Usage: ext3 nG T d epdeg [maxfinals] < graphs      (line: m a b c a b c ...)   Output: HIT lines (every X) and SUMMARY.
#include <bits/stdc++.h>
using namespace std;
typedef uint32_t u32; typedef unsigned long long u64;
int nG,T,d,epdeg; u64 maxfinals=200000000ULL;
static vector<u32> E; // edge masks (G edges then new)
static bool cover_le(const vector<u32>&Es,u32 unc,int k){
  if(!unc) return true; if(k==0) return false;
  int i=__builtin_ctz(unc); u32 e=Es[i];
  while(e){ int v=__builtin_ctz(e); e&=e-1; u32 rest=unc;
    for(size_t j=0;j<Es.size();j++) if((rest>>j&1)&&(Es[j]>>v&1)) rest&=~(1u<<j);
    if(cover_le(Es,rest,k-1)) return true; }
  return false; }
static bool has_edge(u32 e){ for(u32 x:E) if(x==e) return true; return false; }
static bool NOF7=false,NOHALL=false;
static bool has_f7_new(){
  if(NOF7) return false; // any F7 in E (full test; small)
  int ne=E.size(); int deg[32]={0}; for(u32 e:E) for(int v=0;v<32;v++) if(e>>v&1) deg[v]++;
  for(int p=0;p<32;p++){ if(deg[p]<3) continue;
    vector<int> idx; for(int i=0;i<ne;i++) if(E[i]>>p&1) idx.push_back(i);
    int c=idx.size();
    for(int a=0;a<c;a++)for(int b=a+1;b<c;b++)for(int g=b+1;g<c;g++){
      u32 ra=E[idx[a]]&~(1u<<p), rb=E[idx[b]]&~(1u<<p), rc=E[idx[g]]&~(1u<<p);
      u32 a0=ra&-ra,a1=ra^a0,b0=rb&-rb,b1=rb^b0,c0=rc&-rc,c1=rc^c0;
      for(int s2=0;s2<2;s2++)for(int s3=0;s3<2;s3++){
        u32 T1=a0|(s2?b1:b0)|(s3?c1:c0), T2=a1|(s2?b0:b1)|(s3?c0:c1);
        if(has_edge(T1)&&has_edge(T2)) return true; } } }
  return false; }
// Hall test
static int matchv[32],banned_;
static bool aug(int e,u32*seen){ u32 m=E[e]&~(u32)banned_&~*seen;
  while(m){ int v=__builtin_ctz(m); m&=m-1; *seen|=1u<<v; if(matchv[v]<0||aug(matchv[v],seen)){ matchv[v]=e; return true; } } return false; }
static bool hall_ok(){ if(NOHALL) return true; u32 used=0; for(u32 e:E) used|=e; int vs[32],nv=0; for(int v=0;v<32;v++) if(used>>v&1) vs[nv++]=v;
  int ne=E.size();
  for(int x=0;x<nv;x++)for(int y=x+1;y<nv;y++){ banned_=(1u<<vs[x])|(1u<<vs[y]); for(int v=0;v<32;v++) matchv[v]=-1;
    for(int e=0;e<ne;e++){ u32 seen=0; if(!aug(e,&seen)) return false; } }
  return true; }
struct Cov{ vector<u32> masks; };
static int COVK=0;
static void collect_covers(const vector<u32>&Es,u32 unc,int k,u32 cur,set<u32>&out){
  if(!unc){ if(__builtin_popcount(cur)==COVK) out.insert(cur); return; } // covers of size exactly COVK (= tau => all minimal)
  if(k==0) return;
  int i=__builtin_ctz(unc); u32 e=Es[i];
  while(e){ int v=__builtin_ctz(e); e&=e-1; u32 rest=unc;
    for(size_t j=0;j<Es.size();j++) if((rest>>j&1)&&(Es[j]>>v&1)) rest&=~(1u<<j);
    collect_covers(Es,rest,k-1,cur|(1u<<v),out); } }
// globals per graph
static vector<pair<int,int>> P; static vector<vector<u64>> killm; static int ncov,W; static vector<u32> covers;
static vector<int> chosen; static u32 usedv; static set<vector<int>> finals; static u64 nfinal_raw,nodes,nhit; static int mG;
static set<vector<int>> hits_seen;
static void emit_final(){
  vector<int> s=chosen; sort(s.begin(),s.end());
  if(!finals.insert(s).second) return;
  nfinal_raw++;
  if(!hall_ok()) return;
  hits_seen.insert(s); }
static void complete(int start){ // add remaining pairs (index increasing) freely
  if((int)chosen.size()==d){ emit_final(); return; }
  for(int i=start;i<(int)P.size();i++){ u32 pm=(1u<<P[i].first)|(1u<<P[i].second); if(pm&usedv) continue;
    u32 e=pm|(1u<<nG); E.push_back(e); usedv|=pm; chosen.push_back(i);
    if(!has_f7_new()) complete(i+1);
    chosen.pop_back(); usedv&=~pm; E.pop_back(); if(nfinal_raw>maxfinals) return; } }
static void killdfs(vector<u64>&alive){
  nodes++;
  int c0=-1; for(int w=0;w<W;w++) if(alive[w]){ c0=w*64+__builtin_ctzll(alive[w]); break; }
  if(c0<0){ complete(0); return; }
  if((int)chosen.size()==d) return;
  for(int i=0;i<(int)P.size();i++){ if(!(killm[i][c0>>6]>>(c0&63)&1)) continue;
    u32 pm=(1u<<P[i].first)|(1u<<P[i].second); if(pm&usedv) continue;
    u32 e=pm|(1u<<nG); E.push_back(e); usedv|=pm; chosen.push_back(i);
    if(!has_f7_new()){ vector<u64> al2(alive); for(int w=0;w<W;w++) al2[w]&=~killm[i][w]; killdfs(al2); }
    chosen.pop_back(); usedv&=~pm; E.pop_back(); if(nfinal_raw>maxfinals) return; } }
int main(int argc,char**argv){ nG=atoi(argv[1]); T=atoi(argv[2]); d=atoi(argv[3]); epdeg=atoi(argv[4]); if(argc>5) maxfinals=atoll(argv[5]); NOF7=getenv("NOF7")!=NULL; NOHALL=getenv("NOHALL")!=NULL;
  int m; u64 ng=0,skipped=0,uncons=0,totraw=0,tothit=0,totnodes=0,maxcov=0;
  while(scanf("%d",&m)==1){ vector<u32> g(m); int deg[32]={0};
    for(int i=0;i<m;i++){ int a,b,c; if(scanf("%d %d %d",&a,&b,&c)!=3) return 1; g[i]=(1u<<a)|(1u<<b)|(1u<<c); deg[a]++;deg[b]++;deg[c]++; }
    ng++; mG=m;
    // tau(G)
    int tg=0; while(!cover_le(g,(m>=32?0xFFFFFFFFu:((1u<<m)-1)),tg)) tg++;
    if(tg<T-1){ skipped++; continue; }
    covers.clear();
    if(tg==T-1){ set<u32> cs; COVK=T-1; collect_covers(g,(1u<<m)-1,T-1,0,cs); covers.assign(cs.begin(),cs.end()); } else uncons++;
    ncov=covers.size(); maxcov=max<u64>(maxcov,ncov); W=(ncov+63)/64;
    P.clear(); for(int a=0;a<nG;a++)for(int b=a+1;b<nG;b++){ if(deg[a]>epdeg||deg[b]>epdeg) continue; u32 p=(1u<<a)|(1u<<b); bool ok=true; for(u32 e:g) if((e&p)==p){ok=false;break;} if(ok) P.push_back({a,b}); }
    killm.assign(P.size(),vector<u64>(W,0));
    for(size_t i=0;i<P.size();i++){ u32 pm=(1u<<P[i].first)|(1u<<P[i].second); for(int c=0;c<ncov;c++) if(!(covers[c]&pm)) killm[i][c>>6]|=1ULL<<(c&63); }
    E=g; chosen.clear(); usedv=0; finals.clear(); hits_seen.clear(); nfinal_raw=0; nodes=0;
    vector<u64> alive(W,0); for(int c=0;c<ncov;c++) alive[c>>6]|=1ULL<<(c&63);
    killdfs(alive);
    totraw+=nfinal_raw; totnodes+=nodes;
    for(auto&s:hits_seen){ printf("HIT:"); for(u32 e:g){ printf(" ("); bool f=true; for(int v=0;v<nG;v++) if(e>>v&1){ printf(f?"%d":",%d",v); f=false; } printf(")"); }
      for(int i:s){ printf(" (%d,%d,%d)",P[i].first,P[i].second,nG); } printf("\n"); tothit++; }
    if(nfinal_raw>maxfinals) fprintf(stderr,"WARNING: maxfinals exceeded on graph %llu\n",ng);
  }
  printf("SUMMARY graphs=%llu skipped_tauG_low=%llu unconstrained=%llu max_min_covers=%llu kill_nodes=%llu finals_after_F7=%llu hits_after_hall=%llu\n",ng,skipped,uncons,maxcov,totnodes,totraw,tothit);
  return 0; }
