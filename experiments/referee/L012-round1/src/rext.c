/* rext.c -- referee's extension enumerator (L012 round 1), written independently of the prover's ext_d.c.
   Usage: rext NG d EP < inputs   (input lines "m a b c a b c ..." : a 3-graph G on 0..NG-1)
   For each G: t = tau(G) by exhaustive branching (smallest k such that some k-set meets all edges; branching on the vertices of
   the first uncovered edge); all t-covers are listed by brute force over all subsets of size t (popcount filter over 2^NG masks).
   Admissible pairs {a,b}: a<b, not inside an edge of G, deg_G(a), deg_G(b) <= EP.  Output: every d-set of pairwise disjoint
   admissible pairs such that H = G + {NG,a,b} has tau(H) = t+1, i.e. every t-cover of G misses some chosen pair completely
   (a t-cover of H cannot contain NG, since then the rest would cover G with t-1 vertices).  No F7 / P3 pruning at all.
   Search: at each node take the alive (= not yet missed) cover that comes FIRST IN A STATIC ORDER BY INCREASING NUMBER OF KILLING
   PAIRS (a different branching order from the prover's), branch over its compatible, non-excluded killers q1<q2<..., excluding
   q1..q_{i-1} in branch i; when no cover is alive the remaining pairs are chosen as an increasing sequence of compatible,
   non-excluded pairs.  Each output d-set is also checked a posteriori (pairwise disjoint, kills every cover) and printed as
   "X: <graph index> p1a p1b p2a p2b ..." with the pairs sorted, plus "G: <index> t=.. covers=.. pairs=.. hits=.." per input. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64;
#define MAXK 8192
#define MAXPR 300
#define W_MAX (MAXK / 64)
static int NG, D, EP, ne; static uint32_t Em[64];
static uint32_t cov[MAXK]; static int K, W;
static int P, pa[MAXPR], pb[MAXPR]; static uint32_t pmask[MAXPR];
static u64 *kb;           /* kb[p*W + w] : covers killed (missed) by pair p */
static int corder[MAXK];  /* static order of covers */
static int chosen[16], nch; static uint32_t usedv;
static long long hits_this, nodes;
static int gidx;
static int has_cover(int k, uint32_t S, int from) { /* can S + (k more vertices) cover all edges? branching */
    int e = -1; for (int i = from; i < ne; i++) if (!(Em[i] & S)) { e = i; break; }
    if (e < 0) return 1;
    if (k == 0) return 0;
    for (uint32_t r = Em[e]; r; r &= r - 1) { int v = __builtin_ctz(r); if (has_cover(k - 1, S | (1u << v), e + 1)) return 1; }
    return 0;
}
static int tau_of(void) { for (int k = 0; k <= NG; k++) if (has_cover(k, 0, 0)) return k; return -1; }
static void report(void) {
    /* a-posteriori check */
    uint32_t u = 0; for (int i = 0; i < nch; i++) { if (pmask[chosen[i]] & u) { fprintf(stderr, "overlap\n"); exit(5); } u |= pmask[chosen[i]]; }
    for (int c = 0; c < K; c++) { int ok = 0; for (int i = 0; i < nch; i++) if (!(cov[c] & pmask[chosen[i]])) { ok = 1; break; } if (!ok) { fprintf(stderr, "cover not killed\n"); exit(6); } }
    int s[16]; memcpy(s, chosen, sizeof(int) * nch);
    for (int i = 0; i < nch; i++) for (int j = i + 1; j < nch; j++) if (s[j] < s[i]) { int t = s[i]; s[i] = s[j]; s[j] = t; }
    printf("X: %d", gidx); for (int i = 0; i < nch; i++) printf(" %d %d", pa[s[i]], pb[s[i]]); printf("\n");
    hits_this++;
}
static int isex(const u64 *ex, int p) { return (ex[p >> 6] >> (p & 63)) & 1; }
static void freepart(int start, const u64 *ex) {
    if (nch == D) { report(); return; }
    for (int p = start; p < P; p++) {
        if (isex(ex, p) || (pmask[p] & usedv)) continue;
        chosen[nch++] = p; usedv |= pmask[p]; freepart(p + 1, ex); usedv &= ~pmask[p]; nch--;
    }
}
static u64 alive_st[17][W_MAX];
static void search(int depth, const u64 *ex) {
    nodes++;
    const u64 *al = alive_st[depth];
    int c0 = -1; for (int i = 0; i < K; i++) { int c = corder[i]; if ((al[c >> 6] >> (c & 63)) & 1) { c0 = c; break; } }
    if (c0 < 0) { freepart(0, ex); return; }
    if (nch == D) return;
    u64 ex2[MAXPR / 64 + 1]; memcpy(ex2, ex, sizeof ex2);
    for (int p = 0; p < P; p++) {
        if (!((kb[(size_t)p * W + (c0 >> 6)] >> (c0 & 63)) & 1)) continue;
        if (isex(ex2, p) || (pmask[p] & usedv)) continue;
        u64 *nal = alive_st[depth + 1];
        for (int w = 0; w < W; w++) nal[w] = al[w] & ~kb[(size_t)p * W + w];
        chosen[nch++] = p; usedv |= pmask[p];
        search(depth + 1, ex2);
        usedv &= ~pmask[p]; nch--;
        ex2[p >> 6] |= 1ull << (p & 63);
    }
}
static int cnt_kill[MAXK];
static int cmpc(const void *a, const void *b) { int x = *(const int *)a, y = *(const int *)b; if (cnt_kill[x] != cnt_kill[y]) return cnt_kill[x] - cnt_kill[y]; return x - y; }
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: rext NG d EP\n"); return 1; }
    NG = atoi(argv[1]); D = atoi(argv[2]); EP = atoi(argv[3]);
    if (NG > 30 || D > 15) return 1;
    kb = malloc(sizeof(u64) * (size_t)MAXPR * W_MAX);
    int m; long long tot = 0;
    while (scanf("%d", &m) == 1) {
        ne = 0; int deg[32] = {0}; static int inedge[32][32]; memset(inedge, 0, sizeof inedge);
        for (int i = 0; i < m; i++) { int a, b, c; if (scanf("%d %d %d", &a, &b, &c) != 3) return 2;
            Em[ne++] = (1u << a) | (1u << b) | (1u << c); deg[a]++; deg[b]++; deg[c]++;
            inedge[a][b] = inedge[b][a] = inedge[a][c] = inedge[c][a] = inedge[b][c] = inedge[c][b] = 1; }
        int t = tau_of(); K = 0;
        for (uint32_t S = 0; S < (1u << NG); S++) {
            if (__builtin_popcount(S) != t) continue;
            int ok = 1; for (int i = 0; i < ne; i++) if (!(Em[i] & S)) { ok = 0; break; }
            if (ok) { if (K >= MAXK) { fprintf(stderr, "MAXK\n"); return 3; } cov[K++] = S; }
        }
        P = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++)
            if (!inedge[a][b] && deg[a] <= EP && deg[b] <= EP) { if (P >= MAXPR) return 4; pa[P] = a; pb[P] = b; pmask[P] = (1u << a) | (1u << b); P++; }
        W = (K + 63) / 64; if (W == 0) W = 1;
        for (int c = 0; c < K; c++) cnt_kill[c] = 0;
        for (int p = 0; p < P; p++) { u64 *row = kb + (size_t)p * W; memset(row, 0, sizeof(u64) * W);
            for (int c = 0; c < K; c++) if (!(cov[c] & pmask[p])) { row[c >> 6] |= 1ull << (c & 63); cnt_kill[c]++; } }
        for (int c = 0; c < K; c++) corder[c] = c;
        qsort(corder, K, sizeof(int), cmpc);
        memset(alive_st[0], 0, sizeof(u64) * W); for (int c = 0; c < K; c++) alive_st[0][c >> 6] |= 1ull << (c & 63);
        u64 ex[MAXPR / 64 + 1]; memset(ex, 0, sizeof ex);
        hits_this = 0; nodes = 0; nch = 0; usedv = 0;
        search(0, ex);
        printf("G: %d t=%d covers=%d pairs=%d hits=%lld nodes=%lld\n", gidx, t, K, P, hits_this, nodes);
        tot += hits_this; gidx++;
    }
    printf("TOTAL inputs=%d hits=%lld\n", gidx, tot);
    return 0;
}
