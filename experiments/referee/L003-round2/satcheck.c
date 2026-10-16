/* satcheck.c -- referee L003 round 2: independent enumeration of SATURATED n-point (4,5)-sets.
 *
 * Facts used (each re-derived in the review):
 *   (a) a (4,5)-set is weak Sidon, so each point is the midpoint of at most one 3-AP, and min/max are never midpoints;
 *       hence m = n-2 (saturated) iff every interior rank j=1..n-2 is the midpoint of exactly one AP (L[j], j, R[j]).
 *   (b) the system 2x_j = x_L[j] + x_R[j] (j interior), x_0 = 0, x_{n-1} = 1 is nonsingular (weakly chained diagonally
 *       dominant: follow R[j] upwards until it hits n-1), so the map determines the set.
 * Optional, sound pruning (both one-line consequences of the AP equations / the (4,5) property):
 *   K30: for midpoints i < j it is impossible that L[j] <= L[i] and R[j] <= R[i] (that would force x_j <= x_i).
 *   LIN: two 3-APs of a (4,5)-set share at most one point.
 * Leaf: float LU solve, then an EXACT integer certificate: integers X_0 = 0 < ... with X_{n-1} = D != 0 and
 *       2X_j = X_L + X_R for all j  =>  X/D is the unique solution.  If the certificate fails, the map is printed as
 *       "FALLBACK" for exact treatment elsewhere.  Then: strict order, weak Sidon (sums bitmap), (4,5) from the
 *       definition on every 4-subset, 3-AP count of the set == n-2, h = largest Sidon subset by exhaustive branch and
 *       bound on the DEFINITION (all positive differences distinct), canonical affine form (min 0, gcd 1, lexicographic
 *       min of the set and its reflection).  Each affine class is printed once (only from the orientation that is
 *       lexicographically canonical; a reflection-symmetric set comes from a single map).
 * usage: ./satcheck n k30 lin [r1]     (r1: restrict R[1] to this value; default all)
 * output: "S h c0 c1 ... c_{n-1}" per class, then a "STATS" line (labelled counts, i.e. per map/orientation).        */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

#define MAXN 14
static int n, useK30, useLIN, onlyR1 = -1;
static int L[MAXN], R[MAXN];
static long long leaves = 0, singular = 0, fallback = 0, orderfail = 0, notws = 0, not45 = 0, apbad = 0, ok45 = 0, printed = 0;
static long long hhist[MAXN + 1];
static long long canon_eq_refl = 0;

static long long gcdll(long long a, long long b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { long long t = a % b; a = b; b = t; } return a; }

/* max Sidon subset by definition: choose elements in index order, keep bitmap of used differences */
static long long X[MAXN];
static int best;
static uint64_t used[64]; /* differences up to 4095 */
static int chosen[MAXN], nch;
static void sidon_dfs(int k) {
    if (nch > best) best = nch;
    if (k == n) return;
    if (nch + (n - k) <= best) return;
    /* include k */
    int okk = 1; int added[MAXN]; int na = 0;
    for (int t = 0; t < nch; t++) {
        long long d = X[k] - X[chosen[t]];
        if (used[d >> 6] >> (d & 63) & 1ULL) { okk = 0; break; }
        used[d >> 6] |= 1ULL << (d & 63); added[na++] = (int)d;
    }
    if (okk) { chosen[nch++] = k; sidon_dfs(k + 1); nch--; }
    for (int t = 0; t < na; t++) used[added[t] >> 6] &= ~(1ULL << (added[t] & 63));
    /* exclude k */
    sidon_dfs(k + 1);
}

static unsigned char sums[1 << 13];
static int posof[1 << 12];

static void leaf(void) {
    leaves++;
    int m = n - 2; /* unknowns x_1..x_{n-2} */
    double A[MAXN][MAXN + 1];
    for (int a = 0; a < m; a++) { for (int b = 0; b <= m; b++) A[a][b] = 0; }
    for (int j = 1; j <= n - 2; j++) {
        int r = j - 1;
        A[r][j - 1] += 2.0;
        if (L[j] >= 1 && L[j] <= n - 2) A[r][L[j] - 1] -= 1.0;
        if (R[j] >= 1 && R[j] <= n - 2) A[r][R[j] - 1] -= 1.0;
        if (R[j] == n - 1) A[r][m] += 1.0; /* x_{n-1} = 1 ; x_0 = 0 contributes nothing */
    }
    double det = 1.0;
    for (int c = 0; c < m; c++) {
        int p = c; for (int r = c + 1; r < m; r++) if (fabs(A[r][c]) > fabs(A[p][c])) p = r;
        if (fabs(A[p][c]) < 1e-12) { singular++; return; }
        if (p != c) { for (int b = 0; b <= m; b++) { double t = A[c][b]; A[c][b] = A[p][b]; A[p][b] = t; } det = -det; }
        det *= A[c][c];
        for (int r = c + 1; r < m; r++) { double f = A[r][c] / A[c][c]; if (f != 0) for (int b = c; b <= m; b++) A[r][b] -= f * A[c][b]; }
    }
    double y[MAXN];
    for (int c = m - 1; c >= 0; c--) { double s = A[c][m]; for (int b = c + 1; b < m; b++) s -= A[c][b] * y[b]; y[c] = s / A[c][c]; }
    long long D = llround(det);
    if (D == 0) { singular++; return; }
    X[0] = 0; X[n - 1] = D;
    for (int j = 1; j <= n - 2; j++) X[j] = llround((double)D * y[j - 1]);
    for (int j = 1; j <= n - 2; j++) if (2 * X[j] != X[L[j]] + X[R[j]]) {
        fallback++;
        printf("FALLBACK");
        for (int q = 1; q <= n - 2; q++) printf(" %d,%d,%d", L[q], q, R[q]);
        printf("\n");
        return;
    }
    if (D < 0) { orderfail++; return; }
    for (int j = 0; j + 1 < n; j++) if (X[j] >= X[j + 1]) { orderfail++; return; }
    /* now 0 = X_0 < ... < X_{n-1} = D, all integers */
    long long M = X[n - 1];
    if (2 * M >= (long long)sizeof(sums) || M >= (long long)(64 * 64)) { fprintf(stderr, "range overflow M=%lld\n", M); exit(3); }
    int ws = 1;
    for (int a = 0; a < n && ws; a++) for (int b = a + 1; b < n; b++) { long long s = X[a] + X[b]; if (sums[s]) { ws = 0; break; } sums[s] = 1; }
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) sums[X[a] + X[b]] = 0;
    if (!ws) { notws++; return; }
    /* (4,5) by definition */
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) for (int d = c + 1; d < n; d++) {
        long long v[6] = { X[b] - X[a], X[c] - X[a], X[d] - X[a], X[c] - X[b], X[d] - X[b], X[d] - X[c] };
        int distinct = 0;
        for (int i = 0; i < 6; i++) { int seen = 0; for (int k = 0; k < i; k++) if (v[k] == v[i]) { seen = 1; break; } if (!seen) distinct++; }
        if (distinct < 5) { not45++; return; }
    }
    /* 3-AP count of the set itself */
    for (int a = 0; a < n; a++) posof[X[a]] = a + 1;
    int aps = 0, mapok = 1;
    for (int a = 0; a < n; a++) for (int c = a + 2; c < n; c++) {
        long long s = X[a] + X[c]; if (s & 1) continue;
        int b = posof[s / 2]; if (b) { aps++; b--; if (!(L[b] == a && R[b] == c)) mapok = 0; }
    }
    for (int a = 0; a < n; a++) posof[X[a]] = 0;
    if (aps != n - 2 || !mapok) { apbad++; return; }
    ok45++;
    /* h by definition */
    memset(used, 0, sizeof(used)); best = 0; nch = 0; sidon_dfs(0);
    hhist[best]++;
    /* canonical form */
    long long g = 0; for (int a = 0; a < n; a++) g = gcdll(g, X[a]);
    long long P[MAXN], Q[MAXN];
    for (int a = 0; a < n; a++) { P[a] = X[a] / g; }
    for (int a = 0; a < n; a++) { Q[a] = P[n - 1] - P[n - 1 - a]; }
    int cmp = 0; for (int a = 0; a < n; a++) { if (P[a] != Q[a]) { cmp = P[a] < Q[a] ? -1 : 1; break; } }
    if (cmp == 0) canon_eq_refl++;
    if (cmp <= 0) {
        printed++;
        printf("S %d", best); for (int a = 0; a < n; a++) printf(" %lld", P[a]); printf("\n");
    }
}

static void dfs(int j) {
    if (j == n - 1) { leaf(); return; }
    for (int l = 0; l < j; l++) for (int r = j + 1; r <= n - 1; r++) {
        if (j == 1 && onlyR1 >= 0 && r != onlyR1) continue;
        int bad = 0;
        for (int i = 1; i < j && !bad; i++) {
            if (useK30 && l <= L[i] && r <= R[i]) bad = 1;
            if (useLIN && !bad) {
                int common = 0;
                int e1[3] = { L[i], i, R[i] }, e2[3] = { l, j, r };
                for (int u = 0; u < 3; u++) for (int w = 0; w < 3; w++) if (e1[u] == e2[w]) common++;
                if (common >= 2) bad = 1;
            }
        }
        if (bad) continue;
        L[j] = l; R[j] = r;
        dfs(j + 1);
    }
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s n k30 lin [r1]\n", argv[0]); return 1; }
    n = atoi(argv[1]); useK30 = atoi(argv[2]); useLIN = atoi(argv[3]);
    if (argc > 4) onlyR1 = atoi(argv[4]);
    if (n < 3 || n > 12) { fprintf(stderr, "n out of range\n"); return 1; }
    memset(sums, 0, sizeof(sums)); memset(posof, 0, sizeof(posof));
    dfs(1);
    printf("STATS n=%d k30=%d lin=%d r1=%d leaves=%lld singular=%lld fallback=%lld orderfail=%lld notweakSidon=%lld not45=%lld apbad=%lld ok45=%lld printed=%lld symmetric=%lld hhist",
           n, useK30, useLIN, onlyR1, leaves, singular, fallback, orderfail, notws, not45, apbad, ok45, printed, canon_eq_refl);
    for (int h = 0; h <= n; h++) if (hhist[h]) printf(" %d:%lld", h, hhist[h]);
    printf("\n");
    return 0;
}
