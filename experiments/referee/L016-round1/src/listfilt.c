/* listfilt.c -- referee L016 round 1 (own code; derived from g6filt.c).  Filter for stored lists; originally: filter for genbg output (bipartite graphs in graph6; the first n1 nodes
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
    if (argc < 5) { fprintf(stderr, "usage: listfilt n m t D < cell.txt\n"); return 1; }
    N1 = atoi(argv[1]); N2 = atoi(argv[2]); TT = atoi(argv[3]); DD = atoi(argv[4]);
    if (N1 > 31) { fprintf(stderr, "limits\n"); return 1; }
    static char line[1 << 16]; unsigned long long tot = 0, bad = 0, badfmt = 0, nonlin = 0, degbad = 0, disc = 0, f7 = 0, p3bad = 0, taubad = 0, ok = 0;
    while (fgets(line, sizeof line, stdin)) {
        if (strncmp(line, "FOUND:", 6)) continue;
        tot++; m = 0; int fmt = 1; char *p = line + 6; int a, b, c, k;
        while (sscanf(p, " (%d,%d,%d)%n", &a, &b, &c, &k) == 3) {
            if (a < 0 || b < 0 || c < 0 || a >= N1 || b >= N1 || c >= N1 || a == b || a == c || b == c || m >= 63) fmt = 0;
            else E[m++] = (1u << a) | (1u << b) | (1u << c);
            p += k;
        }
        if (m != N2) fmt = 0;
        for (int i = 0; i < m && fmt; i++) for (int j = i + 1; j < m; j++) if (E[i] == E[j]) fmt = 0;
        if (!fmt) { badfmt++; bad++; continue; }
        int lin = 1; for (int x = 0; x < m; x++) for (int y = x + 1; y < m; y++) if (__builtin_popcount(E[x] & E[y]) > 1) lin = 0;
        if (!lin) { nonlin++; bad++; continue; }
        int deg[32] = {0}, mx = 0; for (int i = 0; i < m; i++) for (uint32_t r = E[i]; r; r &= r - 1) { int v = __builtin_ctz(r); if (++deg[v] > mx) mx = deg[v]; }
        if (mx > DD) { degbad++; bad++; continue; }
        if (!connected()) { disc++; bad++; continue; }
        if (has_f7()) { f7++; bad++; continue; }
        if (!p3ok()) { p3bad++; bad++; continue; }
        if (hascov(0, TT - 1, 0) || !hascov(0, TT, 0)) { taubad++; bad++; continue; }
        ok++;
    }
    printf("LISTFILT n=%d m=%d t=%d D=%d total=%llu ok=%llu bad=%llu (format %llu nonlinear %llu degree %llu disconnected %llu F7 %llu P3 %llu tau %llu)\n",
           N1, N2, TT, DD, tot, ok, bad, badfmt, nonlin, degbad, disc, f7, p3bad, taubad);
    return 0;
}
