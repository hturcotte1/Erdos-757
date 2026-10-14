/* Referee L002 -- an independent enumerator of the ordered midpoint class O, written from scratch.
 *
 * Class O on vertices 0..n-1 (rank order): a set of triples (l,j,r), l<j<r, j = midpoint, with
 *   - distinct midpoints (each interior vertex 1..n-2 is the midpoint of at most one triple),
 *   - linear (two triples share at most one vertex),
 *   - K30: (l,j,r),(l',j',r') with l<=l', r<=r', (l,r)!=(l',r')  =>  j<j',
 *   - F7-free (no 5 triples forming AG(2,3) minus two points; tested at the leaves by brute force over 5-subsets).
 * We count members with exactly m triples and alpha <= T.
 *
 * Search design (deliberately different from e757/c/ordered_dfs.c):
 *   - CSP over the interior vertices; variable = interior vertex, value = one of its triples or NONE;
 *   - forward checking with precomputed pairwise compatibility tables (linearity + K30), so every
 *     undecided vertex carries the exact set of triples compatible with all decided triples;
 *   - dynamic variable ordering: branch on the undecided vertex with the fewest remaining triples (MRV);
 *   - bound: H' = decided triples  U  all remaining candidate triples of undecided vertices.  Every completion's
 *     edge set is contained in H', hence alpha(completion) >= alpha(H'); prune iff alpha(H') >= T+1, decided exactly
 *     as "some (n-T-1)-subset of vertices meets every triple of H'" (bitset over all (n-T-1)-subsets).
 *   - prune=0 disables the alpha bound (pure brute force with only the pairwise constraints).
 * Usage: mydfs n=12 m=10 T=7 [prune=1] [allm=0] [print=0] [f7=1] [order=mrv|asc|desc]
 *   allm=1: any number of triples; prints the histogram count[m][alpha] (F7-free leaves) at the end.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

typedef uint64_t u64;
#define MAXN 16
static int n, m_target = -1, T = -1, prune = 1, allm = 0, print = 0, f7 = 1, order = 0; /* 0 mrv 1 asc 2 desc */
static int split_r1 = -1; /* if >=0: midpoint 1 restricted to the triple (0,1,split_r1); split_r1=0 means midpoint 1 is NONE */
static int ntri, tri[MAXN * MAXN * MAXN][3], tid[MAXN][MAXN][MAXN];
static int nopt[MAXN], opt[MAXN][64];           /* triples with midpoint j */
static u64 compat[MAXN * MAXN * MAXN][MAXN];     /* compat[e][j] = options of j compatible with triple e */
static int s_sub, nwords; static u64 *hit;      /* hit[e*nwords + w] = bitset of s-subsets meeting triple e */
static long long nodes = 0, leaves = 0, sols = 0, f7rej = 0;
static long long hist[MAXN * 2][MAXN + 1];
static int dec_tri[MAXN], ndec;                  /* decided triples (stack) */

static int linear_pair(int a, int b) {
    int c = 0;
    for (int x = 0; x < 3; x++) for (int y = 0; y < 3; y++) if (tri[a][x] == tri[b][y]) c++;
    return c <= 1;
}
static int k30_pair(int a, int b) {
    int l = tri[a][0], j = tri[a][1], r = tri[a][2], l2 = tri[b][0], j2 = tri[b][1], r2 = tri[b][2];
    if (l <= l2 && r <= r2 && !(l == l2 && r == r2) && !(j < j2)) return 0;
    if (l2 <= l && r2 <= r && !(l == l2 && r == r2) && !(j2 < j)) return 0;
    return 1;
}
static int alpha_dp(const int *es, int k) {
    static unsigned char ind[1 << MAXN];
    unsigned em[MAXN];
    for (int t = 0; t < k; t++) em[t] = (1u << tri[es[t]][0]) | (1u << tri[es[t]][1]) | (1u << tri[es[t]][2]);
    int best = 0; ind[0] = 1;
    for (unsigned s = 1; s < (1u << n); s++) {
        unsigned low = s & (-s); int ok = ind[s & (s - 1)];
        if (ok) for (int t = 0; t < k; t++) if ((em[t] & low) && (em[t] & s) == em[t]) { ok = 0; break; }
        ind[s] = (unsigned char)ok;
        if (ok && __builtin_popcount(s) > best) best = __builtin_popcount(s);
    }
    return best;
}
static int has_f7(const int *es, int k) {
    int id[5];
    if (k < 5) return 0;
    for (id[0] = 0; id[0] < k; id[0]++) for (id[1] = id[0] + 1; id[1] < k; id[1]++)
    for (id[2] = id[1] + 1; id[2] < k; id[2]++) for (id[3] = id[2] + 1; id[3] < k; id[3]++)
    for (id[4] = id[3] + 1; id[4] < k; id[4]++) {
        int deg[MAXN] = {0};
        for (int t = 0; t < 5; t++) for (int x = 0; x < 3; x++) deg[tri[es[id[t]]][x]]++;
        int nv = 0, d3 = 0, d2 = 0, oth = 0;
        for (int v = 0; v < n; v++) if (deg[v]) { nv++; if (deg[v] == 3) d3++; else if (deg[v] == 2) d2++; else oth++; }
        if (nv == 7 && d3 == 1 && d2 == 6 && oth == 0) return 1;
    }
    return 0;
}
/* alpha(H') >= T+1 ? (H' = given triple list) */
static int alpha_ge(const int *es, int k) {
    if (s_sub < 0) return 0;               /* T >= n: never */
    u64 acc[512];
    for (int w = 0; w < nwords; w++) acc[w] = ~0ULL;
    /* mask off unused bits of the last word */
    int nsub_bits = 0; (void)nsub_bits;
    for (int t = 0; t < k; t++) {
        const u64 *h = hit + (size_t)es[t] * nwords; u64 any = 0;
        for (int w = 0; w < nwords; w++) { acc[w] &= h[w]; any |= acc[w]; }
        if (!any) return 0;
    }
    return 1; /* some s-subset meets every triple (k==0 also: any s-subset) */
}

static int cmp3(const void *p, const void *q) { const int *x = p, *y = q; for (int t = 0; t < 3; t++) if (x[t] != y[t]) return x[t] - y[t]; return 0; }
static void rec(u64 undec, u64 *opts, int nones_left) {
    nodes++;
    /* bound */
    if (prune) {
        int es[1024], k = 0;
        for (int t = 0; t < ndec; t++) es[k++] = dec_tri[t];
        for (int j = 1; j <= n - 2; j++) if ((undec >> j) & 1) { u64 o = opts[j]; while (o) { int b = __builtin_ctzll(o); o &= o - 1; es[k++] = opt[j][b]; } }
        if (alpha_ge(es, k)) return;
    }
    if (!undec) {
        leaves++;
        if (!allm && ndec != m_target) return;
        if (f7 && has_f7(dec_tri, ndec)) { f7rej++; return; }
        int a = alpha_dp(dec_tri, ndec);
        if (allm) { hist[ndec][a]++; return; }
        if (a > T) return;
        sols++;
        if (print) {
            int es[MAXN][3];
            for (int t = 0; t < ndec; t++) for (int x = 0; x < 3; x++) es[t][x] = tri[dec_tri[t]][x];
            qsort(es, ndec, sizeof es[0], cmp3);
            printf("S %d", a);
            for (int t = 0; t < ndec; t++) printf(" %d,%d,%d", es[t][0], es[t][1], es[t][2]);
            printf("\n");
        }
        return;
    }
    /* choose variable */
    int jstar = -1, best = 1 << 30;
    for (int j = 1; j <= n - 2; j++) if ((undec >> j) & 1) {
        int c = __builtin_popcountll(opts[j]);
        if (order == 0) { if (c < best) { best = c; jstar = j; } }
        else if (order == 1) { jstar = j; break; }
        else jstar = j; /* desc: last one */
    }
    /* quick infeasibility: count undecided with zero options */
    int zero = 0;
    for (int j = 1; j <= n - 2; j++) if (((undec >> j) & 1) && opts[j] == 0) zero++;
    if (zero > nones_left) return;
    u64 und2 = undec & ~(1ULL << jstar);
    u64 o = opts[jstar];
    while (o) {
        int b = __builtin_ctzll(o); o &= o - 1;
        int e = opt[jstar][b];
        u64 o2[MAXN];
        for (int j = 1; j <= n - 2; j++) o2[j] = ((und2 >> j) & 1) ? (opts[j] & compat[e][j]) : 0;
        dec_tri[ndec++] = e;
        rec(und2, o2, nones_left);
        ndec--;
    }
    if (nones_left > 0) {
        u64 o2[MAXN];
        for (int j = 1; j <= n - 2; j++) o2[j] = ((und2 >> j) & 1) ? opts[j] : 0;
        rec(und2, o2, nones_left - 1);
    }
}

static long long binom(int a, int b) { if (b < 0 || b > a) return 0; long long r = 1; for (int i = 1; i <= b; i++) r = r * (a - b + i) / i; return r; }

int main(int argc, char **argv) {
    for (int a = 1; a < argc; a++) {
        char key[64]; char val[64];
        if (sscanf(argv[a], "%63[^=]=%63s", key, val) != 2) { fprintf(stderr, "bad arg\n"); return 2; }
        if (!strcmp(key, "n")) n = atoi(val); else if (!strcmp(key, "m")) m_target = atoi(val);
        else if (!strcmp(key, "T")) T = atoi(val); else if (!strcmp(key, "prune")) prune = atoi(val);
        else if (!strcmp(key, "allm")) allm = atoi(val); else if (!strcmp(key, "print")) print = atoi(val);
        else if (!strcmp(key, "f7")) f7 = atoi(val);
        else if (!strcmp(key, "split")) split_r1 = atoi(val);
        else if (!strcmp(key, "order")) order = !strcmp(val, "mrv") ? 0 : !strcmp(val, "asc") ? 1 : 2;
        else { fprintf(stderr, "unknown key %s\n", key); return 2; }
    }
    if (allm) { prune = 0; T = n; }
    if (T < 0) T = n;
    /* triples */
    ntri = 0;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) { tri[ntri][0] = a; tri[ntri][1] = b; tri[ntri][2] = c; tid[a][b][c] = ntri++; }
    for (int j = 1; j <= n - 2; j++) { nopt[j] = 0; for (int l = 0; l < j; l++) for (int r = j + 1; r < n; r++) opt[j][nopt[j]++] = tid[l][j][r]; }
    for (int e = 0; e < ntri; e++) for (int j = 1; j <= n - 2; j++) {
        u64 msk = 0;
        if (tri[e][1] != j) for (int b = 0; b < nopt[j]; b++) { int f = opt[j][b]; if (linear_pair(e, f) && k30_pair(e, f)) msk |= 1ULL << b; }
        compat[e][j] = msk;
    }
    /* s-subsets */
    s_sub = n - T - 1;
    if (s_sub >= 0) {
        long long ns = binom(n, s_sub);
        nwords = (int)((ns + 63) / 64);
        hit = calloc((size_t)ntri * nwords, sizeof(u64));
        long long idx = 0;
        for (unsigned S = 0; S < (1u << n); S++) if (__builtin_popcount(S) == s_sub) {
            for (int e = 0; e < ntri; e++) {
                unsigned em = (1u << tri[e][0]) | (1u << tri[e][1]) | (1u << tri[e][2]);
                if (em & S) hit[(size_t)e * nwords + idx / 64] |= 1ULL << (idx % 64);
            }
            idx++;
        }
        if (idx != ns) { fprintf(stderr, "subset count mismatch\n"); return 3; }
    }
    int budget = allm ? (n - 2) : (n - 2) - m_target;
    if (budget < 0) { fprintf(stderr, "m too large\n"); return 2; }
    u64 undec = 0, opts[MAXN] = {0};
    for (int j = 1; j <= n - 2; j++) { undec |= 1ULL << j; opts[j] = (nopt[j] == 64) ? ~0ULL : ((1ULL << nopt[j]) - 1); }
    clock_t c0 = clock();
    if (split_r1 > 0) {
        /* midpoint 1 must be (0,1,split_r1): decide it now (same forward checking as rec) */
        int e = tid[0][1][split_r1];
        u64 und2 = undec & ~(1ULL << 1), o2[MAXN] = {0};
        for (int j = 2; j <= n - 2; j++) o2[j] = opts[j] & compat[e][j];
        dec_tri[ndec++] = e;
        rec(und2, o2, budget);
        ndec--;
    } else if (split_r1 == 0) {
        u64 und2 = undec & ~(1ULL << 1), o2[MAXN] = {0};
        for (int j = 2; j <= n - 2; j++) o2[j] = opts[j];
        if (budget > 0) rec(und2, o2, budget - 1);
    } else
    rec(undec, opts, budget);
    double sec = (double)(clock() - c0) / CLOCKS_PER_SEC;
    if (allm) {
        for (int mm = 0; mm <= n; mm++) for (int a = 0; a <= n; a++) if (hist[mm][a]) printf("H n=%d m=%d alpha=%d count=%lld\n", n, mm, a, hist[mm][a]);
    }
    printf("DONE split=%d n=%d m=%d T=%d prune=%d order=%d nodes=%lld leaves=%lld f7rej=%lld sols=%lld cpu=%.1f\n", split_r1, n, m_target, T, prune, order, nodes, leaves, f7rej, sols, sec);
    return 0;
}
