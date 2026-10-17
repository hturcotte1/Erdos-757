/* Referee L011 round 2: labelled brute force.  Counts labelled linear 3-graphs on [n] with exactly m edges, max degree <= D,
   every point covered, connected, tau >= T0.  Usage: bf n m D T0  -> prints count. */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long u64;
int n, M, D, T0; int tri[200][3]; int ntri; int deg[32]; u64 pairused[32]; int chosen[64]; u64 cnt = 0;
static int cover(u64 *E, int ne, u64 S, int k) { int j; for (j = 0; j < ne; j++) if (!(E[j] & S)) break;
    if (j == ne) return 1; if (k <= 0) return 0; u64 e = E[j];
    while (e) { u64 b = e & (~e + 1); e ^= b; if (cover(E, ne, S | b, k - 1)) return 1; } return 0; }
static void leaf(void) {
    u64 E[64], all = 0; for (int i = 0; i < M; i++) { int *t = tri[chosen[i]]; E[i] = (1ULL<<t[0])|(1ULL<<t[1])|(1ULL<<t[2]); all |= E[i]; }
    if (all != (n == 64 ? ~0ULL : (1ULL << n) - 1)) return;
    u64 comp = E[0]; int ch = 1; while (ch) { ch = 0; for (int i = 0; i < M; i++) if ((E[i] & comp) && (E[i] & ~comp)) { comp |= E[i]; ch = 1; } }
    if (comp != all) return;
    if (T0 >= 1 && cover(E, M, 0, T0 - 1)) return;
    cnt++;
}
static void rec(int start, int k) {
    if (k == M) { leaf(); return; }
    for (int t = start; t < ntri; t++) {
        int a = tri[t][0], b = tri[t][1], c = tri[t][2];
        if (deg[a] >= D || deg[b] >= D || deg[c] >= D) continue;
        if ((pairused[a] >> b & 1) || (pairused[a] >> c & 1) || (pairused[b] >> c & 1)) continue;
        deg[a]++; deg[b]++; deg[c]++;
        pairused[a] |= 1ULL<<b | 1ULL<<c; pairused[b] |= 1ULL<<a | 1ULL<<c; pairused[c] |= 1ULL<<a | 1ULL<<b;
        chosen[k] = t; rec(t + 1, k + 1);
        deg[a]--; deg[b]--; deg[c]--;
        pairused[a] &= ~(1ULL<<b | 1ULL<<c); pairused[b] &= ~(1ULL<<a | 1ULL<<c); pairused[c] &= ~(1ULL<<a | 1ULL<<b);
    }
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); M = atoi(argv[2]); D = atoi(argv[3]); T0 = atoi(argv[4]);
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) { tri[ntri][0] = a; tri[ntri][1] = b; tri[ntri][2] = c; ntri++; }
    rec(0, 0); printf("%llu\n", cnt); return 0;
}
