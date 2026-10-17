/* bf_count.c: count all labelled linear 3-graphs on [n] by DFS over triples in index order (no isomorphism reduction). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, nt; static uint32_t T[200]; static uint32_t cov[32]; static unsigned long long cnt[40];
static void rec(int start, int m) {
    cnt[m]++;
    for (int i = start; i < nt; i++) {
        uint32_t t = T[i]; int a = __builtin_ctz(t), b = __builtin_ctz(t & (t - 1)), c = 31 - __builtin_clz(t);
        if ((cov[a] >> b & 1) || (cov[a] >> c & 1) || (cov[b] >> c & 1)) continue;
        cov[a] |= (1u<<b)|(1u<<c); cov[b] |= (1u<<a)|(1u<<c); cov[c] |= (1u<<a)|(1u<<b);
        rec(i + 1, m + 1);
        cov[a] &= ~((1u<<b)|(1u<<c)); cov[b] &= ~((1u<<a)|(1u<<c)); cov[c] &= ~((1u<<a)|(1u<<b));
    }
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); nt = 0;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) T[nt++] = (1u<<a)|(1u<<b)|(1u<<c);
    rec(0, 0);
    unsigned long long tot = 0; for (int m = 0; m < 40; m++) if (cnt[m]) { printf("m=%d %llu\n", m, cnt[m]); tot += cnt[m]; }
    printf("total %llu\n", tot); return 0;
}
