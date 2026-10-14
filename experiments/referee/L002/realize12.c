/* Referee L002 -- independent validator + exact realizer for saturated ordered patterns (n=12, m=10).
 * Written from scratch for the referee (does not use e757/, judge/, filter.c, fastreal.py).
 *
 * Input (stdin): one pattern per line; every integer on the line is read, consecutive triples are edges
 * (a,b,c) with a<b<c (rank order), b = midpoint.  Works with the jsonl "[[0,1,3],...]" and "SOL a i,j,k" formats
 * (for SOL lines the first integer, alpha, is skipped).
 *
 * Per pattern:
 *  1. structure: exactly 10 edges, 0<=a<b<c<=11, midpoints distinct (hence = {1..10});
 *  2. class O re-check: linear (pairwise <=1 common vertex), K30 (pairwise), F7-free (all 5-subsets of edges;
 *     F7 == 5 linear edges on 7 vertices with degree sequence 3,2,2,2,2,2,2), exact alpha by DP over 2^12 masks;
 *  3. exact realization: x_0=0, x_11=1, 2x_j - x_l(j) - x_r(j) = 0 for j=1..10; fraction-free Gaussian elimination
 *     with pivoting in int64, exact integer back substitution (N_j = D x_j), divisibility asserted, residual verified;
 *  4. on the integer solution X (X_0=0, X_11=|D|): strict order; set of 3-APs == pattern; every 4-subset has >= 5
 *     distinct distances; h = max Sidon subset by brute force over all 4096 subsets using the definition
 *     (no two distinct pairs with the same difference).
 * Output: summary on stderr; for each realizable pattern one line on stdout:
 *     R <canonical normalized set (min of set and reflection, gcd 1)> | <edges> | alpha h
 * plus (if argv[1] given) a binary file of 64-bit pattern codes for duplicate / reflection-closure checks.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define N 12
#define M 10
typedef long long ll;

static int E[64][3], ne;
static long long cnt_lines = 0, cnt_badstruct = 0, cnt_nonlinear = 0, cnt_k30 = 0, cnt_f7 = 0, cnt_alpha_gt7 = 0;
static long long alpha_hist[N + 1];
static long long cnt_order = 0, cnt_extra = 0, cnt_rep = 0, cnt_real = 0, cnt_singular = 0, cnt_div_fail = 0, cnt_resid_fail = 0;
static long long h_hist[N + 1];

static ll gcdll(ll a, ll b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { ll t = a % b; a = b; b = t; } return a; }

static int popc(unsigned x) { return __builtin_popcount(x); }

static int is_linear(void) {
    for (int a = 0; a < ne; a++) for (int b = a + 1; b < ne; b++) {
        int common = 0;
        for (int x = 0; x < 3; x++) for (int y = 0; y < 3; y++) if (E[a][x] == E[b][y]) common++;
        if (common > 1) return 0;
    }
    return 1;
}
/* K30: edges (i,j,k),(i',j',k') with i<=i', k<=k', (i,k)!=(i',k') must have j<j' */
static int k30_ok(void) {
    for (int a = 0; a < ne; a++) for (int b = 0; b < ne; b++) {
        if (a == b) continue;
        int i = E[a][0], j = E[a][1], k = E[a][2], i2 = E[b][0], j2 = E[b][1], k2 = E[b][2];
        if (i <= i2 && k <= k2 && !(i == i2 && k == k2) && !(j < j2)) return 0;
    }
    return 1;
}
/* F7 as a sub-hypergraph: 5 edges (linear, as H is linear) spanning exactly 7 vertices, degrees 3,2,2,2,2,2,2 */
static int has_f7(void) {
    int idx[5];
    for (idx[0] = 0; idx[0] < ne; idx[0]++)
    for (idx[1] = idx[0] + 1; idx[1] < ne; idx[1]++)
    for (idx[2] = idx[1] + 1; idx[2] < ne; idx[2]++)
    for (idx[3] = idx[2] + 1; idx[3] < ne; idx[3]++)
    for (idx[4] = idx[3] + 1; idx[4] < ne; idx[4]++) {
        int deg[N]; memset(deg, 0, sizeof deg);
        for (int t = 0; t < 5; t++) for (int x = 0; x < 3; x++) deg[E[idx[t]][x]]++;
        int nv = 0, d3 = 0, d2 = 0, other = 0;
        for (int v = 0; v < N; v++) if (deg[v]) { nv++; if (deg[v] == 3) d3++; else if (deg[v] == 2) d2++; else other++; }
        if (nv == 7 && d3 == 1 && d2 == 6 && other == 0) return 1;
    }
    return 0;
}
static int alpha_exact(void) {
    static unsigned char ind[1 << N];
    unsigned emask[64];
    for (int t = 0; t < ne; t++) emask[t] = (1u << E[t][0]) | (1u << E[t][1]) | (1u << E[t][2]);
    int best = 0;
    ind[0] = 1;
    for (unsigned s = 1; s < (1u << N); s++) {
        unsigned low = s & (-s);
        int ok = ind[s & (s - 1)];
        if (ok) for (int t = 0; t < ne; t++) if ((emask[t] & low) && (emask[t] & s) == emask[t]) { ok = 0; break; }
        ind[s] = (unsigned char)ok;
        if (ok && popc(s) > best) best = popc(s);
    }
    return best;
}
/* exact solve; returns 0 on success with X[0..11] integers, X[0]=0, X[11]=|D|>0 */
static int solve(ll X[N]) {
    int l[N], r[N];
    for (int t = 0; t < ne; t++) { l[E[t][1]] = E[t][0]; r[E[t][1]] = E[t][2]; }
    ll A[M][M + 1];
    memset(A, 0, sizeof A);
    for (int j = 1; j <= M; j++) {
        int row = j - 1;
        A[row][j - 1] += 2;
        if (l[j] != 0) A[row][l[j] - 1] -= 1;          /* l[j] < j <= 10, never 11 */
        if (r[j] != 11) A[row][r[j] - 1] -= 1; else A[row][M] += 1; /* x_11 = 1 moves to rhs; r never 0 */
    }
    /* Bareiss with row pivoting */
    ll prev = 1; int sign = 1;
    for (int k = 0; k < M; k++) {
        int p = -1;
        for (int i = k; i < M; i++) if (A[i][k] != 0) { p = i; break; }
        if (p < 0) { cnt_singular++; return -1; }
        if (p != k) { for (int c = 0; c <= M; c++) { ll t = A[k][c]; A[k][c] = A[p][c]; A[p][c] = t; } sign = -sign; }
        for (int i = k + 1; i < M; i++) {
            for (int c = k + 1; c <= M; c++) {
                __int128 v = (__int128)A[k][k] * A[i][c] - (__int128)A[i][k] * A[k][c];
                if (v % prev != 0) { cnt_div_fail++; return -1; }
                A[i][c] = (ll)(v / prev);
            }
            A[i][k] = 0;
        }
        prev = A[k][k];
    }
    ll D = A[M - 1][M - 1];   /* = sign * det */
    if (D == 0) { cnt_singular++; return -1; }
    ll Nn[M];
    for (int k = M - 1; k >= 0; k--) {
        __int128 s = (__int128)D * A[k][M];
        for (int t = k + 1; t < M; t++) s -= (__int128)A[k][t] * Nn[t];
        if (s % A[k][k] != 0) { cnt_div_fail++; return -1; }
        Nn[k] = (ll)(s / A[k][k]);
    }
    /* X_j = D x_j ; X_0 = 0, X_11 = D */
    X[0] = 0; X[N - 1] = D;
    for (int j = 1; j <= M; j++) X[j] = Nn[j - 1];
    /* residual check against the ORIGINAL equations */
    for (int j = 1; j <= M; j++) if (2 * X[j] - X[l[j]] - X[r[j]] != 0) { cnt_resid_fail++; return -1; }
    if (D < 0) for (int j = 0; j < N; j++) X[j] = -X[j];
    return 0;
}
static int cmp_ll(const void *a, const void *b) { ll x = *(const ll *)a, y = *(const ll *)b; return (x > y) - (x < y); }
static int cmp3(const void *a, const void *b) { const int *x = a, *y = b; for (int t = 0; t < 3; t++) if (x[t] != y[t]) return x[t] - y[t]; return 0; }

/* mixed radix code of a saturated pattern: digit for midpoint j is l(j)*(11-j) + (r(j)-j-1) in base j*(11-j) */
static uint64_t code_of(int l[N], int r[N]) {
    uint64_t c = 0;
    for (int j = 1; j <= M; j++) { uint64_t base = (uint64_t)j * (11 - j); c = c * base + (uint64_t)(l[j] * (11 - j) + (r[j] - j - 1)); }
    return c;
}

int main(int argc, char **argv) {
    FILE *codes = argc > 1 ? fopen(argv[1], "wb") : NULL;
    static char line[1 << 16];
    while (fgets(line, sizeof line, stdin)) {
        int vals[256], nv = 0;
        char *p = line;
        int skip_first = (strncmp(line, "SOL", 3) == 0);
        if (strncmp(line, "DONE", 4) == 0 || strncmp(line, "PROG", 4) == 0) continue;
        while (*p) {
            if ((*p >= '0' && *p <= '9') || (*p == '-' && p[1] >= '0' && p[1] <= '9')) {
                long v = strtol(p, &p, 10);
                if (nv < 256) vals[nv++] = (int)v;
            } else p++;
        }
        int off = skip_first ? 1 : 0;
        cnt_lines++;
        if ((nv - off) % 3 != 0) { cnt_badstruct++; continue; }
        ne = (nv - off) / 3;
        int ok = (ne == M);
        int seenmid[N] = {0};
        for (int t = 0; t < ne && t < 64; t++) {
            E[t][0] = vals[off + 3 * t]; E[t][1] = vals[off + 3 * t + 1]; E[t][2] = vals[off + 3 * t + 2];
            if (!(0 <= E[t][0] && E[t][0] < E[t][1] && E[t][1] < E[t][2] && E[t][2] <= N - 1)) ok = 0;
            else { if (seenmid[E[t][1]]) ok = 0; seenmid[E[t][1]] = 1; }
        }
        if (!ok) { cnt_badstruct++; continue; }
        if (!is_linear()) { cnt_nonlinear++; continue; }
        if (!k30_ok()) { cnt_k30++; continue; }
        if (has_f7()) { cnt_f7++; continue; }
        int a = alpha_exact();
        alpha_hist[a]++;
        if (a > 7) { cnt_alpha_gt7++; continue; }
        int l[N], r[N];
        for (int t = 0; t < ne; t++) { l[E[t][1]] = E[t][0]; r[E[t][1]] = E[t][2]; }
        if (codes) { uint64_t c = code_of(l, r); fwrite(&c, 8, 1, codes); }
        ll X[N];
        if (solve(X) != 0) continue;
        int ordered = 1;
        for (int j = 0; j + 1 < N; j++) if (!(X[j] < X[j + 1])) ordered = 0;
        if (!ordered) { cnt_order++; continue; }
        /* all 3-APs of X */
        int isedge[N][N][N]; memset(isedge, 0, sizeof isedge);
        for (int t = 0; t < ne; t++) isedge[E[t][0]][E[t][1]][E[t][2]] = 1;
        int extra = 0;
        for (int i = 0; i < N; i++) for (int j = i + 1; j < N; j++) for (int k = j + 1; k < N; k++) {
            int ap = (X[i] + X[k] == 2 * X[j]);
            if (ap != isedge[i][j][k]) extra = 1;
        }
        if (extra) { cnt_extra++; continue; }
        /* (4,5): every 4 points determine >= 5 distinct distances */
        int ok45 = 1;
        for (int a1 = 0; a1 < N && ok45; a1++) for (int b1 = a1 + 1; b1 < N && ok45; b1++)
        for (int c1 = b1 + 1; c1 < N && ok45; c1++) for (int d1 = c1 + 1; d1 < N && ok45; d1++) {
            ll pts[4] = { X[a1], X[b1], X[c1], X[d1] }, ds[6]; int nd = 0;
            for (int u = 0; u < 4; u++) for (int v = u + 1; v < 4; v++) { ll d = pts[v] - pts[u]; if (d < 0) d = -d; ds[nd++] = d; }
            qsort(ds, 6, sizeof(ll), cmp_ll);
            int distinct = 1; for (int u = 1; u < 6; u++) if (ds[u] != ds[u - 1]) distinct++;
            if (distinct < 5) ok45 = 0;
        }
        if (!ok45) { cnt_rep++; continue; }
        /* h by definition: max subset with all pairwise positive differences distinct */
        unsigned bad[400]; int nb = 0;
        for (int a1 = 0; a1 < N; a1++) for (int b1 = a1 + 1; b1 < N; b1++)
        for (int c1 = 0; c1 < N; c1++) for (int d1 = c1 + 1; d1 < N; d1++) {
            if (a1 * N + b1 >= c1 * N + d1) continue;
            if (X[b1] - X[a1] == X[d1] - X[c1]) { if (nb < 400) bad[nb++] = (1u << a1) | (1u << b1) | (1u << c1) | (1u << d1); }
        }
        int h = 0;
        for (unsigned s = 1; s < (1u << N); s++) {
            int good = 1;
            for (int t = 0; t < nb; t++) if ((bad[t] & s) == bad[t]) { good = 0; break; }
            if (good && popc(s) > h) h = popc(s);
        }
        h_hist[h]++;
        cnt_real++;
        /* canonical normalized set */
        ll g = 0; for (int j = 0; j < N; j++) g = gcdll(g, X[j]);
        ll Y[N], Z[N];
        for (int j = 0; j < N; j++) Y[j] = X[j] / g;
        for (int j = 0; j < N; j++) Z[j] = Y[N - 1] - Y[N - 1 - j];
        int useZ = 0;
        for (int j = 0; j < N; j++) { if (Z[j] < Y[j]) { useZ = 1; break; } if (Z[j] > Y[j]) break; }
        ll *C = useZ ? Z : Y;
        int es[M][3]; for (int t = 0; t < ne; t++) { es[t][0] = E[t][0]; es[t][1] = E[t][1]; es[t][2] = E[t][2]; }
        qsort(es, ne, sizeof es[0], cmp3);
        printf("R");
        for (int j = 0; j < N; j++) printf(" %lld", C[j]);
        printf(" |");
        for (int t = 0; t < ne; t++) printf(" %d,%d,%d", es[t][0], es[t][1], es[t][2]);
        printf(" | %d %d\n", a, h);
    }
    if (codes) fclose(codes);
    fprintf(stderr, "lines=%lld badstruct=%lld nonlinear=%lld k30fail=%lld f7=%lld alpha>7=%lld\n", cnt_lines, cnt_badstruct, cnt_nonlinear, cnt_k30, cnt_f7, cnt_alpha_gt7);
    fprintf(stderr, "alpha_hist:"); for (int a = 0; a <= N; a++) if (alpha_hist[a]) fprintf(stderr, " %d:%lld", a, alpha_hist[a]); fprintf(stderr, "\n");
    fprintf(stderr, "singular=%lld divfail=%lld residfail=%lld order_infeasible=%lld extra_ap=%lld not45=%lld realizable=%lld\n",
            cnt_singular, cnt_div_fail, cnt_resid_fail, cnt_order, cnt_extra, cnt_rep, cnt_real);
    fprintf(stderr, "h_hist:"); for (int a = 0; a <= N; a++) if (h_hist[a]) fprintf(stderr, " %d:%lld", a, h_hist[a]); fprintf(stderr, "\n");
    return 0;
}
