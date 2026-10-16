/* Referee round 2 (L002): independent enumerator of ordered midpoint patterns.
 * Written from scratch; does not use e757/ or the round-1 referee code.
 *
 * Class enumerated: vertices 0..n-1 (rank order); for each interior vertex j (1..n-2) either no edge or one
 * triple (i,j,k) with i<j<k (j = midpoint). Constraints:
 *   - linearity: no pair of vertices lies in two triples;
 *   - K30 (monotone midpoints): for triples (i,j,k),(i',j',k') with j<j' it is NOT the case that i>=i' and k>=k';
 *   - alpha(H) <= T, tested EXACTLY at leaves as: every (T+1)-subset of vertices contains a triple.
 * NO F7 filter in the search; F7 containment is computed at each reported leaf by an independent test
 * (5 edges spanning exactly 7 vertices with degree sequence 3,2,2,2,2,2,2; valid because H is linear).
 *
 * Search order: midpoints j = n-2 DOWN TO 1 (opposite to the census engine).
 * Pruning (sound): at the node where midpoints 1..j are undecided, a (T+1)-subset S that contains no placed
 * triple and has no element r in {1..j} with min(S) < r < max(S) can never contain a triple of any completion
 * (a future triple (i,r,k) inside S needs i<r<k all in S and r<=j), so every completion has alpha >= T+1.
 * prune=0 disables this (pure brute force over the class, exact alpha test at every leaf).
 *
 * Usage: ./enum n T maxnone prune print [split_k]
 *   maxnone: number of interior vertices allowed to have no edge (0 = saturated, m = n-2).
 *   print=1: print every leaf with alpha<=T as "P m f7 i,j,k i,j,k ..." (edges sorted lexicographically).
 *   split_k (optional): restrict midpoint n-2 to have right endpoint... no: restrict the edge at midpoint n-2 to
 *            have LEFT endpoint split_k (-1 = none). Used only to cut work into pieces.
 * Summary on stderr: nodes, leaves (all complete patterns reached), and counts by (m, f7) of alpha<=T leaves.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXN 16
#define MAXW 200

static int n, T, maxnone, prune, print_, split = -2;
static int nsub, nw;
static uint64_t *tmask;           /* [(a*n+b)*n+c][nw] subsets containing {a,b,c} */
static uint64_t Dm[MAXN][MAXW];   /* level j: subsets that must already be hit */
static uint64_t full[MAXW];
static int Ei[MAXN], Ej[MAXN], Ek[MAXN], ne;
static uint32_t cov[MAXN];
static long long nodes = 0, leaves = 0, good[MAXN + 1][2];
static uint64_t hitstack[MAXN + 2][MAXW];

static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

static int has_f7_mine(void) {
    int m = ne;
    if (m < 5) return 0;
    uint32_t em[MAXN];
    for (int t = 0; t < m; t++) em[t] = (1u << Ei[t]) | (1u << Ej[t]) | (1u << Ek[t]);
    int idx[5];
    /* all 5-subsets of edges */
    for (idx[0] = 0; idx[0] < m; idx[0]++)
    for (idx[1] = idx[0] + 1; idx[1] < m; idx[1]++)
    for (idx[2] = idx[1] + 1; idx[2] < m; idx[2]++)
    for (idx[3] = idx[2] + 1; idx[3] < m; idx[3]++)
    for (idx[4] = idx[3] + 1; idx[4] < m; idx[4]++) {
        uint32_t u = 0;
        for (int t = 0; t < 5; t++) u |= em[idx[t]];
        if (__builtin_popcount(u) != 7) continue;
        int d3 = 0, d2 = 0;
        for (int v = 0; v < n; v++) {
            if (!((u >> v) & 1)) continue;
            int d = 0;
            for (int t = 0; t < 5; t++) d += (em[idx[t]] >> v) & 1;
            if (d == 3) d3++; else if (d == 2) d2++;
        }
        if (d3 == 1 && d2 == 6) return 1;
    }
    return 0;
}

static int cmp3(const void *a, const void *b) {
    const int *x = a, *y = b;
    for (int t = 0; t < 3; t++) if (x[t] != y[t]) return x[t] - y[t];
    return 0;
}

static void leaf(void) {
    int f = has_f7_mine();
    good[ne][f]++;
    if (print_) {
        int es[MAXN][3];
        for (int t = 0; t < ne; t++) { es[t][0] = Ei[t]; es[t][1] = Ej[t]; es[t][2] = Ek[t]; }
        qsort(es, ne, sizeof es[0], cmp3);
        printf("P %d %d", ne, f);
        for (int t = 0; t < ne; t++) printf(" %d,%d,%d", es[t][0], es[t][1], es[t][2]);
        putchar('\n');
    }
}

static void dfs(int j, int nones) {
    nodes++;
    uint64_t *hit = hitstack[j];
    if (j == 0) {
        leaves++;
        for (int w = 0; w < nw; w++) if (full[w] & ~hit[w]) return;   /* exact: alpha <= T */
        leaf();
        return;
    }
    if (prune) for (int w = 0; w < nw; w++) if (Dm[j][w] & ~hit[w]) return;
    for (int i = 0; i < j; i++) {
        if ((cov[j] >> i) & 1) continue;
        if (j == n - 2 && split > -2 && i != split) continue;
        for (int k = j + 1; k < n; k++) {
            if ((cov[j] >> k) & 1) continue;
            if ((cov[i] >> k) & 1) continue;
            int ok = 1;
            for (int t = 0; t < ne; t++) if (i >= Ei[t] && k >= Ek[t]) { ok = 0; break; }
            if (!ok) continue;
            uint32_t ci = cov[i], cj = cov[j], ck = cov[k];
            cov[i] |= (1u << j) | (1u << k); cov[j] |= (1u << i) | (1u << k); cov[k] |= (1u << i) | (1u << j);
            Ei[ne] = i; Ej[ne] = j; Ek[ne] = k; ne++;
            uint64_t *tm = tmask + (size_t)((i * n + j) * n + k) * nw;
            for (int w = 0; w < nw; w++) hitstack[j - 1][w] = hit[w] | tm[w];
            dfs(j - 1, nones);
            ne--;
            cov[i] = ci; cov[j] = cj; cov[k] = ck;
        }
    }
    if (nones < maxnone && !(j == n - 2 && split > -2 && split != -1)) {
        for (int w = 0; w < nw; w++) hitstack[j - 1][w] = hit[w];
        dfs(j - 1, nones + 1);
    }
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: enum n T maxnone prune print [split]\n"); return 2; }
    n = atoi(argv[1]); T = atoi(argv[2]); maxnone = atoi(argv[3]); prune = atoi(argv[4]); print_ = atoi(argv[5]);
    if (argc > 6) split = atoi(argv[6]);
    if (n > MAXN || n < 3) return 2;
    int s = T + 1;
    /* enumerate s-subsets as masks */
    uint32_t *subs = malloc(sizeof(uint32_t) * (1u << n));
    nsub = 0;
    for (uint32_t x = 0; x < (1u << n); x++) if (__builtin_popcount(x) == s) subs[nsub++] = x;
    nw = (nsub + 63) / 64;
    if (nw > MAXW) { fprintf(stderr, "too many subsets\n"); return 2; }
    memset(full, 0, sizeof full);
    for (int t = 0; t < nsub; t++) full[t >> 6] |= 1ull << (t & 63);
    tmask = calloc((size_t)n * n * n * nw, sizeof(uint64_t));
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) {
        uint32_t e = (1u << a) | (1u << b) | (1u << c);
        for (int t = 0; t < nsub; t++) if ((subs[t] & e) == e) {
            /* store under every ordering key we use: (i,j,k) with i<j<k */
            tmask[(size_t)((a * n + b) * n + c) * nw + (t >> 6)] |= 1ull << (t & 63);
        }
    }
    for (int j = 0; j <= n - 2; j++) {
        memset(Dm[j], 0, sizeof Dm[j]);
        for (int t = 0; t < nsub; t++) {
            uint32_t S = subs[t];
            int lo = __builtin_ctz(S), hi = 31 - __builtin_clz(S);
            int hittable = 0;
            for (int r = 1; r <= j; r++) if (((S >> r) & 1) && r > lo && r < hi) { hittable = 1; break; }
            if (!hittable) Dm[j][t >> 6] |= 1ull << (t & 63);
        }
    }
    memset(hitstack, 0, sizeof hitstack);
    memset(cov, 0, sizeof cov); ne = 0;
    double t0 = now();
    dfs(n - 2, 0);
    fflush(stdout);
    fprintf(stderr, "DONE n=%d T=%d maxnone=%d prune=%d split=%d nodes=%lld leaves=%lld time=%.1f\n", n, T, maxnone, prune, split, nodes, leaves, now() - t0);
    for (int m = 0; m <= n; m++) if (good[m][0] || good[m][1])
        fprintf(stderr, "COUNT m=%d alpha<=T: f7free=%lld f7=%lld\n", m, good[m][0], good[m][1]);
    return 0;
}
