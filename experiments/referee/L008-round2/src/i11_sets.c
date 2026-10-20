/* i11_sets.c -- referee round 2 (L008): test Lemma A' / Corollary 3 / Theorem 1 / (P3) on every induced subset of real sets.
   Input: one set per line (integers).  For each set A (n <= 28): checks the (4,5) property (all 4-subsets, >= 5 distinct
   |differences|); builds the 3-AP hypergraph in rank order; computes tau(H[S]) for EVERY vertex subset S by the recursion
   tau(S) = 1 + min_{v in e} tau(S - v)  (e = some edge inside S; tau = 0 if none); and checks, for every S:
     P3: e(S) <= |S|-2 (|S|>=2);   I11: 11 tau(S) <= 3|S| + 2 e(S) for |S| <= 16;   T1: tau(S) <= 6 for |S| = 16;
     and h(S) = |S| - tau(S) >= f-values: min over |S| = 14, 15, 16 reported.
   Output per set: n, m, (4,5) flag, number of subsets, violations of P3 / I11 / T1, max of 11tau-3|S|-2e over |S|<=16, and the
   minimum of |S|-tau(S) for |S| = 12..16.  Usage: i11_sets < sets.txt */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static long long A[64]; static int n;
static int cmpll(const void *a, const void *b) { long long x = *(long long *)a, y = *(long long *)b; return x < y ? -1 : x > y; }
static int is45(void) {
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) for (int d = c + 1; d < n; d++) {
        long long q[4] = { A[a], A[b], A[c], A[d] }, df[6]; int k = 0;
        for (int i = 0; i < 4; i++) for (int j = i + 1; j < 4; j++) { long long x = q[i] - q[j]; df[k++] = x < 0 ? -x : x; }
        int dist = 0; for (int i = 0; i < 6; i++) { int seen = 0; for (int j = 0; j < i; j++) if (df[j] == df[i]) seen = 1; if (!seen) dist++; }
        if (dist < 5) return 0;
    }
    return 1;
}
int main(void) {
    char line[100000]; static uint8_t *tau = NULL;
    while (fgets(line, sizeof line, stdin)) {
        n = 0; char *p = line, *endp;
        while (1) { long long v = strtoll(p, &endp, 10); if (endp == p) break; A[n++] = v; p = endp; if (n > 28) break; }
        if (n < 3) continue; if (n > 28) { printf("SKIP n>28\n"); continue; }
        qsort(A, n, sizeof A[0], cmpll);
        uint32_t E[64]; int m = 0;
        for (int i = 0; i < n; i++) for (int k = i + 2; k < n; k++) {
            if ((A[i] + A[k]) % 2) continue; long long mid = (A[i] + A[k]) / 2;
            for (int j = i + 1; j < k; j++) if (A[j] == mid) { E[m++] = (1u << i) | (1u << j) | (1u << k); break; }
        }
        int ok45 = is45();
        uint64_t full = 1ull << n;
        tau = realloc(tau, full);
        unsigned long long nsub = 0, vP3 = 0, vI11 = 0, vT1 = 0; int worst = -1000; int minh[17]; for (int s = 0; s <= 16; s++) minh[s] = 99;
        for (uint64_t S = 0; S < full; S++) {
            int e = 0, first = -1;
            for (int j = 0; j < m; j++) if ((E[j] & S) == E[j]) { e++; if (first < 0) first = j; }
            int t;
            if (first < 0) t = 0;
            else { t = 99; uint32_t ed = E[first]; while (ed) { int v = __builtin_ctz(ed); ed &= ed - 1; int u = tau[S & ~(1ull << v)]; if (u < t) t = u; } t++; }
            tau[S] = (uint8_t)t;
            int s = __builtin_popcountll(S); nsub++;
            if (s >= 2 && e > s - 2) vP3++;
            if (s <= 16) { int d = 11 * t - 3 * s - 2 * e; if (d > worst) worst = d; if (d > 0) vI11++; if (s - t < minh[s]) minh[s] = s - t; }
            if (s == 16 && t > 6) vT1++;
        }
        printf("n=%d m=%d is45=%d subsets=%llu P3_viol=%llu I11_viol(|S|<=16)=%llu T1_viol(|S|=16,tau>6)=%llu max(11tau-3s-2e)=%d minh[12..16]=", n, m, ok45, nsub, vP3, vI11, vT1, worst);
        for (int s = 12; s <= 16; s++) printf(s < 16 ? "%d," : "%d\n", minh[s] == 99 ? -1 : minh[s]);
    }
    return 0;
}
