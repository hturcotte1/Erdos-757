/* Referee L011: membership in C and invariants, written from scratch.
   Usage: rfilt N TAG [v] < file      (lines "TAG: (a,b,c) ..."; every label < N is a point, so isolated points count)
   For each 3-graph:
     LIN  : any two edges share <= 1 point;
     F7   : explicit embedding of F7 = {012,034,056,135,246} as a (not necessarily induced) subhypergraph, by backtracking
            over the images of the edges 012, 034, 056 (ordered) and then checking that the images of 135 and 246 are edges;
     P3   : e(S) <= |S|-2 for all |S| >= 2, tested as |V(F)| >= |F|+2 for every nonempty edge set F (enumerated by DFS);
            certificate: the edge set F with the smallest |V(F)|-|F|;
     TAU  : exact transversal number (branch and bound);
     CONN : connected on all N points (union-find; an isolated point is its own component);
     DMAX : maximum degree.
   Output: with 'v', one line per graph "R: lin f7 p3ok tau conn dmax ncomp | F7 points | P3 certificate S"; always a
   summary line "FSUMMARY ...". inC = lin && !f7 && p3ok. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static int NE, N; static uint32_t E[64]; static uint64_t INC[32];
static int isedge(uint32_t m) { for (int i = 0; i < NE; i++) if (E[i] == m) return 1; return 0; }
static int img[7], f7pts[7];
static int f7_rec(void) {
    /* images of 0,1,2 from an edge (ordered), then 3,4 from an edge through img0, then 5,6 from another edge through img0 */
    for (int i = 0; i < NE; i++) {
        int v[3], k = 0; for (int x = 0; x < N; x++) if (E[i] >> x & 1) v[k++] = x;
        int perm[6][3] = {{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
        for (int p = 0; p < 6; p++) {
            img[0] = v[perm[p][0]]; img[1] = v[perm[p][1]]; img[2] = v[perm[p][2]];
            for (int j = 0; j < NE; j++) {
                if (j == i || !(E[j] >> img[0] & 1)) continue;
                uint32_t r1 = E[j] & ~(1u << img[0]); if (__builtin_popcount(r1) != 2) continue;
                int a1 = __builtin_ctz(r1), b1 = 31 - __builtin_clz(r1);
                for (int o1 = 0; o1 < 2; o1++) {
                    img[3] = o1 ? b1 : a1; img[4] = o1 ? a1 : b1;
                    for (int l = 0; l < NE; l++) {
                        if (l == i || l == j || !(E[l] >> img[0] & 1)) continue;
                        uint32_t r2 = E[l] & ~(1u << img[0]); if (__builtin_popcount(r2) != 2) continue;
                        int a2 = __builtin_ctz(r2), b2 = 31 - __builtin_clz(r2);
                        for (int o2 = 0; o2 < 2; o2++) {
                            img[5] = o2 ? b2 : a2; img[6] = o2 ? a2 : b2;
                            uint32_t all = 0; int inj = 1;
                            for (int t = 0; t < 7; t++) { if (all >> img[t] & 1) { inj = 0; break; } all |= 1u << img[t]; }
                            if (!inj) continue;
                            if (isedge((1u << img[1]) | (1u << img[3]) | (1u << img[5])) && isedge((1u << img[2]) | (1u << img[4]) | (1u << img[6]))) {
                                memcpy(f7pts, img, sizeof img); return 1; }
                        }
                    }
                }
            }
        }
    }
    return 0;
}
static int best; static uint64_t bestF; static uint32_t bestU;
static void p3_dfs(int i, uint64_t F, uint32_t U, int cnt) {   /* stops as soon as a violation (d <= 1) is found */
    if (cnt > 0) { int d = __builtin_popcount(U) - cnt; if (d < best) { best = d; bestF = F; bestU = U; } }
    for (int j = i; j < NE && best >= 2; j++) p3_dfs(j + 1, F | (1ull << j), U | E[j], cnt + 1);
}
static int cover_le(uint64_t left, int k) {
    if (!left) return 1; if (k <= 0) return 0;
    { uint32_t used = 0; int cnt = 0; uint64_t l = left;
      while (l) { int i = __builtin_ctzll(l); l &= l - 1; if (!(E[i] & used)) { used |= E[i]; if (++cnt > k) return 0; } } }
    int i = __builtin_ctzll(left); uint32_t e = E[i];
    while (e) { int x = __builtin_ctz(e); e &= e - 1; if (cover_le(left & ~INC[x], k - 1)) return 1; }
    return 0;
}
static int par[32]; static int fnd(int x) { while (par[x] != x) x = par[x] = par[par[x]]; return x; }
int main(int argc, char **argv) {
    N = atoi(argv[1]); const char *tag = argv[2]; int verbose = argc > 3 && argv[3][0] == 'v';
    static char line[1 << 16]; size_t tl = strlen(tag);
    unsigned long long tot = 0, nlin = 0, nf7 = 0, np3bad = 0, nf7free_p3bad = 0, ninC = 0, nconn = 0, ninC_conn = 0;
    int tmin = 99, tmax = -1, dmaxmax = 0; unsigned long long taucount[32] = {0};
    while (fgets(line, sizeof line, stdin)) {
        if (strncmp(line, tag, tl) || line[tl] != ':') continue;
        NE = 0; char *p = line + tl + 1; int a, b, c;
        while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) != 3) return 2;
            if (a >= N || b >= N || c >= N || a == b || b == c || a == c) { fprintf(stderr, "bad edge\n"); return 3; }
            E[NE++] = (1u << a) | (1u << b) | (1u << c); p++; }
        tot++;
        int lin = 1; for (int i = 0; i < NE; i++) for (int j = i + 1; j < NE; j++) if (__builtin_popcount(E[i] & E[j]) > 1) lin = 0;
        int f7 = f7_rec();
        best = 1000; p3_dfs(0, 0, 0, 0); int p3ok = best >= 2;
        for (int x = 0; x < N; x++) INC[x] = 0;
        for (int i = 0; i < NE; i++) for (int x = 0; x < N; x++) if (E[i] >> x & 1) INC[x] |= 1ull << i;
        int t = 0; uint64_t all = (1ull << NE) - 1; while (!cover_le(all, t)) t++;
        int dmax = 0; for (int x = 0; x < N; x++) { int d = __builtin_popcountll(INC[x]); if (d > dmax) dmax = d; }
        for (int x = 0; x < N; x++) par[x] = x;
        for (int i = 0; i < NE; i++) { int v[3], k = 0; for (int x = 0; x < N; x++) if (E[i] >> x & 1) v[k++] = x; par[fnd(v[1])] = fnd(v[0]); par[fnd(v[2])] = fnd(v[0]); }
        int ncomp = 0; for (int x = 0; x < N; x++) if (fnd(x) == x) ncomp++;
        int conn = ncomp == 1, inC = lin && !f7 && p3ok;
        nlin += lin; nf7 += f7; np3bad += !p3ok; nf7free_p3bad += (!f7 && !p3ok); ninC += inC; nconn += conn; ninC_conn += inC && conn;
        if (t < tmin) tmin = t; if (t > tmax) tmax = t; if (dmax > dmaxmax) dmaxmax = dmax; taucount[t]++;
        if (verbose) {
            printf("R: lin=%d f7=%d p3ok=%d tau=%d conn=%d dmax=%d ncomp=%d |", lin, f7, p3ok, t, conn, dmax, ncomp);
            if (f7) { printf(" F7img="); for (int k = 0; k < 7; k++) printf("%d%s", f7pts[k], k < 6 ? "," : ""); }
            if (!p3ok) { printf(" P3S="); int fs = 1; for (int x = 0; x < N; x++) if (bestU >> x & 1) { printf(fs ? "%d" : ",%d", x); fs = 0; } printf(" eF=%d", __builtin_popcountll(bestF)); }
            printf(" | %s", line + tl + 1);
        }
    }
    printf("FSUMMARY tag=%s N=%d total=%llu linear=%llu F7=%llu P3bad=%llu F7free_P3bad=%llu inC=%llu connected=%llu inC_and_connected=%llu tau_range=[%d,%d] dmax=%d tau_counts:",
           tag, N, tot, nlin, nf7, np3bad, nf7free_p3bad, ninC, nconn, ninC_conn, tmin, tmax, dmaxmax);
    for (int t = 0; t < 32; t++) if (taucount[t]) printf(" %d:%llu", t, taucount[t]);
    printf("\n");
    return 0;
}
