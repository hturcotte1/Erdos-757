/* Referee L014 round 1 -- own re-insertion program (written from scratch; shares no code with ext_d.c).
   Input lines: "m a1 b1 c1 a2 b2 c2 ..." (a graph G on vertices 0..NV-1).
   Usage: myext NV T D EP
   For each G: compute tau(G) exactly (iterative deepening branching on the first uncovered edge, with exclusion of earlier
   siblings); if tau(G) == T-1, list ALL minimum covers (each minimal cover is produced exactly once by the exclusion branching);
   admissible pairs: {a,b}, a<b, deg_G(a) <= EP, deg_G(b) <= EP, a and b not in a common edge of G;
   then every D-set of pairwise vertex-disjoint admissible pairs is tested: tau(H) >= T iff every minimum cover of G is disjoint
   from at least one of the D pairs (H = G + {w,a_i,b_i}, w = NV).  If tau(G) >= T every D-set is a hit; if tau(G) <= T-2 none is.
   Output: "X <inputno> <m+D> edges..." for every hit (H on NV+1 vertices), and a SUMMARY line. No F7 / P3 pruning at all. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t u32; typedef uint64_t u64;
static int NV, T, D, EP, m; static u32 E[64]; static int ev[64][3];
static u32 *covers; static long ncov, capcov;
static long nodes_tau;
/* is there a cover of size <= k extending (chosen, forbidden)? enumerate if collect */
static int collect;
static int rec(u32 chosen, u32 forb, int k) {
  nodes_tau++;
  int i; for (i = 0; i < m; i++) if (!(E[i] & chosen)) break;
  if (i == m) { if (collect) { if (ncov == capcov) { capcov = capcov ? 2*capcov : 1024; covers = realloc(covers, capcov*sizeof(u32)); }
                   covers[ncov++] = chosen; } return 1; }
  if (k == 0) return 0;
  int found = 0; u32 f = forb;
  for (int j = 0; j < 3; j++) { int v = ev[i][j]; u32 b = 1u << v; if (f & b) continue;
    if (rec(chosen | b, f, k - 1)) { found = 1; if (!collect) return 1; }
    f |= b; }
  return found;
}
static int tau_exact(void) { collect = 0; for (int k = 0; k <= m; k++) if (rec(0, 0, k)) return k; return m; }
int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage: myext NV T D EP\n"); return 2; }
  NV = atoi(argv[1]); T = atoi(argv[2]); D = atoi(argv[3]); EP = atoi(argv[4]);
  if (NV > 31 || D > 4) { fprintf(stderr, "limits\n"); return 2; }
  long ninp = 0, nhits = 0, tau_eq = 0, tau_hi = 0, tau_lo = 0, maxcov = 0, totpairs = 0, totdsets = 0;
  long hist_tau[40] = {0};
  while (scanf("%d", &m) == 1) {
    if (m > 60) { fprintf(stderr, "too many edges\n"); return 3; }
    int deg[32] = {0};
    for (int i = 0; i < m; i++) { E[i] = 0; for (int j = 0; j < 3; j++) { int v; if (scanf("%d", &v) != 1) return 4; if (v < 0 || v >= NV) { fprintf(stderr, "bad vertex\n"); return 5; }
        ev[i][j] = v; E[i] |= 1u << v; deg[v]++; }
      if (__builtin_popcount(E[i]) != 3) { fprintf(stderr, "repeated vertex in edge (input %ld)\n", ninp); return 6; } }
    ninp++;
    int t0 = tau_exact(); hist_tau[t0]++;
    ncov = 0;
    if (t0 == T - 1) { collect = 1; rec(0, 0, t0); tau_eq++; }
    else if (t0 >= T) tau_hi++; else { tau_lo++; continue; }
    if (ncov > maxcov) maxcov = ncov;
    /* admissible pairs */
    int pa[512], pb[512]; u32 pm[512]; int np = 0;
    for (int a = 0; a < NV; a++) for (int b = a + 1; b < NV; b++) {
      if (deg[a] > EP || deg[b] > EP) continue;
      u32 ab = (1u << a) | (1u << b); int bad = 0;
      for (int i = 0; i < m; i++) if ((E[i] & ab) == ab) { bad = 1; break; }
      if (bad) continue;
      if (np >= 512) { fprintf(stderr, "too many pairs\n"); return 7; }
      pa[np] = a; pb[np] = b; pm[np] = ab; np++; }
    totpairs += np;
    int W = (int)((ncov + 63) / 64); if (W == 0) W = 1;
    u64 *K = calloc((size_t)np * W, sizeof(u64)); u64 *full = calloc(W, sizeof(u64));
    for (long c = 0; c < ncov; c++) full[c >> 6] |= 1ull << (c & 63);
    for (int p = 0; p < np; p++) for (long c = 0; c < ncov; c++) if (!(covers[c] & pm[p])) K[(size_t)p*W + (c >> 6)] |= 1ull << (c & 63);
    /* D-sets of pairwise disjoint pairs, D in 1..4 */
    int idx[4]; u64 acc[5][64]; /* W <= 64 assumed: ncov <= 4096 */
    if (W > 64) { fprintf(stderr, "too many covers %ld\n", ncov); return 8; }
    for (int w = 0; w < W; w++) acc[0][w] = 0;
    /* iterative nested loops via recursion emulation */
    int lvl = 0; idx[0] = -1; u32 used[5]; used[0] = 0;
    while (lvl >= 0) {
      idx[lvl]++;
      if (idx[lvl] >= np) { lvl--; continue; }
      int p = idx[lvl]; if (pm[p] & used[lvl]) continue;
      for (int w = 0; w < W; w++) acc[lvl+1][w] = acc[lvl][w] | K[(size_t)p*W + w];
      used[lvl+1] = used[lvl] | pm[p];
      if (lvl + 1 == D) {
        totdsets++;
        int ok = 1;
        if (t0 == T - 1) { for (int w = 0; w < W; w++) if (acc[D][w] != full[w]) { ok = 0; break; } }
        if (ok) { nhits++;
          printf("X %ld %d", ninp, m + D);
          for (int i = 0; i < m; i++) printf(" %d %d %d", ev[i][0], ev[i][1], ev[i][2]);
          for (int q = 0; q < D; q++) printf(" %d %d %d", NV, pa[idx[q]], pb[idx[q]]);
          printf("\n"); }
      } else { lvl++; idx[lvl] = idx[lvl-1]; }
    }
    free(K); free(full);
  }
  printf("SUMMARY inputs=%ld tauG_eq_T-1=%ld tauG_ge_T=%ld tauG_lt=%ld max_min_covers=%ld pairs=%ld dsets=%ld hits=%ld nodes_tau=%ld\n",
         ninp, tau_eq, tau_hi, tau_lo, maxcov, totpairs, totdsets, nhits, nodes_tau);
  printf("TAUHIST"); for (int i = 0; i < 40; i++) if (hist_tau[i]) printf(" %d:%ld", i, hist_tau[i]); printf("\n");
  return 0;
}
