/* rz.c -- referee round 2 (L012): independent exact realizability test for saturated 3-graphs (m = n-2).
   Enumeration: for every unmatched pair {u<v}, every bijection beta: V\{u,v} -> E with w in beta(w) (DFS over vertices).
   (mu = beta^{-1} is then an injective midpoint assignment; every injective mu arises exactly once.)
   System: unknowns x_w (w != u,v), row w: 2 x_w - x_a - x_c = [a==v]+[c==v], {a,c} = beta(w)\{w}, x_u=0, x_v=1.
   The matrix is 2I - B (B >= 0, row sums <= 2): a Z-matrix; nonsingular (Lemma N) => nonsingular M-matrix => all leading
   principal minors > 0, so elimination without pivoting is valid over Q.
   MODE f (default): double elimination w/o pivoting, D = round(prod pivots), y = round(D x), then EXACT integer check of every
   equation (y_u = 0, y_v = D != 0).  If anything fails -> exact Bareiss fallback (counted).
   MODE e: exact fraction-free Bareiss (int64 entries, __int128 products, partial pivoting, exact-division asserts) for every
   assignment; y = D x via exact back substitution; same integer check.
   Then on the exact integers y: distinct values (sort) and number of 3-APs (two-pointer per middle element).
   Usage: rz NV [f|e] [print] < lines ("TAG: (a,b,c) ..." or "m a b c ...").  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
typedef long long i64; typedef __int128 i128;
static int n, m, ed[64][3];
static int inc[64][8], ninc[64];          /* edges at each vertex */
static int U, V, W[64], nw, idxv[64], beta[64], eused[64];
static int MODE_E = 0, PRINT = 0;
static unsigned long long c_asg, c_dist, c_real, c_fb, c_bad, c_detneg; static int minextra;
static i64 y[64];
static int cmpll(const void *a, const void *b) { i64 x = *(const i64*)a, z = *(const i64*)b; return x < z ? -1 : x > z; }
static void die(const char *s) { fprintf(stderr, "FATAL %s\n", s); exit(9); }
/* build integer system: A (nw x nw), b */
static void build(i64 A[64][65]) {
    for (int r = 0; r < nw; r++) { for (int c = 0; c <= nw; c++) A[r][c] = 0; }
    for (int r = 0; r < nw; r++) {
        int w = W[r], e = beta[r];
        A[r][r] += 2;
        for (int t = 0; t < 3; t++) { int a = ed[e][t]; if (a == w) continue;
            if (a == V) A[r][nw] += 1; else if (a != U) A[r][idxv[a]] -= 1; }
    }
}
static int check_int(i64 D) {  /* exact check of every equation, with y_u=0, y_v=D */
    if (D == 0) return 0;
    if (y[U] != 0 || y[V] != D) return 0;
    for (int r = 0; r < nw; r++) { int w = W[r], e = beta[r], o[2], k = 0;
        for (int t = 0; t < 3; t++) if (ed[e][t] != w) o[k++] = ed[e][t];
        if (k != 2) return 0;
        if ((i128)2 * y[w] - (i128)y[o[0]] - (i128)y[o[1]] != 0) return 0; }
    return 1;
}
static int solve_exact(void) {   /* Bareiss with partial pivoting; returns 1 and fills y on success */
    static i64 A[64][65]; build(A);
    int N = nw; int sign = 1; i64 prev = 1; int perm_ok = 1;
    for (int k = 0; k < N; k++) {
        int p = -1; for (int r = k; r < N; r++) if (A[r][k] != 0) { p = r; break; }
        if (p < 0) return 0;   /* singular */
        if (p != k) { for (int c = 0; c <= N; c++) { i64 t = A[p][c]; A[p][c] = A[k][c]; A[k][c] = t; } sign = -sign; }
        for (int i = k + 1; i < N; i++) {
            for (int j = k + 1; j <= N; j++) {
                i128 num = (i128)A[k][k] * A[i][j] - (i128)A[i][k] * A[k][j];
                if (num % prev != 0) die("bareiss inexact");
                i128 q = num / prev; if (q > ((i128)1 << 62) || q < -((i128)1 << 62)) die("bareiss overflow");
                A[i][j] = (i64)q;
            }
            A[i][k] = 0;
        }
        prev = A[k][k];
    }
    (void)perm_ok;
    i64 D = A[N-1][N-1];     /* = sign * det(original) ; with D as scale the back substitution below is exact */
    /* y_i = (D*b_i - sum_{j>i} A_ij y_j) / A_ii  -- integer for the scale D (Cramer with the permuted matrix) */
    i64 yy[64];
    for (int i = N - 1; i >= 0; i--) {
        i128 s = (i128)D * A[i][N];
        for (int j = i + 1; j < N; j++) s -= (i128)A[i][j] * yy[j];
        if (s % A[i][i] != 0) die("backsub inexact");
        i128 q = s / A[i][i]; if (q > ((i128)1 << 62) || q < -((i128)1 << 62)) die("backsub overflow");
        yy[i] = (i64)q;
    }
    for (int w = 0; w < n; w++) y[w] = 0;
    y[V] = D; for (int r = 0; r < N; r++) y[W[r]] = yy[r];
    if (sign * D <= 0) c_detneg++;   /* det(2I-B) must be > 0 (M-matrix) */
    if (!check_int(D)) die("exact solution fails check");
    return 1;
}
static int solve_float(void) {
    static double A[64][65]; int N = nw;
    for (int r = 0; r < N; r++) for (int c = 0; c <= N; c++) A[r][c] = 0.0;
    for (int r = 0; r < N; r++) { int w = W[r], e = beta[r]; A[r][r] += 2.0;
        for (int t = 0; t < 3; t++) { int a = ed[e][t]; if (a == w) continue;
            if (a == V) A[r][N] += 1.0; else if (a != U) A[r][idxv[a]] -= 1.0; } }
    double det = 1.0;
    for (int k = 0; k < N; k++) {
        double p = A[k][k]; if (!(p > 1e-9)) return 0;
        det *= p;
        for (int i = k + 1; i < N; i++) { double f = A[i][k]; if (f == 0.0) continue; f /= p;
            for (int j = k + 1; j <= N; j++) A[i][j] -= f * A[k][j]; A[i][k] = 0.0; }
    }
    double x[64];
    for (int i = N - 1; i >= 0; i--) { double s = A[i][N]; for (int j = i + 1; j < N; j++) s -= A[i][j] * x[j]; x[i] = s / A[i][i]; }
    if (!(det >= 0.5 && det < 4.0e18)) return 0;
    i64 D = llround(det);
    for (int w = 0; w < n; w++) y[w] = 0;
    y[V] = D; for (int r = 0; r < N; r++) { double z = (double)D * x[r]; if (!(fabs(z) < 4.0e18)) return 0; y[W[r]] = llround(z); }
    return check_int(D);
}
static void leaf(void) {
    c_asg++;
    int ok;
    if (MODE_E) ok = solve_exact();
    else { ok = solve_float(); if (!ok) { c_fb++; ok = solve_exact(); } }
    if (!ok) { c_bad++; return; }
#ifdef DUMP
    printf("S %d %d", U, V); for (int w = 0; w < n; w++) printf(" %lld", (long long)y[w]); printf("\n");
#endif
    i64 s[64]; memcpy(s, y, sizeof(i64) * n); qsort(s, n, sizeof(i64), cmpll);
    for (int i = 1; i < n; i++) if (s[i] == s[i-1]) return;
    c_dist++;
    int aps = 0;
    for (int j = 1; j < n - 1; j++) { int i = j - 1, k = j + 1; i128 t = (i128)2 * s[j];
        while (i >= 0 && k < n) { i128 z = (i128)s[i] + s[k]; if (z == t) { aps++; i--; k++; } else if (z < t) k++; else i--; } }
    if (aps < m) die("fewer APs than edges");
    if (aps - m < minextra) minextra = aps - m;
    if (aps == m) { c_real++; if (PRINT) { printf("REAL u=%d v=%d:", U, V); for (int w = 0; w < n; w++) printf(" %lld", (long long)y[w]); printf("\n"); } }
}
static void dfs(int k) {
    if (k == nw) { leaf(); return; }
    int w = W[k];
    for (int i = 0; i < ninc[w]; i++) { int e = inc[w][i]; if (eused[e]) continue; eused[e] = 1; beta[k] = e; dfs(k + 1); eused[e] = 0; }
}
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage\n"); return 1; }
    n = atoi(argv[1]);
    for (int i = 2; i < argc; i++) { if (!strcmp(argv[i], "e")) MODE_E = 1; if (!strcmp(argv[i], "print")) PRINT = 1; }
    static char line[1 << 16]; unsigned long long G = 0, TA = 0, TD = 0, TR = 0, TF = 0, RG = 0;
    while (fgets(line, sizeof line, stdin)) {
        m = 0;
        if (strchr(line, '(')) { char *p = line; while ((p = strchr(p, '('))) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) == 3) { ed[m][0] = a; ed[m][1] = b; ed[m][2] = c; m++; } p++; } }
        else { char *p = line; int k, mm; if (sscanf(p, "%d%n", &mm, &k) != 1) continue; p += k; for (int i = 0; i < mm; i++) { if (sscanf(p, "%d %d %d%n", &ed[i][0], &ed[i][1], &ed[i][2], &k) != 3) die("parse"); p += k; } m = mm; }
        if (m == 0) continue;
        if (m != n - 2) die("not saturated");
        memset(ninc, 0, sizeof ninc);
        for (int e = 0; e < m; e++) { for (int t = 0; t < 3; t++) { int a = ed[e][t]; if (a < 0 || a >= n) die("label"); if (ninc[a] >= 8) die("deg"); inc[a][ninc[a]++] = e; }
            if (ed[e][0] == ed[e][1] || ed[e][0] == ed[e][2] || ed[e][1] == ed[e][2]) die("repeated vertex"); }
        G++; c_asg = c_dist = c_real = c_fb = c_bad = c_detneg = 0; minextra = 1 << 30;
        for (U = 0; U < n; U++) for (V = U + 1; V < n; V++) {
            nw = 0; for (int w = 0; w < n; w++) idxv[w] = -1;
            /* static vertex order: increasing degree, ties by label */
            for (int d = 0; d <= 8; d++) for (int w = 0; w < n; w++) if (w != U && w != V && ninc[w] == d) { idxv[w] = nw; W[nw++] = w; }
            memset(eused, 0, sizeof eused);
            dfs(0);
        }
        printf("G %llu asg=%llu dist=%llu real=%llu fallback=%llu singular=%llu detneg=%llu minextra=%d\n", G, c_asg, c_dist, c_real, c_fb, c_bad, c_detneg, minextra == (1 << 30) ? -1 : minextra);
        fflush(stdout);
        TA += c_asg; TD += c_dist; TR += c_real; TF += c_fb; if (c_real) RG++;
    }
    printf("TOTAL graphs=%llu asg=%llu dist=%llu real=%llu fallback=%llu realizable_graphs=%llu\n", G, TA, TD, TR, TF, RG);
    return 0;
}
