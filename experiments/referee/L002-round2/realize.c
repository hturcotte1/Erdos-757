/* Referee round 2 (L002): independent exact realizer for SATURATED ordered midpoint patterns on n points.
 * Input lines: "P m f7 i,j,k i,j,k ..." (from enum.c) or plain "i,j,k i,j,k ..." lines.
 * Method: unknowns x_1..x_{n-2}, x_0=0, x_{n-1}=1, equations 2x_j = x_l(j) + x_r(j).
 *   (1) solve in long double (partial pivoting), det = signed product of pivots, D = |round(det)|;
 *   (2) X_j = round(D*x_j); CERTIFY EXACTLY in int64 that X_0=0, X_{n-1}=D>0 and 2X_j = X_l(j)+X_r(j) for all j.
 *       Then X/D is the unique solution (the system is nonsingular: D != 0 and det is an integer computed with
 *       error << 1/2; nonsingularity is also proved by the M-matrix argument).
 *   (3) exact integer checks: strict order; set of 3-APs == pattern; (4,5) on all 4-subsets; h = largest Sidon
 *       subset by exhaustive DFS from the definition (positive differences distinct), plus a witness.
 * Output for realizable patterns: "R <labelled pattern> | <canonical normalized set>" where canonical = min over
 * {X/g, reflection} (lexicographic), g = gcd. Summary on stderr.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>

#define N 12
typedef long long ll;
static ll gcdll(ll a, ll b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { ll t = a % b; a = b; b = t; } return a; }

static int best_sidon; static ll vals[N];
static ll diffs[64]; static int nd;
static void sidon_dfs(int start, int size) {
    if (size > best_sidon) best_sidon = size;
    if (size + (N - start) <= best_sidon) return;
    static int chosen[N];
    for (int v = start; v < N; v++) {
        /* new differences vals[v]-vals[c] for chosen c; must be distinct from each other and from diffs */
        int ok = 1, nd0 = nd;
        for (int c = 0; c < size && ok; c++) {
            ll d = vals[v] - vals[chosen[c]];
            for (int t = 0; t < nd; t++) if (diffs[t] == d) { ok = 0; break; }
            if (ok) diffs[nd++] = d;
        }
        if (ok) { chosen[size] = v; sidon_dfs(v + 1, size + 1); }
        nd = nd0;
        if (size + (N - v - 1) <= best_sidon) return;
    }
}

int main(void) {
    char line[4096];
    ll nlines = 0, badparse = 0, notsat = 0, singular = 0, certfail = 0, order_inf = 0, extra_ap = 0, not45 = 0, realizable = 0;
    ll hhist[N + 1] = {0}, f7real = 0, f7lines = 0, maxD = 0;
    while (fgets(line, sizeof line, stdin)) {
        char *p = line; int f7 = 0;
        if (line[0] == 'P') { int m; if (sscanf(line, "P %d %d", &m, &f7) != 2) { badparse++; continue; }
            p = line + 2; while (*p && *p != ' ') p++; p++; while (*p && *p != ' ') p++; }
        int l[N], r[N], cnt = 0; for (int j = 0; j < N; j++) l[j] = r[j] = -1;
        int E[N][3];
        char *tok = strtok(p, " \n");
        int bad = 0;
        while (tok) {
            int a, b, c; if (sscanf(tok, "%d,%d,%d", &a, &b, &c) != 3) { bad = 1; break; }
            if (!(0 <= a && a < b && b < c && c < N) || l[b] != -1) { bad = 1; break; }
            l[b] = a; r[b] = c; E[cnt][0] = a; E[cnt][1] = b; E[cnt][2] = c; cnt++;
            tok = strtok(NULL, " \n");
        }
        nlines++;
        if (bad) { badparse++; continue; }
        if (f7) f7lines++;
        int sat = (cnt == N - 2); for (int j = 1; j <= N - 2; j++) if (l[j] < 0) sat = 0;
        if (!sat) { notsat++; continue; }
        /* (1) float solve */
        const int K = N - 2; long double A[N][N + 1];
        for (int a = 0; a < K; a++) for (int b = 0; b <= K; b++) A[a][b] = 0;
        for (int j = 1; j <= K; j++) {
            int row = j - 1; A[row][row] += 2;
            if (l[j] >= 1 && l[j] <= K) A[row][l[j] - 1] -= 1;
            if (r[j] >= 1 && r[j] <= K) A[row][r[j] - 1] -= 1; else if (r[j] == N - 1) A[row][K] += 1;
        }
        long double det = 1;
        for (int c = 0; c < K; c++) {
            int pv = c; for (int a = c + 1; a < K; a++) if (fabsl(A[a][c]) > fabsl(A[pv][c])) pv = a;
            if (fabsl(A[pv][c]) < 1e-12L) { det = 0; break; }
            if (pv != c) { for (int b = 0; b <= K; b++) { long double t = A[c][b]; A[c][b] = A[pv][b]; A[pv][b] = t; } det = -det; }
            det *= A[c][c];
            for (int a = c + 1; a < K; a++) { long double f = A[a][c] / A[c][c]; if (f != 0) for (int b = c; b <= K; b++) A[a][b] -= f * A[c][b]; }
        }
        ll D = llroundl(fabsl(det));
        if (D == 0) { singular++; continue; }
        long double x[N];
        for (int c = K - 1; c >= 0; c--) { long double s = A[c][K]; for (int b = c + 1; b < K; b++) s -= A[c][b] * x[b]; x[c] = s / A[c][c]; }
        ll X[N]; X[0] = 0; X[N - 1] = D;
        for (int j = 1; j <= K; j++) X[j] = llroundl(x[j - 1] * (long double)D);
        /* (2) exact certificate */
        int cert = 1;
        for (int j = 1; j <= K; j++) if (2 * X[j] != X[l[j]] + X[r[j]]) cert = 0;
        if (!cert) { certfail++; fprintf(stderr, "CERTFAIL %s\n", line); continue; }
        if (D > maxD) maxD = D;
        /* (3) order */
        int ord = 1; for (int j = 0; j + 1 < N; j++) if (!(X[j] < X[j + 1])) ord = 0;
        if (!ord) { order_inf++; continue; }
        /* 3-APs */
        int naps = 0, extra = 0;
        for (int a = 0; a < N; a++) for (int c = a + 2; c < N; c++) {
            ll s = X[a] + X[c]; if (s & 1) continue; s /= 2;
            for (int b = a + 1; b < c; b++) if (X[b] == s) { naps++; if (!(l[b] == a && r[b] == c)) extra = 1; }
        }
        if (extra || naps != N - 2) { extra_ap++; continue; }
        /* (4,5) */
        int ok45 = 1;
        for (int a = 0; a < N && ok45; a++) for (int b = a + 1; b < N && ok45; b++) for (int c = b + 1; c < N && ok45; c++) for (int d = c + 1; d < N && ok45; d++) {
            ll q[6] = { X[b]-X[a], X[c]-X[a], X[d]-X[a], X[c]-X[b], X[d]-X[b], X[d]-X[c] };
            int distinct = 0;
            for (int s = 0; s < 6; s++) { int seen = 0; for (int t = 0; t < s; t++) if (q[t] == q[s]) seen = 1; if (!seen) distinct++; }
            if (distinct < 5) ok45 = 0;
        }
        if (!ok45) { not45++; continue; }
        realizable++;
        if (f7) f7real++;
        for (int j = 0; j < N; j++) vals[j] = X[j];
        best_sidon = 0; nd = 0; sidon_dfs(0, 0);
        hhist[best_sidon]++;
        /* canonical normalized set */
        ll g = 0; for (int j = 0; j < N; j++) g = gcdll(g, X[j]);
        ll U[N], V[N]; for (int j = 0; j < N; j++) { U[j] = X[j] / g; V[j] = (D - X[N - 1 - j]) / g; }
        int useV = 0; for (int j = 0; j < N; j++) { if (V[j] < U[j]) { useV = 1; break; } if (V[j] > U[j]) break; }
        printf("R");
        for (int t = 0; t < cnt; t++) printf(" %d,%d,%d", E[t][0], E[t][1], E[t][2]);
        printf(" |");
        for (int j = 0; j < N; j++) printf(" %lld", useV ? V[j] : U[j]);
        printf(" | h=%d\n", best_sidon);
    }
    fprintf(stderr, "lines=%lld badparse=%lld notsat=%lld singular=%lld certfail=%lld order_infeasible=%lld extra_ap=%lld not45=%lld realizable=%lld f7lines=%lld f7realizable=%lld maxD=%lld\n",
            nlines, badparse, notsat, singular, certfail, order_inf, extra_ap, not45, realizable, f7lines, f7real, maxD);
    fprintf(stderr, "h_hist:"); for (int h = 0; h <= N; h++) if (hhist[h]) fprintf(stderr, " %d:%lld", h, hhist[h]); fprintf(stderr, "\n");
    return 0;
}
