/* mytau.c -- referee L016 round 1 (own code): exact transversal number of each input 3-graph ("m a1 b1 c1 ..." lines);
   prints one number per line (branch and bound: unmet edge with fewest candidates, earlier siblings excluded, matching bound). */
#include <stdio.h>
#include <stdint.h>
static uint32_t E[64]; static int m;
static int lbound(uint32_t S) { uint32_t used = 0; int k = 0; for (int i = 0; i < m; i++) if (!(E[i] & S) && !(E[i] & used)) { used |= E[i]; k++; } return k; }
static int hascov(uint32_t S, int budget, uint32_t forb) {
    int best = -1, bc = 4;
    for (int i = 0; i < m; i++) if (!(E[i] & S)) { int c = __builtin_popcount(E[i] & ~forb); if (c < bc) { bc = c; best = i; if (c == 0) break; } }
    if (best < 0) return 1;
    if (bc == 0 || budget == 0) return 0;
    if (lbound(S) > budget) return 0;
    uint32_t f2 = forb;
    for (uint32_t r = E[best] & ~forb; r; r &= r - 1) { uint32_t v = r & -r; if (hascov(S | v, budget - 1, f2)) return 1; f2 |= v; }
    return 0;
}
int main(void) {
    while (scanf("%d", &m) == 1) {
        for (int i = 0; i < m; i++) { int a, b, c; if (scanf("%d %d %d", &a, &b, &c) != 3) return 2; E[i] = (1u << a) | (1u << b) | (1u << c); }
        int t = 0; while (!hascov(0, t, 0)) t++;
        printf("%d\n", t);
    }
    return 0;
}
