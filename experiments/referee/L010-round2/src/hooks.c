/* hooks.c -- referee L010 round 2 (written from scratch).  genbg hooks.
   Class 1 = hypergraph vertices 0..n1-1, class 2 = hyperedges (genbg -Z1 => any two edges share <= 1 vertex = linear;
   -D..:3 -d..:3 => edges have exactly 3 vertices).  genbg adds class-2 vertices one at a time and calls PRUNE1 on every
   intermediate graph whose parent (last edge deleted) has already passed PRUNE1 (genbg.c documentation), so a pruning
   test is safe if it holds for every sub-hypergraph (same vertex set, fewer edges) of every wanted output.
   Env: TAU0  (wanted: tau >= TAU0).  Prune (i): tau(current) < TAU0 - (maxn2 - n2) [one edge raises tau by <= 1].
        F7PRUNE=1: prune (ii) current graph contains F7 (a copy of F7 survives adding edges).
        Output: exact tau, F7 by a SECOND method, (P3) by all edge subsets, connectivity (with isolated vertices counted),
        min/max degree; prints  "G: (a,b,c) ... | tau=T f7=0/1 p3=0/1 conn=0/1"  for every output with tau >= TAU0.
   F7 methods (valid for linear 3-graphs):
     A (prune): vertex p of degree >= 3, three edges {p,a_i,b_i}; F7 iff for some choice x_i in {a_i,b_i} both
        {x_1,x_2,x_3} and its complement {y_1,y_2,y_3} are edges (edge lookup in a pair table).
     B (output): two disjoint edges f1,f2 and a vertex p outside them with >= 3 edges through p that meet f1 and f2 in
        exactly one vertex each (by linearity those 3 edges pair f1 with f2 bijectively, giving F7 = {p x_i y_i, f1, f2}). */
#include "gtools.h"
#include <stdint.h>
static int T0 = -1, F7P = 0;
static uint32_t E[64]; static int NE, NV;
static unsigned long long n_calls = 0, n_cut_tau = 0, n_cut_f7 = 0, n_out = 0, n_out_lowtau = 0, n_print = 0;
static void init(void) { if (T0 < 0) { char *s = getenv("TAU0"); T0 = s ? atoi(s) : 0; s = getenv("F7PRUNE"); F7P = s ? atoi(s) : 0; } }
static void load(graph *g, int n1, int n2) {
    NV = n1; NE = n2;
    for (int j = 0; j < n2; j++) { set *row = GRAPHROW(g, n1 + j, 1); uint32_t e = 0;
        for (int i = 0; i < n1; i++) if (ISELEMENT(row, i)) e |= 1u << i;
        E[j] = e; }
}
/* can the edges in 'left' (bitmask over E) be met by <= k vertices?  branch on the uncovered edge of smallest index */
static int coverable(uint64_t left, int k) {
    if (!left) return 1;
    if (k <= 0) return 0;
    int i = __builtin_ctzll(left); uint32_t e = E[i];
    while (e) { int v = __builtin_ctz(e); e &= e - 1;
        uint64_t l2 = left; for (int j = i; j < NE; j++) if ((l2 >> j & 1) && (E[j] >> v & 1)) l2 &= ~(1ull << j);
        if (coverable(l2, k - 1)) return 1; }
    return 0;
}
static uint64_t ALL(void) { return NE >= 64 ? ~0ull : ((1ull << NE) - 1); }
static int tau_exact(void) { int k = 0; while (!coverable(ALL(), k)) k++; return k; }
static int pairedge[32][32]; /* index+1 of the edge containing the pair, 0 if none */
static void build_pairs(void) {
    memset(pairedge, 0, sizeof pairedge);
    for (int j = 0; j < NE; j++) { int v[3], c = 0; uint32_t e = E[j]; while (e) { v[c++] = __builtin_ctz(e); e &= e - 1; }
        pairedge[v[0]][v[1]] = pairedge[v[1]][v[0]] = pairedge[v[0]][v[2]] = pairedge[v[2]][v[0]] =
        pairedge[v[1]][v[2]] = pairedge[v[2]][v[1]] = j + 1; }
}
static int is_edge(int a, int b, int c) { int j = pairedge[a][b]; return j && (E[j - 1] >> c & 1); }
static int f7_A(void) {
    build_pairs();
    for (int p = 0; p < NV; p++) {
        int at[64], k = 0; for (int j = 0; j < NE; j++) if (E[j] >> p & 1) at[k++] = j;
        if (k < 3) continue;
        for (int x = 0; x < k; x++) for (int y = x + 1; y < k; y++) for (int z = y + 1; z < k; z++) {
            int P[3][2]; int ids[3] = { at[x], at[y], at[z] };
            for (int t = 0; t < 3; t++) { uint32_t e = E[ids[t]] & ~(1u << p); P[t][0] = __builtin_ctz(e); e &= e - 1; P[t][1] = __builtin_ctz(e); }
            for (int c = 0; c < 8; c++) {
                int a = P[0][c & 1], b = P[1][(c >> 1) & 1], d = P[2][(c >> 2) & 1];
                int a2 = P[0][1 - (c & 1)], b2 = P[1][1 - ((c >> 1) & 1)], d2 = P[2][1 - ((c >> 2) & 1)];
                if (is_edge(a, b, d) && is_edge(a2, b2, d2)) return 1;
            }
        }
    }
    return 0;
}
static int f7_B(void) {
    for (int i = 0; i < NE; i++) for (int j = i + 1; j < NE; j++) {
        if (E[i] & E[j]) continue;
        uint32_t U = E[i] | E[j];
        for (int p = 0; p < NV; p++) { if (U >> p & 1) continue;
            int cnt = 0;
            for (int t = 0; t < NE; t++) { uint32_t e = E[t]; if (!(e >> p & 1)) continue;
                if (__builtin_popcount(e & E[i]) == 1 && __builtin_popcount(e & E[j]) == 1) cnt++; }
            if (cnt >= 3) return 1; }
    }
    return 0;
}
static int p3_ok(void) { /* |union F| >= |F| + 2 for every nonempty F, by recursion over subsets */
    static uint32_t U[1 << 16]; if (NE > 16) { fprintf(stderr, "NE>16\n"); exit(5); }
    U[0] = 0;
    for (uint32_t F = 1; F < (1u << NE); F++) { int hi = 31 - __builtin_clz(F); U[F] = U[F ^ (1u << hi)] | E[hi];
        if (__builtin_popcount(U[F]) < __builtin_popcount(F) + 2) return 0; }
    return 1;
}
static int connected_all(void) { /* every vertex 0..NV-1 reached from vertex 0 */
    uint32_t R = 1, prev = 0;
    while (R != prev) { prev = R; for (int j = 0; j < NE; j++) if (E[j] & R) R |= E[j]; }
    return R == ((NV >= 32) ? 0xffffffffu : ((1u << NV) - 1));
}
int r2prune(graph *g, int *deg, int n1, int n2, int maxn2) {
    init(); n_calls++; load(g, n1, n2);
    int need = T0 - (maxn2 - n2);
    if (need > 0 && coverable(ALL(), need - 1)) { n_cut_tau++; return 1; }
    if (F7P && n2 >= 5 && f7_A()) { n_cut_f7++; return 1; }
    return 0;
}
void r2out(FILE *f, graph *g, int n1, int n2) {
    init(); n_out++; load(g, n1, n2);
    int t = tau_exact(); if (t < T0) { n_out_lowtau++; return; }
    int fa = f7_A(), fb = f7_B(); if (fa != fb) { fprintf(stderr, "F7 METHODS DISAGREE\n"); exit(6); }
    int p3 = p3_ok(), cn = connected_all();
    n_print++;
    fprintf(f, "G:");
    for (int j = 0; j < NE; j++) { uint32_t e = E[j]; int a = __builtin_ctz(e); e &= e - 1; int b = __builtin_ctz(e); e &= e - 1; int c = __builtin_ctz(e);
        fprintf(f, " (%d,%d,%d)", a, b, c); }
    fprintf(f, " | tau=%d f7=%d p3=%d conn=%d\n", t, fb, p3, cn);
}
void r2sum(nauty_counter nout, double cpu) {
    fprintf(stderr, "R2SUMMARY TAU0=%d F7PRUNE=%d calls=%llu cut_tau=%llu cut_f7=%llu genbg_out=%llu out_lowtau=%llu printed=%llu cpu=%.2f\n",
            T0, F7P, n_calls, n_cut_tau, n_cut_f7, (unsigned long long)nout, n_out_lowtau, n_print, cpu);
}
