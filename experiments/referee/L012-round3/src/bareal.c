/* bareal.c (referee L012 round 3) -- independent exact realizability test for saturated 3-graphs (m = n-2).
   Differences from the prover's realize.c and the round-1 referee's rreal.c:
     * the injective midpoint assignments mu: E -> V (mu(e) in e) are enumerated VERTEX BY VERTEX (each vertex is either one of the
       two unmatched vertices or the midpoint of one of its own still-unassigned edges), not edge by edge;
     * the linear system 2 x_mu(e) = x_a + x_c, x_u = 0, x_v = 1 is solved by FRACTION-FREE GAUSS-JORDAN elimination (Bareiss) over the
       integers in 64-bit arithmetic with overflow checks: no modular arithmetic, no lifting; every exact division is checked;
     * the final integer vector y (= det * x) is re-verified against every equation, so a reported solution is certified whatever the
       algorithm did; the two unmatched vertices get y_u = 0, y_v = D.
   Tests at each leaf: (i) all n values distinct, (ii) the number of 3-term APs among the values equals m (then the AP set is exactly
   the edge set, every edge being an AP by the equations).  Per graph: assignments, singular (should be 0 by Lemma N), distinct-valued,
   realizations, minimum number of extra APs over the distinct-valued solutions.  Option 'print' prints every realization.
   Input lines: "TAG: (a,b,c) (d,e,f) ..." or "m a b c ...".  Usage: bareal NV [print] < lines */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef long long i64; typedef unsigned long long u64;
static int n, m, ed[40][3];
static int inc[40][8], ninc[40];            /* edges at each vertex */
static int mu[40];                          /* midpoint vertex of each edge, -1 if unassigned */
static int unm[2], nunm;
static u64 c_asg, c_sing, c_dist, c_real, c_verifyfail, c_divfail; static int minextra; static int PRINT;
static int cmpi(const void *a, const void *b) { i64 x = *(const i64 *)a, y = *(const i64 *)b; return x < y ? -1 : x > y; }
static i64 A[40][41];
static void leaf(void) {
    c_asg++;
    int u = unm[0], v = unm[1];
    int idx[40], N = 0; for (int w = 0; w < n; w++) idx[w] = -1;
    for (int w = 0; w < n; w++) if (w != u && w != v) idx[w] = N++;
    if (N != m) { fprintf(stderr, "internal: N != m\n"); exit(9); }
    for (int e = 0; e < m; e++) {
        for (int c = 0; c <= N; c++) A[e][c] = 0;
        int j = mu[e]; A[e][idx[j]] += 2;
        for (int t = 0; t < 3; t++) { int w = ed[e][t]; if (w == j) continue;
            if (w == v) A[e][N] += 1; else if (w != u) A[e][idx[w]] -= 1; }
    }
    /* fraction-free Gauss-Jordan */
    i64 prev = 1;
    for (int k = 0; k < N; k++) {
        int pr = -1; for (int r = k; r < N; r++) if (A[r][k] != 0) { pr = r; break; }
        if (pr < 0) { c_sing++; return; }
        if (pr != k) for (int c = 0; c <= N; c++) { i64 z = A[pr][c]; A[pr][c] = A[k][c]; A[k][c] = z; }
        i64 piv = A[k][k];
        for (int i = 0; i < N; i++) {
            if (i == k) continue;
            i64 f = A[i][k];
            for (int j = k + 1; j <= N; j++) {
                i64 p1, p2, num;
                if (__builtin_mul_overflow(piv, A[i][j], &p1) || __builtin_mul_overflow(f, A[k][j], &p2) || __builtin_sub_overflow(p1, p2, &num)) {
                    fprintf(stderr, "overflow\n"); exit(7); }
                if (num % prev != 0) { c_divfail++; return; }
                A[i][j] = num / prev;
            }
            A[i][k] = 0;
            if (i < k) A[i][i] = piv;   /* columns j < k: only the diagonal entry of an earlier pivot row is nonzero; (piv*prev - 0)/prev = piv */
        }
        prev = piv;
    }
    i64 D = A[N - 1][N - 1];
    for (int k = 0; k < N; k++) if (A[k][k] != D) { fprintf(stderr, "diagonal not constant\n"); exit(8); }
    if (D == 0) { c_sing++; return; }
    i64 y[40]; for (int w = 0; w < n; w++) y[w] = 0;
    y[v] = D; for (int w = 0; w < n; w++) if (idx[w] >= 0) y[w] = A[idx[w]][N];
    /* certify over Z */
    for (int e = 0; e < m; e++) { int j = mu[e], a = -1, c = -1;
        for (int t = 0; t < 3; t++) if (ed[e][t] != j) { if (a < 0) a = ed[e][t]; else c = ed[e][t]; }
        if ((__int128)2 * y[j] - (__int128)y[a] - (__int128)y[c] != 0) { c_verifyfail++; return; } }
    i64 s[40]; memcpy(s, y, sizeof(i64) * n); qsort(s, n, sizeof(i64), cmpi);
    for (int i = 1; i < n; i++) if (s[i] == s[i - 1]) return;
    c_dist++;
    int aps = 0;
    for (int a = 0; a < n; a++) for (int c = a + 2; c < n; c++) {
        __int128 sum = (__int128)s[a] + s[c]; if (sum & 1) continue; i64 mid = (i64)(sum / 2);
        int lo = a + 1, hi = c - 1; while (lo <= hi) { int md = (lo + hi) >> 1; if (s[md] == mid) { aps++; break; } if (s[md] < mid) lo = md + 1; else hi = md - 1; }
    }
    if (aps < m) { fprintf(stderr, "internal: fewer APs than edges\n"); exit(6); }
    if (aps - m < minextra) minextra = aps - m;
    if (aps == m) { c_real++; if (PRINT) { printf("REALIZATION D=%lld u=%d v=%d:", D, u, v); for (int w = 0; w < n; w++) printf(" %lld", y[w]); printf("\n"); } }
}
static void rec(int w) {
    if (w == n) { if (nunm == 2) leaf(); return; }
    if (nunm < 2) { unm[nunm++] = w; rec(w + 1); nunm--; }
    for (int t = 0; t < ninc[w]; t++) { int e = inc[w][t]; if (mu[e] >= 0) continue; mu[e] = w; rec(w + 1); mu[e] = -1; }
}
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: bareal NV [print] < lines\n"); return 1; }
    n = atoi(argv[1]); PRINT = argc > 2;
    static char line[1 << 14]; u64 G = 0, TA = 0, TS = 0, TD = 0, TR = 0, RG = 0, TV = 0, TF = 0;
    while (fgets(line, sizeof line, stdin)) {
        m = 0;
        if (strchr(line, '(')) { char *p = line; while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &ed[m][0], &ed[m][1], &ed[m][2]) == 3) m++; p++; } }
        else { char *p = line; int k, mm; if (sscanf(p, "%d%n", &mm, &k) != 1) continue; p += k; for (int i = 0; i < mm; i++) { if (sscanf(p, "%d %d %d%n", &ed[i][0], &ed[i][1], &ed[i][2], &k) != 3) { fprintf(stderr, "bad line\n"); return 2; } p += k; } m = mm; }
        if (m == 0) continue;
        if (m != n - 2) { fprintf(stderr, "not saturated: m=%d n=%d\n", m, n); return 2; }
        for (int w = 0; w < n; w++) ninc[w] = 0;
        for (int i = 0; i < m; i++) for (int t = 0; t < 3; t++) { int w = ed[i][t]; if (w < 0 || w >= n) { fprintf(stderr, "label\n"); return 3; } if (ninc[w] >= 8) { fprintf(stderr, "degree > 8\n"); return 3; } inc[w][ninc[w]++] = i; }
        G++; c_asg = c_sing = c_dist = c_real = c_verifyfail = c_divfail = 0; minextra = 1 << 30; nunm = 0;
        for (int e = 0; e < m; e++) mu[e] = -1;
        rec(0);
        printf("STAT graph=%llu assignments=%llu singular=%llu divfail=%llu verifyfail=%llu distinct=%llu realizations=%llu minextra=%d\n",
               G, c_asg, c_sing, c_divfail, c_verifyfail, c_dist, c_real, c_dist ? minextra : -1);
        TA += c_asg; TS += c_sing; TD += c_dist; TR += c_real; TV += c_verifyfail; TF += c_divfail; if (c_real) RG++;
    }
    printf("TOTAL graphs=%llu assignments=%llu singular=%llu divfail=%llu verifyfail=%llu distinct=%llu realizations=%llu realizable_graphs=%llu\n", G, TA, TS, TF, TV, TD, TR, RG);
    return 0;
}
