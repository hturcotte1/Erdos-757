/* L003 round-3 referee: independent enumerator of saturated (4,5)-sets.
   usage: ./sat3 n T k30 lin [chunk] [force_exact] [printall]
   Enumerates ALL midpoint maps j -> (L[j], j, R[j]), 0 <= L[j] < j < R[j] <= n-1, j = 1..n-2,
   in outside-in order (1, n-2, 2, n-3, ...), optionally pruned by
     k30: monotone midpoints (j < j' forbids L[j] >= L[j'] && R[j] >= R[j']),
     lin: two APs share at most one point.
   Leaf: x_0 = 0, x_{n-1} = 1, 2x_j = x_L + x_R. Float LU gives a candidate integer vector X = D*x which is
   accepted only after the exact integer check 2X_j = X_L + X_R, X_0 = 0, X_{n-1} = D; otherwise exact
   fraction-free Bareiss (__int128). Then: strict order, primitive normalisation, AP set == map (exact count),
   weak Sidon, (4,5) on all 4-subsets, h = max Sidon subset (all pairwise differences distinct, DFS).
   Prints "S x_0 .. x_{n-1}" for every (4,5)-set with h == T in the orientation X <=lex reflection(X)
   (each affine class exactly once), "SYM" flag for reflection-symmetric ones, and a final STATS line.
   chunk c (optional) restricts R[1] = c + 2. Imports nothing; no float decision is unverified. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef long long ll;
typedef __int128 i128;

static int n, T, K30, LIN, CHUNK = -1, FORCE_EXACT = 0, PRINTALL = 0;
static int ord[16], L[16], R[16], asg[16];
static ll leaves, singular, fallback, orderfail, apextra, apextra_but45, notws, not45, ok45, hT, outcnt, symcnt, maxX;
static ll hist[20];

static int lin_ok(int j) {
  for (int t = 1; t <= n - 2; t++) if (asg[t]) {
    int a0 = L[j], a1 = j, a2 = R[j], b[3] = {L[t], t, R[t]}, c = 0;
    for (int v = 0; v < 3; v++) c += (a0 == b[v]) + (a1 == b[v]) + (a2 == b[v]);
    if (c >= 2) return 0;
  }
  return 1;
}
static int k30_ok(int j) {
  for (int t = 1; t <= n - 2; t++) if (asg[t]) {
    if (j < t) { if (L[j] >= L[t] && R[j] >= R[t]) return 0; }
    else       { if (L[t] >= L[j] && R[t] >= R[j]) return 0; }
  }
  return 1;
}
static ll gcdll(ll a, ll b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { ll t = a % b; a = b; b = t; } return a; }

static int check_eq(const ll *X, ll D) {
  if (X[0] != 0 || X[n - 1] != D) return 0;
  for (int j = 1; j <= n - 2; j++) if (2 * X[j] != X[L[j]] + X[R[j]]) return 0;
  return 1;
}
/* exact: returns 0 if singular, else fills X with D*x, D = |det| > 0 */
static int exact_solve(ll *X) {
  int N = n - 2; i128 a[14][15]; int perm_sign = 1;
  for (int r = 0; r < N; r++) { for (int c = 0; c <= N; c++) a[r][c] = 0; }
  for (int j = 1; j <= n - 2; j++) {
    int r = j - 1; a[r][r] = 2;
    if (L[j] >= 1) a[r][L[j] - 1] -= 1;
    if (R[j] <= n - 2) a[r][R[j] - 1] -= 1; else a[r][N] += 1;
  }
  i128 prev = 1;
  for (int k = 0; k < N; k++) {
    int p = -1; for (int r = k; r < N; r++) if (a[r][k] != 0) { p = r; break; }
    if (p < 0) return 0;
    if (p != k) { for (int c = 0; c <= N; c++) { i128 t = a[k][c]; a[k][c] = a[p][c]; a[p][c] = t; } perm_sign = -perm_sign; }
    for (int r = k + 1; r < N; r++) {
      for (int c = k + 1; c <= N; c++) a[r][c] = (a[k][k] * a[r][c] - a[r][k] * a[k][c]) / prev;
      a[r][k] = 0;
    }
    prev = a[k][k];
  }
  i128 det = a[N - 1][N - 1]; /* = perm_sign * det(M) */
  if (det == 0) return 0;
  i128 Xi[14];
  for (int i = N - 1; i >= 0; i--) {
    i128 s = det * a[i][N];
    for (int c = i + 1; c < N; c++) s -= a[i][c] * Xi[c];
    if (s % a[i][i] != 0) { fprintf(stderr, "non-exact division\n"); exit(2); }
    Xi[i] = s / a[i][i];
  }
  i128 D = det; if (D < 0) { D = -D; for (int i = 0; i < N; i++) Xi[i] = -Xi[i]; }
  X[0] = 0; X[n - 1] = (ll)D; for (int i = 0; i < N; i++) X[i + 1] = (ll)Xi[i];
  return 1;
}
static int float_solve(ll *X) {
  int N = n - 2; double a[14][15];
  for (int r = 0; r < N; r++) for (int c = 0; c <= N; c++) a[r][c] = 0;
  for (int j = 1; j <= n - 2; j++) {
    int r = j - 1; a[r][r] = 2;
    if (L[j] >= 1) a[r][L[j] - 1] -= 1;
    if (R[j] <= n - 2) a[r][R[j] - 1] -= 1; else a[r][N] += 1;
  }
  double det = 1;
  for (int k = 0; k < N; k++) {
    int p = k; double best = fabs(a[k][k]);
    for (int r = k + 1; r < N; r++) if (fabs(a[r][k]) > best) { best = fabs(a[r][k]); p = r; }
    if (best < 1e-9) return 0;
    if (p != k) { for (int c = 0; c <= N; c++) { double t = a[k][c]; a[k][c] = a[p][c]; a[p][c] = t; } det = -det; }
    det *= a[k][k];
    for (int r = k + 1; r < N; r++) { double f = a[r][k] / a[k][k]; if (f != 0) for (int c = k; c <= N; c++) a[r][c] -= f * a[k][c]; }
  }
  double x[14];
  for (int i = N - 1; i >= 0; i--) { double s = a[i][N]; for (int c = i + 1; c < N; c++) s -= a[i][c] * x[c]; x[i] = s / a[i][i]; }
  ll D = llround(fabs(det)); if (D <= 0) return 0;
  X[0] = 0; X[n - 1] = D; for (int i = 0; i < N; i++) X[i + 1] = llround((double)D * x[i]);
  return check_eq(X, D);
}

static ll SX[16]; static int usedd[1 << 12]; static int bestS;
static void sidon_dfs(int i, int cnt, int *chosen) {
  if (cnt + (n - i) <= bestS) return;
  if (i == n) { if (cnt > bestS) bestS = cnt; return; }
  /* include i */
  int ok = 1, k;
  for (k = 0; k < cnt; k++) if (usedd[SX[i] - SX[chosen[k]]]) { ok = 0; break; }
  if (ok) {
    for (k = 0; k < cnt; k++) usedd[SX[i] - SX[chosen[k]]] = 1;
    /* distinctness among the new differences themselves holds since SX strictly increasing */
    chosen[cnt] = i; sidon_dfs(i + 1, cnt + 1, chosen);
    for (k = 0; k < cnt; k++) usedd[SX[i] - SX[chosen[k]]] = 0;
  }
  sidon_dfs(i + 1, cnt, chosen);
}
static int is45(const ll *X) {
  for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) for (int d = c + 1; d < n; d++) {
    ll v[6] = {X[b] - X[a], X[c] - X[a], X[d] - X[a], X[c] - X[b], X[d] - X[b], X[d] - X[c]};
    int distinct = 0;
    for (int i = 0; i < 6; i++) { int dup = 0; for (int k = 0; k < i; k++) if (v[k] == v[i]) { dup = 1; break; } if (!dup) distinct++; }
    if (distinct < 5) return 0;
  }
  return 1;
}
static void leaf(void) {
  ll X[16];
  leaves++;
  if (FORCE_EXACT || !float_solve(X)) {
    if (!exact_solve(X)) { singular++; return; }
    if (!FORCE_EXACT) fallback++;
    if (!check_eq(X, X[n - 1])) { fprintf(stderr, "exact solve failed check\n"); exit(3); }
  }
  for (int i = 0; i + 1 < n; i++) if (X[i] >= X[i + 1]) { orderfail++; return; }
  ll g = 0; for (int i = 0; i < n; i++) g = gcdll(g, X[i]);
  for (int i = 0; i < n; i++) X[i] /= g;
  if (X[n - 1] > maxX) maxX = X[n - 1];
  if (X[n - 1] >= (1 << 11)) { fprintf(stderr, "coordinate too large %lld\n", X[n - 1]); exit(4); }
  /* AP count */
  static int pos[1 << 12]; for (ll v = 0; v <= X[n - 1]; v++) pos[v] = -1; for (int i = 0; i < n; i++) pos[X[i]] = i;
  int aps = 0;
  for (int i = 0; i < n; i++) for (int k = i + 1; k < n; k++) { ll s = X[i] + X[k]; if (!(s & 1) && pos[s / 2] >= 0) aps++; }
  int f45 = is45(X);
  if (PRINTALL) { printf("%s", aps != n - 2 ? "E" : (f45 ? "A" : "N")); for (int i = 0; i < n; i++) printf(" %lld", X[i]); }
  if (aps != n - 2) { if (PRINTALL) printf("\n"); apextra++; if (f45) apextra_but45++; return; }
  /* weak Sidon */
  static int sums[1 << 13]; for (ll v = 0; v <= 2 * X[n - 1]; v++) sums[v] = 0;
  int ws = 1; for (int i = 0; i < n && ws; i++) for (int k = i + 1; k < n; k++) { ll s = X[i] + X[k]; if (sums[s]) { ws = 0; break; } sums[s] = 1; }
  if (!f45) { if (PRINTALL) printf("\n"); not45++; if (!ws) notws++; return; }
  if (!ws) { fprintf(stderr, "(4,5) but not weak Sidon?!\n"); exit(5); }
  ok45++;
  for (int i = 0; i < n; i++) SX[i] = X[i];
  for (ll v = 0; v <= X[n - 1]; v++) usedd[v] = 0;
  int chosen[16]; bestS = 0; sidon_dfs(0, 0, chosen);
  hist[bestS]++;
  if (PRINTALL) printf(" h=%d\n", bestS);
  if (bestS != T) return;
  hT++;
  ll Rf[16]; for (int i = 0; i < n; i++) Rf[i] = X[n - 1] - X[n - 1 - i];
  int cmp = 0; for (int i = 0; i < n; i++) if (X[i] != Rf[i]) { cmp = X[i] < Rf[i] ? -1 : 1; break; }
  if (cmp > 0) return;
  outcnt++; if (cmp == 0) symcnt++;
  printf("S"); for (int i = 0; i < n; i++) printf(" %lld", X[i]); printf(cmp == 0 ? " SYM\n" : "\n");
}
static void dfs(int p) {
  if (p == n - 2) { leaf(); return; }
  int j = ord[p];
  for (int l = 0; l < j; l++) for (int r = j + 1; r <= n - 1; r++) {
    if (p == 0 && CHUNK >= 0 && r != CHUNK + 2) continue;
    L[j] = l; R[j] = r;
    if (K30 && !k30_ok(j)) continue;
    if (LIN && !lin_ok(j)) continue;
    asg[j] = 1; dfs(p + 1); asg[j] = 0;
  }
}
int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage: sat3 n T k30 lin [chunk]\n"); return 1; }
  n = atoi(argv[1]); T = atoi(argv[2]); K30 = atoi(argv[3]); LIN = atoi(argv[4]); if (argc > 5) CHUNK = atoi(argv[5]); if (argc > 6) FORCE_EXACT = atoi(argv[6]); if (argc > 7) PRINTALL = atoi(argv[7]);
  if (n < 4 || n > 12) return 1;
  int lo = 1, hi = n - 2, p = 0;
  while (lo <= hi) { ord[p++] = lo++; if (lo <= hi) ord[p++] = hi--; }
  dfs(0);
  printf("STATS n=%d T=%d k30=%d lin=%d chunk=%d leaves=%lld singular=%lld fallback=%lld orderfail=%lld apextra=%lld apextra_but45=%lld not45=%lld notws=%lld ok45=%lld hT=%lld out=%lld sym=%lld maxX=%lld hist",
         n, T, K30, LIN, CHUNK, leaves, singular, fallback, orderfail, apextra, apextra_but45, not45, notws, ok45, hT, outcnt, symcnt, maxX);
  for (int h = 0; h < 20; h++) if (hist[h]) printf(" %d:%lld", h, hist[h]);
  printf("\n");
  return 0;
}
