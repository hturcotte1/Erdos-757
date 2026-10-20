/* Referee L011 round 3: shared exact tests for 3-graphs given as edge bitmasks over <= 32 points (<= 64 edges). */
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
typedef struct { int ne, np; uint32_t E[64]; uint64_t INC[32]; } HG;
static void hg_build(HG *h, int np) { h->np = np; for (int x = 0; x < 32; x++) h->INC[x] = 0;
    for (int i = 0; i < h->ne; i++) { uint32_t e = h->E[i]; while (e) { int x = __builtin_ctz(e); e &= e - 1; h->INC[x] |= 1ull << i; } } }
static int hg_linear(const HG *h) { for (int i = 0; i < h->ne; i++) for (int j = i + 1; j < h->ne; j++) if (__builtin_popcount(h->E[i] & h->E[j]) >= 2) return 0; return 1; }
static int hg_isedge(const HG *h, uint32_t m) { for (int i = 0; i < h->ne; i++) if (h->E[i] == m) return 1; return 0; }
/* transversal test: can the edges in 'left' be met by <= k points?  branch on the last uncovered edge; greedy matching bound */
static int hg_cov(const HG *h, uint64_t left, int k) {
    if (!left) return 1;
    if (k <= 0) return 0;
    { uint64_t l = left; uint32_t used = 0; int c = 0;
      while (l) { int i = 63 - __builtin_clzll(l); l &= ~(1ull << i); if (!(h->E[i] & used)) { used |= h->E[i]; if (++c > k) return 0; } } }
    int i = 63 - __builtin_clzll(left); uint32_t e = h->E[i];
    while (e) { int x = 31 - __builtin_clz(e); e &= ~(1u << x); if (hg_cov(h, left & ~h->INC[x], k - 1)) return 1; }
    return 0;
}
static uint64_t hg_all(const HG *h) { return h->ne >= 64 ? ~0ull : ((1ull << h->ne) - 1); }
static int hg_tau(const HG *h) { int k = 0; while (!hg_cov(h, hg_all(h), k)) k++; return k; }
/* generic sub-hypergraph embedding of F7 = {012,034,056,135,246}: assign F7 vertices 0..6 in order to distinct points,
   checking every F7 edge as soon as all its vertices are assigned.  Uses no structural lemma. */
static const int F7E[5][3] = { {0,1,2}, {0,3,4}, {0,5,6}, {1,3,5}, {2,4,6} };
static int f7_rec(const HG *h, int v, int *img, uint32_t usedpts) {
    if (v == 7) return 1;
    for (int x = 0; x < h->np; x++) {
        if (usedpts >> x & 1) continue;
        img[v] = x; int ok = 1;
        for (int e = 0; e < 5 && ok; e++) {
            int mx = F7E[e][0] > F7E[e][1] ? F7E[e][0] : F7E[e][1]; if (F7E[e][2] > mx) mx = F7E[e][2];
            if (mx != v) continue;   /* edge becomes fully assigned exactly when its max vertex is assigned */
            uint32_t m = (1u << img[F7E[e][0]]) | (1u << img[F7E[e][1]]) | (1u << img[F7E[e][2]]);
            if (!hg_isedge(h, m)) ok = 0;
        }
        if (ok && f7_rec(h, v + 1, img, usedpts | (1u << x))) return 1;
    }
    return 0;
}
static int hg_has_f7(const HG *h) { int img[7]; return f7_rec(h, 0, img, 0); }
/* Lemma-F style test (only meaningful for linear graphs): five edges whose union has 7 points with degrees 3,2,2,2,2,2,2 */
static int hg_has_f7_lemmaF(const HG *h) {
    int n = h->ne, a[5];
    for (a[0] = 0; a[0] < n; a[0]++) for (a[1] = a[0] + 1; a[1] < n; a[1]++) for (a[2] = a[1] + 1; a[2] < n; a[2]++)
    for (a[3] = a[2] + 1; a[3] < n; a[3]++) for (a[4] = a[3] + 1; a[4] < n; a[4]++) {
        uint32_t U = 0; for (int k = 0; k < 5; k++) U |= h->E[a[k]];
        if (__builtin_popcount(U) != 7) continue;
        int d3 = 0, d2 = 0, other = 0;
        for (uint32_t u = U; u; u &= u - 1) { int x = __builtin_ctz(u), d = 0; for (int k = 0; k < 5; k++) if (h->E[a[k]] >> x & 1) d++; if (d == 3) d3++; else if (d == 2) d2++; else other++; }
        if (d3 == 1 && d2 == 6 && !other) return 1;
    }
    return 0;
}
/* (P3): e(S) <= |S|-2 for all |S| >= 2  <=>  |U(F)| - |F| >= 2 for every nonempty edge set F.  Returns min over F. */
static int hg_p3_worst(const HG *h) {
    static uint32_t U[1 << 22]; if (h->ne > 22) { fprintf(stderr, "p3: too many edges\n"); exit(9); }
    int w = 1000; U[0] = 0;
    for (uint32_t F = 1; F < (1u << h->ne); F++) { U[F] = U[F & (F - 1)] | h->E[__builtin_ctz(F)];
        int d = __builtin_popcount(U[F]) - __builtin_popcount(F); if (d < w) w = d; }
    return w;
}
/* connectivity over ALL np points (a point in no edge is its own component); returns number of components, sizes sorted */
static int hg_components(const HG *h, int *sizes) {
    int par[32]; for (int x = 0; x < h->np; x++) par[x] = x;
    #define FIND(x) ({ int _r = (x); while (par[_r] != _r) _r = par[_r]; _r; })
    for (int i = 0; i < h->ne; i++) { uint32_t e = h->E[i]; int r0 = FIND(__builtin_ctz(e)); for (uint32_t f = e; f; f &= f - 1) { int r = FIND(__builtin_ctz(f)); par[r] = r0; } }
    int cnt[32] = {0}; for (int x = 0; x < h->np; x++) cnt[FIND(x)]++;
    int k = 0; for (int x = 0; x < h->np; x++) if (cnt[x]) sizes[k++] = cnt[x];
    for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++) if (sizes[j] < sizes[i]) { int t = sizes[i]; sizes[i] = sizes[j]; sizes[j] = t; }
    return k;
}
static int hg_maxdeg(const HG *h) { int md = 0; for (int x = 0; x < h->np; x++) { int d = __builtin_popcountll(h->INC[x]); if (d > md) md = d; } return md; }
/* parse one line: numeric "m a b c ..." or "TAG: (a,b,c) (d,e,f) ..." ; returns number of edges or -1 */
static int hg_parse(const char *line, HG *h, int np) {
    const char *p = line; while (*p == ' ') p++;
    int m = 0;
    if (*p >= '0' && *p <= '9') { char *q; int k = (int)strtol(p, &q, 10); p = q;
        for (int i = 0; i < k; i++) { int a = (int)strtol(p, &q, 10); p = q; int b = (int)strtol(p, &q, 10); p = q; int c = (int)strtol(p, &q, 10); p = q;
            if (a >= np || b >= np || c >= np || a < 0 || b < 0 || c < 0) return -2; h->E[m++] = (1u << a) | (1u << b) | (1u << c); } }
    else { const char *c = strchr(line, ':'); if (!c) return -1; p = c + 1;
        while ((p = strchr(p, '('))) { int a, b, cc; if (sscanf(p, "(%d,%d,%d)", &a, &b, &cc) != 3) return -1;
            if (a >= np || b >= np || cc >= np || a < 0 || b < 0 || cc < 0) return -2; h->E[m++] = (1u << a) | (1u << b) | (1u << cc); p++; } }
    h->ne = m; hg_build(h, np); return m;
}
static void hg_print(FILE *f, const HG *h) { for (int i = 0; i < h->ne; i++) { uint32_t e = h->E[i]; int v[3], k = 0; while (e) { v[k++] = __builtin_ctz(e); e &= e - 1; } fprintf(f, " (%d,%d,%d)", v[0], v[1], v[2]); } }
