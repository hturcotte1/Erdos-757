/* Referee L017 round 1 (independent code): matching number by subset DP for graph6 graphs (N <= 20);
   reports min over M>0 of 11*nu-3*M, the minimum ratio nu/M, and the graphs attaining them. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int N; static unsigned nb[32];
static signed char *memo;
static int nu(unsigned mask) {
    if (!mask) return 0;
    if (memo[mask] >= 0) return memo[mask];
    int v = __builtin_ctz(mask);
    unsigned rest = mask & ~(1u << v);
    int best = nu(rest);
    unsigned c = nb[v] & rest;
    while (c) { int u = __builtin_ctz(c); c &= c - 1; int t = 1 + nu(rest & ~(1u << u)); if (t > best) best = t; }
    return memo[mask] = best;
}
int main(void) {
    char line[1024];
    long long cnt = 0; int minval = 1 << 30; double minratio = 1e9; char argmin[1024] = "", argratio[1024] = "";
    int minval_N = 0, minval_M = 0, minval_nu = 0, ratio_nu = 0, ratio_M = 0;
    long long nviol = 0, neq = 0;
    memo = malloc(1u << 20);
    while (fgets(line, sizeof line, stdin)) {
        int len = strlen(line); while (len && (line[len-1] == '\n')) line[--len] = 0;
        if (!len || line[0] == '>') continue;
        N = line[0] - 63;
        memset(nb, 0, sizeof nb); int M = 0, bit = 0;
        for (int j = 1; j < N; j++) for (int i = 0; i < j; i++) {
            int b = ((line[1 + bit / 6] - 63) >> (5 - bit % 6)) & 1; bit++;
            if (b) { nb[i] |= 1u << j; nb[j] |= 1u << i; M++; }
        }
        for (int v = 0; v < N; v++) if (__builtin_popcount(nb[v]) > 3) { fprintf(stderr, "degree>3\n"); return 1; }
        memset(memo, -1, 1u << N);
        int x = nu((1u << N) - 1);
        cnt++;
        int val = 11 * x - 3 * M;
        if (val < 0) nviol++;
        if (val == 0 && M > 0) neq++;
        if (M > 0 && val < minval) { minval = val; strcpy(argmin, line); minval_N = N; minval_M = M; minval_nu = x; }
        if (M > 0 && (double)x / M < minratio - 1e-12) { minratio = (double)x / M; strcpy(argratio, line); ratio_nu = x; ratio_M = M; }
    }
    printf("graphs=%lld violations(11nu<3M)=%lld equality_with_M>0=%lld min(11nu-3M | M>0)=%d at %s (N=%d M=%d nu=%d); min nu/M=%d/%d at %s\n",
           cnt, nviol, neq, minval, argmin, minval_N, minval_M, minval_nu, ratio_nu, ratio_M, argratio);
    return 0;
}
