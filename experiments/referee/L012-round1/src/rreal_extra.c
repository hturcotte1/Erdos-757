/* rreal.c -- referee's independent exact realizability test for saturated 3-graphs (m = n-2), L012 round 1.
   Method (different from the prover's realize.c):
   - all n values are unknowns; for an injective midpoint assignment mu (mu(e) in e) the m = n-2 homogeneous rows
     2 x_mu(e) - x_a - x_c = 0 are added INCREMENTALLY along a DFS over the edges (forward elimination modulo p = 2^31-1,
     each new row reduced against the earlier pivot rows; nothing is recomputed at the leaves);
   - at a leaf the null space mod p has dimension 2 (rank m); a null vector z with z_f1 = 0, z_f2 = 1 (f1 < f2 the two free
     columns) is obtained by back substitution; z = alpha + beta x* (mod p), beta != 0, where x* is the exact solution with
     x*_u = 0, x*_v = 1 (u, v unmatched).  With y = D x* (D the determinant of the (n-2)x(n-2) system), y_i = det(M_i) by
     Cramer, and Hadamard gives |y_i|, |D| <= H = 6^((n-2)/2) (every row has euclidean norm <= sqrt 6).  If 4H < p then:
       z_i == z_j (mod p)  <=>  y_i = y_j  (|y_i - y_j| <= 2H < p),
       z_i + z_k == 2 z_j (mod p)  <=>  y_i + y_k = 2 y_j  (|.| <= 4H < p),
     and D != 0 (Lemma N) with |D| < p gives rank m mod p, so a rank drop mod p is impossible (counted as 'singular' anyway).
   - tests: (i) all n values distinct, (ii) number of 3-term APs among the values == m.
   Usage: rreal NV [print] < lines ("TAG: (a,b,c) ..." or "m a b c ...").  print: output z for each realization. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
typedef uint64_t u64;
static const u64 P = 2147483647ULL;
static u64 inv_tab_dummy;
static u64 pw(u64 a, u64 e) { u64 r = 1; a %= P; while (e) { if (e & 1) r = r * a % P; a = a * a % P; e >>= 1; } return r; }
static u64 inv(u64 a) { return pw(a, P - 2); }
static int n, m, E[40][3], ord[40], used[40], PRINT, mu[40];
static u64 R[40][40];   /* pivot rows (normalised: R[k][piv[k]] = 1) */
static int piv[40], ispiv[40];
static u64 c_asg, c_sing, c_dist, c_real, c_nodes, c_target; static int min_extra; static int HAVE_T; static u64 TGT[40];
static u64 INV2;
static int cmpu(const void *a, const void *b) { u64 x = *(const u64 *)a, y = *(const u64 *)b; return x < y ? -1 : x > y; }
static void leaf(void) {
    c_asg++;
    int f[2], nf = 0; for (int c = 0; c < n; c++) if (!ispiv[c]) { if (nf < 2) f[nf] = c; nf++; }
    if (nf != 2) { fprintf(stderr, "free columns %d\n", nf); exit(7); }
    u64 z[40]; for (int c = 0; c < n; c++) z[c] = 0; z[f[0]] = 0; z[f[1]] = 1;
    for (int k = m - 1; k >= 0; k--) {
        u64 s = 0; for (int c = 0; c < n; c++) if (c != piv[k] && R[k][c]) s = (s + R[k][c] * z[c]) % P;
        z[piv[k]] = (P - s) % P;
    }
    /* sanity: every edge equation holds mod p */
    for (int k = 0; k < m; k++) { int e = ord[k], w = mu[k]; u64 s2 = 2 * z[w] % P;
        for (int q = 0; q < 3; q++) if (E[e][q] != w) s2 = (s2 + P - z[E[e][q]]) % P;
        if (s2) { fprintf(stderr, "equation check failed\n"); exit(10); } }
    u64 s[40]; memcpy(s, z, sizeof(u64) * n); qsort(s, n, sizeof(u64), cmpu);
    for (int i = 1; i < n; i++) if (s[i] == s[i - 1]) return;
    c_dist++;
    int aps = 0;
    for (int i = 0; i < n; i++) for (int k = i + 1; k < n; k++) {
        u64 t = (s[i] + s[k]) % P * INV2 % P;
        int lo = 0, hi = n - 1;
        while (lo <= hi) { int md = (lo + hi) / 2; if (s[md] == t) { if (md != i && md != k) aps++; break; } if (s[md] < t) lo = md + 1; else hi = md - 1; }
    }
    if (aps < m) { fprintf(stderr, "fewer APs than edges (%d < %d)\n", aps, m); exit(8); }
    if (aps - m < min_extra) min_extra = aps - m;
    if (aps == m && HAVE_T) { int uv[2], nu = 0; for (int c = 0; c < n; c++) if (!used[c]) { if (nu < 2) uv[nu] = c; nu++; }
        u64 den = inv((z[uv[1]] + P - z[uv[0]]) % P); int eq = 1;
        for (int c = 0; c < n; c++) if ((z[c] + P - z[uv[0]]) % P * den % P != TGT[c]) { eq = 0; break; }
        if (eq) c_target++; }
    if (aps == m) { c_real++; if (PRINT) { int uv[2], nu = 0; for (int c = 0; c < n; c++) if (!used[c]) { if (nu < 2) uv[nu] = c; nu++; }
            u64 den = inv((z[uv[1]] + P - z[uv[0]]) % P);
            printf("REAL u=%d v=%d mu=", uv[0], uv[1]); for (int k = 0; k < m; k++) printf("%d%s", mu[k], k + 1 < m ? "," : "");
            printf(" x="); for (int c = 0; c < n; c++) printf("%llu%s", (unsigned long long)((z[c] + P - z[uv[0]]) % P * den % P), c + 1 < n ? "," : "");
            printf("\n"); } }
}
static void dfs(int k) {
    c_nodes++;
    if (k == m) { leaf(); return; }
    int e = ord[k];
    for (int t = 0; t < 3; t++) {
        int w = E[e][t]; if (used[w]) continue;
        u64 *r = R[k]; for (int c = 0; c < n; c++) r[c] = 0;
        r[w] = 2; for (int q = 0; q < 3; q++) if (q != t) r[E[e][q]] = P - 1;
        for (int j = 0; j < k; j++) { u64 f = r[piv[j]]; if (!f) continue; u64 g = P - f;
            for (int c = 0; c < n; c++) if (R[j][c]) r[c] = (r[c] + g * R[j][c]) % P; }
        int pc = -1; for (int c = 0; c < n; c++) if (r[c]) { pc = c; break; }
        if (pc < 0) { c_sing++; continue; }
        u64 iv = inv(r[pc]); for (int c = 0; c < n; c++) if (r[c]) r[c] = r[c] * iv % P;
        piv[k] = pc; ispiv[pc] = 1; used[w] = 1; mu[k] = w;
        dfs(k + 1);
        used[w] = 0; ispiv[pc] = 0;
    }
}
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: rreal NV [print]\n"); return 1; }
    n = atoi(argv[1]); PRINT = argc > 2; INV2 = inv(2);
    double H = pow(6.0, (n - 2) / 2.0);
    if (!(4.0 * H < (double)P)) { fprintf(stderr, "bound 4H=%g not < p\n", 4 * H); return 9; }
    static char line[1 << 15]; u64 G = 0, TA = 0, TS = 0, TD = 0, TR = 0, RG = 0;
    while (fgets(line, sizeof line, stdin)) {
        m = 0; HAVE_T = 0; c_target = 0;
        { char *bar = strchr(line, '|'); if (bar) { *bar = 0; char *q = bar + 1; for (int c = 0; c < 40; c++) { char *nx; TGT[c] = strtoull(q, &nx, 10); if (nx == q) break; q = nx; if (*q == ',') q++; } HAVE_T = 1; } }
        if (strchr(line, '(')) { char *p = line; while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &E[m][0], &E[m][1], &E[m][2]) == 3) m++; p++; } }
        else { char *p = line; int k, mm; if (sscanf(p, "%d%n", &mm, &k) != 1) continue; p += k;
            for (int i = 0; i < mm; i++) { if (sscanf(p, "%d %d %d%n", &E[i][0], &E[i][1], &E[i][2], &k) != 3) return 2; p += k; } m = mm; }
        if (m == 0) continue;
        if (m != n - 2) { fprintf(stderr, "not saturated m=%d n=%d\n", m, n); return 3; }
        for (int i = 0; i < m; i++) for (int t = 0; t < 3; t++) if (E[i][t] < 0 || E[i][t] >= n) return 4;
        for (int i = 0; i < m; i++) ord[i] = m - 1 - i;   /* reversed input order */
        memset(used, 0, sizeof used); memset(ispiv, 0, sizeof ispiv);
        c_asg = c_sing = c_dist = c_real = c_nodes = 0; min_extra = 999; G++;
        dfs(0);
        printf("STAT graph=%llu assignments=%llu singular=%llu distinct=%llu realizations=%llu nodes=%llu target_found=%llu min_extra=%d\n",
               (unsigned long long)G, (unsigned long long)c_asg, (unsigned long long)c_sing, (unsigned long long)c_dist, (unsigned long long)c_real, (unsigned long long)c_nodes, (unsigned long long)c_target, min_extra);
        fflush(stdout);
        TA += c_asg; TS += c_sing; TD += c_dist; TR += c_real; if (c_real) RG++;
    }
    printf("TOTAL graphs=%llu assignments=%llu singular=%llu distinct=%llu realizations=%llu realizable_graphs=%llu\n",
           (unsigned long long)G, (unsigned long long)TA, (unsigned long long)TS, (unsigned long long)TD, (unsigned long long)TR, (unsigned long long)RG);
    (void)inv_tab_dummy;
    return 0;
}
