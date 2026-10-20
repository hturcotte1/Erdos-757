/* Referee L011 round 2: genbg hooks as in hk.c (tau prune, env TAU0) plus an optional F7 prune (env F7P=1).
   F7 prune: genbg calls the prune on a graph whose parent (delete the last class-2 vertex = edge E[n2-1]) already passed, so
   any F7 copy must use the newest edge e, as a spoke (e contains the centre v) or as one of the two transversal edges.  The
   prune fires only on an explicit F7 copy, so it never removes an F7-free graph (sound); outputs are re-filtered anyway. */
#include "gtools.h"
#include <stdlib.h>
typedef unsigned long long u64;
static int T0 = -1, F7P = 0;
static u64 ncalls = 0, npruned = 0, nf7 = 0, nout = 0, nbad = 0;
static void edges_of(graph *g, int n1, int n2, u64 *E) {
    for (int j = 0; j < n2; j++) { set *row = GRAPHROW(g, n1 + j, 1); u64 msk = 0;
        for (int i = 0; i < n1; i++) if (ISELEMENT(row, i)) msk |= 1ULL << i; E[j] = msk; }
}
static int cover(const u64 *E, int ne, u64 S, int k) { int j; for (j = 0; j < ne; j++) if (!(E[j] & S)) break;
    if (j == ne) return 1; if (k <= 0) return 0; u64 e = E[j];
    while (e) { u64 b = e & (~e + 1); e ^= b; if (cover(E, ne, S | b, k - 1)) return 1; } return 0; }
static int isedge(const u64 *E, int ne, u64 t) { for (int j = 0; j < ne; j++) if (E[j] == t) return 1; return 0; }
/* does the graph contain an F7 copy using edge index q? */
static int f7_with(const u64 *E, int ne, int n1, int q) {
    u64 e = E[q];
    for (int v = 0; v < n1; v++) {
        int at[64], na = 0; for (int j = 0; j < ne; j++) if (E[j] >> v & 1) at[na++] = j;
        if (na < 3) continue;
        for (int a = 0; a < na; a++) for (int b = a + 1; b < na; b++) for (int c = b + 1; c < na; c++) {
            u64 P0 = E[at[a]] & ~(1ULL << v), P1 = E[at[b]] & ~(1ULL << v), P2 = E[at[c]] & ~(1ULL << v);
            if ((P0 & P1) || (P0 & P2) || (P1 & P2)) continue;
            int spoke = (at[a] == q || at[b] == q || at[c] == q);
            u64 all = P0 | P1 | P2;
            if (spoke) {
                u64 P[3] = {P0, P1, P2};
                for (int s = 0; s < 8; s++) { u64 T1 = 0; for (int i = 0; i < 3; i++) { u64 lo = P[i] & (~P[i] + 1); T1 |= (s >> i & 1) ? (P[i] ^ lo) : lo; }
                    if (isedge(E, ne, T1) && isedge(E, ne, all ^ T1)) return 1; }
            } else if (!(e >> v & 1)) {
                if ((e & ~all) == 0 && __builtin_popcountll(e & P0) == 1 && __builtin_popcountll(e & P1) == 1 && __builtin_popcountll(e & P2) == 1
                    && isedge(E, ne, all ^ e)) return 1;
            }
        }
    }
    return 0;
}
static void init(void) { if (T0 < 0) { char *s = getenv("TAU0"); T0 = s ? atoi(s) : 0; s = getenv("F7P"); F7P = s ? atoi(s) : 0; } }
int hprune(graph *g, int *deg, int n1, int n2, int maxn2) {
    init(); ncalls++;
    u64 E[64]; int got = 0;
    if (F7P && n2 >= 5) { edges_of(g, n1, n2, E); got = 1; if (f7_with(E, n2, n1, n2 - 1)) { nf7++; return 1; } }
    int need = T0 - (maxn2 - n2);
    if (need <= 1) return 0;
    if (need > n2) { npruned++; return 1; }
    if (!got) edges_of(g, n1, n2, E);
    if (cover(E, n2, 0, need - 1)) { npruned++; return 1; }
    return 0;
}
void hout(FILE *f, graph *g, int n1, int n2) {
    u64 E[64]; edges_of(g, n1, n2, E); init();
    if (T0 >= 1 && cover(E, n2, 0, T0 - 1)) { nbad++; return; }
    nout++; fprintf(f, "G:");
    for (int j = 0; j < n2; j++) { int v[3], c = 0; for (int i = 0; i < n1; i++) if (E[j] >> i & 1) { if (c < 3) v[c] = i; c++; }
        if (c != 3) { nbad++; fprintf(f, " BAD"); continue; } fprintf(f, " (%d,%d,%d)", v[0], v[1], v[2]); }
    fprintf(f, "\n");
}
void hsum(nauty_counter n, double cpu) {
    fprintf(stderr, "HSUM tau0=%d f7p=%d calls=%llu pruned_tau=%llu pruned_f7=%llu out=%llu bad=%llu genbg_nout=%llu cpu=%.2f\n",
            T0, F7P, ncalls, npruned, nf7, nout, nbad, (unsigned long long)n, cpu);
}
