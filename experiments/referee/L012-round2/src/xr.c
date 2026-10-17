/* xr.c -- referee round 2 (L012): independent extension enumerator.
   Input lines "m a b c ..." (graph G on NG vertices).  Args: NG d EP T.
   Admissible pair {a<b}: deg_G(a),deg_G(b) <= EP and no edge of G contains both.
   Output: every set of d pairwise disjoint admissible pairs such that tau(G + {NG,a_i,b_i}) >= T, printed as
   "HIT: (edges of G) (a1,b1,NG) ..." -- each set exactly once.
   tau(G) exact by branching; if tau(G) >= T every d-set is a hit (free mode); if tau(G) = T-1 all (T-1)-covers of G are listed by
   brute force over all (T-1)-subsets, and a d-set is a hit iff every such cover is disjoint from one of its pairs (kill search with
   exclusion; the branching cover is chosen dynamically among the first 4 alive covers: fewest available vertices outside it).
   tau(G) < T-1: no hits (tau(H) <= tau(G)+1).  No F7 pruning. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned long long u64;
#define MAXC 200000
#define MAXP 512
static int NG, D, EP, T, m, ed[64][3], deg[64];
static unsigned emask[64];
static int np, pa[MAXP], pb[MAXP]; static unsigned pmask[MAXP];
static int nc, CW; static unsigned cov[MAXC];
static u64 *kill;            /* kill[p*CW + w] */
static u64 hits, nodes; static int chosen[16];
static char linebuf[1 << 16];
static int tau_rec(unsigned sel, int k, int best) {   /* min cover size >= k extending sel; returns best found */
    if (k >= best) return best;
    int e; for (e = 0; e < m; e++) if (!(sel & emask[e])) break;
    if (e == m) return k;
    for (int t = 0; t < 3; t++) { int r = tau_rec(sel | (1u << ed[e][t]), k + 1, best); if (r < best) best = r; }
    return best;
}
static void out_hit(int k) {
    hits++;
    printf("HIT:"); for (int e = 0; e < m; e++) printf(" (%d,%d,%d)", ed[e][0], ed[e][1], ed[e][2]);
    for (int i = 0; i < k; i++) printf(" (%d,%d,%d)", pa[chosen[i]], pb[chosen[i]], NG);
    printf("\n");
}
/* completions: choose r more pairs from allowed (not excluded, disjoint from used), index > last, pairwise disjoint */
static void complete(int k, int r, unsigned used, const u64 *excl, int start) {
    if (r == 0) { out_hit(k); return; }
    for (int p = start; p < np; p++) {
        if (excl[p >> 6] >> (p & 63) & 1) continue;
        if (pmask[p] & used) continue;
        chosen[k] = p; complete(k + 1, r - 1, used | pmask[p], excl, p + 1);
    }
}
static void dfs(int k, unsigned used, u64 *alive, u64 *excl) {
    nodes++;
    int first = -1;
    for (int w = 0; w < CW; w++) if (alive[w]) { first = w * 64 + __builtin_ctzll(alive[w]); break; }
    if (first < 0) { complete(k, D - k, used, excl, 0); return; }
    if (k == D) return;
    unsigned full = (NG >= 32) ? 0xffffffffu : ((1u << NG) - 1);
    /* choose among the first 4 alive covers the one with fewest available vertices outside it */
    int best = -1, bestc = 1 << 30, seen = 0;
    for (int w = first >> 6; w < CW && seen < 4; w++) { u64 z = alive[w];
        while (z && seen < 4) { int c = w * 64 + __builtin_ctzll(z); z &= z - 1; seen++;
            int cnt = __builtin_popcount(full & ~cov[c] & ~used);
            if (cnt < bestc) { bestc = cnt; best = c; } } }
    unsigned outside = full & ~cov[best] & ~used;
    u64 ex2[MAXP / 64]; memcpy(ex2, excl, sizeof(u64) * (MAXP / 64));
    u64 *al2 = alloca(sizeof(u64) * CW);
    for (int p = 0; p < np; p++) {
        if ((pmask[p] & outside) != pmask[p]) continue;      /* p must avoid the cover and the used vertices */
        if (ex2[p >> 6] >> (p & 63) & 1) continue;
        for (int w = 0; w < CW; w++) al2[w] = alive[w] & ~kill[(size_t)p * CW + w];
        chosen[k] = p;
        dfs(k + 1, used | pmask[p], al2, ex2);
        ex2[p >> 6] |= 1ULL << (p & 63);                    /* exclude this sibling from later branches */
    }
}
int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: xr NG d EP T\n"); return 1; }
    NG = atoi(argv[1]); D = atoi(argv[2]); EP = atoi(argv[3]); T = atoi(argv[4]);
    if (NG > 31) { fprintf(stderr, "NG too big\n"); return 1; }
    kill = malloc(sizeof(u64) * (size_t)MAXP * (MAXC / 64 + 1));
    long G = 0, freeg = 0, lowg = 0; u64 TH = 0; int maxcov = 0;
    while (fgets(linebuf, sizeof linebuf, stdin)) {
        char *p = linebuf; int k, mm; if (sscanf(p, "%d%n", &mm, &k) != 1) continue; p += k; m = mm;
        memset(deg, 0, sizeof deg);
        for (int e = 0; e < m; e++) { if (sscanf(p, "%d %d %d%n", &ed[e][0], &ed[e][1], &ed[e][2], &k) != 3) { fprintf(stderr, "parse\n"); return 2; } p += k;
            emask[e] = 0; for (int t = 0; t < 3; t++) { if (ed[e][t] < 0 || ed[e][t] >= NG) { fprintf(stderr, "label\n"); return 2; } emask[e] |= 1u << ed[e][t]; deg[ed[e][t]]++; } }
        G++;
        np = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > EP || deg[b] > EP) continue;
            unsigned pm = (1u << a) | (1u << b); int bad = 0;
            for (int e = 0; e < m; e++) if ((emask[e] & pm) == pm) { bad = 1; break; }
            if (bad) continue;
            if (np >= MAXP) { fprintf(stderr, "too many pairs\n"); return 3; }
            pa[np] = a; pb[np] = b; pmask[np] = pm; np++;
        }
        int tg = tau_rec(0, 0, 64);
        u64 h0 = hits;
        u64 ex[MAXP / 64]; memset(ex, 0, sizeof ex);
        if (tg >= T) { freeg++; complete(0, D, 0, ex, 0); }
        else if (tg == T - 1) {
            nc = 0; int r = T - 1;
            if (r == 0) { cov[nc++] = 0; }
            else {
                unsigned x = (1u << r) - 1, lim = 1u << NG;
                while (x < lim) {
                    int ok = 1; for (int e = 0; e < m; e++) if (!(x & emask[e])) { ok = 0; break; }
                    if (ok) { if (nc >= MAXC) { fprintf(stderr, "too many covers\n"); return 4; } cov[nc++] = x; }
                    unsigned c = x & -x, rr = x + c; x = (((rr ^ x) >> 2) / c) | rr;
                }
            }
            if (nc > maxcov) maxcov = nc;
            CW = (nc + 63) / 64;
            for (int q = 0; q < np; q++) { for (int w = 0; w < CW; w++) kill[(size_t)q * CW + w] = 0;
                for (int c = 0; c < nc; c++) if (!(cov[c] & pmask[q])) kill[(size_t)q * CW + (c >> 6)] |= 1ULL << (c & 63); }
            u64 *alive = calloc(CW, sizeof(u64));
            for (int c = 0; c < nc; c++) alive[c >> 6] |= 1ULL << (c & 63);
            dfs(0, 0, alive, ex); free(alive);
        } else lowg++;
        TH += hits - h0;
        fprintf(stderr, "G%ld tau=%d pairs=%d covers=%d hits=%llu\n", G, tg, np, (tg == T - 1) ? nc : -1, hits - h0);
    }
    fprintf(stderr, "XRSUMMARY graphs=%ld free=%ld low=%ld hits=%llu nodes=%llu maxcovers=%d\n", G, freeg, lowg, TH, nodes, maxcov);
    printf("XRSUMMARY graphs=%ld free=%ld low=%ld hits=%llu nodes=%llu maxcovers=%d\n", G, freeg, lowg, TH, nodes, maxcov);
    return 0;
}
