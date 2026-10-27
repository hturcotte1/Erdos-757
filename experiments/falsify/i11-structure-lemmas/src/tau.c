// exact transversal number of a 3-uniform (or <=64 vertex general) hypergraph, branch and bound
#include <stdint.h>
#include <string.h>
typedef uint64_t u64;
static int best;
static int popc(u64 x){return __builtin_popcountll(x);}
static void rec(const u64*ed,int m,u64 F,int cnt,int*unc_idx,int nunc){
    // ed: edge masks; unc_idx: indices of uncovered edges
    if(nunc==0){ if(cnt<best) best=cnt; return; }
    if(cnt+1>=best) return;
    // lower bound: greedy disjoint packing of available masks
    u64 used=0; int lb=0; int mn=100, mi=-1;
    for(int k=0;k<nunc;k++){
        u64 a=ed[unc_idx[k]]&~F;
        int pc=popc(a);
        if(pc==0) return;
        if(pc<mn){mn=pc;mi=unc_idx[k];}
        if(!(a&used)){ used|=a; lb++; }
    }
    // degree bound
    // (skip: packing bound usually enough)
    if(cnt+lb>=best) return;
    u64 a=ed[mi]&~F;
    int buf[600];
    u64 tried=0;
    while(a){
        u64 bit=a&-a; a^=bit;
        // include bit, exclude previously tried
        int n2=0;
        for(int k=0;k<nunc;k++){ if(!(ed[unc_idx[k]]&bit)) buf[n2++]=unc_idx[k]; }
        // copy buf onto stack-safe array
        int loc[600]; memcpy(loc,buf,n2*sizeof(int));
        rec(ed,m,F|tried,cnt+1,loc,n2);
        tried|=bit;
        if(cnt+1>=best) return;
    }
}
// edges: array of 3*m ints (vertex indices <64) ; alive mask: vertices allowed (others deleted with incident edges)
int tau_induced(int m,const int*e,u64 alive){
    u64 ed[600]; int idx[600]; int k=0;
    for(int i=0;i<m;i++){
        u64 mk=(1ULL<<e[3*i])|(1ULL<<e[3*i+1])|(1ULL<<e[3*i+2]);
        if((mk&alive)==mk){ ed[k]=mk; idx[k]=k; k++; }
    }
    best=k+1; // trivial: one vertex per edge
    // greedy upper bound
    rec(ed,k,0,0,idx,k);
    return best;
}
int tau_all(int m,const int*e){ return tau_induced(m,e,~0ULL); }
