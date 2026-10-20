/* Referee L013 round 3: own hypergraph library (3-uniform, <= 32 vertices, <= 40 edges). Written from the definitions.
   linear, connected (on all n vertices), max degree, F7 (centre + 3 edges + two complementary transversal edges),
   P3 (e(S) <= |S|-2 for all |S|>=2  <=>  for every pair {u,v} a matching saturating all edges into V\{u,v}),
   tau exact (branch on first uncovered edge, matching lower bound), all minimum covers. */
#ifndef HYP_H
#define HYP_H
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXV 32
#define MAXE 40
typedef struct { int n, m; int e[MAXE][3]; uint32_t em[MAXE]; } hyp;
static void hyp_finish(hyp *h) { for (int i = 0; i < h->m; i++) h->em[i] = (1u << h->e[i][0]) | (1u << h->e[i][1]) | (1u << h->e[i][2]); }
static int popc(uint32_t x) { return __builtin_popcount(x); }
static int hyp_valid(const hyp *h) { /* distinct vertices in each edge, labels in range, distinct edges */
    for (int i = 0; i < h->m; i++) { for (int k = 0; k < 3; k++) if (h->e[i][k] < 0 || h->e[i][k] >= h->n) return 0; if (popc(h->em[i]) != 3) return 0;
        for (int j = 0; j < i; j++) if (h->em[i] == h->em[j]) return 0; }
    return 1; }
static int hyp_linear(const hyp *h) { for (int i = 0; i < h->m; i++) for (int j = 0; j < i; j++) if (popc(h->em[i] & h->em[j]) >= 2) return 0; return 1; }
static int hyp_maxdeg(const hyp *h) { int d[MAXV] = {0}, mx = 0; for (int i = 0; i < h->m; i++) for (int k = 0; k < 3; k++) d[h->e[i][k]]++; for (int v = 0; v < h->n; v++) if (d[v] > mx) mx = d[v]; return mx; }
static void hyp_degs(const hyp *h, int *d) { for (int v = 0; v < h->n; v++) d[v] = 0; for (int i = 0; i < h->m; i++) for (int k = 0; k < 3; k++) d[h->e[i][k]]++; }
static int hyp_connected(const hyp *h) { /* all n vertices in one component (n==1: connected) */
    if (h->n <= 1) return 1; uint32_t reach = 1u; int changed = 1;
    while (changed) { changed = 0; for (int i = 0; i < h->m; i++) if ((h->em[i] & reach) && (h->em[i] & ~reach)) { reach |= h->em[i]; changed = 1; } }
    return reach == ((h->n == 32) ? 0xffffffffu : ((1u << h->n) - 1)); }
static int hyp_has_F7(const hyp *h) {
    for (int c = 0; c < h->n; c++) {
        int at[MAXE], na = 0; for (int i = 0; i < h->m; i++) if (h->em[i] & (1u << c)) at[na++] = i;
        if (na < 3) continue;
        for (int a = 0; a < na; a++) for (int b = a + 1; b < na; b++) for (int cc = b + 1; cc < na; cc++) {
            uint32_t P1 = h->em[at[a]] & ~(1u << c), P2 = h->em[at[b]] & ~(1u << c), P3 = h->em[at[cc]] & ~(1u << c);
            if ((P1 & P2) || (P1 & P3) || (P2 & P3)) continue; /* not linear at c; cannot be F7 anyway */
            uint32_t six = P1 | P2 | P3;
            for (int f = 0; f < h->m; f++) { uint32_t F = h->em[f]; if (F & (1u << c)) continue; if ((F & six) != F) continue;
                if (popc(F & P1) != 1 || popc(F & P2) != 1 || popc(F & P3) != 1) continue;
                uint32_t G = six & ~F; for (int g = 0; g < h->m; g++) if (h->em[g] == G) return 1; }
        }
    }
    return 0; }
/* bipartite matching edges -> vertices avoiding mask 'forbid'; returns 1 iff all edges matched */
static int match_try(const hyp *h, int ei, uint32_t forbid, int *matchv, uint32_t *seen) {
    for (int k = 0; k < 3; k++) { int v = h->e[ei][k]; if (forbid & (1u << v)) continue; if (*seen & (1u << v)) continue; *seen |= (1u << v);
        if (matchv[v] < 0 || match_try(h, matchv[v], forbid, matchv, seen)) { matchv[v] = ei; return 1; } }
    return 0; }
static int hyp_saturating(const hyp *h, uint32_t forbid) { int matchv[MAXV]; for (int v = 0; v < MAXV; v++) matchv[v] = -1;
    for (int i = 0; i < h->m; i++) { uint32_t seen = 0; if (!match_try(h, i, forbid, matchv, &seen)) return 0; } return 1; }
static int hyp_P3(const hyp *h) { if (h->m == 0) return 1; if (h->n < 2) return 0;
    for (int u = 0; u < h->n; u++) for (int v = u + 1; v < h->n; v++) if (!hyp_saturating(h, (1u << u) | (1u << v))) return 0; return 1; }
/* P3 by brute force over all subsets (for validation, n <= 20) */
static int hyp_P3_brute(const hyp *h) { for (uint32_t S = 0; S < (1u << h->n); S++) { int sz = popc(S); if (sz < 2) continue; int e = 0;
    for (int i = 0; i < h->m; i++) if ((h->em[i] & S) == h->em[i]) e++; if (e > sz - 2) return 0; } return 1; }
/* cover search: is there a cover of size <= k of the edges not yet covered (covered = vertex mask chosen) */
static int cover_le(const hyp *h, uint32_t chosen, int k) {
    int first = -1, cnt = 0; uint32_t used = 0; int mu = 0;
    for (int i = 0; i < h->m; i++) if (!(h->em[i] & chosen)) { if (first < 0) first = i; cnt++; if (!(h->em[i] & used)) { used |= h->em[i]; mu++; } }
    if (first < 0) return 1; if (k <= 0) return 0; if (mu > k) return 0;
    for (int kk = 0; kk < 3; kk++) if (cover_le(h, chosen | (1u << h->e[first][kk]), k - 1)) return 1;
    return 0; }
static int hyp_tau(const hyp *h) { int k = 0; while (!cover_le(h, 0, k)) k++; return k; }
static int hyp_tau_ge(const hyp *h, int t) { return !cover_le(h, 0, t - 1); }
/* all covers of size exactly T (minimum covers when T = tau): branch on first uncovered edge; dedupe by sort */
static int cmpu32(const void *a, const void *b) { uint32_t x = *(const uint32_t*)a, y = *(const uint32_t*)b; return x < y ? -1 : x > y; }
static void covers_rec(const hyp *h, uint32_t chosen, int sz, int T, uint32_t *out, int *cnt, int cap, int *overflow, int *smaller) {
    int first = -1; for (int i = 0; i < h->m; i++) if (!(h->em[i] & chosen)) { first = i; break; }
    if (first < 0) { if (sz < T) { *smaller = 1; return; } if (*cnt < cap) out[(*cnt)++] = chosen; else *overflow = 1; return; }
    if (sz >= T) return;
    for (int kk = 0; kk < 3; kk++) covers_rec(h, chosen | (1u << h->e[first][kk]), sz + 1, T, out, cnt, cap, overflow, smaller); }
static int hyp_min_covers(const hyp *h, int T, uint32_t *out, int cap, int *smaller) { int cnt = 0, overflow = 0; *smaller = 0;
    covers_rec(h, 0, 0, T, out, &cnt, cap, &overflow, smaller); if (overflow) return -1;
    qsort(out, cnt, sizeof(uint32_t), cmpu32); int u = 0; for (int i = 0; i < cnt; i++) if (i == 0 || out[i] != out[i-1]) out[u++] = out[i]; return u; }
/* parse "FOUND: (a,b,c) (d,e,f) ..." or "k a b c d e f ..." */
static int parse_found(const char *line, hyp *h, int n) { h->n = n; h->m = 0; const char *p = line;
    while ((p = strchr(p, '(')) != NULL) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) != 3) return 0; if (h->m >= MAXE) return 0; h->e[h->m][0] = a; h->e[h->m][1] = b; h->e[h->m][2] = c; h->m++; p++; }
    hyp_finish(h); return 1; }
static int parse_klist(const char *line, hyp *h, int n) { h->n = n; h->m = 0; int k; const char *p = line; int off;
    if (sscanf(p, "%d%n", &k, &off) != 1) return 0; p += off; if (k > MAXE) return 0;
    for (int i = 0; i < k; i++) { int a, b, c; if (sscanf(p, "%d %d %d%n", &a, &b, &c, &off) != 3) return 0; p += off; h->e[i][0] = a; h->e[i][1] = b; h->e[i][2] = c; } h->m = k; hyp_finish(h); return 1; }
static void print_found(FILE *f, const hyp *h) { fprintf(f, "FOUND:"); for (int i = 0; i < h->m; i++) fprintf(f, " (%d,%d,%d)", h->e[i][0], h->e[i][1], h->e[i][2]); fprintf(f, "\n"); }
#endif
