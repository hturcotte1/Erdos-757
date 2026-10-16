/* Referee L003: count ordered midpoint patterns (K30 + linearity only during the search, j = n-2 down to 1) with exactly
 * m APs and alpha <= T, split by F7-containment (own test), plus the number of reflection-symmetric ones.
 * usage: patcount n T m */
#include <stdio.h>
#include <stdlib.h>
static int n, T, m; static int L[32], R[32], has[32], cov[32][32];
static long long leaves = 0, f7free = 0, f7cont = 0, symfree = 0;
static unsigned emask[32]; static int ne; static unsigned char isedge[1 << 16];
static int indep(unsigned s) { for (int t = 0; t < ne; t++) if ((s & emask[t]) == emask[t]) return 0; return 1; }
static int has_f7(void) {
    for (int c = 0; c < n; c++) {
        unsigned arms[32]; int na = 0;
        for (int t = 0; t < ne; t++) if (emask[t] >> c & 1) arms[na++] = emask[t] & ~(1u << c);
        for (int a = 0; a < na; a++) for (int b = a + 1; b < na; b++) for (int d = b + 1; d < na; d++) {
            if ((arms[a] & arms[b]) || (arms[a] & arms[d]) || (arms[b] & arms[d])) continue;
            unsigned all = arms[a] | arms[b] | arms[d];
            unsigned a0 = arms[a] & -arms[a];
            /* t1 contains a0, one vertex of arm b, one vertex of arm d; t2 = all \ t1 */
            for (unsigned xb = arms[b]; xb; xb &= xb - 1) for (unsigned xd = arms[d]; xd; xd &= xd - 1) {
                unsigned t1 = a0 | (xb & -xb) | (xd & -xd), t2 = all & ~t1;
                int e1 = 0, e2 = 0;
                for (int t = 0; t < ne; t++) { if (emask[t] == t1) e1 = 1; if (emask[t] == t2) e2 = 1; }
                if (e1 && e2) return 1;
            }
        }
    }
    return 0;
}
static void leaf(void) {
    leaves++;
    ne = 0; for (int j = 1; j <= n - 2; j++) if (has[j]) emask[ne++] = (1u << L[j]) | (1u << j) | (1u << R[j]);
    unsigned full = (1u << n) - 1;
    if (T + 1 <= n) {
        unsigned s = (1u << (T + 1)) - 1;
        while (s <= full) { if (indep(s)) return; unsigned c = s & -s, r = s + c; s = (((r ^ s) >> 2) / c) | r; }
    }
    if (has_f7()) { f7cont++; return; }
    f7free++;
    /* reflection symmetric?  reflection maps AP (l,j,r) to (n-1-r, n-1-j, n-1-l): need has[n-1-j] with that AP */
    int sym = 1;
    for (int j = 1; j <= n - 2 && sym; j++) {
        int jj = n - 1 - j;
        if (has[j] != has[jj]) sym = 0;
        else if (has[j] && (L[jj] != n - 1 - R[j] || R[jj] != n - 1 - L[j])) sym = 0;
    }
    symfree += sym;
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
    printf("PATCOUNT n=%d T=%d m=%d leaves=%lld alpha<=T: f7free=%lld (sym %lld, up to refl %lld) f7=%lld\n", n, T, m, leaves, f7free, symfree, (f7free + symfree) / 2, f7cont);
    return 0;
}
