/* referee_hooks_f7.c -- as referee_hooks.c (tau prune), plus an F7 prune: reject an intermediate graph if the LAST added edge
   lies in a copy of F7 = {012,034,056,135,246}.  Valid for enumerating F7-free graphs: every intermediate graph is a
   sub-hypergraph of the output, and genbg guarantees that the graph minus its last edge-vertex already passed the prune, so
   any F7 copy in the intermediate graph must use the last edge.  Linearity (-Z1) is assumed (pair -> third vertex is unique).
   Checks: (i) last edge e* as one of the three edges at the centre p (p in e*); (ii) e* as one of the two edges avoiding p. */
#include "gtools.h"
#include <stdint.h>
static int T0 = -999;
static uint32_t EE[64]; static int NE; static int third[32][32];
static unsigned long long n_calls = 0, n_pr_tau = 0, n_pr_f7 = 0, n_out = 0;
static int coverable(uint32_t left, int k) {
    if (!left) return 1;
    if (k <= 0) return 0;
    int i = __builtin_ctz(left); uint32_t e = EE[i];
    while (e) { int v = __builtin_ctz(e); e &= e - 1; uint32_t l2 = left;
        for (int j = 0; j < NE; j++) if ((l2 >> j & 1) && (EE[j] >> v & 1)) l2 &= ~(1u << j);
        if (coverable(l2, k - 1)) return 1; }
    return 0;
}
static void load(graph *g, int n1, int n2) {
    NE = n2;
    for (int j = 0; j < n2; j++) { setword w = g[n1 + j]; uint32_t e = 0; for (int i = 0; i < n1; i++) if (w & bit[i]) e |= 1u << i; EE[j] = e; }
}
static void vs(uint32_t e, int *a) { a[0] = __builtin_ctz(e); e &= e - 1; a[1] = __builtin_ctz(e); e &= e - 1; a[2] = __builtin_ctz(e); }
static int last_in_f7(int n1) {
    for (int a = 0; a < n1; a++) for (int b = 0; b < n1; b++) third[a][b] = -1;
    for (int j = 0; j < NE; j++) { int x[3]; vs(EE[j], x);
        third[x[0]][x[1]] = third[x[1]][x[0]] = x[2]; third[x[0]][x[2]] = third[x[2]][x[0]] = x[1]; third[x[1]][x[2]] = third[x[2]][x[1]] = x[0]; }
    uint32_t es = EE[NE - 1]; int s[3]; vs(es, s);
    /* (i) e* contains the centre p */
    for (int k = 0; k < 3; k++) {
        int p = s[k], a1 = s[(k + 1) % 3], b1 = s[(k + 2) % 3];
        int oth[8][2], no = 0;
        for (int j = 0; j < NE - 1; j++) if (EE[j] >> p & 1) { uint32_t r = EE[j] & ~(1u << p); oth[no][0] = __builtin_ctz(r); r &= r - 1; oth[no][1] = __builtin_ctz(r); no++; }
        for (int u = 0; u < no; u++) for (int w = u + 1; w < no; w++)
            for (int c2 = 0; c2 < 2; c2++) for (int c3 = 0; c3 < 2; c3++) {
                int x2 = oth[u][c2], y2 = oth[u][1 - c2], x3 = oth[w][c3], y3 = oth[w][1 - c3];
                if (third[a1][x2] == x3 && third[b1][y2] == y3) return 1;
            }
    }
    /* (ii) e* = {x1,x2,x3} avoids the centre p: E_i = {p, x_i, y_i}, and {y1,y2,y3} is an edge */
    for (int p = 0; p < n1; p++) {
        if (es >> p & 1) continue;
        int y1 = third[p][s[0]], y2 = third[p][s[1]], y3 = third[p][s[2]];
        if (y1 < 0 || y2 < 0 || y3 < 0) continue;
        if (third[y1][y2] == y3) return 1;
    }
    return 0;
}
int tauf7prune(graph *g, int *deg, int n1, int n2, int maxn2) {
    if (T0 == -999) { char *s = getenv("TAU0"); T0 = s ? atoi(s) : 0; }
    n_calls++;
    load(g, n1, n2);
    if (n2 >= 5 && last_in_f7(n1)) { n_pr_f7++; return 1; }
    int need = T0 - (maxn2 - n2);
    if (need <= 0) return 0;
    uint32_t all = (n2 >= 32) ? 0xffffffffu : ((1u << n2) - 1);
    if (coverable(all, need - 1)) { n_pr_tau++; return 1; }
    return 0;
}
void refout(FILE *f, graph *g, int n1, int n2) {
    load(g, n1, n2); n_out++;
    fprintf(f, "FOUND:");
    for (int j = 0; j < n2; j++) { int first = 1; fprintf(f, " ("); for (int i = 0; i < n1; i++) if (EE[j] >> i & 1) { fprintf(f, first ? "%d" : ",%d", i); first = 0; } fprintf(f, ")"); }
    fprintf(f, "\n");
}
void refsummary(nauty_counter nout, double cpu) {
    fprintf(stderr, "REFSUMMARY TAU0=%d calls=%llu pruned_f7=%llu pruned_tau=%llu outputs=%llu cpu=%.2f\n", T0, n_calls, n_pr_f7, n_pr_tau, n_out, cpu);
}
