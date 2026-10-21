/* g6filt.c -- referee L016 round 1 (own code).  Filter for genbg output (bipartite graphs in graph6; the first n1 nodes
   are the vertices, the other n2 nodes the edges of a 3-graph).
   Usage: g6filt n1 n2 t D < graphs.g6
   For each graph: every edge node must have degree 3 (else counted 'baddeg3'); linearity (two edges share <= 1 vertex);
   max vertex degree <= D; connectivity of all n1 vertices; F7 test; (P3) by Hall with surplus 2; exact tau (own branch and
   bound with matching lower bound).  Prints counters, the tau histogram, and every member of C(n1,n2,t,D) as FOUND line. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int N1, N2, TT, DD;
static uint32_t E[64]; static int m;
static int lbound(uint32_t S) { uint32_t used = 0; int k = 0; for (int i = 0; i < m; i++) if (!(E[i] & S) && !(E[i] & used)) { used |= E[i]; k++; } return k; }
static int hascov(uint32_t S, int budget, uint32_t forb) {
    int best = -1, bc = 4;
    for (int i = 0; i < m; i++) if (!(E[i] & S)) { int c = __builtin_popcount(E[i] & ~forb); if (c < bc) { bc = c; best = i; if (c == 0) break; } }
    if (best < 0) return 1;
    if (bc == 0 || budget == 0) return 0;
    if (lbound(S) > budget) return 0;
    uint32_t f2 = forb;
    for (uint32_t r = E[best] & ~forb; r; r &= r - 1) { uint32_t v = r & -r; if (hascov(S | v, budget - 1, f2)) return 1; f2 |= v; }
    return 0;
}
static int tau(void) { for (int k = 0; k <= m; k++) if (hascov(0, k, 0)) return k; return -1; }
static int isedge(uint32_t mask) { for (int i = 0; i < m; i++) if (E[i] == mask) return 1; return 0; }
static int has_f7(void) {
    for (int v = 0; v < N1; v++) {
        int at[64], na = 0;
        for (int i = 0; i < m; i++) if (E[i] >> v & 1) at[na++] = i;
        for (int i = 0; i < na; i++) for (int j = i + 1; j < na; j++) for (int k = j + 1; k < na; k++) {
            uint32_t A0 = E[at[i]] & ~(1u << v), A1 = E[at[j]] & ~(1u << v), A2 = E[at[k]] & ~(1u << v);
            if ((A0 & A1) || (A0 & A2) || (A1 & A2)) continue;
            int a0 = __builtin_ctz(A0), a1 = 31 - __builtin_clz(A0), b0 = __builtin_ctz(A1), b1 = 31 - __builtin_clz(A1), c0 = __builtin_ctz(A2), c1 = 31 - __builtin_clz(A2);
            for (int sb = 0; sb < 2; sb++) for (int sc = 0; sc < 2; sc++) {
                int bx = sb ? b1 : b0, by = sb ? b0 : b1, cx = sc ? c1 : c0, cy = sc ? c0 : c1;
                if (isedge((1u << a0) | (1u << bx) | (1u << cx)) && isedge((1u << a1) | (1u << by) | (1u << cy))) return 1;
            }
        }
    }
    return 0;
}
static uint32_t Lm[80]; static int mr[32];
static int aug(int i, uint32_t *vis) { for (uint32_t r = Lm[i] & ~*vis; r; r &= r - 1) { int v = __builtin_ctz(r); *vis |= 1u << v; if (mr[v] < 0 || aug(mr[v], vis)) { mr[v] = i; return 1; } } return 0; }
static int p3ok(void) {
    int base[32]; for (int v = 0; v < 32; v++) mr[v] = -1;
    for (int i = 0; i < m; i++) Lm[i] = E[i];
    for (int i = 0; i < m; i++) { uint32_t vis = 0; if (!aug(i, &vis)) return 0; }
    memcpy(base, mr, sizeof base);
    for (int e = 0; e < m; e++) { memcpy(mr, base, sizeof base); Lm[m] = E[e]; Lm[m + 1] = E[e];
        uint32_t vis = 0; if (!aug(m, &vis)) return 0; vis = 0; if (!aug(m + 1, &vis)) return 0; }
    return 1;
}
static int connected(void) {
    uint32_t seen = 1u, fr = 1u;
    while (fr) { uint32_t nf = 0; for (int i = 0; i < m; i++) if (E[i] & fr) nf |= E[i]; nf &= ~seen; seen |= nf; fr = nf; }
    uint32_t all = (N1 == 32) ? 0xffffffffu : ((1u << N1) - 1); return seen == all;
}
int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: g6filt n1 n2 t D\n"); return 1; }
    N1 = atoi(argv[1]); N2 = atoi(argv[2]); TT = atoi(argv[3]); DD = atoi(argv[4]);
    int n = N1 + N2; if (N1 > 31 || n > 62) { fprintf(stderr, "limits\n"); return 1; }
    static char line[4096]; unsigned long long tot = 0, baddeg3 = 0, nonlin = 0, degbad = 0, disc = 0, f7 = 0, p3bad = 0, members = 0, hist[64] = {0}, histC[64] = {0};
    static unsigned char adj[64][64];
    while (fgets(line, sizeof line, stdin)) {
        int L = strlen(line); while (L && (line[L - 1] == '\n' || line[L - 1] == '\r')) line[--L] = 0;
        if (!L) continue;
        if (line[0] - 63 != n) { fprintf(stderr, "n mismatch %d\n", line[0] - 63); return 2; }
        tot++; memset(adj, 0, sizeof adj);
        int bit = 0; const char *p = line + 1;
        for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) {
            int byte = bit / 6, off = 5 - bit % 6; int x = (p[byte] - 63) >> off & 1; bit++;
            if (x) adj[i][j] = adj[j][i] = 1;
        }
        int ok = 1; m = 0; int deg[32] = {0};
        for (int j = N1; j < n; j++) { uint32_t e = 0; int c = 0; for (int i = 0; i < n; i++) if (adj[i][j]) { if (i >= N1) { ok = 0; } else { e |= 1u << i; c++; } }
            if (c != 3) ok = 0; E[m++] = e; }
        for (int i = 0; i < N1; i++) for (int k = 0; k < N1; k++) if (adj[i][k]) ok = 0;
        if (!ok) { baddeg3++; continue; }
        int lin = 1; for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++) if (__builtin_popcount(E[a] & E[b]) > 1) lin = 0;
        if (!lin) { nonlin++; continue; }
        int mx = 0; for (int i = 0; i < m; i++) for (uint32_t r = E[i]; r; r &= r - 1) { int v = __builtin_ctz(r); if (++deg[v] > mx) mx = deg[v]; }
        if (mx > DD) { degbad++; continue; }
        if (!connected()) { disc++; continue; }
        int t = tau(); hist[t]++;
        if (has_f7()) { f7++; continue; }
        if (!p3ok()) { p3bad++; continue; }
        histC[t]++;
        if (t == TT) { members++; printf("FOUND:"); for (int i = 0; i < m; i++) { int v[3], k = 0; for (uint32_t r = E[i]; r; r &= r - 1) v[k++] = __builtin_ctz(r); printf(" (%d,%d,%d)", v[0], v[1], v[2]); } printf("\n"); }
    }
    printf("G6FILT n1=%d n2=%d t=%d D=%d total=%llu baddeg3=%llu nonlinear=%llu degbad=%llu disconnected=%llu F7=%llu P3bad=%llu members=%llu\n", N1, N2, TT, DD, tot, baddeg3, nonlin, degbad, disc, f7, p3bad, members);
    printf("TAUHIST(all connected linear):"); for (int k = 0; k < 64; k++) if (hist[k]) printf(" %d:%llu", k, hist[k]); printf("\n");
    printf("TAUHIST(in C):"); for (int k = 0; k < 64; k++) if (histC[k]) printf(" %d:%llu", k, histC[k]); printf("\n");
    return 0;
}
