/* bfs_enum.c -- referee round 2 for L008 (written from scratch; shares no code with enum_conn.c, conn_dfs3.c, genbg or the
   round-1 hooks).
   METHOD: level-by-level "generate everything, then deduplicate by canonical form".  Level k holds one representative of
   every isomorphism class of admissible k-edge 3-graphs; level k+1 is obtained by adding every admissible edge to every
   representative and keeping one copy per canonical form.  Canonical forms: nauty's densenauty (library call only) on the
   vertex/edge incidence graph with the two colour classes kept apart; key = (nv, ne, sorted list of canonically relabelled
   edges).  Equal keys <=> isomorphic 3-graphs.
   Admissible (hereditary under edge deletion, so every prefix of a suitable edge order of a final graph is admissible):
     linear; max degree <= DMAX; tau(P) >= T0 - (M - |P|).
     CONN=1: vertex set = union of edges, each new edge meets the current vertex set (new vertices get labels nv, nv+1);
             nv <= N and nv + 2(M-|P|) >= N.  (A connected 3-graph has an edge order in which every edge meets the earlier
             ones; all its prefixes are connected and pass these tests.)
     CONN=0: vertex set {0..N-1} fixed (isolated vertices allowed), new edge = any triple.
   Output at level M: every class with tau >= T0 (CONN=1: and nv == N), as "FOUND: (a,b,c) ..." plus "AUT: <|Aut|>".
   Usage: bfs_enum N M T0 DMAX CONN [print]                                                                              */
#include "nauty.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef struct { uint64_t w[3]; } key_t3;
static int N, M, T0, DMAX, CONN, PRINT = 1;

typedef struct { int nv, ne; int ed[16][3]; } hg;

/* ---------- canonical key ---------- */
static void sort3(int *a, int *b, int *c) { int t; if (*a > *b) { t = *a; *a = *b; *b = t; } if (*b > *c) { t = *b; *b = *c; *c = t; } if (*a > *b) { t = *a; *a = *b; *b = t; } }
static key_t3 pack(int nv, int ne, int *tr) {
    key_t3 k; k.w[0] = k.w[1] = k.w[2] = 0;
    /* bits: nv 5, ne 5, then 12 bits per edge; total <= 10 + 14*12 = 178 */
    int pos = 0;
    uint64_t vals[20]; int widths[20]; int nvals = 0;
    vals[nvals] = nv; widths[nvals++] = 5; vals[nvals] = ne; widths[nvals++] = 5;
    for (int j = 0; j < ne; j++) { vals[nvals] = tr[j]; widths[nvals++] = 12; }
    for (int i = 0; i < nvals; i++) {
        for (int b = 0; b < widths[i]; b++, pos++) if (vals[i] >> b & 1) k.w[pos >> 6] |= 1ull << (pos & 63);
    }
    return k;
}
static void unpack(key_t3 k, hg *g) {
    int pos = 0;
    #define GETBITS(wd) ({ uint64_t _v = 0; for (int _b = 0; _b < (wd); _b++, pos++) if (k.w[pos >> 6] >> (pos & 63) & 1) _v |= 1ull << _b; _v; })
    g->nv = (int)GETBITS(5); g->ne = (int)GETBITS(5);
    for (int j = 0; j < g->ne; j++) { int t = (int)GETBITS(12); g->ed[j][0] = t >> 8; g->ed[j][1] = (t >> 4) & 15; g->ed[j][2] = t & 15; }
}
static double last_grpsize;
static key_t3 canon_key(const hg *g) {
    int n = g->nv + g->ne;
    int m = SETWORDSNEEDED(n);
    graph G[MAXN * 1], cg[MAXN * 1];
    int lab[MAXN], ptn[MAXN], orbits[MAXN];
    static DEFAULTOPTIONS_GRAPH(options);
    statsblk stats;
    options.getcanon = TRUE; options.defaultptn = FALSE;
    EMPTYGRAPH(G, m, n);
    for (int j = 0; j < g->ne; j++) for (int t = 0; t < 3; t++) ADDONEEDGE(G, g->ed[j][t], g->nv + j, m);
    for (int i = 0; i < n; i++) { lab[i] = i; ptn[i] = 1; }
    ptn[g->nv - 1] = 0; ptn[n - 1] = 0;
    densenauty(G, lab, ptn, orbits, &options, &stats, m, n, cg);
    last_grpsize = stats.grpsize1;
    for (int e = 0; e < stats.grpsize2; e++) last_grpsize *= 10.0;
    int cl[MAXN];
    for (int i = 0; i < g->nv; i++) { if (lab[i] >= g->nv) { fprintf(stderr, "colour order broken\n"); exit(5); } cl[lab[i]] = i; }
    int tr[16];
    for (int j = 0; j < g->ne; j++) {
        int a = cl[g->ed[j][0]], b = cl[g->ed[j][1]], c = cl[g->ed[j][2]]; sort3(&a, &b, &c);
        tr[j] = (a << 8) | (b << 4) | c;
    }
    for (int i = 1; i < g->ne; i++) { int x = tr[i], j = i - 1; while (j >= 0 && tr[j] > x) { tr[j + 1] = tr[j]; j--; } tr[j + 1] = x; }
    return pack(g->nv, g->ne, tr);
}

/* ---------- hash set of keys ---------- */
typedef struct { key_t3 *k; unsigned char *used; uint64_t cap, cnt; } hset;
static uint64_t hkey(key_t3 k) { uint64_t h = k.w[0] * 0x9E3779B97F4A7C15ull ^ (k.w[1] + 0x632BE59BD9B4E019ull) * 0xC2B2AE3D27D4EB4Full ^ (k.w[2] * 0x165667B19E3779F9ull); h ^= h >> 29; h *= 0xBF58476D1CE4E5B9ull; h ^= h >> 32; return h; }
static void hs_init(hset *s, uint64_t cap) { s->cap = cap; s->cnt = 0; s->k = malloc(cap * sizeof(key_t3)); s->used = calloc(cap, 1); if (!s->k || !s->used) { fprintf(stderr, "oom\n"); exit(3); } }
static void hs_free(hset *s) { free(s->k); free(s->used); }
static int hs_insert(hset *s, key_t3 k);
static void hs_grow(hset *s) {
    hset t; hs_init(&t, s->cap * 2);
    for (uint64_t i = 0; i < s->cap; i++) if (s->used[i]) hs_insert(&t, s->k[i]);
    hs_free(s); *s = t;
}
static int hs_insert(hset *s, key_t3 k) {
    if (2 * (s->cnt + 1) > s->cap) hs_grow(s);
    uint64_t i = hkey(k) & (s->cap - 1);
    while (s->used[i]) { if (!memcmp(&s->k[i], &k, sizeof k)) return 0; i = (i + 1) & (s->cap - 1); }
    s->used[i] = 1; s->k[i] = k; s->cnt++; return 1;
}

/* ---------- transversal test ---------- */
static uint32_t EM[16]; static int NEM;
/* can the edges in 'left' be met by at most k vertices?  branch on the vertices of the lowest-index edge in 'left' */
static int cover_le(uint32_t left, int k) {
    if (!left) return 1;
    if (k == 0) return 0;
    int i = __builtin_ctz(left);
    uint32_t e = EM[i];
    while (e) {
        int v = __builtin_ctz(e); e &= e - 1;
        uint32_t l2 = 0;
        for (int j = 0; j < NEM; j++) if ((left >> j & 1) && !(EM[j] >> v & 1)) l2 |= 1u << j;
        if (cover_le(l2, k - 1)) return 1;
    }
    return 0;
}
static int tau_at_least(const hg *g, int t) {
    if (t <= 0) return 1;
    NEM = g->ne; for (int j = 0; j < g->ne; j++) EM[j] = (1u << g->ed[j][0]) | (1u << g->ed[j][1]) | (1u << g->ed[j][2]);
    uint32_t all = (g->ne == 32) ? 0xffffffffu : ((1u << g->ne) - 1);
    return !cover_le(all, t - 1);
}
static int tau_exact(const hg *g) { int t = 0; while (tau_at_least(g, t + 1)) t++; return t; }

/* ---------- generation ---------- */
static unsigned long long children = 0;
static void try_child(hset *next, const hg *p, int a, int b, int c, int nvnew) {
    hg ch = *p; ch.nv = nvnew; ch.ed[ch.ne][0] = a; ch.ed[ch.ne][1] = b; ch.ed[ch.ne][2] = c; ch.ne++;
    children++;
    int r = M - ch.ne;
    if (CONN) { if (ch.nv > N || ch.nv + 2 * r < N) return; }
    if (!tau_at_least(&ch, T0 - r)) return;
    hs_insert(next, canon_key(&ch));
}
static void expand(hset *next, const hg *p) {
    int deg[16] = {0}; uint32_t nb[16] = {0};
    for (int j = 0; j < p->ne; j++) for (int t = 0; t < 3; t++) {
        int x = p->ed[j][t]; deg[x]++;
        for (int u = 0; u < 3; u++) if (u != t) nb[x] |= 1u << p->ed[j][u];
    }
    int nv = p->nv;
    for (int a = 0; a < nv; a++) {
        if (deg[a] >= DMAX) continue;
        for (int b = a + 1; b < nv; b++) {
            if (deg[b] >= DMAX || (nb[a] >> b & 1)) continue;
            for (int c = b + 1; c < nv; c++) {
                if (deg[c] >= DMAX || (nb[a] >> c & 1) || (nb[b] >> c & 1)) continue;
                try_child(next, p, a, b, c, nv);                     /* three old vertices */
            }
            if (CONN && nv + 1 <= N) try_child(next, p, a, b, nv, nv + 1);   /* two old, one new */
        }
        if (CONN && nv + 2 <= N) try_child(next, p, a, nv, nv + 1, nv + 2);   /* one old, two new */
    }
}
int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: bfs_enum N M T0 DMAX CONN [print]\n"); return 1; }
    N = atoi(argv[1]); M = atoi(argv[2]); T0 = atoi(argv[3]); DMAX = atoi(argv[4]); CONN = atoi(argv[5]);
    if (argc > 6) PRINT = atoi(argv[6]);
    if (N > 16 || M > 14 || N < 3 || M < 1) { fprintf(stderr, "range\n"); return 1; }
    hset cur; hs_init(&cur, 1024);
    hg g0; memset(&g0, 0, sizeof g0);
    int k0;
    if (CONN) { g0.nv = 3; g0.ne = 1; g0.ed[0][0] = 0; g0.ed[0][1] = 1; g0.ed[0][2] = 2; k0 = 1;
        int r = M - 1; if (!(3 + 2 * r < N) && tau_at_least(&g0, T0 - r)) hs_insert(&cur, canon_key(&g0)); }
    else { g0.nv = N; g0.ne = 0; k0 = 0; hs_insert(&cur, pack(N, 0, NULL)); }
    for (int k = k0; k < M; k++) {
        hset next; hs_init(&next, 1024);
        for (uint64_t i = 0; i < cur.cap; i++) if (cur.used[i]) { hg p; unpack(cur.k[i], &p); expand(&next, &p); }
        fprintf(stderr, "level %d -> %d: classes %llu (children tried so far %llu)\n", k, k + 1, (unsigned long long)next.cnt, children);
        hs_free(&cur); cur = next;
    }
    unsigned long long out = 0; double labelled = 0;
    double fact = 1; for (int i = 2; i <= N; i++) fact *= i;
    for (uint64_t i = 0; i < cur.cap; i++) if (cur.used[i]) {
        hg p; unpack(cur.k[i], &p);
        if (CONN && p.nv != N) continue;
        if (!tau_at_least(&p, T0)) continue;
        canon_key(&p); double aut = last_grpsize;
        out++; labelled += fact / aut;
        if (PRINT) {
            printf("FOUND:");
            for (int j = 0; j < p.ne; j++) printf(" (%d,%d,%d)", p.ed[j][0], p.ed[j][1], p.ed[j][2]);
            printf(" AUT=%.0f TAU=%d\n", aut, tau_exact(&p));
        }
    }
    printf("SUMMARY bfs_enum N=%d M=%d T0=%d DMAX=%d CONN=%d classes=%llu labelled=%.0f children=%llu\n", N, M, T0, DMAX, CONN, out, labelled, children);
    return 0;
}
