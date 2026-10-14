/* L003 round 3: count saturated class-O patterns (K30 + linear midpoint maps, F7-free, alpha <= T)
   usage: ./patc3 n T   -> labelled, reflection-symmetric, up to reflection; also counts with F7 allowed */
#include <stdio.h>
#include <stdlib.h>
typedef long long ll;
static int n, T, ord[16], L[16], R[16], asg[16];
static int masksT1[5000], nmT1;
static ll lab, sym, labF7, symF7;
static int edge_exists(int a, int b, int c) {
  /* {a,b,c} is an edge iff its middle element m (by index) is a midpoint with endpoints the other two */
  int x = a, y = b, z = c, t;
  if (x > y) { t = x; x = y; y = t; } if (y > z) { t = y; y = z; z = t; } if (x > y) { t = x; x = y; y = t; }
  return y >= 1 && y <= n - 2 && L[y] == x && R[y] == z;
}
static int has_f7(void) {
  for (int v = 0; v < n; v++) {
    int e[16][2], d = 0;
    for (int j = 1; j <= n - 2; j++) {
      if (j == v) { e[d][0] = L[j]; e[d][1] = R[j]; d++; }
      else if (L[j] == v) { e[d][0] = j; e[d][1] = R[j]; d++; }
      else if (R[j] == v) { e[d][0] = L[j]; e[d][1] = j; d++; }
    }
    for (int p = 0; p < d; p++) for (int q = p + 1; q < d; q++) for (int r = q + 1; r < d; r++)
      for (int s2 = 0; s2 < 2; s2++) for (int s3 = 0; s3 < 2; s3++) {
        int x1 = e[p][0], y1 = e[p][1], x2 = e[q][s2], y2 = e[q][1 - s2], x3 = e[r][s3], y3 = e[r][1 - s3];
        if (edge_exists(x1, x2, x3) && edge_exists(y1, y2, y3)) return 1;
      }
  }
  return 0;
}
static void leaf(void) {
  int em[16];
  for (int j = 1; j <= n - 2; j++) em[j] = (1 << L[j]) | (1 << j) | (1 << R[j]);
  for (int t = 0; t < nmT1; t++) {           /* alpha <= T iff every (T+1)-set contains an edge */
    int S = masksT1[t], hit = 0;
    for (int j = 1; j <= n - 2; j++) if ((em[j] & S) == em[j]) { hit = 1; break; }
    if (!hit) return;
  }
  int sy = 1;
  for (int j = 1; j <= n - 2; j++) if (L[n - 1 - j] != n - 1 - R[j] || R[n - 1 - j] != n - 1 - L[j]) { sy = 0; break; }
  labF7++; symF7 += sy;
  if (has_f7()) return;
  lab++; sym += sy;
}
static void dfs(int p) {
  if (p == n - 2) { leaf(); return; }
  int j = ord[p];
  for (int l = 0; l < j; l++) for (int r = j + 1; r <= n - 1; r++) {
    L[j] = l; R[j] = r; int ok = 1;
    for (int t = 1; t <= n - 2 && ok; t++) if (asg[t]) {
      if (j < t) { if (L[j] >= L[t] && R[j] >= R[t]) ok = 0; } else { if (L[t] >= L[j] && R[t] >= R[j]) ok = 0; }
      int c = 0, b[3] = {L[t], t, R[t]};
      for (int v = 0; v < 3; v++) c += (l == b[v]) + (j == b[v]) + (r == b[v]);
      if (c >= 2) ok = 0;
    }
    if (!ok) continue;
    asg[j] = 1; dfs(p + 1); asg[j] = 0;
  }
}
int main(int argc, char **argv) {
  n = atoi(argv[1]); T = atoi(argv[2]);
  for (int S = 0; S < (1 << n); S++) if (__builtin_popcount(S) == T + 1) masksT1[nmT1++] = S;
  int lo = 1, hi = n - 2, p = 0; while (lo <= hi) { ord[p++] = lo++; if (lo <= hi) ord[p++] = hi--; }
  dfs(0);
  printf("PAT n=%d T=%d F7-free: labelled=%lld sym=%lld up_to_refl=%lld | F7 allowed: labelled=%lld sym=%lld\n", n, T, lab, sym, (lab + sym) / 2, labF7, symF7);
  return 0;
}
