/* r3_hooks.c -- referee L008 round 3, written from scratch.  PRUNE1 / OUTPROC / SUMMARY hooks for nauty genbg.
   Encoding: first class = vertices of the 3-graph (n1), second class = edges (n2); -D3:3 -d1:3 => every edge-vertex has exactly
   3 neighbours (3-uniform), every vertex degree 1..3; -Z1 => two edges share <= 1 vertex (linear, no repeated edge); -c => connected.
   Prunes (all hereditary, so no output graph loses its canonical ancestor chain):
     TAU0=t    : reject an intermediate graph with k edges if tau(current) < t - (maxn2 - k)  [removing one edge lowers tau by <= 1]
     F7PRUNE=1 : reject if the current edges contain a copy of F7 (DEFINITIONAL test: some 5 edges on 7 vertices are the image of
                 F7 = {012,034,056,135,246} under one of the 7! bijections; a degree-multiset prefilter {3,2,2,2,2,2,2} is applied
                 first, which is a necessary condition for isomorphism).  Containment is monotone under adding edges.
     P3PRUNE=1 : reject if some non-empty edge set F has |union F| <= |F| + 1  (equivalent to e(S) > |S|-2 for S = union F).
   tau algorithm (different from the authors' edge-branching): branch on a vertex of maximum degree in the uncovered edges,
   include it or exclude it (delete it from all edges); bound: k * maxdeg >= #uncovered edges. */
#include "gtools.h"
#include <stdint.h>
#include <stdlib.h>
static int T0 = -1, F7P = -1, P3P = -1;
static uint32_t E[64]; static int NE, N1;
static unsigned long long calls = 0, pr_tau = 0, pr_f7 = 0, pr_p3 = 0, nout = 0;
static const int F7E[5][3] = {{0,1,2},{0,3,4},{0,5,6},{1,3,5},{2,4,6}};

/* can the edges (given as vertex masks, nedges of them) be hit by <= k vertices?  vertex include/exclude branching */
static int hit_le(uint32_t *ed, int ned, int k) {
    /* drop nothing; find max degree vertex */
    if (ned == 0) return 1;
    if (k <= 0) return 0;
    int cnt[32] = {0}, best = -1, bd = 0;
    for (int i = 0; i < ned; i++) { uint32_t e = ed[i]; if (!e) return 0; while (e) { int v = __builtin_ctz(e); e &= e-1; if (++cnt[v] > bd) { bd = cnt[v]; best = v; } } }
    if ((long)k * bd < ned) return 0;           /* each chosen vertex covers <= bd edges */
    if (bd == 1) return ned <= k;                /* all edges pairwise disjoint */
    uint32_t sub[64]; int ns;
    /* include best */
    ns = 0; for (int i = 0; i < ned; i++) if (!(ed[i] >> best & 1)) sub[ns++] = ed[i];
    if (hit_le(sub, ns, k-1)) return 1;
    /* exclude best: remove it from all edges */
    ns = 0; for (int i = 0; i < ned; i++) sub[ns++] = ed[i] & ~(1u << best);
    return hit_le(sub, ns, k);
}
static int tau_lt(int t) {  /* tau(current) < t ? */
    uint32_t ed[64]; for (int i = 0; i < NE; i++) ed[i] = E[i];
    return hit_le(ed, NE, t-1);
}
static int perm7[5040][7]; static int nperm = 0;
static void gen_perms(void) {
    int p[7] = {0,1,2,3,4,5,6};
    /* Heap's algorithm */
    int c[7] = {0}; for (int i = 0; i < 7; i++) perm7[nperm][i] = p[i]; nperm++;
    int i = 0;
    while (i < 7) {
        if (c[i] < i) { int j = (i % 2 == 0) ? 0 : c[i]; int t = p[i]; p[i] = p[j]; p[j] = t;
            for (int q = 0; q < 7; q++) perm7[nperm][q] = p[q]; nperm++; c[i]++; i = 0; }
        else { c[i] = 0; i++; }
    }
}
static int is_f7_image(uint32_t *five) {   /* definitional: is {five} the image of F7 under some bijection of its 7 vertices? */
    uint32_t U = 0; for (int k = 0; k < 5; k++) U |= five[k];
    if (__builtin_popcount(U) != 7) return 0;
    int verts[7], nv = 0; for (int v = 0; v < 32; v++) if (U >> v & 1) verts[nv++] = v;
    /* prefilter: degree multiset must be {3,2,2,2,2,2,2} (isomorphism invariant) */
    int d3 = 0, d2 = 0;
    for (int q = 0; q < 7; q++) { int d = 0; for (int k = 0; k < 5; k++) if (five[k] >> verts[q] & 1) d++; if (d == 3) d3++; else if (d == 2) d2++; }
    if (d3 != 1 || d2 != 6) return 0;
    if (!nperm) gen_perms();
    for (int p = 0; p < nperm; p++) {
        int ok = 1;
        for (int k = 0; k < 5 && ok; k++) {
            uint32_t img = (1u << verts[perm7[p][F7E[k][0]]]) | (1u << verts[perm7[p][F7E[k][1]]]) | (1u << verts[perm7[p][F7E[k][2]]]);
            int found = 0; for (int j = 0; j < 5; j++) if (five[j] == img) { found = 1; break; }
            if (!found) ok = 0;
        }
        if (ok) return 1;
    }
    return 0;
}
static int contains_f7(void) {
    if (NE < 5) return 0;
    uint32_t five[5]; int a, b, c, d, e;
    for (a = 0; a < NE; a++) for (b = a+1; b < NE; b++) for (c = b+1; c < NE; c++) for (d = c+1; d < NE; d++) for (e = d+1; e < NE; e++) {
        five[0] = E[a]; five[1] = E[b]; five[2] = E[c]; five[3] = E[d]; five[4] = E[e];
        if (is_f7_image(five)) return 1;
    }
    return 0;
}
static int violates_p3(void) {  /* some nonempty F with |U F| <= |F|+1 ? */
    static uint32_t U[1 << 16];
    if (NE > 16) { fprintf(stderr, "too many edges for P3 table\n"); exit(9); }
    U[0] = 0;
    for (uint32_t F = 1; F < (1u << NE); F++) {
        int low = __builtin_ctz(F); U[F] = U[F & (F-1)] | E[low];
        if (__builtin_popcount(U[F]) <= __builtin_popcount(F) + 1) return 1;
    }
    return 0;
}
static void load(graph *g, int n1, int n2) {
    N1 = n1; NE = n2;
    for (int j = 0; j < n2; j++) { setword w = g[n1 + j]; uint32_t e = 0; for (int i = 0; i < n1; i++) if (w & bit[i]) e |= 1u << i; E[j] = e; }
}
static void init(void) {
    if (T0 == -1) { char *s = getenv("TAU0"); T0 = s ? atoi(s) : 0; s = getenv("F7PRUNE"); F7P = s ? atoi(s) : 0; s = getenv("P3PRUNE"); P3P = s ? atoi(s) : 0; }
}
int r3prune(graph *g, int *deg, int n1, int n2, int maxn2) {
    init(); calls++;
    load(g, n1, n2);
    int need = T0 - (maxn2 - n2);
    if (need > 0 && tau_lt(need)) { pr_tau++; return 1; }
    if (F7P && contains_f7()) { pr_f7++; return 1; }
    if (P3P && violates_p3()) { pr_p3++; return 1; }
    return 0;
}
void r3out(FILE *f, graph *g, int n1, int n2) {
    load(g, n1, n2); nout++;
    fprintf(f, "FOUND:");
    for (int j = 0; j < n2; j++) { int first = 1; fprintf(f, " ("); for (int i = 0; i < n1; i++) if (E[j] >> i & 1) { fprintf(f, first ? "%d" : ",%d", i); first = 0; } fprintf(f, ")"); }
    fprintf(f, "\n");
}
void r3summary(nauty_counter n, double cpu) {
    fprintf(stderr, "R3SUMMARY TAU0=%d F7PRUNE=%d P3PRUNE=%d prune_calls=%llu pruned_tau=%llu pruned_f7=%llu pruned_p3=%llu outputs=%llu cpu=%.2f\n",
            T0, F7P, P3P, calls, pr_tau, pr_f7, pr_p3, nout, cpu);
}
