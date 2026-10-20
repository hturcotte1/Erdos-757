/* Referee L013 r1: PRUNE1 hook for (unmodified) genbg.c, using the documented PRUNE1 interface.
   Prunes an intermediate bicoloured graph (class 1 = hypergraph vertices, class 2 = edges added so far) iff
   (a) tau(partial) + (maxn2 - n2) < TARGET_T  (each later edge raises tau by at most 1), or
   (b) the partial hypergraph contains F7 (inherited by every supergraph), or
   (c) the partial hypergraph violates (P3) e(S) <= |S|-2 (inherited by every supergraph).
   TARGET_T is read from the environment variable PRUNE_T. */
#include "gtools.h"
static int TT = -1;
static int pE[64][3], pn2, pn1; static unsigned long long pinc[64];
static int p_hc(unsigned long long mask, int k) {
    if (!mask) return 1;
    if (!k) return 0;
    unsigned long long used = 0; int c = 0;
    for (int e = 0; e < pn2; e++) if (mask >> e & 1) { unsigned long long vs = (1ULL << pE[e][0]) | (1ULL << pE[e][1]) | (1ULL << pE[e][2]); if (!(vs & used)) { used |= vs; c++; } }
    if (c > k) return 0;
    int e = __builtin_ctzll(mask);
    for (int i = 0; i < 3; i++) if (p_hc(mask & ~pinc[pE[e][i]], k - 1)) return 1;
    return 0;
}
static int p_isedge(int a, int b, int c) { return (pinc[a] & pinc[b] & pinc[c]) != 0; }
static int p_f7(void) {
    for (int c = 0; c < pn1; c++) {
        int inc[64], ni = 0;
        for (int e = 0; e < pn2; e++) if (pinc[c] >> e & 1) inc[ni++] = e;
        for (int x = 0; x < ni; x++) for (int y = x + 1; y < ni; y++) for (int z = y + 1; z < ni; z++) {
            int P[3][2]; int es[3] = {inc[x], inc[y], inc[z]};
            for (int r = 0; r < 3; r++) { int q = 0; for (int i = 0; i < 3; i++) if (pE[es[r]][i] != c) P[r][q++] = pE[es[r]][i]; }
            for (int a = 0; a < 2; a++) for (int b = 0; b < 2; b++) for (int g = 0; g < 2; g++)
                if (p_isedge(P[0][a], P[1][b], P[2][g]) && p_isedge(P[0][1 - a], P[1][1 - b], P[2][1 - g])) return 1;
        }
    }
    return 0;
}
static int pm[64], ps[64], pst, pu, pv;
static int p_try(int e) { for (int i = 0; i < 3; i++) { int v = pE[e][i]; if (v == pu || v == pv || ps[v] == pst) continue; ps[v] = pst; if (pm[v] < 0 || p_try(pm[v])) { pm[v] = e; return 1; } } return 0; }
static int p_p3(void) {
    for (pu = 0; pu < pn1; pu++) for (pv = pu + 1; pv < pn1; pv++) {
        for (int i = 0; i < pn1; i++) pm[i] = -1;
        for (int e = 0; e < pn2; e++) { pst++; if (!p_try(e)) return 0; }
    }
    return 1;
}
int prune_tau(graph *g, int *deg, int n1, int n2, int maxn2) {
    if (TT < 0) { char *s = getenv("PRUNE_T"); TT = s ? atoi(s) : 0; }
    pn1 = n1; pn2 = n2;
    for (int v = 0; v < n1; v++) pinc[v] = 0;
    for (int j = 0; j < n2; j++) {
        set *gj = GRAPHROW(g, n1 + j, 1); int q = 0;
        for (int v = 0; v < n1; v++) if (ISELEMENT(gj, v)) { if (q < 3) pE[j][q] = v; q++; }
        if (q != 3) return 0;  /* not a 3-edge: leave to genbg/hfilt */
        for (int i = 0; i < 3; i++) pinc[pE[j][i]] |= 1ULL << j;
    }
    unsigned long long all = (n2 == 64) ? ~0ULL : ((1ULL << n2) - 1);
    int need = TT - (maxn2 - n2);          /* tau(partial) must be >= need */
    if (need > 0 && p_hc(all, need - 1)) return 1;
    if (p_f7()) return 1;
    if (!p_p3()) return 1;
    return 0;
}
