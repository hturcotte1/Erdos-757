/* count K30-only (and K30+linearity) saturated maps, j = n-2 down to 1, no leaf work */
#include <stdio.h>
#include <stdlib.h>
static int n, lin; static int L[32], R[32], cov[32][32]; static long long leaves = 0;
static void dfs(int j) {
    if (j == 0) { leaves++; return; }
    for (int l = 0; l < j; l++) for (int r = j + 1; r < n; r++) {
        int bad = 0;
        for (int j2 = j + 1; j2 <= n - 2; j2++) if (l >= L[j2] && r >= R[j2]) { bad = 1; break; }
        if (bad) continue;
        if (lin && (cov[l][j] || cov[j][r] || cov[l][r])) continue;
        L[j] = l; R[j] = r;
        if (lin) { cov[l][j] = cov[j][l] = cov[j][r] = cov[r][j] = cov[l][r] = cov[r][l] = 1; }
        dfs(j - 1);
        if (lin) { cov[l][j] = cov[j][l] = cov[j][r] = cov[r][j] = cov[l][r] = cov[r][l] = 0; }
    }
}
int main(int c, char **v) { n = atoi(v[1]); lin = atoi(v[2]); dfs(n - 2); printf("n=%d lin=%d leaves=%lld\n", n, lin, leaves); return 0; }
