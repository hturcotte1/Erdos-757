/* Referee L017 round 1 (independent code): Theorem 7 check on genbg output (linear 3-graphs, max degree <= 2).
   For each: tau by exhaustive branch and bound; dual graph G (vertices = edges of H, one G-edge per degree-2
   vertex); nu(G) by subset DP; checks tau == m - nu, and s = 3n+2m-11tau == 3*n0 + 11nu - 3|E(G)| (n0 = 0 here). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
static int n1, n2; static u64 em[64];
static int hitk(u64 unc, int k) {
    if (!unc) return 1; if (k == 0) return 0;
    u64 used = 0; int c = 0; u64 t = unc;
    while (t) { int i = __builtin_ctzll(t); t &= t - 1; if (!(em[i] & used)) { used |= em[i]; c++; } }
    if (c > k) return 0;
    int i = __builtin_ctzll(unc); u64 mk = em[i];
    while (mk) { int v = __builtin_ctzll(mk); mk &= mk - 1; u64 rest = 0;
        for (int j = 0; j < n2; j++) if ((unc >> j & 1) && !(em[j] >> v & 1)) rest |= 1ULL << j;
        if (hitk(rest, k - 1)) return 1; }
    return 0;
}
static unsigned gnb[64]; static signed char memo[1 << 22];
static int nu(unsigned mask) {
    if (!mask) return 0; if (memo[mask] >= 0) return memo[mask];
    int v = __builtin_ctz(mask); unsigned rest = mask & ~(1u << v); int best = nu(rest);
    unsigned c = gnb[v] & rest; while (c) { int u = __builtin_ctz(c); c &= c - 1; int t = 1 + nu(rest & ~(1u << u)); if (t > best) best = t; }
    return memo[mask] = best;
}
int main(int argc, char **argv) {
    n1 = atoi(argv[1]); n2 = atoi(argv[2]); int N = n1 + n2; char line[4096];
    long long cnt = 0, bad = 0, mins = 1 << 30;
    while (fgets(line, sizeof line, stdin)) {
        int len = strlen(line); while (len && line[len-1] == '\n') line[--len] = 0;
        if (!len || line[0] == '>') continue;
        static int adj[64][64]; memset(adj, 0, sizeof adj); int bit = 0;
        for (int j = 1; j < N; j++) for (int i = 0; i < j; i++) { int b = ((line[1 + bit/6] - 63) >> (5 - bit%6)) & 1; bit++; adj[i][j] = adj[j][i] = b; }
        int deg[64] = {0};
        for (int e = 0; e < n2; e++) { em[e] = 0; for (int v = 0; v < n1; v++) if (adj[n1+e][v]) { em[e] |= 1ULL << v; deg[v]++; } }
        int tau = 0; u64 all = (1ULL << n2) - 1; while (!hitk(all, tau)) tau++;
        memset(gnb, 0, sizeof gnb); int EG = 0, n0 = 0;
        for (int v = 0; v < n1; v++) {
            if (deg[v] == 0) n0++;
            if (deg[v] > 2) { fprintf(stderr, "deg>2\n"); return 1; }
            if (deg[v] == 2) { int a = -1, b = -1; for (int e = 0; e < n2; e++) if (em[e] >> v & 1) { if (a < 0) a = e; else b = e; }
                if (gnb[a] >> b & 1) { fprintf(stderr, "multi-edge in dual\n"); return 1; }
                gnb[a] |= 1u << b; gnb[b] |= 1u << a; EG++; }
        }
        memset(memo, -1, 1u << n2); int x = nu((1u << n2) - 1);
        int s = 3*n1 + 2*n2 - 11*tau;
        cnt++;
        if (tau != n2 - x || s != 3*n0 + 11*x - 3*EG) { bad++; printf("BAD %s\n", line); }
        if (s < mins) mins = s;
    }
    printf("n=%d m=%d graphs=%lld bad=%lld min_slack=%lld\n", n1, n2, cnt, bad, cnt ? mins : -1);
    return 0;
}
