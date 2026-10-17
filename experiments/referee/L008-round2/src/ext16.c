/* ext16.c -- referee round 2 (L008): one-point extensions of 15-point (4,5)-sets.  For each input set B (15 integers, one set
   per line), every candidate x in {2a-b, (a+b)/2 : a != b in B} \ B (x forms a new 3-AP with two points of B) is tested: B+{x}
   is a (4,5)-set iff every 4-subset containing x has >= 5 distinct |differences| (B itself is assumed (4,5); re-checked by
   i11_sets afterwards).  Prints each (4,5) extension B+{x} sorted, once per input set.  Usage: ext16 < sets15.txt */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static long long B[64]; static int n;
static int cmpll(const void *a, const void *b) { long long x = *(long long *)a, y = *(long long *)b; return x < y ? -1 : x > y; }
static int ok_with(long long x) {
    for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) for (int k = j + 1; k < n; k++) {
        long long q[4] = { B[i], B[j], B[k], x }, d[6]; int c = 0;
        for (int u = 0; u < 4; u++) for (int v = u + 1; v < 4; v++) { long long t = q[u] - q[v]; d[c++] = t < 0 ? -t : t; }
        int dist = 0; for (int u = 0; u < 6; u++) { int s = 0; for (int v = 0; v < u; v++) if (d[v] == d[u]) s = 1; if (!s) dist++; }
        if (dist < 5) return 0;
    }
    return 1;
}
int main(void) {
    char line[100000]; static long long cand[20000];
    while (fgets(line, sizeof line, stdin)) {
        n = 0; char *p = line, *e;
        while (1) { long long v = strtoll(p, &e, 10); if (e == p) break; B[n++] = v; p = e; }
        if (n < 4) continue;
        qsort(B, n, sizeof B[0], cmpll);
        int nc = 0;
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (i != j) {
            cand[nc++] = 2 * B[i] - B[j];
            if ((B[i] + B[j]) % 2 == 0 && i < j) cand[nc++] = (B[i] + B[j]) / 2;
        }
        qsort(cand, nc, sizeof cand[0], cmpll);
        for (int c = 0; c < nc; c++) {
            if (c && cand[c] == cand[c - 1]) continue;
            long long x = cand[c]; int in = 0; for (int i = 0; i < n; i++) if (B[i] == x) in = 1;
            if (in || !ok_with(x)) continue;
            long long S[64]; memcpy(S, B, n * sizeof B[0]); S[n] = x; qsort(S, n + 1, sizeof S[0], cmpll);
            for (int i = 0; i <= n; i++) printf(i < n ? "%lld " : "%lld\n", S[i]);
        }
    }
    return 0;
}
