/* enum_conn.c -- independent enumerator written for certificate L007 (prover), not derived from conn_dfs2.c.
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
static unsigned long long calls = 0, found = 0;

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

/* ---- class C check (added): F7-free through the newest edge, and P3 (e(S)<=|S|-2 for |S|>=2) in Hall form ---- */
static int own[32]; static uint32_t fbd;
static int augm(int e, uint32_t *seen) {
    for (uint32_t r = ed[e] & ~fbd & ~*seen; r; r &= r - 1) {
        int v = __builtin_ctz(r); *seen |= 1u << v;
        if (own[v] < 0 || augm(own[v], seen)) { own[v] = e; return 1; }
    }
    return 0;
}
static int c_ok(void) {
    /* F7 through the newest edge: five edges, union of 7 vertices, within-degrees 3,2,2,2,2,2,2 */
    int n1 = ne - 1; uint32_t E0 = ed[n1];
    for (int a = 0; a < n1; a++) { uint32_t U1 = E0 | ed[a]; if (__builtin_popcount(U1) > 7) continue;
     for (int b = a + 1; b < n1; b++) { uint32_t U2 = U1 | ed[b]; if (__builtin_popcount(U2) > 7) continue;
      for (int c = b + 1; c < n1; c++) { uint32_t U3 = U2 | ed[c]; if (__builtin_popcount(U3) > 7) continue;
       for (int d = c + 1; d < n1; d++) { uint32_t U = U3 | ed[d]; if (__builtin_popcount(U) != 7) continue;
        int es[5] = {n1, a, b, c, d}; int d3 = 0, d2 = 0;
        for (uint32_t r = U; r; r &= r - 1) { int v = __builtin_ctz(r), dd = 0; for (int k = 0; k < 5; k++) dd += (ed[es[k]] >> v) & 1; if (dd == 3) d3++; else if (dd == 2) d2++; }
        if (d3 == 1 && d2 == 6) return 0; } } } }
    /* P3 */
    uint32_t used = 0; for (int i = 0; i < ne; i++) used |= ed[i];
    for (uint32_t rx = used; rx; rx &= rx - 1) { int x = __builtin_ctz(rx);
      for (uint32_t ry = rx & (rx - 1); ry; ry &= ry - 1) { int y = __builtin_ctz(ry);
        fbd = (1u << x) | (1u << y); for (int v = 0; v < 32; v++) own[v] = -1;
        for (int e = 0; e < ne; e++) { uint32_t seen = 0; if (!augm(e, &seen)) return 0; } } }
    return 1;
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
        if (c_ok() && !finished() && viable()) phaseC(c);
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
        if (c_ok() && !finished() && viable()) phaseB(c, vstart, a);
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
            if (c_ok() && !finished() && viable()) phaseA(c, vstart, a, b);
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
    if (N > 31 || M > 31 || N < 3 || M < 1) { fprintf(stderr, "range\n"); return 1; }
    vertex_turn(0);
    printf("enum_conn N=%d M=%d T0=%d DMAX=%d calls=%llu found=%llu\n", N, M, T0, DMAX, calls, found);
    return 0;
}
