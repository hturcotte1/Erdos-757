/* Referee L014 r1 -- own re-insertion + filter (written from scratch; no code shared with ext_d.c / filt.c).
   Usage: myext2 NV T D EP < inputs ("m a b c ..." per line; G on vertices 0..NV-1)
   For each G: (P1)-(P3) and F7-freeness of G are checked once (input sanity, counted); tau(G) exactly.
     tau(G) <= T-2: no extension has tau >= T.
     tau(G) == T-1: all minimum covers are enumerated (exclusion branching); a D-set of pairwise disjoint admissible pairs gives
        tau(H) >= T iff every minimum cover misses one of its pairs.  The D-sets are found by branching on the pairs that kill the
        first unkilled cover (NO exclusion of siblings), completions free once every cover is killed; duplicates are removed with a
        hash set of sorted index tuples.  So every hitting D-set is found (some pair of it kills the first unkilled cover at every node).
     tau(G) >= T: every D-set; tau(H) computed exactly and kept iff tau(H) == T.
   Admissible pair {a,b}: a != b, deg_G(a), deg_G(b) <= EP, no edge of G contains both.
   Every distinct hit H = G + {w,a_i,b_i} (w = NV) is filtered: F7-free (full search), (P3) on H (Hall test for all pairs {w,v};
   valid because G satisfies (P3), so a violating set contains w -- G's (P3) is verified on every input), connected on NV+1 vertices.
   Survivors are printed as "FOUND: (a,b,c) ..."; SUMMARY at the end. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t u32; typedef uint64_t u64;
static int NV, T, D, EP, m, M; static u32 E[64]; static int ev[64][3];
static u32 *covers; static long ncov, capcov; static int collect;
static int rec(u32 ch, u32 fb, int k, int mm) {
  int i; for (i = 0; i < mm; i++) if (!(E[i] & ch)) break;
  if (i == mm) { if (collect) { if (ncov == capcov) { capcov = capcov ? 2*capcov : 1024; covers = realloc(covers, capcov*sizeof(u32)); } covers[ncov++] = ch; } return 1; }
  if (k == 0) return 0;
  int found = 0; u32 f = fb;
  for (int j = 0; j < 3; j++) { u32 b = 1u << ev[i][j]; if (f & b) continue; if (rec(ch | b, f, k - 1, mm)) { found = 1; if (!collect) return 1; } f |= b; }
  return found;
}
static int tau_of(int mm) { collect = 0; for (int k = 0; k <= mm; k++) if (rec(0, 0, k, mm)) return k; return mm; }
static int hasF7(int nv, int mm) {
  for (int x = 0; x < nv; x++) {
    int inc[16], ni = 0; for (int i = 0; i < mm; i++) if (E[i] >> x & 1) { if (ni < 16) inc[ni++] = i; }
    for (int a = 0; a < ni; a++) for (int b = a + 1; b < ni; b++) for (int c = b + 1; c < ni; c++) {
      int pr[3][2], id[3] = {inc[a], inc[b], inc[c]};
      for (int q = 0; q < 3; q++) { int k = 0; for (int j = 0; j < 3; j++) if (ev[id[q]][j] != x) pr[q][k++] = ev[id[q]][j]; }
      for (int s = 0; s < 8; s++) { u32 m1 = 0, m2 = 0;
        for (int q = 0; q < 3; q++) { int bit = s >> q & 1; m1 |= 1u << pr[q][bit]; m2 |= 1u << pr[q][1 - bit]; }
        int f1 = 0, f2 = 0; for (int i = 0; i < mm; i++) { if (E[i] == m1) f1 = 1; if (E[i] == m2) f2 = 1; }
        if (f1 && f2) return 1; } } }
  return 0;
}
static int mv[33], seen[33];
static int aug(int i, int u, int v) {
  for (int j = 0; j < 3; j++) { int x = ev[i][j]; if (x == u || x == v || seen[x]) continue; seen[x] = 1;
    if (mv[x] < 0 || aug(mv[x], u, v)) { mv[x] = i; return 1; } }
  return 0;
}
static int hall(int nv, int mm, int u, int v) { for (int x = 0; x < nv; x++) mv[x] = -1;
  for (int i = 0; i < mm; i++) { memset(seen, 0, sizeof seen); if (!aug(i, u, v)) return 0; } return 1; }
static int p3_all(int nv, int mm) { for (int u = 0; u < nv; u++) for (int v = u + 1; v < nv; v++) if (!hall(nv, mm, u, v)) return 0; return 1; }
static int connected(int nv, int mm) { u32 r = 1, old = 0; while (r != old) { old = r; for (int i = 0; i < mm; i++) if (E[i] & r) r |= E[i]; }
  return r == (nv == 32 ? 0xffffffffu : ((1u << nv) - 1)); }
static int linear(int mm) { for (int a = 0; a < mm; a++) for (int b = a + 1; b < mm; b++) if (__builtin_popcount(E[a] & E[b]) > 1) return 0; return 1; }
/* pairs */
static int np, pa[1024], pb[1024]; static u32 pm[1024]; static int W; static u64 *K;
/* hash set of D-sets */
static u64 *hs; static long hcap, hcnt;
static void hs_reset(void) { if (!hs) { hcap = 1 << 16; hs = malloc(hcap * sizeof(u64)); } memset(hs, 0xff, hcap * sizeof(u64)); hcnt = 0; }
static int hs_insert(u64 key) {
  if (2 * (hcnt + 1) > hcap) { long oc = hcap; u64 *old = hs; hcap *= 2; hs = malloc(hcap * sizeof(u64)); memset(hs, 0xff, hcap * sizeof(u64)); hcnt = 0;
    for (long i = 0; i < oc; i++) if (old[i] != ~0ull) hs_insert(old[i]); free(old); }
  u64 h = key * 0x9E3779B97F4A7C15ull; long i = (long)(h >> 20) & (hcap - 1);
  while (hs[i] != ~0ull) { if (hs[i] == key) return 0; i = (i + 1) & (hcap - 1); }
  hs[i] = key; hcnt++; return 1;
}
static long st_inputs, st_badG, st_tlo, st_teq, st_thi, st_nodes, st_dsets, st_hits, st_f7, st_p3, st_dis, st_wrongtau, st_surv, st_maxcov;
static int chosen[8];
static void process_dset(int *ids) {   /* ids sorted */
  u64 key = 0; for (int q = 0; q < D; q++) key = key << 10 | (u64)ids[q];
  if (!hs_insert(key)) return;
  st_hits++;
  for (int q = 0; q < D; q++) { int e = m + q; ev[e][0] = NV; ev[e][1] = pa[ids[q]]; ev[e][2] = pb[ids[q]]; E[e] = (1u << NV) | pm[ids[q]]; }
  M = m + D; int nv = NV + 1;
  if (hasF7(nv, M)) { st_f7++; return; }
  for (int v = 0; v < NV; v++) if (!hall(nv, M, NV, v)) { st_p3++; return; }
  if (!connected(nv, M)) { st_dis++; return; }
  if (ncov == 0) { /* tau(G) >= T branch: exact tau(H) */ if (tau_of(M) != T) { st_wrongtau++; return; } }
  st_surv++; printf("FOUND:"); for (int i = 0; i < M; i++) printf(" (%d,%d,%d)", ev[i][0], ev[i][1], ev[i][2]); printf("\n");
}
static void sort_and_process(int *c) { int ids[8]; memcpy(ids, c, D * sizeof(int));
  for (int i = 1; i < D; i++) for (int j = i; j > 0 && ids[j-1] > ids[j]; j--) { int t = ids[j]; ids[j] = ids[j-1]; ids[j-1] = t; }
  process_dset(ids); }
static void freecomp(int lvl, u32 used, int start) {
  if (lvl == D) { st_dsets++; sort_and_process(chosen); return; }
  for (int p = start; p < np; p++) { if (pm[p] & used) continue; chosen[lvl] = p; freecomp(lvl + 1, used | pm[p], p + 1); }
}
static void search(int lvl, u32 used, u64 *U) {
  st_nodes++;
  int first = -1; for (int w = 0; w < W; w++) if (U[w]) { first = w * 64 + __builtin_ctzll(U[w]); break; }
  if (first < 0) { freecomp(lvl, used, 0); return; }
  if (lvl == D) return;
  u64 U2[64]; int fw = first >> 6; u64 fb = 1ull << (first & 63);
  for (int p = 0; p < np; p++) {
    if (pm[p] & used) continue;
    if (!(K[(size_t)p * W + fw] & fb)) continue;
    for (int w = 0; w < W; w++) U2[w] = U[w] & ~K[(size_t)p * W + w];
    chosen[lvl] = p; search(lvl + 1, used | pm[p], U2);
  }
}
int main(int argc, char **argv) {
  NV = atoi(argv[1]); T = atoi(argv[2]); D = atoi(argv[3]); EP = atoi(argv[4]);
  if (NV > 31 || D > 6) { fprintf(stderr, "limits\n"); return 2; }
  while (scanf("%d", &m) == 1) {
    if (m + D > 64) { fprintf(stderr, "too many edges\n"); return 3; }
    int deg[32] = {0};
    for (int i = 0; i < m; i++) { E[i] = 0; for (int j = 0; j < 3; j++) { int v; if (scanf("%d", &v) != 1) return 4; if (v < 0 || v >= NV) return 5; ev[i][j] = v; E[i] |= 1u << v; deg[v]++; }
      if (__builtin_popcount(E[i]) != 3) return 6; }
    st_inputs++;
    if (!linear(m) || hasF7(NV, m) || !p3_all(NV, m)) st_badG++;   /* G should be in C (sound lists); counted, and H is fully filtered anyway */
    int bad = !linear(m) || !p3_all(NV, m);
    int t0 = tau_of(m); ncov = 0;
    if (t0 <= T - 2) { st_tlo++; continue; }
    if (t0 == T - 1) { st_teq++; collect = 1; rec(0, 0, t0, m); } else st_thi++;
    if (ncov > st_maxcov) st_maxcov = ncov;
    np = 0;
    for (int a = 0; a < NV; a++) for (int b = a + 1; b < NV; b++) {
      if (deg[a] > EP || deg[b] > EP) continue; u32 ab = (1u << a) | (1u << b); int in = 0;
      for (int i = 0; i < m; i++) if ((E[i] & ab) == ab) { in = 1; break; }
      if (in) continue; if (np >= 1024) { fprintf(stderr, "too many pairs\n"); return 7; }
      pa[np] = a; pb[np] = b; pm[np] = ab; np++; }
    W = (int)((ncov + 63) / 64); if (W < 1) W = 1; if (W > 64) { fprintf(stderr, "too many covers\n"); return 8; }
    K = realloc(K, (size_t)(np ? np : 1) * W * sizeof(u64)); memset(K, 0, (size_t)(np ? np : 1) * W * sizeof(u64));
    for (int p = 0; p < np; p++) for (long c = 0; c < ncov; c++) if (!(covers[c] & pm[p])) K[(size_t)p * W + (c >> 6)] |= 1ull << (c & 63);
    u64 U[64]; for (int w = 0; w < W; w++) U[w] = 0; for (long c = 0; c < ncov; c++) U[c >> 6] |= 1ull << (c & 63);
    hs_reset();
    if (bad) { /* a G violating (P1)/(P3): the P3 shortcut for H would be invalid; filter H with the full test instead */
      fprintf(stderr, "input %ld not in C (P1/P3); stopping\n", st_inputs); return 9; }
    search(0, 0, U);
  }
  printf("SUMMARY inputs=%ld G_not_in_C=%ld tauG_low=%ld tauG_eq=%ld tauG_high=%ld max_min_covers=%ld nodes=%ld dset_visits=%ld distinct_tau_hits=%ld F7=%ld P3fail=%ld disconnected=%ld wrongtau=%ld survivors=%ld\n",
         st_inputs, st_badG, st_tlo, st_teq, st_thi, st_maxcov, st_nodes, st_dsets, st_hits, st_f7, st_p3, st_dis, st_wrongtau, st_surv);
  return 0;
}
