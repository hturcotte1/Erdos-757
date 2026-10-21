/* referee: exact check of a point set (<= 31 points): distinct; every 4-subset has >= 5 distinct |differences|;
   all additive coincidences a+b=c+d ({a,b} != {c,d}, a<=b, c<=d) as vertex masks; brute force over ALL k-subsets for
   k = K and K+1: number of Sidon k-subsets. Usage: c27check K < points */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef long long ll; typedef uint32_t u32;
int main(int argc, char **argv) {
    int K = atoi(argv[1]); ll x[64]; int n = 0; while (n < 64 && scanf("%lld", &x[n]) == 1) n++;
    for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) if (x[i] == x[j]) { printf("DUPLICATE\n"); return 1; }
    long bad4 = 0, n4 = 0;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) for (int d = c + 1; d < n; d++) {
        ll p[4] = {x[a], x[b], x[c], x[d]}, df[6]; int k = 0;
        for (int i = 0; i < 4; i++) for (int j = i + 1; j < 4; j++) df[k++] = llabs(p[i] - p[j]);
        int dist = 0; for (int i = 0; i < 6; i++) { int seen = 0; for (int j = 0; j < i; j++) if (df[j] == df[i]) seen = 1; if (!seen) dist++; }
        n4++; if (dist < 5) bad4++;
    }
    printf("n=%d four_subsets=%ld with_fewer_than_5_distances=%ld\n", n, n4, bad4);
    static u32 viol[100000]; int nv = 0, n3 = 0, n4v = 0;
    for (int a = 0; a < n; a++) for (int b = a; b < n; b++) for (int c = 0; c < n; c++) for (int d = c; d < n; d++) {
        if (a == c && b == d) continue;
        if (x[a] + x[b] != x[c] + x[d]) continue;
        if (a > c || (a == c && b > d)) continue;  /* each unordered coincidence once */
        u32 m = (1u << a) | (1u << b) | (1u << c) | (1u << d);
        if (__builtin_popcount(m) == 3) n3++; else n4v++;
        viol[nv++] = m;
    }
    printf("coincidences a+b=c+d: total=%d (3-point, i.e. 3-APs: %d; 4-point: %d)\n", nv, n3, n4v);
    for (int k = K; k <= K + 1; k++) {
        if (k > n) break;
        u32 S = (1u << k) - 1, lim = (n == 32) ? 0xffffffffu : ((1u << n) - 1); long long cnt = 0, sid = 0; u32 ex = 0;
        while (S <= lim) {
            cnt++; int ok = 1; for (int i = 0; i < nv; i++) if ((viol[i] & S) == viol[i]) { ok = 0; break; }
            if (ok) { if (!sid) ex = S; sid++; }
            u32 c = S & -S, r = S + c; if (r == 0) break; S = (((r ^ S) >> 2) / c) | r;
        }
        printf("k=%d: subsets=%lld Sidon=%lld", k, cnt, sid);
        if (sid) { printf(" example:"); for (int i = 0; i < n; i++) if (ex >> i & 1) printf(" %lld", x[i]); }
        printf("\n");
    }
    return 0;
}
