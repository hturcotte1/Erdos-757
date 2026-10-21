/* Referee's PRUNE1 function for UNMODIFIED nauty genbg (documented compile-time hook, genbg.c lines 58-95).
   genbg adds class-2 vertices (= hyperedges, each with exactly 3 neighbours by -d?:3 -D?:3) one at a time; every ancestor of an
   output graph is passed to this function.  Hereditary prunes (valid for every subgraph obtained by deleting edges of a final
   graph X with tau(X) = T, X in C):  tau(partial) >= T - (maxn2 - n2)  (deleting an edge lowers tau by at most 1);
   F7-free; (P3) e(S) <= |S|-2 (both monotone under adding edges).  T is read from the environment variable RPRUNE_T. */
#include "gtools.h"
#include <stdint.h>
static int TT = -1;
static uint32_t PE[64]; static int PM;
static int lbu(uint32_t S) { uint32_t used = 0; int c = 0; for (int i = 0; i < PM; i++) if (!(PE[i] & S) && !(PE[i] & used)) { used |= PE[i]; c++; } return c; }
static int ex(uint32_t S, int b) {
    int e = -1; for (int i = 0; i < PM; i++) if (!(PE[i] & S)) { e = i; break; }
    if (e < 0) return 1; if (b == 0) return 0; if (lbu(S) > b) return 0;
    for (uint32_t r = PE[e]; r; r &= r - 1) if (ex(S | (r & -r), b - 1)) return 1;
    return 0;
}
static int f7(int n) {
    for (int x = 0; x < n; x++) { int at[64], k = 0; for (int i = 0; i < PM; i++) if (PE[i] >> x & 1) at[k++] = i;
        for (int a = 0; a < k; a++) for (int b = a + 1; b < k; b++) for (int c = b + 1; c < k; c++) {
            uint32_t A1 = PE[at[a]] & ~(1u << x), A2 = PE[at[b]] & ~(1u << x), A3 = PE[at[c]] & ~(1u << x), U = A1 | A2 | A3;
            if (__builtin_popcount(U) != 6) continue;
            for (int f = 0; f < PM; f++) { uint32_t F = PE[f]; if (F & ~U) continue;
                if (__builtin_popcount(F & A1) != 1 || __builtin_popcount(F & A2) != 1 || __builtin_popcount(F & A3) != 1) continue;
                uint32_t G = U & ~F; for (int g = 0; g < PM; g++) if (PE[g] == G) return 1; } } }
    return 0;
}
static int own[32]; static uint32_t av;
static int aug(int e, uint32_t *seen) { for (uint32_t r = PE[e] & ~av & ~*seen; r; r &= r - 1) { int v = __builtin_ctz(r); *seen |= 1u << v;
    if (own[v] < 0 || aug(own[v], seen)) { own[v] = e; return 1; } } return 0; }
static int p3bad(int n) {
    for (int x = 0; x < n; x++) for (int y = x + 1; y < n; y++) { av = (1u << x) | (1u << y); for (int v = 0; v < 32; v++) own[v] = -1;
        for (int e = 0; e < PM; e++) { uint32_t s = 0; if (!aug(e, &s)) return 1; } }
    return 0;
}
int rprune(graph *g, int *deg, int n1, int n2, int maxn2) {
    if (TT < 0) { char *s = getenv("RPRUNE_T"); TT = s ? atoi(s) : 0; }
    int m = SETWORDSNEEDED(n1 + n2);
    PM = n2;
    for (int e = 0; e < n2; e++) { set *row = GRAPHROW(g, n1 + e, m); uint32_t mk = 0;
        for (int v = 0; v < n1; v++) if (ISELEMENT(row, v)) mk |= 1u << v; PE[e] = mk; }
    int need = TT - (maxn2 - n2);
    if (need >= 1 && ex(0, need - 1)) return 1;      /* tau(partial) <= need-1: prune */
    if (f7(n1)) return 1;
    /* (P3) is tested on the outputs by rext gb (monotone, so pruning on it is optional) */
    return 0;
}
