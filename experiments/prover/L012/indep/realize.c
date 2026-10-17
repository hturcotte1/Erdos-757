/* realize.c (prover, certificate L012) -- exact realizability test for saturated patterns (n vertices, m = n-2 edges).
   A finite set A of reals whose 3-AP hypergraph is H, with an injective midpoint map, gives (after the affine normalisation
   x -> (x - min)/(max - min), or its reflection) an injective assignment mu: edge -> one of its vertices (its midpoint), whose two
   unmatched vertices u < v are the extremes, and the values x with x_u = 0, x_v = 1 solve 2 x_mu(e) = x_a + x_c (e = {a, mu(e), c}).
   For every such assignment this program solves the system EXACTLY: Gaussian elimination modulo p = 2^61-1 gives D = det and y = D x
   modulo p; they are lifted to the symmetric range and the lifted integers are then CHECKED over Z (2 y_j - y_a - y_c = 0 for every
   edge, with y_u = 0, y_v = D, D != 0), so x = y / D is the exact rational solution (unique, the system being nonsingular).  It then
   tests (i) all n values distinct, (ii) the number of 3-term APs among the values equals m (every edge is one, so this means no
   other AP).  An assignment passing (i) and (ii) is a realization of H (its AP pattern is exactly H).
   Usage: realize NV [print] < lines ("FOUND: (a,b,c) ..." or "HIT: ..." or "m a b c ...").  Prints one STAT line per graph and a TOTAL. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned long long u64; typedef __int128 i128; typedef long long i64;
static const u64 PR = 2305843009213693951ULL;   /* 2^61 - 1 */
static u64 mulm(u64 a, u64 b) { unsigned __int128 z = (unsigned __int128)a * b; u64 lo = (u64)(z & PR), hi = (u64)(z >> 61); u64 r = lo + hi; if (r >= PR) r -= PR; return r; }
static u64 addm(u64 a, u64 b) { u64 r = a + b; if (r >= PR) r -= PR; return r; }
static u64 subm(u64 a, u64 b) { return a >= b ? a - b : a + PR - b; }
static u64 powm(u64 a, u64 e) { u64 r = 1; while (e) { if (e & 1) r = mulm(r, a); a = mulm(a, a); e >>= 1; } return r; }
static u64 invm(u64 a) { return powm(a, PR - 2); }
static i64 lift(u64 a) { return a > PR / 2 ? (i64)a - (i64)PR : (i64)a; }
static int n, m, ed[40][3], mu[40], usedv[40];
static u64 cnt_asg, cnt_sing, cnt_liftfail, cnt_dist, cnt_real; static int PRINT;
static int cmpi64(const void *a, const void *b) { i64 x = *(const i64 *)a, y = *(const i64 *)b; return x < y ? -1 : x > y; }
static void solve(void) {
    cnt_asg++;
    int un[2], k = 0; for (int v = 0; v < n; v++) if (!usedv[v]) { if (k < 2) un[k] = v; k++; }
    if (k != 2) { fprintf(stderr, "unmatched count %d\n", k); exit(5); }
    int u = un[0], v = un[1];
    int idx[40], nu = 0; for (int w = 0; w < n; w++) idx[w] = -1;
    for (int w = 0; w < n; w++) if (w != u && w != v) idx[w] = nu++;
    /* rows: one per edge e, unknown order by idx; equation 2 x_mid - x_a - x_c = [a==v] + [c==v] */
    static u64 A[40][41]; int N = nu;
    for (int e = 0; e < m; e++) { for (int c = 0; c <= N; c++) A[e][c] = 0;
        int j = mu[e]; A[e][idx[j]] = addm(A[e][idx[j]], 2);
        for (int t = 0; t < 3; t++) { int w = ed[e][t]; if (w == j) continue;
            if (w == v) A[e][N] = addm(A[e][N], 1); else if (w != u) A[e][idx[w]] = subm(A[e][idx[w]], 1); } }
    u64 det = 1;
    for (int c = 0; c < N; c++) {
        int pr = -1; for (int r = c; r < N; r++) if (A[r][c]) { pr = r; break; }
        if (pr < 0) { cnt_sing++; return; }
        if (pr != c) { for (int t = 0; t <= N; t++) { u64 z = A[pr][t]; A[pr][t] = A[c][t]; A[c][t] = z; } det = subm(0, det); }
        det = mulm(det, A[c][c]); u64 iv = invm(A[c][c]);
        for (int t = c; t <= N; t++) A[c][t] = mulm(A[c][t], iv);
        for (int r = 0; r < N; r++) if (r != c && A[r][c]) { u64 f = A[r][c]; for (int t = c; t <= N; t++) A[r][t] = subm(A[r][t], mulm(f, A[c][t])); }
    }
    i64 D = lift(det); i64 y[40];
    for (int w = 0; w < n; w++) y[w] = 0;
    y[v] = D; for (int w = 0; w < n; w++) if (idx[w] >= 0) y[w] = lift(mulm(det, A[idx[w]][N]));
    /* exact verification over Z of the lifted solution */
    if (D == 0) { cnt_liftfail++; return; }
    for (int e = 0; e < m; e++) { int j = mu[e], a = -1, c = -1; for (int t = 0; t < 3; t++) if (ed[e][t] != j) { if (a < 0) a = ed[e][t]; else c = ed[e][t]; }
        if ((i128)2 * y[j] - y[a] - y[c] != 0) { cnt_liftfail++; return; } }
    i64 s[40]; memcpy(s, y, sizeof(i64) * n); qsort(s, n, sizeof(i64), cmpi64);
    for (int i = 1; i < n; i++) if (s[i] == s[i - 1]) return;
    cnt_dist++;
    int aps = 0;
    for (int a = 0; a < n; a++) for (int c = a + 2; c < n; c++) {
        i128 sum = (i128)s[a] + s[c]; if (sum & 1) continue; i64 mid = (i64)(sum / 2);
        int lo = a + 1, hi = c - 1; while (lo <= hi) { int md = (lo + hi) / 2; if (s[md] == mid) { aps++; break; } if (s[md] < mid) lo = md + 1; else hi = md - 1; }
    }
    if (aps < m) { fprintf(stderr, "fewer APs than edges?\n"); exit(6); }
    if (aps == m) { cnt_real++; if (PRINT) { printf("REALIZATION D=%lld:", (long long)D); for (int w = 0; w < n; w++) printf(" %lld", (long long)y[w]); printf("\n"); } }
}
static void rec(int e) {
    if (e == m) { solve(); return; }
    for (int t = 0; t < 3; t++) { int w = ed[e][t]; if (usedv[w]) continue; usedv[w] = 1; mu[e] = w; rec(e + 1); usedv[w] = 0; }
}
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: realize NV [print]\n"); return 1; }
    n = atoi(argv[1]); PRINT = argc > 2;
    static char line[1 << 14]; u64 G = 0, TA = 0, TS = 0, TL = 0, TD = 0, TR = 0, RG = 0;
    while (fgets(line, sizeof line, stdin)) {
        m = 0;
        if (strchr(line, '(')) { char *p = line; while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &ed[m][0], &ed[m][1], &ed[m][2]) == 3) m++; p++; } }
        else { char *p = line; int k, mm; if (sscanf(p, "%d%n", &mm, &k) != 1) continue; p += k; for (int i = 0; i < mm; i++) { sscanf(p, "%d %d %d%n", &ed[i][0], &ed[i][1], &ed[i][2], &k); p += k; } m = mm; }
        if (m == 0) continue;
        if (m != n - 2) { fprintf(stderr, "not saturated: m=%d n=%d\n", m, n); return 2; }
        for (int i = 0; i < m; i++) for (int t = 0; t < 3; t++) if (ed[i][t] < 0 || ed[i][t] >= n) { fprintf(stderr, "label\n"); return 3; }
        G++; cnt_asg = cnt_sing = cnt_liftfail = cnt_dist = cnt_real = 0; memset(usedv, 0, sizeof usedv);
        rec(0);
        printf("STAT graph=%llu assignments=%llu singular=%llu liftfail=%llu distinct=%llu realizations=%llu\n", G, cnt_asg, cnt_sing, cnt_liftfail, cnt_dist, cnt_real);
        TA += cnt_asg; TS += cnt_sing; TL += cnt_liftfail; TD += cnt_dist; TR += cnt_real; if (cnt_real) RG++;
    }
    printf("TOTAL graphs=%llu assignments=%llu singular=%llu liftfail=%llu distinct=%llu realizations=%llu realizable_graphs=%llu\n", G, TA, TS, TL, TD, TR, RG);
    return 0;
}
