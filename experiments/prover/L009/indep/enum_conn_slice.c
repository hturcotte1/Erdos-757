/* enum_conn_slice.c -- enum_conn.c (certificate L007) plus optional slicing for random-sample validation (certificate L009):
   with arguments K I SD, the subtree below the c-th node created with exactly SD edges (counted in DFS order) is explored iff c % K == I.
   The part of the tree above depth SD does not depend on I, so the K slices partition the search.
   enum_conn.c -- independent enumerator written for certificate L007 (prover), not derived from conn_dfs2.c.
   Enumerates, up to isomorphism (each isomorphism class at least once), all CONNECTED LINEAR 3-uniform
   hypergraphs with exactly N vertices, exactly M edges, transversal number tau >= T0 and maximum degree <= DMAX.
   Usage: enum_conn N M T0 [DMAX] [print(0/1)]
   Method (proof of completeness in results/proofs/L007-...md, step C1): breadth-first canonical growth.
   Vertex 0 is labelled first.  Vertices are processed in label order c = 0,1,2,...; processing c places ALL
   remaining edges through c, in three phases:
     A: edges {c,a,b} with c<a<b<vstart (both other vertices already labelled when c's turn began), in
        increasing lexicographic order of (a,b);
     B: edges {c,a,new} with c<a<vstart, in increasing order of a; the new vertex gets the next free label;
     C: edges {c,new,new'}; the two new vertices get the next two free labels.
   (vstart = number of labelled vertices when c's turn began.)  After phase C the search moves to c+1.
   Pruning (all valid for every completion): nv+2r >= N (r = edges still to place, each adds <= 2 new
   vertices); tau(placed) >= T0 - r (each edge raises tau by <= 1); degrees <= DMAX; linearity.          */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int N, M, T0, DMAX = 1000, PRINT = 0;
static uint32_t ed[32];            /* placed edges, vertex bitmasks, in placement order */
static int ne = 0, nv = 1;         /* placed edges, labelled vertices (labels 0..nv-1) */
static int dg[32];
static uint32_t nb[32];            /* nb[x]: vertices y with {x,y} inside a placed edge */
static unsigned long long calls = 0, found = 0, cnt = 0;
static long long K = 1, I = 0; static int SD = -1;
static int slice_ok(void) { if (K <= 1 || ne != SD) return 1; cnt++; return (long long)(cnt % (unsigned long long)K) == I; }

/* exact: is there a set of at most k vertices meeting every placed edge whose index is in 'left'?
   branch on the highest-index edge not yet met */
static int hit_le(uint32_t left, int k) {
    if (!left) return 1;
    if (k <= 0) return 0;
    int i = 31 - __builtin_clz(left);
    uint32_t e = ed[i];
    for (int x = 0; x < 32; x++) {
        if (!(e >> x & 1)) continue;
        uint32_t l2 = left;
        for (int j = 0; j < ne; j++)
            if ((l2 >> j & 1) && (ed[j] >> x & 1)) l2 &= ~(1u << j);
        if (hit_le(l2, k - 1)) return 1;
    }
    return 0;
}
static uint32_t all_edges(void) { return ne >= 32 ? 0xffffffffu : ((1u << ne) - 1); }
static int tau_ge(int t) { /* tau(placed) >= t ? */
    if (t <= 0) return 1;
    return !hit_le(all_edges(), t - 1);
}
static int pair_free(int x, int y) { return !(nb[x] >> y & 1); }
static void place(int x, int y, int z) {
    ed[ne++] = (1u << x) | (1u << y) | (1u << z);
    dg[x]++; dg[y]++; dg[z]++;
    nb[x] |= (1u << y) | (1u << z); nb[y] |= (1u << x) | (1u << z); nb[z] |= (1u << x) | (1u << y);
}
static void unplace(int x, int y, int z) {
    ne--; dg[x]--; dg[y]--; dg[z]--;
    /* linear hypergraph: each pair lies in at most one edge, so the pairs of this edge were free before */
    nb[x] &= ~((1u << y) | (1u << z)); nb[y] &= ~((1u << x) | (1u << z)); nb[z] &= ~((1u << x) | (1u << y));
}
static void report(void) {
    found++;
    if (!PRINT) return;
    printf("FOUND:");
    for (int i = 0; i < ne; i++) {
        int f = 1; printf(" (");
        for (int x = 0; x < 32; x++) if (ed[i] >> x & 1) { printf(f ? "%d" : ",%d", x); f = 0; }
        printf(")");
    }
    printf("\n");
}
/* after placing an edge: 1 = branch finished (all M edges placed), 0 = continue if viable */
static int finished(void) {
    if (ne == M) { if (nv == N && tau_ge(T0)) report(); return 1; }
    return 0;
}
static int viable(void) {
    int r = M - ne;
    if (nv > N || nv + 2 * r < N) return 0;
    if (!tau_ge(T0 - r)) return 0;
    return 1;
}
static void vertex_turn(int c);
static void phaseC(int c) {
    calls++;
    /* option 1: close c */
    if (c + 1 < nv) vertex_turn(c + 1);
    /* option 2: one more edge {c, nv, nv+1} */
    if (nv + 2 <= N && dg[c] < DMAX) {
        int a = nv, b = nv + 1;
        place(c, a, b); nv += 2;
        if (!finished() && viable() && slice_ok()) phaseC(c);
        nv -= 2; unplace(c, a, b);
    }
}
static void phaseB(int c, int vstart, int lasta) {
    calls++;
    phaseC(c);                                   /* option 1: no further B edges */
    if (dg[c] >= DMAX || nv + 1 > N) return;
    for (int a = (lasta > c ? lasta + 1 : c + 1); a < vstart; a++) {
        if (dg[a] >= DMAX || !pair_free(c, a)) continue;
        int w = nv;
        place(c, a, w); nv++;
        if (!finished() && viable() && slice_ok()) phaseB(c, vstart, a);
        nv--; unplace(c, a, w);
    }
}
static void phaseA(int c, int vstart, int la, int lb) {
    calls++;
    phaseB(c, vstart, -1);                       /* option 1: no further A edges */
    if (dg[c] >= DMAX) return;
    for (int a = (la > c ? la : c + 1); a < vstart; a++) {
        if (dg[a] >= DMAX || !pair_free(c, a)) continue;
        for (int b = (a == la ? lb + 1 : a + 1); b < vstart; b++) {
            if (dg[b] >= DMAX || !pair_free(c, b) || !pair_free(a, b)) continue;
            place(c, a, b);
            if (!finished() && viable() && slice_ok()) phaseA(c, vstart, a, b);
            unplace(c, a, b);
        }
    }
}
static void vertex_turn(int c) { calls++; phaseA(c, nv, -1, -1); }
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: enum_conn N M T0 [DMAX] [print]\n"); return 1; }
    N = atoi(argv[1]); M = atoi(argv[2]); T0 = atoi(argv[3]);
    if (argc > 4) DMAX = atoi(argv[4]);
    if (argc > 5) PRINT = atoi(argv[5]);
    if (argc > 8) { K = atoll(argv[6]); I = atoll(argv[7]); SD = atoi(argv[8]); }
    if (N > 31 || M > 31 || N < 3 || M < 1) { fprintf(stderr, "range\n"); return 1; }
    vertex_turn(0);
    printf("enum_conn N=%d M=%d T0=%d DMAX=%d K=%lld I=%lld SD=%d cnt=%llu calls=%llu found=%llu\n", N, M, T0, DMAX, K, I, SD, cnt, calls, found);
    return 0;
}
