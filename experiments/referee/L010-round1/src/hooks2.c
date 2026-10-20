/* hooks2.c -- referee L010 round 1.  genbg hooks for a DIRECT search of members of C (no rebuild, no decomposition):
   PRUNE1 rejects an intermediate graph (= the output minus its last-added edges, a sub-hypergraph on the same vertex set) if
   (i) tau(current) < TAU0 - (maxn2 - n2), or (ii) it contains F7.  Both properties are inherited by every super-hypergraph
   (adding edges never lowers tau by more than... it never lowers tau; deleting one edge lowers tau by <= 1; a copy of F7 stays a copy),
   so no member of C with tau >= TAU0 is lost.  OUTPROC: exact tau, F7 again, property (P3) via all edge subsets,
   prints "FOUND:" for linear (by -Z1), F7-free, (P3), tau >= TAU0 graphs, and counts the rejected outputs.
   F7 test: a vertex p with three edges E1,E2,E3 whose other six vertices W are covered by two disjoint edges T1,T2 inside W,
   each meeting every E_i - p in exactly one vertex. */
#include "gtools.h"
#include <stdint.h>
static int T0 = -1;
static uint32_t E[64]; static int NE, NVV;
static unsigned long long npr = 0, ncut_tau = 0, ncut_f7 = 0, nout = 0, nrej_p3 = 0, nrej_tau = 0, nrej_f7 = 0;
static int cov(uint64_t left, int k) {
    if (!left) return 1;
    if (k == 0) return 0;
    int i = __builtin_ctzll(left); uint32_t e = E[i];
    for (int t = 0; t < 3; t++) {
        int v = __builtin_ctz(e); e &= e - 1;
        uint64_t l2 = left;
        for (int j = 0; j < NE; j++) if ((l2 >> j & 1ULL) && (E[j] >> v & 1u)) l2 &= ~(1ULL << j);
        if (cov(l2, k - 1)) return 1;
    }
    return 0;
}
static uint64_t allm(void) { return NE >= 64 ? ~0ULL : ((1ULL << NE) - 1); }
static int f7(void) {
    for (int p = 0; p < NVV; p++) {
        int at[64], k = 0; for (int i = 0; i < NE; i++) if (E[i] >> p & 1) at[k++] = i;
        if (k < 3) continue;
        for (int x = 0; x < k; x++) for (int y = x + 1; y < k; y++) for (int z = y + 1; z < k; z++) {
            uint32_t A = E[at[x]] & ~(1u << p), Bm = E[at[y]] & ~(1u << p), Cm = E[at[z]] & ~(1u << p);
            uint32_t W = A | Bm | Cm; if (__builtin_popcount(W) != 6) continue;
            int tr[64], nt = 0;
            for (int i = 0; i < NE; i++) {
                uint32_t e = E[i]; if ((e & W) != e) continue;
                if (__builtin_popcount(e & A) == 1 && __builtin_popcount(e & Bm) == 1 && __builtin_popcount(e & Cm) == 1) tr[nt++] = i;
            }
            for (int u = 0; u < nt; u++) for (int v = u + 1; v < nt; v++) if (!(E[tr[u]] & E[tr[v]])) return 1;
        }
    }
    return 0;
}
static int p3bad;
static void p3rec(int i, int cnt, uint32_t U) {
    if (p3bad) return;
    if (i == NE) { if (cnt > 0 && __builtin_popcount(U) < cnt + 2) p3bad = 1; return; }
    p3rec(i + 1, cnt, U); p3rec(i + 1, cnt + 1, U | E[i]);
}
static void load(graph *g, int n1, int n2) {
    NE = n2; NVV = n1;
    for (int j = 0; j < n2; j++) {
        setword w = g[n1 + j]; uint32_t e = 0;
        for (int i = 0; i < n1; i++) if (w & bit[i]) e |= 1u << i;
        E[j] = e;
    }
}
int refprune2(graph *g, int *deg, int n1, int n2, int maxn2) {
    if (T0 < 0) { char *s = getenv("TAU0"); T0 = s ? atoi(s) : 0; }
    npr++;
    load(g, n1, n2);
    int need = T0 - (maxn2 - n2);
    if (need > 0 && cov(allm(), need - 1)) { ncut_tau++; return 1; }
    if (n2 >= 5 && f7()) { ncut_f7++; return 1; }
    return 0;
}
void refout2(FILE *f, graph *g, int n1, int n2) {
    if (T0 < 0) { char *s = getenv("TAU0"); T0 = s ? atoi(s) : 0; }
    load(g, n1, n2);
    int k = 0; while (!cov(allm(), k)) k++;
    if (k < T0) { nrej_tau++; return; }
    if (f7()) { nrej_f7++; return; }
    p3bad = 0; p3rec(0, 0, 0); if (p3bad) { nrej_p3++; return; }
    nout++;
    fprintf(f, "FOUND:");
    for (int j = 0; j < n2; j++) { uint32_t e = E[j]; fprintf(f, " ("); for (int c = 0; c < 3; c++) { int v = __builtin_ctz(e); e &= e - 1; fprintf(f, c ? ",%d" : "%d", v); } fprintf(f, ")"); }
    fprintf(f, " tau=%d\n", k);
}
void refsummary2(nauty_counter n, double cpu) {
    fprintf(stderr, "REFSUMMARY2 TAU0=%d prune_calls=%llu cut_tau=%llu cut_f7=%llu genbg_out=%llu out_rej_tau=%llu out_rej_f7=%llu out_rej_p3=%llu printed_inC=%llu cpu=%.2f\n",
            T0, npr, ncut_tau, ncut_f7, (unsigned long long)n, nrej_tau, nrej_f7, nrej_p3, nout, cpu);
}
