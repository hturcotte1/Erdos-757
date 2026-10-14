/* Referee L003: independent enumeration of SATURATED n-point (4,5)-sets.
 * A saturated (4,5)-set (m = n-2) has, for every interior rank j (1..n-2), exactly one 3-AP with midpoint j:
 * (weak Sidon => midpoints injective; midpoints never extreme; m = n-2).  So the set is a solution of
 *   2 x_j = x_{l(j)} + x_{r(j)},  j = 1..n-2,   x_0 = 0, x_{n-1} = 1        (*)
 * for a midpoint map j -> (l(j), r(j)), l(j) < j < r(j).  (*) is nonsingular (weakly chained diagonally dominant);
 * we check it anyway (count singular systems).
 * Search: maps assigned for j = n-2 DOWN TO 1 (reverse of the census engine).  The only pruning is the one-line
 * order fact (K30): for j1 < j2 NOT (l(j1) >= l(j2) and r(j1) >= r(j2)), because then x_{j1} >= x_{j2}.
 * Optional: lin=1 adds linearity pruning (never used for the reported counts unless stated).
 * NO alpha pruning, NO F7 test.  At each leaf: exact integer Bareiss solve, strict order, (4,5) test on all 4-subsets
 * (from the definition), 3-AP recount from the set, h = largest Sidon subset by a DFS on differences (definition).
 * Output: "SET h v0 v1 ... v_{n-1} | l1,r1 l2,r2 ..." for every saturated (4,5)-set with h <= T (normal form:
 * min 0, gcd 1, lexicographically smaller of set and reflection), plus a STATS line.
 * usage: satenum n T lin [brute]   (brute=1: no K30 pruning at all, plain product over all maps) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef long long ll;
typedef __int128 i128;
static int n, T, lin = 0, brute = 0;
static int L[32], R[32];
static int cov[32][32];
static ll leaves = 0, singular = 0, orderfail = 0, not45 = 0, apmismatch = 0, ok45 = 0, out_cnt = 0, hhist[40];
static ll maxval = 0, maxdet = 0;

static ll gcdll(ll a, ll b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { ll t = a % b; a = b; b = t; } return a; }

/* largest Sidon subset: DFS in index order with a used-difference table (values are small after normalisation) */
static ll V[32];
static int best;
static unsigned char *used; static ll usedsz = 0;
static int cur[32];
static void sidon_dfs(int idx, int sz) {
    if (sz > best) best = sz;
    for (int t = idx; t < n; t++) {
        if (sz + (n - t) <= best) return;
        /* try adding V[t] */
        int okk = 1, k;
        ll d[32];
        for (k = 0; k < sz; k++) {
            d[k] = V[t] - V[cur[k]];
            if (used[d[k]]) { okk = 0; break; }
            /* duplicates among new differences are impossible: V[t]-V[a] distinct for distinct a */
        }
        if (!okk) continue;
        for (k = 0; k < sz; k++) used[d[k]] = 1;
        cur[sz] = t;
        sidon_dfs(t + 1, sz + 1);
        for (k = 0; k < sz; k++) used[d[k]] = 0;
    }
}

static int is45(void) {
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) for (int d = c + 1; d < n; d++) {
        ll x[6] = { V[b]-V[a], V[c]-V[a], V[d]-V[a], V[c]-V[b], V[d]-V[b], V[d]-V[c] };
        int distinct = 0;
        for (int i = 0; i < 6; i++) { int dup = 0; for (int j = 0; j < i; j++) if (x[j] == x[i]) { dup = 1; break; } if (!dup) distinct++; }
        if (distinct < 5) return 0;
    }
    return 1;
}

static int usefloat = 0;
static ll fl_reject = 0, fl_pass = 0;
/* Float pre-filter (only rejects): the system matrix A = 2I - B is a WCDD Z-matrix, hence a nonsingular M-matrix,
 * so 0 < det A <= prod a_ii = 2^(n-2) (Hadamard-Fischer for M-matrices) and every exact gap x_{j+1}-x_j is an integer
 * multiple of 1/det A, i.e. 0 or of size >= 2^-(n-2) >= 1/512 for n <= 11.  The double solve of a 9x9 system with
 * entries in {2,-1,0} and partial pivoting has error << 1e-9, so a float gap < -1e-6 certifies an exact negative gap. */
static int float_reject(void) {
    int N2 = n - 2; double A[32][33];
    for (int r = 0; r < N2; r++) for (int c = 0; c <= N2; c++) A[r][c] = 0;
    for (int j = 1; j <= n - 2; j++) { int r = j - 1; A[r][j-1] += 2; if (L[j] >= 1) A[r][L[j]-1] -= 1; if (R[j] <= n-2) A[r][R[j]-1] -= 1; else A[r][N2] += 1; }
    for (int k = 0; k < N2; k++) {
        int p = k; for (int r = k + 1; r < N2; r++) if (__builtin_fabs(A[r][k]) > __builtin_fabs(A[p][k])) p = r;
        if (A[p][k] == 0) return 0;
        if (p != k) for (int c = 0; c <= N2; c++) { double t = A[k][c]; A[k][c] = A[p][c]; A[p][c] = t; }
        for (int r = k + 1; r < N2; r++) { double f = A[r][k] / A[k][k]; if (f != 0) for (int c = k; c <= N2; c++) A[r][c] -= f * A[k][c]; }
    }
    double x[32];
    for (int k = N2 - 1; k >= 0; k--) { double s = A[k][N2]; for (int c = k + 1; c < N2; c++) s -= A[k][c] * x[c]; x[k] = s / A[k][k]; }
    double y[32]; y[0] = 0; y[n-1] = 1; for (int j = 1; j <= n - 2; j++) y[j] = x[j-1];
    /* float determinant = +- product of pivots; assert the bound |det| <= 2^(n-2) used in the soundness argument */
    double det = 1; for (int k = 0; k < N2; k++) det *= A[k][k];
    if (__builtin_fabs(det) > (double)(1LL << (n - 2)) + 0.5) { fprintf(stderr, "det bound violated %g\n", det); exit(6); }
    /* exact gaps are multiples of 1/|det| >= 2^-(n-2): a float gap < 1e-6 certifies an exact gap <= 0 */
    for (int j = 0; j + 1 < n; j++) if (y[j+1] - y[j] < 1e-6) return 1;
    /* float (4,5) test with the same granularity argument: exact distances are multiples of 1/|det|, so two exact
     * distances are equal iff their float values differ by < 1e-6.  Only rejects; survivors get the exact test. */
    if (usefloat >= 2) {
        for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) for (int d = c + 1; d < n; d++) {
            double z[6] = { y[b]-y[a], y[c]-y[a], y[d]-y[a], y[c]-y[b], y[d]-y[b], y[d]-y[c] };
            int distinct = 0;
            for (int i = 0; i < 6; i++) { int dup = 0; for (int j = 0; j < i; j++) if (__builtin_fabs(z[j] - z[i]) < 1e-6) { dup = 1; break; } if (!dup) distinct++; }
            if (distinct < 5) return 2;
        }
    }
    return 0;
}

static void leaf(void) {
    leaves++;
    if (usefloat) { int fr = float_reject(); if (fr == 1) { fl_reject++; orderfail++; return; } if (fr == 2) { fl_reject++; not45++; return; } fl_pass++; }
    int N2 = n - 2;
    i128 M[32][33];
    for (int r = 0; r < N2; r++) { for (int c = 0; c <= N2; c++) M[r][c] = 0; }
    for (int j = 1; j <= n - 2; j++) {
        int r = j - 1;
        M[r][j - 1] += 2;
        if (L[j] >= 1) M[r][L[j] - 1] -= 1;            /* x_0 = 0 contributes nothing */
        if (R[j] <= n - 2) M[r][R[j] - 1] -= 1; else M[r][N2] += 1; /* x_{n-1} = 1 to the rhs */
    }
    /* Bareiss with row swaps */
    i128 prev = 1;
    for (int k = 0; k < N2; k++) {
        if (M[k][k] == 0) {
            int p = -1; for (int r = k + 1; r < N2; r++) if (M[r][k] != 0) { p = r; break; }
            if (p < 0) { singular++; return; }
            for (int c = 0; c <= N2; c++) { i128 t = M[k][c]; M[k][c] = M[p][c]; M[p][c] = t; }
        }
        for (int r = k + 1; r < N2; r++) {
            for (int c = k + 1; c <= N2; c++) {
                i128 num = M[r][c] * M[k][k] - M[r][k] * M[k][c];
                if (num % prev != 0) { fprintf(stderr, "Bareiss inexact\n"); exit(3); }
                M[r][c] = num / prev;
            }
            M[r][k] = 0;
        }
        prev = M[k][k];
    }
    i128 D = M[N2 - 1][N2 - 1];
    if (D == 0) { singular++; return; }
    { ll ad = (ll)(D < 0 ? -D : D); if (ad > maxdet) maxdet = ad; }
    i128 X[32];
    for (int k = N2 - 1; k >= 0; k--) {
        i128 s = D * M[k][N2];
        for (int c = k + 1; c < N2; c++) s -= M[k][c] * X[c];
        if (s % M[k][k] != 0) { fprintf(stderr, "backsub inexact\n"); exit(4); }
        X[k] = s / M[k][k];
    }
    /* exact residual check of (*) with x = X/D: 2X_j - X_l - X_r = 0, X_0 = 0, X_{n-1} = D */
    i128 Y[32]; Y[0] = 0; Y[n - 1] = D; for (int j = 1; j <= n - 2; j++) Y[j] = X[j - 1];
    if (D < 0) for (int j = 0; j < n; j++) Y[j] = -Y[j];
    for (int j = 1; j <= n - 2; j++) if (2 * Y[j] != Y[L[j]] + Y[R[j]]) { fprintf(stderr, "residual fail\n"); exit(5); }
    for (int j = 0; j + 1 < n; j++) if (!(Y[j] < Y[j + 1])) { orderfail++; return; }
    ll g = 0; for (int j = 0; j < n; j++) g = gcdll(g, (ll)Y[j]);
    for (int j = 0; j < n; j++) V[j] = (ll)(Y[j] / g);
    if (V[n - 1] > maxval) maxval = V[n - 1];
    if (!is45()) { not45++; return; }
    ok45++;
    /* recount 3-APs from the set and compare with the map */
    int nap = 0, match = 1;
    for (int i = 0; i < n; i++) for (int k = i + 2; k < n; k++) {
        ll s2 = V[i] + V[k]; if (s2 & 1) continue;
        for (int j = i + 1; j < k; j++) if (2 * V[j] == s2) { nap++; if (L[j] != i || R[j] != k) match = 0; }
    }
    if (nap != n - 2 || !match) { apmismatch++; }
    /* largest Sidon subset */
    if (V[n - 1] + 1 > usedsz) { free(used); usedsz = 2 * (V[n - 1] + 1); used = calloc(usedsz, 1); }
    best = 0; sidon_dfs(0, 0);
    hhist[best]++;
    if (best <= T) {
        /* normal form: min(V, reflection) lexicographic */
        ll W[32]; for (int j = 0; j < n; j++) W[j] = V[n - 1] - V[n - 1 - j];
        int useW = 0; for (int j = 0; j < n; j++) { if (W[j] != V[j]) { useW = W[j] < V[j]; break; } }
        printf("SET %d", best);
        for (int j = 0; j < n; j++) printf(" %lld", useW ? W[j] : V[j]);
        printf(" |");
        for (int j = 1; j <= n - 2; j++) printf(" %d,%d", L[j], R[j]);
        printf("\n");
        out_cnt++;
    }
}

static void dfs(int j) {
    if (j == 0) { leaf(); return; }
    for (int l = 0; l < j; l++) for (int r = j + 1; r < n; r++) {
        if (!brute) {
            int bad = 0;
            for (int j2 = j + 1; j2 <= n - 2; j2++) if (l >= L[j2] && r >= R[j2]) { bad = 1; break; }
            if (bad) continue;
        }
        if (lin && (cov[l][j] || cov[j][r] || cov[l][r])) continue;
        L[j] = l; R[j] = r;
        if (lin) { cov[l][j] = cov[j][l] = cov[j][r] = cov[r][j] = cov[l][r] = cov[r][l] = 1; }
        dfs(j - 1);
        if (lin) { cov[l][j] = cov[j][l] = cov[j][r] = cov[r][j] = cov[l][r] = cov[r][l] = 0; }
    }
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: satenum n T lin [brute]\n"); return 2; }
    n = atoi(argv[1]); T = atoi(argv[2]); lin = atoi(argv[3]); brute = argc > 4 ? atoi(argv[4]) : 0; usefloat = argc > 5 ? atoi(argv[5]) : 0;
    usedsz = 1 << 16; used = calloc(usedsz, 1);
    dfs(n - 2);
    fprintf(stdout, "STATS n=%d T=%d lin=%d brute=%d leaves=%lld singular=%lld orderfail=%lld not45=%lld ok45=%lld apmismatch=%lld out=%lld maxval=%lld maxdet=%lld float=%d fl_reject=%lld fl_pass=%lld hhist",
            n, T, lin, brute, leaves, singular, orderfail, not45, ok45, apmismatch, out_cnt, maxval, maxdet, usefloat, fl_reject, fl_pass);
    for (int h = 0; h <= n; h++) if (hhist[h]) fprintf(stdout, " %d:%lld", h, hhist[h]);
    fprintf(stdout, "\n");
    return 0;
}
