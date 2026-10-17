/* Referee L013 round 2: independent filter + extension program (written from scratch).
   Hypergraphs: n <= 32 vertices (bitmask uint32), m <= 48 edges.
   Checks: linear (pairwise |e cap f| <= 1, edges distinct, 3 distinct vertices), F7 by a generic injective embedding search of
   F7 = {012,034,056,135,246} (edge-by-edge backtracking over H's edges), (P3) via Hall with surplus 2 (for each edge e0: the
   bipartite graph edges->vertices with e0 tripled has an edge-saturating matching; Kuhn's algorithm), connectivity on all n vertices,
   max degree, tau exactly (DFS over the first uncovered edge with a disjoint-edges lower bound).
   Modes:
     filter n m t D           : read graph6 bipartite graphs from genbg (first n vertices = points, next m = edges);
                                print 'SURV: (a,b,c) ...' for connected members of C with tau == t and maxdeg <= D; summary.
     ext NG TG T d EP [hits]  : read inputs 'k a b c a b c ...' on NG vertices; check tau(G) == TG; enumerate all d-sets of pairwise
                                disjoint pairs {a,b} (not inside an edge of G, deg_G <= EP) such that tau(G + w) >= T, where w = NG;
                                method: every maximum independent set of G (complement of a minimum cover) must CONTAIN one of the
                                pairs (if TG == T-1), lexicographic enumeration p1<p2<..., last pair inside the intersection of the
                                still-uncontained MIS's; if TG >= T every d-set is a hit.  Every hit is re-checked: tau(H) >= T
                                computed directly.  Counts hits, F7-free, in C, connected, connected-in-C-with-tau==T-and-maxdeg<=d.
     brute NG TG T d EP       : same counts by brute force over ALL d-sets of disjoint admissible pairs with tau(H) computed directly.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t u32;
#define MAXV 32
#define MAXE 48
typedef struct { int n, m; int e[MAXE][3]; u32 em[MAXE]; } HG;
static int popc(u32 x){ return __builtin_popcount(x); }
/* ---------- tau ---------- */
static long long tau_nodes = 0;
static int cover_k(const u32 *em, int m, u32 chosen, int k) {
  tau_nodes++;
  int i; for (i = 0; i < m; i++) if (!(em[i] & chosen)) break;
  if (i == m) return 1;
  if (k == 0) return 0;
  u32 used = 0; int lb = 0;
  for (int j = i; j < m; j++) if (!(em[j] & chosen) && !(em[j] & used)) { used |= em[j]; if (++lb > k) return 0; }
  u32 e = em[i];
  while (e) { int v = __builtin_ctz(e); e &= e - 1; if (cover_k(em, m, chosen | (1u << v), k - 1)) return 1; }
  return 0;
}
static int tau_of(const HG *g) { for (int k = 0;; k++) if (cover_k(g->em, g->m, 0, k)) return k; }
/* all covers of size <= k (k = tau): collect masks */
static u32 *covs; static int ncov, capcov;
static void allcov(const u32 *em, int m, u32 chosen, int k) {
  int i; for (i = 0; i < m; i++) if (!(em[i] & chosen)) break;
  if (i == m) { if (ncov == capcov) { capcov = capcov ? 2 * capcov : 1024; covs = realloc(covs, capcov * sizeof(u32)); } covs[ncov++] = chosen; return; }
  if (k == 0) return;
  u32 e = em[i];
  while (e) { int v = __builtin_ctz(e); e &= e - 1; allcov(em, m, chosen | (1u << v), k - 1); }
}
static int cmpu(const void *a, const void *b) { u32 x = *(u32*)a, y = *(u32*)b; return x < y ? -1 : x > y; }
/* ---------- basic checks ---------- */
static int is_linear(const HG *g) {
  for (int i = 0; i < g->m; i++) { if (popc(g->em[i]) != 3) return 0;
    for (int j = i + 1; j < g->m; j++) if (popc(g->em[i] & g->em[j]) > 1) return 0; }
  return 1;
}
static int connected_all(const HG *g) {
  if (g->n == 0) return 1;
  u32 all = (g->n == 32) ? 0xffffffffu : ((1u << g->n) - 1), reach = 1u; int ch = 1;
  while (ch) { ch = 0; for (int i = 0; i < g->m; i++) if ((g->em[i] & reach) && (g->em[i] & ~reach)) { reach |= g->em[i]; ch = 1; } }
  return reach == all;
}
static int maxdeg(const HG *g) { int d[MAXV] = {0}, mx = 0; for (int i = 0; i < g->m; i++) for (int j = 0; j < 3; j++) d[g->e[i][j]]++;
  for (int v = 0; v < g->n; v++) if (d[v] > mx) mx = d[v]; return mx; }
/* F7 generic embedding: F7 edges in order 012,034,056,135,246 */
static const int F7[5][3] = {{0,1,2},{0,3,4},{0,5,6},{1,3,5},{2,4,6}};
static int phi[7]; static u32 usedv;
static int edge_index_of(const HG *g, u32 mask) { for (int i = 0; i < g->m; i++) if (g->em[i] == mask) return i; return -1; }
static int f7_rec(const HG *g, int k) {
  if (k == 5) return 1;
  /* map F7 edge k onto some edge of H, consistent with phi */
  for (int i = 0; i < g->m; i++) {
    int *E = (int*)g->e[i];
    /* try all 6 orderings */
    static const int perm[6][3] = {{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
    for (int p = 0; p < 6; p++) {
      int ok = 1, setv[3], ns = 0;
      for (int j = 0; j < 3 && ok; j++) {
        int fv = F7[k][j], hv = E[perm[p][j]];
        if (phi[fv] >= 0) { if (phi[fv] != hv) ok = 0; }
        else if (usedv & (1u << hv)) ok = 0;
        else { phi[fv] = hv; usedv |= 1u << hv; setv[ns++] = fv; }
      }
      if (ok && f7_rec(g, k + 1)) return 1;
      for (int j = 0; j < ns; j++) { usedv &= ~(1u << phi[setv[j]]); phi[setv[j]] = -1; }
    }
  }
  return 0;
}
static int has_f7(const HG *g) { for (int i = 0; i < 7; i++) phi[i] = -1; usedv = 0; return f7_rec(g, 0); }
/* (P3) via Hall surplus 2 */
static int matchv[MAXV]; static int visv[MAXV]; static int slots_edge[MAXE + 4]; static int nslots;
static int kuhn(const HG *g, int s) {
  int ei = slots_edge[s];
  for (int j = 0; j < 3; j++) { int v = g->e[ei][j]; if (visv[v]) continue; visv[v] = 1;
    if (matchv[v] < 0 || kuhn(g, matchv[v])) { matchv[v] = s; return 1; } }
  return 0;
}
static int p3_ok(const HG *g) {
  if (g->m == 0) return 1;
  if (g->m > g->n - 2) return 0;
  for (int e0 = 0; e0 < g->m; e0++) {
    nslots = 0; for (int i = 0; i < g->m; i++) { slots_edge[nslots++] = i; if (i == e0) { slots_edge[nslots++] = i; slots_edge[nslots++] = i; } }
    for (int v = 0; v < g->n; v++) matchv[v] = -1;
    for (int s = 0; s < nslots; s++) { memset(visv, 0, sizeof visv); if (!kuhn(g, s)) return 0; }
  }
  return 1;
}
/* brute (P3) over all edge subsets, for cross-checks (m <= 24) */
static int p3_brute(const HG *g) {
  int m = g->m; if (m > 24) { fprintf(stderr, "p3_brute m too big\n"); exit(2); }
  for (u32 F = 1; F < (1u << m); F++) { u32 V = 0; for (int i = 0; i < m; i++) if (F >> i & 1) V |= g->em[i];
    if (popc(V) < popc(F) + 2) return 0; }
  return 1;
}
static void finish(HG *g) { for (int i = 0; i < g->m; i++) g->em[i] = (1u << g->e[i][0]) | (1u << g->e[i][1]) | (1u << g->e[i][2]); }
static void print_edges(const char *tag, const HG *g) {
  printf("%s:", tag); for (int i = 0; i < g->m; i++) printf(" (%d,%d,%d)", g->e[i][0], g->e[i][1], g->e[i][2]); printf("\n");
}
/* ---------- graph6 ---------- */
static int parse_g6(const char *s, int *N, unsigned char adj[64][64]) {
  const unsigned char *p = (const unsigned char*)s; int n;
  if (*p == '>') return -1;
  if (p[0] < 126) { n = p[0] - 63; p++; } else { n = ((p[1] - 63) << 12) | ((p[2] - 63) << 6) | (p[3] - 63); p += 4; }
  if (n > 64) return -1;
  *N = n; memset(adj, 0, 64 * 64); int k = 0, bit = 0; int cur = 0;
  for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) {
    if (bit == 0) { cur = *p++ - 63; bit = 6; }
    bit--; if ((cur >> bit) & 1) { adj[i][j] = adj[j][i] = 1; }
    k++;
  }
  return 0;
}
static char line[1 << 16];
int main(int argc, char **argv) {
  if (argc < 2) { fprintf(stderr, "usage\n"); return 1; }
  if (!strcmp(argv[1], "filter")) {
    int n = atoi(argv[2]), m = atoi(argv[3]), t = atoi(argv[4]), D = atoi(argv[5]);
    long long tot = 0, lin = 0, f7 = 0, p3bad = 0, conn = 0, degok = 0, tauok = 0, surv = 0, bad = 0; int tmin = 99, tmax = -1;
    static unsigned char adj[64][64];
    while (fgets(line, sizeof line, stdin)) {
      if (line[0] == '\n' || line[0] == '>') continue;
      line[strcspn(line, "\r\n")] = 0; int N;
      if (parse_g6(line, &N, adj) || N != n + m) { bad++; continue; }
      tot++; HG g; g.n = n; g.m = m; int okk = 1;
      for (int i = 0; i < m && okk; i++) { int c = 0; for (int v = 0; v < n; v++) if (adj[v][n + i]) { if (c < 3) g.e[i][c] = v; c++; } if (c != 3) okk = 0; }
      for (int a = 0; a < n && okk; a++) for (int b = 0; b < n; b++) if (adj[a][b]) okk = 0;
      for (int a = 0; a < m && okk; a++) for (int b = 0; b < m; b++) if (adj[n + a][n + b]) okk = 0;
      if (!okk) { bad++; continue; }
      finish(&g);
      if (!is_linear(&g)) continue; lin++;
      if (!connected_all(&g)) continue; conn++;
      if (maxdeg(&g) > D) continue; degok++;
      if (has_f7(&g)) { f7++; continue; }
      if (!p3_ok(&g)) { p3bad++; continue; }
      int tt = tau_of(&g); if (tt < tmin) tmin = tt; if (tt > tmax) tmax = tt;
      if (tt != t) continue; tauok++;
      surv++; print_edges("SURV", &g);
    }
    printf("SUMMARY filter n=%d m=%d t=%d D=%d total=%lld bad=%lld linear=%lld connected=%lld degok=%lld f7=%lld p3bad=%lld inC_tau_range=[%d,%d] survivors=%lld\n",
           n, m, t, D, tot, bad, lin, conn, degok, f7, p3bad, tmin, tmax, surv);
    return 0;
  }
  if (!strcmp(argv[1], "check")) { /* read 'TAG: (a,b,c) ...' lines with n given; print properties */
    int n = atoi(argv[2]); int brute = argc > 3 && !strcmp(argv[3], "brute");
    while (fgets(line, sizeof line, stdin)) {
      HG g; g.n = n; g.m = 0; char *p = strchr(line, ':'); if (!p) continue; p++;
      int a, b, c, k;
      while (sscanf(p, " (%d,%d,%d)%n", &a, &b, &c, &k) == 3) { g.e[g.m][0] = a; g.e[g.m][1] = b; g.e[g.m][2] = c; g.m++; p += k; }
      finish(&g);
      int lin = is_linear(&g), con = connected_all(&g), f7 = has_f7(&g), p3 = p3_ok(&g), tt = tau_of(&g), md = maxdeg(&g);
      int p3b = brute ? p3_brute(&g) : -1;
      printf("CHECK m=%d linear=%d connected=%d F7=%d P3=%d P3brute=%d tau=%d maxdeg=%d\n", g.m, lin, con, f7, p3, p3b, tt, md);
    }
    return 0;
  }
  int isext = !strcmp(argv[1], "ext"), isbrute = !strcmp(argv[1], "brute");
  if (isext || isbrute) {
    int NG = atoi(argv[2]), TG = atoi(argv[3]), T = atoi(argv[4]), d = atoi(argv[5]), EP = atoi(argv[6]);
    int printhits = argc > 7 && !strcmp(argv[7], "hits");
    long long ninp = 0, badtau = 0, hits = 0, f7free = 0, inC = 0, conn = 0, good = 0, connf7 = 0, connp3 = 0, taufail = 0, nlin = 0;
    long long totcov = 0; int maxcov = 0;
    int w = NG;
    while (fgets(line, sizeof line, stdin)) {
      char *p = line; int k, off; if (sscanf(p, "%d%n", &k, &off) != 1) continue; p += off;
      HG G; G.n = NG; G.m = k;
      for (int i = 0; i < k; i++) { for (int j = 0; j < 3; j++) { sscanf(p, "%d%n", &G.e[i][j], &off); p += off; } }
      finish(&G); ninp++;
      int tg = tau_of(&G); if (tg != TG) { badtau++; continue; }
      int deg[MAXV] = {0}; for (int i = 0; i < k; i++) for (int j = 0; j < 3; j++) deg[G.e[i][j]]++;
      /* admissible pairs */
      u32 P[600]; int np = 0;
      for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
        if (deg[a] > EP || deg[b] > EP) continue;
        u32 pm = (1u << a) | (1u << b); int inside = 0;
        for (int i = 0; i < k; i++) if ((G.em[i] & pm) == pm) { inside = 1; break; }
        if (!inside) P[np++] = pm;
      }
      /* MIS list */
      u32 all = (1u << NG) - 1;
      ncov = 0;
      int constrained = (TG < T);
      if (constrained) {
        if (TG != T - 1) { fprintf(stderr, "TG < T-1 not supported\n"); return 2; }
        allcov(G.em, k, 0, TG); qsort(covs, ncov, sizeof(u32), cmpu);
        int q = 0; for (int i = 0; i < ncov; i++) if (i == 0 || covs[i] != covs[i - 1]) covs[q++] = covs[i]; ncov = q;
        for (int i = 0; i < ncov; i++) { if (popc(covs[i]) != TG) { fprintf(stderr, "cover size error\n"); return 2; } covs[i] = all & ~covs[i]; }
        totcov += ncov; if (ncov > maxcov) maxcov = ncov;
      }
      /* enumerate d-sets */
      int idx[8]; 
      /* generic iterative recursion with explicit stacks of uncovered MIS lists */
      static u32 *U[8]; static int Ucap[8]; int Un[8];
      for (int l = 0; l <= d; l++) { if (Ucap[l] < ncov + 1) { Ucap[l] = ncov + 1; U[l] = realloc(U[l], Ucap[l] * sizeof(u32)); } }
      if (constrained) { memcpy(U[0], covs, ncov * sizeof(u32)); Un[0] = ncov; } else Un[0] = 0;
      #define EMIT(...) do { \
        HG H = G; H.n = NG + 1; for (int z = 0; z < d; z++) { u32 pm = P[idx[z]]; int a = __builtin_ctz(pm); int b = 31 - __builtin_clz(pm); \
          H.e[H.m][0] = w; H.e[H.m][1] = a; H.e[H.m][2] = b; H.m++; } finish(&H); \
        hits++; int th = tau_of(&H); if (th < T) taufail++; \
        if (is_linear(&H)) nlin++; \
        int ff = !has_f7(&H), pp = ff ? p3_ok(&H) : 0, cc = connected_all(&H); \
        if (ff) f7free++; if (ff && pp) inC++; if (cc) { conn++; if (!ff) connf7++; else if (!pp) connp3++; } \
        if (ff && pp && cc && th == T && maxdeg(&H) <= d) { good++; print_edges("GOOD", &H); } \
        if (printhits) print_edges("HIT", &H); } while (0)
      if (isbrute) {
        /* all d-sets of pairwise disjoint pairs, tau(H) directly */
        int l = 0; idx[0] = -1; u32 usedm[9]; usedm[0] = 0;
        while (l >= 0) {
          idx[l]++;
          if (idx[l] >= np) { l--; continue; }
          if (P[idx[l]] & usedm[l]) continue;
          usedm[l + 1] = usedm[l] | P[idx[l]];
          if (l == d - 1) {
            HG H = G; H.n = NG + 1; for (int z = 0; z < d; z++) { u32 pm = P[idx[z]]; int a = __builtin_ctz(pm); int b = 31 - __builtin_clz(pm);
              H.e[H.m][0] = w; H.e[H.m][1] = a; H.e[H.m][2] = b; H.m++; } finish(&H);
            if (cover_k(H.em, H.m, 0, T - 1)) continue; /* tau(H) <= T-1: not a hit */
            hits++; nlin += is_linear(&H);
            int ff = !has_f7(&H), pp = ff ? p3_ok(&H) : 0, cc = connected_all(&H); int th = tau_of(&H);
            if (ff) f7free++; if (ff && pp) inC++; if (cc) { conn++; if (!ff) connf7++; else if (!pp) connp3++; }
            if (ff && pp && cc && th == T && maxdeg(&H) <= d) { good++; print_edges("GOOD", &H); }
            if (printhits) print_edges("HIT", &H);
          } else { l++; idx[l] = idx[l - 1]; }
        }
        continue;
      }
      /* fast method */
      {
        int l = 0; idx[0] = -1; u32 usedm[9]; usedm[0] = 0;
        while (l >= 0) {
          idx[l]++;
          if (idx[l] >= np) { l--; continue; }
          u32 pm = P[idx[l]];
          if (pm & usedm[l]) continue;
          if (l == d - 1) {
            /* last pair: must be contained in every MIS of U[l] */
            int ok = 1; for (int i = 0; i < Un[l]; i++) if ((U[l][i] & pm) != pm) { ok = 0; break; }
            if (ok) { EMIT(); }
            continue;
          }
          usedm[l + 1] = usedm[l] | pm;
          /* filter MIS's not containing pm */
          int q = 0; for (int i = 0; i < Un[l]; i++) if ((U[l][i] & pm) != pm) U[l + 1][q++] = U[l][i];
          Un[l + 1] = q;
          if (l + 1 == d - 1 && q > 0) {
            /* prune: intersection of remaining MIS's must contain >= 2 free vertices */
            u32 inter = all & ~usedm[l + 1];
            for (int i = 0; i < q && popc(inter) >= 2; i++) inter &= U[l + 1][i];
            if (popc(inter) < 2) continue;
          }
          l++; idx[l] = idx[l - 1];
        }
      }
    }
    printf("SUMMARY %s NG=%d TG=%d T=%d d=%d EP=%d inputs=%lld badtau=%lld maxcov=%d totcov=%lld hits=%lld taufail=%lld linear=%lld f7free=%lld inC=%lld connected=%lld conn_withF7=%lld conn_P3bad=%lld GOOD=%lld\n",
           argv[1], NG, TG, T, d, EP, ninp, badtau, maxcov, totcov, hits, taufail, nlin, f7free, inC, conn, connf7, connp3, good);
    return 0;
  }
  fprintf(stderr, "unknown mode\n"); return 1;
}
