/* Referee L017 round 1 (independent code): read genbg bipartite graph6 lines (first class = n1 hypergraph
   vertices, second class = n2 hyperedges of size 3), compute for every vertex subset W the I11 slack of the
   induced subgraph H[W] (tau via alpha, alpha by subset DP), and report every violator (s(H)<0) together
   with whether it is vertex-critical (s(H[W]) >= 0 for every proper W).  n1 <= 16.
   usage: vcrit n1 n2 < graph6 ; prints "VIOL crit=<0/1> n m tau s edges..." for each violator, and a summary. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n1, n2;
static unsigned emask[64];
static unsigned char indep[1 << 16], alpha[1 << 16], medges[1 << 16];
int main(int argc, char **argv) {
    if (argc < 3) return 1;
    n1 = atoi(argv[1]); n2 = atoi(argv[2]);
    int N = n1 + n2;
    char line[4096];
    long long ngraphs = 0, nviol = 0, ncrit = 0;
    while (fgets(line, sizeof line, stdin)) {
        int len = strlen(line);
        while (len && (line[len-1] == '\n' || line[len-1] == '\r')) line[--len] = 0;
        if (!len || line[0] == '>') continue;
        int NN = line[0] - 63;
        if (NN != N) { fprintf(stderr, "size mismatch %d %d\n", NN, N); return 1; }
        /* decode adjacency */
        static int adj[64][64];
        memset(adj, 0, sizeof adj);
        int bit = 0;
        for (int j = 1; j < N; j++) for (int i = 0; i < j; i++) {
            int byte = line[1 + bit / 6] - 63;
            int b = (byte >> (5 - bit % 6)) & 1;
            adj[i][j] = adj[j][i] = b;
            bit++;
        }
        for (int e = 0; e < n2; e++) {
            unsigned mk = 0; int c = 0;
            for (int v = 0; v < n1; v++) if (adj[n1 + e][v]) { mk |= 1u << v; c++; }
            for (int f = 0; f < n2; f++) if (adj[n1 + e][n1 + f]) { fprintf(stderr, "not bipartite\n"); return 1; }
            if (c != 3) { fprintf(stderr, "edge size %d\n", c); return 1; }
            emask[e] = mk;
        }
        ngraphs++;
        unsigned full = (1u << n1) - 1;
        for (unsigned W = 0; W <= full; W++) {
            int me = 0, ind = 1;
            for (int e = 0; e < n2; e++) if ((emask[e] & W) == emask[e]) { me++; ind = 0; }
            medges[W] = me; indep[W] = ind;
        }
        for (unsigned W = 0; W <= full; W++) {
            if (indep[W]) { alpha[W] = __builtin_popcount(W); continue; }
            int best = 0;
            for (int v = 0; v < n1; v++) if (W >> v & 1) { int a = alpha[W & ~(1u << v)]; if (a > best) best = a; }
            alpha[W] = best;
        }
        int tau = n1 - alpha[full];
        int s = 3 * n1 + 2 * n2 - 11 * tau;
        if (s >= 0) continue;
        nviol++;
        int crit = 1;
        for (unsigned W = 0; W < full && crit; W++) {
            int w = __builtin_popcount(W);
            int sw = 3 * w + 2 * medges[W] - 11 * (w - alpha[W]);
            if (sw < 0) crit = 0;
        }
        if (crit) ncrit++;
        printf("VIOL crit=%d n=%d m=%d tau=%d s=%d edges=", crit, n1, n2, tau, s);
        for (int e = 0; e < n2; e++) {
            int first = 1;
            printf("(");
            for (int v = 0; v < n1; v++) if (emask[e] >> v & 1) { printf(first ? "%d" : ",%d", v); first = 0; }
            printf(")");
        }
        printf("\n");
    }
    printf("SUMMARY n=%d m=%d graphs=%lld violators=%lld vertex_critical=%lld\n", n1, n2, ngraphs, nviol, ncrit);
    return 0;
}
