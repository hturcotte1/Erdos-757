/* Referee L007 r2: own brute force.  All labelled linear 3-graphs on [n] (each edge set once: edges added in
   increasing triple index).  For every one that is connected and spans [n], tally (m, tau, maxdeg, hasF7).
   tau: smallest k such that some k-subset of [n] meets every edge (exhaustive over all 2^n subsets).
   hasF7: centre-based search (a vertex p of degree>=3, three edges at p, T1/T2 complementary transversal
   choices both present) -- validated against the definitional Python detector in f7_ref.py.
   Output lines: m tau maxdeg hasF7 count */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, NT; static int TA[300], TB[300], TC[300]; static uint32_t TM[300];
static int idx3[16][16][16];
static int ed[64]; static int ne = 0; static uint32_t pairused[16];
static unsigned long long tally[40][16][16][2];
static int popcnt(uint32_t x){ return __builtin_popcount(x); }
static int edge_present[300];
static int has_f7(void){
  for (int p = 0; p < n; p++) {
    int at[16], k = 0;
    for (int i = 0; i < ne; i++) if (TM[ed[i]] >> p & 1) at[k++] = ed[i];
    if (k < 3) continue;
    for (int a = 0; a < k; a++) for (int b = a+1; b < k; b++) for (int c = b+1; c < k; c++) {
      int r[3][2]; int E3[3] = {at[a], at[b], at[c]};
      for (int t = 0; t < 3; t++) { int q = 0; int x[3] = {TA[E3[t]], TB[E3[t]], TC[E3[t]]};
        for (int s = 0; s < 3; s++) if (x[s] != p) r[t][q++] = x[s]; }
      for (int c2 = 0; c2 < 2; c2++) for (int c3 = 0; c3 < 2; c3++) {
        int u[3] = {r[0][0], r[1][c2], r[2][c3]}, w[3] = {r[0][1], r[1][1-c2], r[2][1-c3]};
        /* sort */
        for (int i = 0; i < 3; i++) for (int j = i+1; j < 3; j++) { if (u[j] < u[i]) { int z=u[i];u[i]=u[j];u[j]=z; } if (w[j] < w[i]) { int z=w[i];w[i]=w[j];w[j]=z; } }
        if (u[0]==u[1]||u[1]==u[2]||w[0]==w[1]||w[1]==w[2]) continue;
        if (edge_present[idx3[u[0]][u[1]][u[2]]] && edge_present[idx3[w[0]][w[1]][w[2]]]) return 1;
      }
    }
  }
  return 0;
}
static void leaf(void){
  uint32_t used = 0; for (int i = 0; i < ne; i++) used |= TM[ed[i]];
  if (used != (1u<<n)-1) return;
  uint32_t comp = TM[ed[0]], prev = 0;
  while (comp != prev) { prev = comp; for (int i = 0; i < ne; i++) if (TM[ed[i]] & comp) comp |= TM[ed[i]]; }
  if (comp != used) return;
  int tau = n;
  for (uint32_t S = 0; S < (1u<<n); S++) { int p = popcnt(S); if (p >= tau) continue; int ok = 1;
    for (int i = 0; i < ne; i++) if (!(TM[ed[i]] & S)) { ok = 0; break; } if (ok) tau = p; }
  int md = 0; for (int x = 0; x < n; x++) { int d = 0; for (int i = 0; i < ne; i++) if (TM[ed[i]] >> x & 1) d++; if (d > md) md = d; }
  tally[ne][tau][md][has_f7()]++;
}
static void rec(int start){
  if (ne >= 1) leaf();
  for (int i = start; i < NT; i++) {
    int a = TA[i], b = TB[i], c = TC[i];
    if ((pairused[a] >> b & 1) || (pairused[a] >> c & 1) || (pairused[b] >> c & 1)) continue;
    pairused[a] |= (1u<<b)|(1u<<c); pairused[b] |= (1u<<a)|(1u<<c); pairused[c] |= (1u<<a)|(1u<<b);
    ed[ne++] = i; edge_present[i] = 1;
    rec(i + 1);
    ne--; edge_present[i] = 0;
    pairused[a] &= ~((1u<<b)|(1u<<c)); pairused[b] &= ~((1u<<a)|(1u<<c)); pairused[c] &= ~((1u<<a)|(1u<<b));
  }
}
int main(int argc, char **argv){
  n = atoi(argv[1]); NT = 0;
  for (int a = 0; a < n; a++) for (int b = a+1; b < n; b++) for (int c = b+1; c < n; c++) {
    TA[NT]=a; TB[NT]=b; TC[NT]=c; TM[NT]=(1u<<a)|(1u<<b)|(1u<<c); idx3[a][b][c]=NT; NT++; }
  rec(0);
  for (int m = 0; m < 40; m++) for (int t = 0; t < 16; t++) for (int d = 0; d < 16; d++) for (int f = 0; f < 2; f++)
    if (tally[m][t][d][f]) printf("%d %d %d %d %llu\n", m, t, d, f, tally[m][t][d][f]);
  return 0;
}
