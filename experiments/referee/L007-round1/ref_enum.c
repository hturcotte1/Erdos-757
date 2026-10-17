/* ref_enum.c -- referee's enumerator for L007 (written from scratch; method differs from the BFS canonical growth
   of conn_dfs2.c / enum_conn.c).
   Enumerates CONNECTED LINEAR 3-graphs on [N] with exactly M edges, tau >= T0, max degree <= DMAX.
   Method: necessary conditions satisfied by the LEXICOGRAPHICALLY MINIMAL labelling of H (the labelling minimizing
   the sorted list of sorted triples, compared lexicographically):
    (L1) the edges are produced in strictly increasing lex order;
    (L2) vertex 0 has maximum degree D and its edges are {0,1,2},{0,3,4},...,{0,2D-1,2D} (the first D edges);
    (L3) the vertices used by the first t edges are exactly {0,...,l_t-1} (first occurrence in increasing order);
    (L4) (H connected) every edge after the first contains an already used vertex;
    (L5) (H connected, optional flag) a component of the partial graph whose largest vertex is smaller than the
         least vertex of the last placed edge can never be joined to anything (later edges have larger minima).
   Pruning: l + 2r >= N, tau(placed) >= T0 - r (r = edges still to place).  Leaves: l == N, connected, tau >= T0.
   Usage: ref_enum N M T0 DMAX print(0/1) closeprune(0/1) [Donly]  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int N, M, T0, DMAX, PRINT, CLOSE, DONLY = -1, D;
static int ea[32], eb[32], ec[32];   /* placed edges as sorted triples */
static uint32_t inc[32];             /* inc[v]: bitmask of edge indices containing v */
static uint32_t adj[32];             /* adj[v]: vertices sharing an edge with v */
static int deg[32];
static unsigned long long nodes = 0, out = 0;
/* exists a set of <= k vertices meeting all edges in 'rem' (bitmask of edge indices)? */
static int hit(uint32_t rem, int k) {
    if (!rem) return 1;
    if (k == 0) return 0;
    int i = __builtin_ctz(rem);
    int vs[3] = { ea[i], eb[i], ec[i] };
    for (int j = 0; j < 3; j++) if (hit(rem & ~inc[vs[j]], k - 1)) return 1;
    return 0;
}
static int tau_at_least(int t, int ne) { if (t <= 0) return 1; return !hit(ne == 32 ? 0xffffffffu : ((1u << ne) - 1), t - 1); }
static int find(int *p, int x) { while (p[x] != x) x = p[x] = p[p[x]]; return x; }
static int connected_all(int ne, int nv) {
    int p[32]; for (int i = 0; i < nv; i++) p[i] = i;
    for (int i = 0; i < ne; i++) { int x = find(p, ea[i]), y = find(p, eb[i]), z = find(p, ec[i]); p[y] = x; z = find(p, ec[i]); p[z] = x; }
    int r = find(p, 0); for (int i = 1; i < nv; i++) if (find(p, i) != r) return 0; return 1;
}
/* (L5): is there a component (of the placed graph on vertices 0..nv-1) all of whose vertices are < pmin,
   while the final graph must have N vertices and be connected? */
static int closed_component(int ne, int nv, int pmin) {
    int p[32]; for (int i = 0; i < nv; i++) p[i] = i;
    for (int i = 0; i < ne; i++) { int x = find(p, ea[i]), y = find(p, eb[i]); p[y] = x; int z = find(p, ec[i]); p[z] = find(p, ea[i]); }
    int mx[32]; for (int i = 0; i < nv; i++) mx[i] = -1;
    for (int i = 0; i < nv; i++) { int r = find(p, i); if (i > mx[r]) mx[r] = i; }
    int ncomp = 0, closed = 0;
    for (int i = 0; i < nv; i++) if (find(p, i) == i) { ncomp++; if (mx[i] < pmin) closed = 1; }
    if (!closed) return 0;
    if (ncomp > 1 || nv < N) return 1;   /* a closed component that is not everything */
    return 0;
}
static void put(int ne, int a, int b, int c) {
    ea[ne] = a; eb[ne] = b; ec[ne] = c;
    inc[a] |= 1u << ne; inc[b] |= 1u << ne; inc[c] |= 1u << ne;
    adj[a] |= (1u << b) | (1u << c); adj[b] |= (1u << a) | (1u << c); adj[c] |= (1u << a) | (1u << b);
    deg[a]++; deg[b]++; deg[c]++;
}
static void take(int ne, int a, int b, int c) {
    inc[a] &= ~(1u << ne); inc[b] &= ~(1u << ne); inc[c] &= ~(1u << ne);
    adj[a] &= ~((1u << b) | (1u << c)); adj[b] &= ~((1u << a) | (1u << c)); adj[c] &= ~((1u << a) | (1u << b));
    deg[a]--; deg[b]--; deg[c]--;
}
static void emit(int ne) {
    out++;
    if (!PRINT) return;
    printf("G:");
    for (int i = 0; i < ne; i++) printf(" (%d,%d,%d)", ea[i], eb[i], ec[i]);
    printf("\n");
}
static void dfs(int ne, int nv) {
    nodes++;
    int r = M - ne;
    if (nv > N) return;
    if (r == 0) {
        if (nv == N && connected_all(ne, nv) && tau_at_least(T0, ne)) emit(ne);
        return;
    }
    if (nv + 2 * r < N) return;
    if (!tau_at_least(T0 - r, ne)) return;
    int la = ea[ne - 1], lb = eb[ne - 1], lc = ec[ne - 1];
    if (CLOSE && closed_component(ne, nv, la)) return;
    for (int a = (la >= 1 ? la : 1); a < nv; a++) {
        if (deg[a] >= D) continue;
        for (int b = a + 1; b <= nv; b++) {          /* b old (< nv) or the next new vertex nv */
            if (b < nv && (deg[b] >= D || (adj[a] >> b & 1))) continue;
            for (int c = b + 1; c <= nv + 1; c++) {
                int knew = (b == nv) + (c >= nv);
                if (b == nv && c != nv + 1) continue;    /* two new vertices must be nv, nv+1 */
                if (b < nv && c > nv) continue;          /* one new vertex must be nv */
                if (c < nv && (deg[c] >= D || (adj[a] >> c & 1) || (adj[b] >> c & 1))) continue;
                /* strict lex order */
                if (a == la && (b < lb || (b == lb && c <= lc))) continue;
                if (nv + knew > N) continue;
                put(ne, a, b, c);
                dfs(ne + 1, nv + knew);
                take(ne, a, b, c);
            }
        }
    }
}
int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: ref_enum N M T0 DMAX print closeprune [Donly]\n"); return 1; }
    N = atoi(argv[1]); M = atoi(argv[2]); T0 = atoi(argv[3]); DMAX = atoi(argv[4]); PRINT = atoi(argv[5]); CLOSE = atoi(argv[6]);
    if (argc > 7) DONLY = atoi(argv[7]);
    if (N > 30 || M > 31 || N < 3 || M < 1) return 1;
    for (D = 1; D <= DMAX && 2 * D + 1 <= N && D <= M; D++) {
        if (DONLY >= 0 && D != DONLY) continue;
        memset(inc, 0, sizeof inc); memset(adj, 0, sizeof adj); memset(deg, 0, sizeof deg);
        for (int i = 0; i < D; i++) put(i, 0, 2 * i + 1, 2 * i + 2);
        /* the star itself must satisfy the pruning tests too; dfs handles r==0 when D==M */
        dfs(D, 2 * D + 1);
    }
    fprintf(stderr, "ref_enum N=%d M=%d T0=%d DMAX=%d close=%d nodes=%llu out=%llu\n", N, M, T0, DMAX, CLOSE, nodes, out);
    printf("#END N=%d M=%d T0=%d DMAX=%d close=%d nodes=%llu out=%llu\n", N, M, T0, DMAX, CLOSE, nodes, out);
    return 0;
}
