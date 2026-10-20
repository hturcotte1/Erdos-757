/* Referee L014 r1: filter for genbg output (graph6 of the incidence graph: first class = N hypergraph vertices, second class =
   M edge-nodes of degree 3).  Keeps hypergraphs with tau == T exactly, F7-free, (P3) e(S) <= |S|-2 for all |S|>=2 (Hall test:
   for every vertex pair {u,v}, the edges have an SDR avoiding u,v), max degree <= D, connected on all N vertices.
   Prints "FOUND: (a,b,c) ..." for survivors and a SUMMARY line.  Usage: genbg ... | gfilt N M T D   (own code) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t u32;
static int N, M, T, D, ev[64][3]; static u32 E[64];
static int rec(u32 ch, u32 fb, int k) {
  int i; for (i = 0; i < M; i++) if (!(E[i] & ch)) break;
  if (i == M) return 1; if (k == 0) return 0;
  u32 f = fb; for (int j = 0; j < 3; j++) { u32 b = 1u << ev[i][j]; if (f & b) continue; if (rec(ch | b, f, k - 1)) return 1; f |= b; }
  return 0;
}
static int tau(void) { for (int k = 0; k <= M; k++) if (rec(0, 0, k)) return k; return M; }
static int hasF7(void) {
  /* x with three edges e1,e2,e3; pairs p_i = e_i - x; two edges choosing complementary transversals */
  for (int x = 0; x < N; x++) {
    int inc[8], ni = 0; for (int i = 0; i < M; i++) if (E[i] >> x & 1) { if (ni < 8) inc[ni++] = i; }
    for (int a = 0; a < ni; a++) for (int b = a + 1; b < ni; b++) for (int c = b + 1; c < ni; c++) {
      int pr[3][2], id[3] = {inc[a], inc[b], inc[c]};
      for (int q = 0; q < 3; q++) { int k = 0; for (int j = 0; j < 3; j++) if (ev[id[q]][j] != x) pr[q][k++] = ev[id[q]][j]; }
      for (int s = 0; s < 8; s++) {
        u32 m1 = 0, m2 = 0; for (int q = 0; q < 3; q++) { int bit = s >> q & 1; m1 |= 1u << pr[q][bit]; m2 |= 1u << pr[q][1 - bit]; }
        int f1 = 0, f2 = 0; for (int i = 0; i < M; i++) { if (E[i] == m1) f1 = 1; if (E[i] == m2) f2 = 1; }
        if (f1 && f2) return 1; } } }
  return 0;
}
static int mv[32], seen[32];
static int aug(int i, int u, int v) {
  for (int j = 0; j < 3; j++) { int x = ev[i][j]; if (x == u || x == v || seen[x]) continue; seen[x] = 1;
    if (mv[x] < 0 || aug(mv[x], u, v)) { mv[x] = i; return 1; } }
  return 0;
}
static int p3ok(void) {
  for (int u = 0; u < N; u++) for (int v = u + 1; v < N; v++) {
    for (int x = 0; x < N; x++) mv[x] = -1;
    for (int i = 0; i < M; i++) { memset(seen, 0, sizeof seen); if (!aug(i, u, v)) return 0; } }
  return 1;
}
static int connected(void) {
  u32 r = 1, old = 0; while (r != old) { old = r; for (int i = 0; i < M; i++) if (E[i] & r) r |= E[i]; }
  return r == ((N == 32) ? 0xffffffffu : ((1u << N) - 1));
}
int main(int argc, char **argv) {
  N = atoi(argv[1]); M = atoi(argv[2]); T = atoi(argv[3]); D = atoi(argv[4]);
  char line[4096]; long tot = 0, bad = 0, wrongtau = 0, f7 = 0, p3 = 0, dis = 0, degbad = 0, surv = 0;
  while (fgets(line, sizeof line, stdin)) {
    if (line[0] == '>' ) continue;
    int nv = line[0] - 63; if (nv != N + M) { bad++; continue; }
    tot++;
    /* graph6 upper triangle, column-wise: bit for (i,j), i<j, in order j=1..n-1, i=0..j-1 */
    int deg[64] = {0}; int cnt[64] = {0}; for (int i = 0; i < M; i++) E[i] = 0;
    int pos = 0; char *p = line + 1; int ok = 1;
    for (int j = 1; j < nv; j++) for (int i = 0; i < j; i++) {
      int byte = pos / 6, bit = 5 - pos % 6; int val = (p[byte] - 63) >> bit & 1; pos++;
      if (val) { /* i < j */
        if (i < N && j >= N) { int e = j - N; if (cnt[e] >= 3) { ok = 0; continue; } ev[e][cnt[e]++] = i; E[e] |= 1u << i; deg[i]++; }
        else ok = 0; } }
    for (int e = 0; e < M; e++) if (cnt[e] != 3) ok = 0;
    if (!ok) { bad++; continue; }
    int md = 0; for (int i = 0; i < N; i++) if (deg[i] > md) md = deg[i];
    if (md > D) { degbad++; continue; }
    /* linear check (genbg -Z1 should guarantee) */
    for (int a = 0; a < M; a++) for (int b = a + 1; b < M; b++) if (__builtin_popcount(E[a] & E[b]) > 1) ok = 0;
    if (!ok) { bad++; continue; }
    if (tau() != T) { wrongtau++; continue; }
    if (hasF7()) { f7++; continue; }
    if (!p3ok()) { p3++; continue; }
    if (!connected()) { dis++; continue; }
    surv++; printf("FOUND:"); for (int e = 0; e < M; e++) printf(" (%d,%d,%d)", ev[e][0], ev[e][1], ev[e][2]); printf("\n");
  }
  printf("SUMMARY N=%d M=%d T=%d D=%d graphs=%ld bad=%ld degbad=%ld wrongtau=%ld F7=%ld P3fail=%ld disconnected=%ld survivors=%ld\n",
         N, M, T, D, tot, bad, degbad, wrongtau, f7, p3, dis, surv);
  return 0;
}
