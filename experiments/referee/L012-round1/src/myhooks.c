/* myhooks.c -- referee L012 round 1: pruning/output hooks for unmodified nauty genbg
   (compile genbg.c with -DPRUNE1=mprune1 -DPRUNE2=mprune2 -DOUTPROC=mout -DSUMMARY=msum).
   Model: first class = points 0..n1-1, second class = hyperedges (genbg -d1:3 -D<D>:3 -Z1 -c: every hyperedge has 3 points,
   points have degree 1..D, two hyperedges share <= 1 point (linear), connected).
   Prunes (each isomorphism-invariant and valid for every completion, as genbg requires):
     mprune1: tau(partial) + (maxn2 - n2) < T   (one more hyperedge raises tau by at most 1);
     mprune2: the partial 3-graph contains F7, or violates (P3) e(S) <= |S|-2 (both inherited by supergraphs).
   mout: prints "FOUND: (a,b,c) ..." iff tau == T exactly, F7-free and (P3) (re-checked).  Env: TT = T. */
#include "gtools.h"
#include <stdint.h>
#include <string.h>
static int T = 0, inited = 0, NE, NV; static int ed[64][3]; static uint32_t EM[64];
static unsigned long long c1 = 0, p1 = 0, c2 = 0, p2f7 = 0, p2p3 = 0, nout = 0, nrej = 0;
static void init(void) { char *s = getenv("TT"); if (s) T = atoi(s); inited = 1; }
static void load(graph *g, int n1, int n2) {
    NE = n2; NV = n1;
    for (int i = 0; i < n2; i++) { set *row = GRAPHROW(g, n1 + i, MAXM); int k = 0; uint32_t m = 0;
        for (int j = 0; j < n1; j++) if (ISELEMENT(row, j)) { if (k < 3) ed[i][k] = j; k++; m |= 1u << j; }
        EM[i] = m; }
}
static int cover_k(int k, uint32_t S, int from) {
    int e = -1; for (int i = from; i < NE; i++) if (!(EM[i] & S)) { e = i; break; }
    if (e < 0) return 1; if (!k) return 0;
    for (int t = 0; t < 3; t++) if (cover_k(k - 1, S | (1u << ed[e][t]), e + 1)) return 1;
    return 0;
}
static int tau(void) { for (int k = 0; ; k++) if (cover_k(k, 0, 0)) return k; }
static int isedge3(int a, int b, int c) { uint32_t m = (1u << a) | (1u << b) | (1u << c); for (int i = 0; i < NE; i++) if (EM[i] == m) return 1; return 0; }
static int f7(void) {
    for (int p = 0; p < NV; p++) {
        int at[32], na = 0; for (int e = 0; e < NE; e++) if (EM[e] >> p & 1) at[na++] = e;
        for (int i = 0; i < na; i++) for (int j = i + 1; j < na; j++) for (int k = j + 1; k < na; k++) {
            int o[3][2]; int ids[3] = {at[i], at[j], at[k]};
            for (int q = 0; q < 3; q++) { int c = 0; for (int r = 0; r < 3; r++) if (ed[ids[q]][r] != p) o[q][c++] = ed[ids[q]][r]; }
            for (int s2 = 0; s2 < 2; s2++) for (int s3 = 0; s3 < 2; s3++)
                if (isedge3(o[0][0], o[1][s2], o[2][s3]) && isedge3(o[0][1], o[1][1 - s2], o[2][1 - s3])) return 1;
        }
    }
    return 0;
}
static int matchE[64], matchV[32];
static int bfs_aug(int src, int x, int y) {
    int prevE[32], from[64], q[64], qh = 0, qt = 0; int seenV[32]; memset(seenV, 0, sizeof seenV);
    for (int i = 0; i < 64; i++) from[i] = -2;
    q[qt++] = src; from[src] = -1;
    while (qh < qt) {
        int e = q[qh++];
        for (int k = 0; k < 3; k++) { int v = ed[e][k]; if (v == x || v == y || seenV[v]) continue; seenV[v] = 1; prevE[v] = e;
            if (matchV[v] < 0) { int cv = v;
                while (1) { int ce = prevE[cv]; int nxt = matchE[ce]; matchE[ce] = cv; matchV[cv] = ce; if (from[ce] == -1) break; cv = nxt; }
                return 1; }
            int e2 = matchV[v]; if (from[e2] == -2) { from[e2] = e; q[qt++] = e2; } }
    }
    return 0;
}
static int p3(void) {
    for (int x = 0; x < NV; x++) for (int y = x + 1; y < NV; y++) {
        for (int i = 0; i < 64; i++) matchE[i] = -1;
        for (int i = 0; i < 32; i++) matchV[i] = -1;
        for (int e = 0; e < NE; e++) if (!bfs_aug(e, x, y)) return 0;
    }
    return 1;
}
int mprune1(graph *g, int *deg, int n1, int n2, int maxn2) {
    if (!inited) init(); c1++; load(g, n1, n2);
    int need = T - (maxn2 - n2);
    if (need > 0 && !cover_k(need - 1, 0, 0) == 0) { p1++; return 1; }   /* some (need-1)-set covers: tau < need */
    return 0;
}
int mprune2(graph *g, int *deg, int n1, int n2, int maxn2) {
    if (!inited) init(); c2++; load(g, n1, n2);
    if (f7()) { p2f7++; return 1; }
    if (!p3()) { p2p3++; return 1; }
    return 0;
}
void mout(FILE *f, graph *g, int n1, int n2) {
    if (!inited) init(); load(g, n1, n2);
    if (tau() != T || f7() || !p3()) { nrej++; return; }
    nout++; fprintf(f, "FOUND:"); for (int i = 0; i < n2; i++) fprintf(f, " (%d,%d,%d)", ed[i][0], ed[i][1], ed[i][2]); fprintf(f, "\n");
}
void msum(nauty_counter n, double cpu) {
    fprintf(stderr, "MSUM T=%d prune1_calls=%llu pruned_tau=%llu prune2_calls=%llu pruned_F7=%llu pruned_P3=%llu genbg_out=%llu kept=%llu rejected_at_output=%llu cpu=%.1f\n",
            T, c1, p1, c2, p2f7, p2p3, (unsigned long long)n, nout, nrej, cpu);
}
