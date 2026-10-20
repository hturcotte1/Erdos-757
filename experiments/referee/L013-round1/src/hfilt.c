/* Referee L013 round 1: own filter for genbg output (graph6 bipartite incidence graphs, class 1 = n1 hypergraph vertices,
   class 2 = n2 hyperedges).  Usage: hfilt n1 n2 t D [print]
   For every input graph: decode; check every class-2 node has exactly 3 neighbours, all in class 1, and there are no
   class1-class1 or class2-class2 adjacencies; linear (two edges share <= 1 vertex); connected on all n1 vertices;
   max degree <= D; tau >= t by exhaustive cover search; exact tau; F7-free (structural test: centre c, three edges at c,
   an edge meeting each of the three pairs, and the complementary choice also an edge); (P3) e(S) <= |S|-2 for all |S|>=2
   via Hall: for every pair {u,v} the edges have a matching into V\{u,v}.
   Prints 'FOUND: (a,b,c) ...' for graphs that are connected, linear, F7-free, (P3), Delta<=D and tau == t (if 'print'),
   and a summary line. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXV 64
#define MAXE 40
static int n1, n2, T, Dmax;
static int E[MAXE][3];
static unsigned long long vmask_edges[MAXV]; /* bitmask of edges containing vertex */
static int deg[MAXV];
static int decode(const char *s, unsigned char adj[MAXV][MAXV]) {
    int n = s[0] - 63; if (n < 0 || n > 62) return -1;
    memset(adj, 0, sizeof(unsigned char) * MAXV * MAXV);
    int k = 0, bitpos = 6; const char *p = s + 1; int cur = 0; int have = 0;
    for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) {
        if (!have) { cur = *p - 63; p++; have = 6; }
        have--; int b = (cur >> have) & 1; if (b) { adj[i][j] = adj[j][i] = 1; }
        k++;
    }
    (void)bitpos; return n;
}
static int greedy_lb(unsigned long long mask) {
    /* size of a greedy set of pairwise disjoint edges in mask: a lower bound for the cover number */
    unsigned long long used = 0; int c = 0;
    for (int e = 0; e < n2; e++) if (mask >> e & 1) {
        unsigned long long vs = (1ULL << E[e][0]) | (1ULL << E[e][1]) | (1ULL << E[e][2]);
        if (!(vs & used)) { used |= vs; c++; }
    }
    return c;
}
static int has_cover(unsigned long long mask, int k) {
    if (!mask) return 1;
    if (k == 0) return 0;
    if (greedy_lb(mask) > k) return 0;
    int e = __builtin_ctzll(mask);
    for (int i = 0; i < 3; i++) {
        int v = E[e][i];
        if (has_cover(mask & ~vmask_edges[v], k - 1)) return 1;
    }
    return 0;
}
static int tau_exact(void) {
    unsigned long long all = (n2 == 64) ? ~0ULL : ((1ULL << n2) - 1);
    for (int k = 0; k <= n2; k++) if (has_cover(all, k)) return k;
    return n2;
}
static int is_edge(int a, int b, int c) {
    /* is {a,b,c} an edge? */
    unsigned long long m = vmask_edges[a] & vmask_edges[b] & vmask_edges[c];
    return m != 0;
}
static int has_F7(void) {
    for (int c = 0; c < n1; c++) {
        int inc[MAXE], ni = 0;
        for (int e = 0; e < n2; e++) if (vmask_edges[c] >> e & 1) inc[ni++] = e;
        if (ni < 3) continue;
        for (int x = 0; x < ni; x++) for (int y = x + 1; y < ni; y++) for (int z = y + 1; z < ni; z++) {
            int P[3][2], q = 0;
            int es[3] = {inc[x], inc[y], inc[z]};
            for (int r = 0; r < 3; r++) { q = 0; for (int i = 0; i < 3; i++) if (E[es[r]][i] != c) P[r][q++] = E[es[r]][i]; }
            for (int a = 0; a < 2; a++) for (int b = 0; b < 2; b++) for (int g = 0; g < 2; g++) {
                if (is_edge(P[0][a], P[1][b], P[2][g]) && is_edge(P[0][1 - a], P[1][1 - b], P[2][1 - g])) return 1;
            }
        }
    }
    return 0;
}
static int matchV[MAXV], seenV[MAXV], stampc;
static int forbidden_u, forbidden_v;
static int try_edge(int e) {
    for (int i = 0; i < 3; i++) {
        int v = E[e][i];
        if (v == forbidden_u || v == forbidden_v || seenV[v] == stampc) continue;
        seenV[v] = stampc;
        if (matchV[v] < 0 || try_edge(matchV[v])) { matchV[v] = e; return 1; }
    }
    return 0;
}
static int P3_ok(void) {
    if (n2 > n1 - 2) return 0;
    for (int u = 0; u < n1; u++) for (int v = u + 1; v < n1; v++) {
        forbidden_u = u; forbidden_v = v;
        for (int i = 0; i < n1; i++) matchV[i] = -1;
        for (int e = 0; e < n2; e++) { stampc++; if (!try_edge(e)) return 0; }
    }
    return 1;
}
static int connected(void) {
    int seen[MAXV] = {0}, st[MAXV], sp = 0, cnt = 1; seen[0] = 1; st[sp++] = 0;
    while (sp) { int v = st[--sp];
        for (int e = 0; e < n2; e++) if (vmask_edges[v] >> e & 1) for (int i = 0; i < 3; i++) { int w = E[e][i]; if (!seen[w]) { seen[w] = 1; cnt++; st[sp++] = w; } } }
    return cnt == n1;
}
int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: hfilt n1 n2 t D [print]\n"); return 2; }
    n1 = atoi(argv[1]); n2 = atoi(argv[2]); T = atoi(argv[3]); Dmax = atoi(argv[4]); int pr = argc > 5;
    if (n1 + n2 > 62 || n2 > MAXE || n1 > 63) { fprintf(stderr, "too big\n"); return 2; }
    static unsigned char adj[MAXV][MAXV]; static char line[4096];
    long long total = 0, badfmt = 0, nonlin = 0, disc = 0, degbad = 0, tausmall = 0, f7 = 0, p3 = 0, survivors = 0, taubig = 0;
    long long tauhist[MAXE + 1]; memset(tauhist, 0, sizeof tauhist);
    while (fgets(line, sizeof line, stdin)) {
        int L = strlen(line); while (L && (line[L - 1] == '\n' || line[L - 1] == '\r')) line[--L] = 0;
        if (!L || line[0] == '>') continue;
        total++;
        int n = decode(line, adj);
        if (n != n1 + n2) { badfmt++; continue; }
        int ok = 1;
        for (int i = 0; i < n1 && ok; i++) for (int j = 0; j < n1; j++) if (adj[i][j]) ok = 0;
        for (int i = n1; i < n && ok; i++) for (int j = n1; j < n; j++) if (adj[i][j]) ok = 0;
        for (int e = 0; e < n2 && ok; e++) { int q = 0; for (int v = 0; v < n1; v++) if (adj[n1 + e][v]) { if (q < 3) E[e][q] = v; q++; } if (q != 3) ok = 0; }
        if (!ok) { badfmt++; continue; }
        memset(vmask_edges, 0, sizeof vmask_edges); memset(deg, 0, sizeof deg);
        for (int e = 0; e < n2; e++) for (int i = 0; i < 3; i++) { vmask_edges[E[e][i]] |= 1ULL << e; deg[E[e][i]]++; }
        int lin = 1;
        for (int a = 0; a < n2 && lin; a++) for (int b = a + 1; b < n2; b++) { int c = 0; for (int i = 0; i < 3; i++) for (int j = 0; j < 3; j++) if (E[a][i] == E[b][j]) c++; if (c > 1) { lin = 0; break; } }
        if (!lin) { nonlin++; continue; }
        if (!connected()) { disc++; continue; }
        int dm = 0; for (int v = 0; v < n1; v++) if (deg[v] > dm) dm = deg[v];
        if (dm > Dmax) { degbad++; continue; }
        unsigned long long all = (1ULL << n2) - 1;
        if (has_cover(all, T - 1)) { tausmall++; continue; }
        int tau = tau_exact(); tauhist[tau]++;
        if (has_F7()) { f7++; continue; }
        if (!P3_ok()) { p3++; continue; }
        if (tau != T) { taubig++; continue; }
        survivors++;
        if (pr) { printf("FOUND:"); for (int e = 0; e < n2; e++) printf(" (%d,%d,%d)", E[e][0], E[e][1], E[e][2]); printf("\n"); }
    }
    printf("SUMMARY n1=%d n2=%d t=%d D=%d total=%lld badfmt=%lld nonlinear=%lld disconnected=%lld deg_too_big=%lld tau_lt_t=%lld F7=%lld P3_violated=%lld tau_gt_t=%lld survivors=%lld taudist(>=t):",
           n1, n2, T, Dmax, total, badfmt, nonlin, disc, degbad, tausmall, f7, p3, taubig, survivors);
    for (int k = 0; k <= n2; k++) if (tauhist[k]) printf(" %d:%lld", k, tauhist[k]);
    printf("\n");
    return 0;
}
