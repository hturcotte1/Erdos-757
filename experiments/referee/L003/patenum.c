/* Referee L003: independent enumeration of ordered midpoint patterns on n vertices with exactly m APs:
 * each interior j (1..n-2) gets either no AP or an AP (l, j, r), l < j < r; assigned for j = n-2 DOWN TO 1.
 * Pruning: K30 (j1 < j2 assigned => l(j1) < l(j2) or r(j1) < r(j2)) and linearity (no pair in two APs).
 * NO F7 filter, NO alpha pruning: alpha is computed exactly at the leaf (all subsets of size T+1, then exact max).
 * Output: "PAT alpha i,j,k ..." (edges sorted) for every pattern with alpha <= T; STATS line with counts.
 * usage: patenum n T m */
#include <stdio.h>
#include <stdlib.h>
static int n, T, m; static int L[32], R[32], has[32], cov[32][32];
static long long leaves = 0, out = 0;
static unsigned emask[32]; static int ne;
static int indep(unsigned s) { for (int t = 0; t < ne; t++) if ((s & emask[t]) == emask[t]) return 0; return 1; }
static int alpha_exact(void) { int best = 0; for (unsigned s = 0; s < (1u << n); s++) { int c = __builtin_popcount(s); if (c > best && indep(s)) best = c; } return best; }
static void leaf(void) {
    leaves++;
    ne = 0; for (int j = 1; j <= n - 2; j++) if (has[j]) emask[ne++] = (1u << L[j]) | (1u << j) | (1u << R[j]);
    /* quick test: is there an independent set of size T+1?  (then alpha > T) */
    unsigned full = (1u << n) - 1;
    /* enumerate subsets of size T+1 via Gosper's hack */
    if (T + 1 <= n) {
        unsigned s = (1u << (T + 1)) - 1;
        while (s <= full) {
            if (indep(s)) return;
            unsigned c = s & -s, r = s + c; s = (((r ^ s) >> 2) / c) | r;
        }
    }
    int a = alpha_exact();
    if (a > T) { fprintf(stderr, "inconsistent alpha\n"); exit(3); }
    out++;
    /* print edges sorted lexicographically by (i,j,k) */
    int E[32][3], k = 0;
    for (int j = 1; j <= n - 2; j++) if (has[j]) { E[k][0] = L[j]; E[k][1] = j; E[k][2] = R[j]; k++; }
    for (int x = 0; x < k; x++) for (int y = x + 1; y < k; y++) {
        int sw = 0; for (int t = 0; t < 3; t++) { if (E[y][t] != E[x][t]) { sw = E[y][t] < E[x][t]; break; } }
        if (sw) for (int t = 0; t < 3; t++) { int z = E[x][t]; E[x][t] = E[y][t]; E[y][t] = z; }
    }
    printf("PAT %d", a); for (int x = 0; x < k; x++) printf(" %d,%d,%d", E[x][0], E[x][1], E[x][2]); printf("\n");
}
static void dfs(int j, int cnt) {
    if (cnt > m || cnt + j < m) return;
    if (j == 0) { if (cnt == m) leaf(); return; }
    has[j] = 0; dfs(j - 1, cnt);
    for (int l = 0; l < j; l++) for (int r = j + 1; r < n; r++) {
        int bad = 0;
        for (int j2 = j + 1; j2 <= n - 2; j2++) if (has[j2] && l >= L[j2] && r >= R[j2]) { bad = 1; break; }
        if (bad || cov[l][j] || cov[j][r] || cov[l][r]) continue;
        L[j] = l; R[j] = r; has[j] = 1;
        cov[l][j] = cov[j][l] = cov[j][r] = cov[r][j] = cov[l][r] = cov[r][l] = 1;
        dfs(j - 1, cnt + 1);
        cov[l][j] = cov[j][l] = cov[j][r] = cov[r][j] = cov[l][r] = cov[r][l] = 0;
        has[j] = 0;
    }
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); T = atoi(argv[2]); m = atoi(argv[3]);
    dfs(n - 2, 0);
    printf("STATS n=%d T=%d m=%d leaves=%lld out=%lld\n", n, T, m, leaves, out);
    return 0;
}
