/* Referee L007 r2: dual-graph brute force for connected linear 3-graphs with max degree <= 2.
   Such an H with m edges and n vertices <-> its dual G*: simple graph on m nodes, 3m-n edges, max degree <= 3,
   connected iff H is; tau(H) = m - nu(G*).  Usage: dual_bf m e numax  -> counts labelled G* on [m] with e edges,
   max degree <= 3, connected, matching number <= numax. */
#include <stdio.h>
#include <stdlib.h>
static int M, NE, NUMAX, P, pa[64], pb[64], deg[16], sel[64];
static long long total = 0, good = 0;
static int nu_rec(unsigned used, int k) { /* max matching using edges sel[k..] */
  int best = 0;
  for (int i = k; i < NE; i++) { int a = pa[sel[i]], b = pb[sel[i]];
    if ((used >> a & 1) || (used >> b & 1)) continue;
    int r = 1 + nu_rec(used | (1u << a) | (1u << b), i + 1); if (r > best) best = r; }
  return best;
}
static int connected(void) { unsigned comp = 1, prev = 0;
  while (comp != prev) { prev = comp; for (int i = 0; i < NE; i++) { int a = pa[sel[i]], b = pb[sel[i]];
    if ((comp >> a & 1) || (comp >> b & 1)) comp |= (1u << a) | (1u << b); } }
  return comp == (1u << M) - 1; }
static void rec(int start, int k) {
  if (k == NE) { total++; if (connected() && nu_rec(0, 0) <= NUMAX) { good++; if (good <= 5) { printf("G*:"); for (int i = 0; i < NE; i++) printf(" %d-%d", pa[sel[i]], pb[sel[i]]); printf("\n"); } } return; }
  for (int i = start; i <= P - (NE - k); i++) { int a = pa[i], b = pb[i];
    if (deg[a] >= 3 || deg[b] >= 3) continue;
    deg[a]++; deg[b]++; sel[k] = i; rec(i + 1, k + 1); deg[a]--; deg[b]--; }
}
int main(int argc, char **argv) { M = atoi(argv[1]); NE = atoi(argv[2]); NUMAX = atoi(argv[3]); P = 0;
  for (int a = 0; a < M; a++) for (int b = a + 1; b < M; b++) { pa[P] = a; pb[P] = b; P++; }
  rec(0, 0); printf("m=%d e=%d numax=%d : graphs with maxdeg<=3: %lld, connected with nu<=numax: %lld\n", M, NE, NUMAX, total, good);
  return 0; }
