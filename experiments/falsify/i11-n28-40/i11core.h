/* i11core.h: class C membership, exact tau (frontier DP), RNG.  Vertices 0..n-1 (n<=MAXN), edges are 64-bit masks. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
typedef uint64_t u64;
#define MAXN 60
#define MAXM 64
#define MAXDEG 16
#define MAXSLOT 22
typedef struct { int n, m; u64 e[MAXM]; } G;
static int DMAX = 3; /* max degree allowed when adding edges */

static u64 rs0 = 88172645463325252ULL, rs1 = 1234567891011ULL;
static inline u64 rnd64(void) { u64 s1 = rs0, s0 = rs1; rs0 = s0; s1 ^= s1 << 23; rs1 = s1 ^ s0 ^ (s1 >> 18) ^ (s0 >> 5); return rs1 + s0; }
static inline int rndint(int k) { return (int)(rnd64() % (u64)k); }
static inline double rnd01(void) { return (rnd64() >> 11) * (1.0 / 9007199254740992.0); }
static void seed_rng(u64 s) { rs0 = s * 0x9E3779B97F4A7C15ULL + 1; rs1 = (s ^ 0xDEADBEEFCAFEBABEULL) * 0xBF58476D1CE4E5B9ULL + 7; for (int i = 0; i < 20; i++) rnd64(); }

static inline u64 vmask(int a, int b, int c) { return (1ULL << a) | (1ULL << b) | (1ULL << c); }

/* ---------- degrees, linearity ---------- */
static int degree_of(const G *g, int v) { int d = 0; for (int i = 0; i < g->m; i++) d += (g->e[i] >> v) & 1; return d; }
static int maxdeg(const G *g) { int d = 0; for (int v = 0; v < g->n; v++) { int x = degree_of(g, v); if (x > d) d = x; } return d; }
static int linear_all(const G *g) { for (int i = 0; i < g->m; i++) for (int j = i + 1; j < g->m; j++) if (__builtin_popcountll(g->e[i] & g->e[j]) >= 2) return 0; return 1; }

/* ---------- F7 (subgraph, not nec. induced): vertex v with three edges, two disjoint edges X,Y that each take one vertex of every pair ---------- */
static int has_edge(const G *g, u64 x) { for (int i = 0; i < g->m; i++) if (g->e[i] == x) return 1; return 0; }
static int has_f7(const G *g) {
    int inc[MAXN][MAXDEG], ninc[MAXN]; memset(ninc, 0, sizeof(int) * g->n);
    for (int i = 0; i < g->m; i++) for (u64 r = g->e[i]; r; r &= r - 1) { int v = __builtin_ctzll(r); if (ninc[v] < MAXDEG) inc[v][ninc[v]++] = i; }
    for (int v = 0; v < g->n; v++) if (ninc[v] >= 3)
        for (int a = 0; a < ninc[v]; a++) for (int b = a + 1; b < ninc[v]; b++) for (int c = b + 1; c < ninc[v]; c++) {
            u64 P[3] = { g->e[inc[v][a]] & ~(1ULL << v), g->e[inc[v][b]] & ~(1ULL << v), g->e[inc[v][c]] & ~(1ULL << v) };
            u64 U = P[0] | P[1] | P[2];
            u64 lo[3], hi[3];
            for (int k = 0; k < 3; k++) { lo[k] = P[k] & -P[k]; hi[k] = P[k] ^ lo[k]; }
            for (int ch = 0; ch < 4; ch++) { /* first pair fixed to lo to halve symmetric duplicates */
                u64 X = lo[0] | ((ch & 1) ? hi[1] : lo[1]) | ((ch & 2) ? hi[2] : lo[2]);
                u64 Y = U ^ X;
                if (has_edge(g, X) && has_edge(g, Y)) return 1;
            }
        }
    return 0;
}

/* ---------- Hall / midpoint injectivity: for pair (x,y) all edges can be given distinct representatives avoiding x,y ---------- */
static int aug_(const G *g, int e, u64 *seen, int *owner, u64 forbid) {
    for (u64 r = g->e[e] & ~forbid; r; r &= r - 1) {
        int v = __builtin_ctzll(r); if ((*seen >> v) & 1) continue; *seen |= 1ULL << v;
        if (owner[v] < 0 || aug_(g, owner[v], seen, owner, forbid)) { owner[v] = e; return 1; }
    }
    return 0;
}
static int hall_pair(const G *g, int x, int y) {
    int owner[MAXN]; for (int v = 0; v < g->n; v++) owner[v] = -1;
    u64 forbid = (1ULL << x) | (1ULL << y);
    for (int e = 0; e < g->m; e++) { u64 seen = 0; if (!aug_(g, e, &seen, owner, forbid)) return 0; }
    return 1;
}
static int hall_full(const G *g) {
    u64 used = 0; for (int i = 0; i < g->m; i++) used |= g->e[i];
    for (int x = 0; x < g->n; x++) if ((used >> x) & 1) for (int y = x + 1; y < g->n; y++) if ((used >> y) & 1) if (!hall_pair(g, x, y)) return 0;
    return 1;
}
static int hall_new_edge(const G *g, u64 e) { /* g already contains e as last edge; check the 3 pairs inside e */
    int v[3], k = 0; for (u64 r = e; r; r &= r - 1) v[k++] = __builtin_ctzll(r);
    return hall_pair(g, v[0], v[1]) && hall_pair(g, v[0], v[2]) && hall_pair(g, v[1], v[2]);
}
/* full membership in C with degree cap dmax (dmax<=0: no cap). returns 0 if in class, else code of the failure */
static int check_class(const G *g, int dmax) {
    for (int i = 0; i < g->m; i++) if (__builtin_popcountll(g->e[i]) != 3 || (g->e[i] >> g->n)) return 1;
    if (!linear_all(g)) return 2;
    if (dmax > 0 && maxdeg(g) > dmax) return 3;
    if (has_f7(g)) return 4;
    if (!hall_full(g)) return 5;
    return 0;
}
/* try to append edge e (mask) to g: returns 1 on success (g modified), else 0 (g unchanged). assumes g in C with degree cap DMAX */
static int try_add(G *g, u64 e) {
    if (g->m >= MAXM) return 0;
    if (__builtin_popcountll(e) != 3) return 0;
    for (int i = 0; i < g->m; i++) if (__builtin_popcountll(g->e[i] & e) >= 2) return 0;
    for (u64 r = e; r; r &= r - 1) { int v = __builtin_ctzll(r); if (DMAX > 0 && degree_of(g, v) >= DMAX) return 0; }
    g->e[g->m++] = e;
    if (has_f7(g) || !hall_new_edge(g, e)) { g->m--; return 0; }
    return 1;
}

/* ---------- exact alpha / tau via frontier DP ---------- */
static int8_t bufA[1 << MAXSLOT], bufB[1 << MAXSLOT];
static double cntA[1 << MAXSLOT], cntB[1 << MAXSLOT];
static int ord_cost(const G *g, const int *ord, double *lcost);
static void make_order(const G *g, int *ord, int randomize) {
    int n = g->n, m = g->m;
    int inc[MAXN][MAXDEG], ninc[MAXN], cnt[MAXN], rem[MAXM], done[MAXN];
    memset(ninc, 0, sizeof(int) * n);
    for (int i = 0; i < m; i++) { rem[i] = 3; for (u64 r = g->e[i]; r; r &= r - 1) { int v = __builtin_ctzll(r); if (ninc[v] < MAXDEG) inc[v][ninc[v]++] = i; } }
    for (int v = 0; v < n; v++) { cnt[v] = ninc[v]; done[v] = 0; }
    for (int t = 0; t < n; t++) {
        int bestv = -1, bestd = 1000, bests = -1, nties = 0;
        for (int v = 0; v < n; v++) if (!done[v]) {
            int closed = 0, dying = 0, touched = 0;
            for (int k = 0; k < ninc[v]; k++) { int e = inc[v][k]; if (rem[e] == 1) { closed++; for (u64 r = g->e[e] & ~(1ULL << v); r; r &= r - 1) { int u = __builtin_ctzll(r); if (cnt[u] == 1) dying++; } } if (rem[e] < 3) touched++; }
            int delta = ((cnt[v] - closed) > 0 ? 1 : 0) - dying;
            int score = touched;
            if (delta < bestd || (delta == bestd && score > bests)) { bestd = delta; bests = score; bestv = v; nties = 1; }
            else if (delta == bestd && (score == bests) && randomize) { nties++; if (rndint(nties) == 0) bestv = v; }
        }
        int v = bestv; done[v] = 1; ord[t] = v;
        for (int k = 0; k < ninc[v]; k++) { int e = inc[v][k]; rem[e]--; if (rem[e] == 0) for (u64 r = g->e[e]; r; r &= r - 1) cnt[__builtin_ctzll(r)]--; }
    }
}
/* returns alpha (>=0), or -1 if frontier too large. if docount, *lcount = log(number of maximum independent sets) */
static int alpha_dp(const G *g, const int *ord, int docount, double *lcount) {
    int n = g->n, m = g->m, pos[MAXN], last[MAXM], death[MAXN], slot[MAXN];
    for (int i = 0; i < n; i++) pos[ord[i]] = i;
    for (int i = 0; i < m; i++) { int l = 0; for (u64 r = g->e[i]; r; r &= r - 1) { int p = pos[__builtin_ctzll(r)]; if (p > l) l = p; } last[i] = l; }
    for (int v = 0; v < n; v++) death[v] = pos[v];
    for (int i = 0; i < m; i++) for (u64 r = g->e[i]; r; r &= r - 1) { int v = __builtin_ctzll(r); if (last[i] > death[v]) death[v] = last[i]; }
    int8_t *cur = bufA, *nxt = bufB; double *cc = cntA, *cn = cntB;
    cur[0] = 0; if (docount) cc[0] = 1.0;
    u64 used = 0; int hsz = 0; /* cur valid for indices < (1<<hsz) */
    for (int t = 0; t < n; t++) {
        int v = ord[t];
        int sv = 0; while ((used >> sv) & 1) sv++;
        if (sv >= MAXSLOT) return -1;
        slot[v] = sv; used |= 1ULL << sv;
        int hs = 64 - __builtin_clzll(used);
        if (hs > hsz) { memset(cur + (1 << hsz), -1, (size_t)((1 << hs) - (1 << hsz))); if (docount) memset(cc + (1 << hsz), 0, sizeof(double) * ((size_t)((1 << hs) - (1 << hsz)))); }
        int size = 1 << hs;
        unsigned chk[MAXDEG * 2]; int nchk = 0;
        for (int i = 0; i < m; i++) if (last[i] == t) { unsigned mk = 0; for (u64 r = g->e[i] & ~(1ULL << v); r; r &= r - 1) mk |= 1u << slot[__builtin_ctzll(r)]; if (nchk < MAXDEG * 2) chk[nchk++] = mk; }
        unsigned kill = 0;
        for (int u = 0; u < n; u++) if (pos[u] <= t && death[u] == t) kill |= 1u << slot[u];
        unsigned keep = ~kill; unsigned bv = 1u << sv;
        memset(nxt, -1, (size_t)size); if (docount) memset(cn, 0, sizeof(double) * (size_t)size);
        for (int s = 0; s < size; s++) {
            int val = cur[s]; if (val < 0) continue;
            unsigned s0 = (unsigned)s & keep;
            if (nxt[s0] < val) { nxt[s0] = val; if (docount) cn[s0] = cc[s]; } else if (docount && nxt[s0] == val) cn[s0] += cc[s];
            int ok = 1; for (int k = 0; k < nchk; k++) if (((unsigned)s & chk[k]) == chk[k]) { ok = 0; break; }
            if (ok) { unsigned s1 = ((unsigned)s | bv) & keep; int v1 = val + 1; if (nxt[s1] < v1) { nxt[s1] = v1; if (docount) cn[s1] = cc[s]; } else if (docount && nxt[s1] == v1) cn[s1] += cc[s]; }
        }
        used &= ~(u64)kill;
        { int8_t *tp = cur; cur = nxt; nxt = tp; double *tc = cc; cc = cn; cn = tc; }
        hsz = hs;
    }
    int best = 0; double bc = 0; for (int s = 0; s < (1 << hsz); s++) if (cur[s] >= 0) { if (cur[s] > best) { best = cur[s]; if (docount) bc = cc[s]; } else if (docount && cur[s] == best) bc += cc[s]; }
    if (docount && lcount) *lcount = log(bc > 0 ? bc : 1.0);
    return best;
}
/* best of several orderings by cost; returns tau or -1 */
static int tau_of(const G *g, int tries, int docount, double *lcount) {
    int bestord[MAXN], ord[MAXN]; double bestcost = 1e300;
    for (int t = 0; t < tries; t++) {
        make_order(g, ord, t > 0);
        double c; ord_cost(g, ord, &c);
        if (c < bestcost) { bestcost = c; memcpy(bestord, ord, sizeof(int) * g->n); }
    }
    int a = alpha_dp(g, bestord, docount, lcount);
    return a < 0 ? -1 : g->n - a;
}
static int ord_cost(const G *g, const int *ord, double *lcost) {
    int n = g->n, m = g->m, pos[MAXN], death[MAXN];
    for (int i = 0; i < n; i++) pos[ord[i]] = i;
    for (int v = 0; v < n; v++) death[v] = pos[v];
    for (int i = 0; i < m; i++) { int l = 0; for (u64 r = g->e[i]; r; r &= r - 1) { int p = pos[__builtin_ctzll(r)]; if (p > l) l = p; }
        for (u64 r = g->e[i]; r; r &= r - 1) { int v = __builtin_ctzll(r); if (l > death[v]) death[v] = l; } }
    double c = 0; int mx = 0;
    for (int t = 0; t < n; t++) { int live = 0; for (int u = 0; u < n; u++) if (pos[u] <= t && death[u] > t) live++; if (live + 1 > mx) mx = live + 1; c += ldexp(1.0, live + 1); }
    *lcost = c; return mx;
}

/* ---------- misc ---------- */
static int components(const G *g, int *isolated) {
    u64 all = 0; for (int i = 0; i < g->m; i++) all |= g->e[i];
    u64 seen = 0; int nc = 0;
    for (int i = 0; i < g->m; i++) if (!((seen >> __builtin_ctzll(g->e[i])) & 1)) {
        u64 comp = g->e[i], prev = 0; while (comp != prev) { prev = comp; for (int j = 0; j < g->m; j++) if (g->e[j] & comp) comp |= g->e[j]; }
        seen |= comp; nc++;
    }
    if (isolated) *isolated = g->n - __builtin_popcountll(all);
    return nc;
}
static int slack_of(const G *g, int tau) { return 3 * g->n + 2 * g->m - 11 * tau; }
static void print_graph(FILE *f, const G *g) { fprintf(f, "%d %d", g->n, g->m); for (int i = 0; i < g->m; i++) { fprintf(f, " "); int k = 0; for (u64 r = g->e[i]; r; r &= r - 1) fprintf(f, k++ ? ",%d" : "%d", __builtin_ctzll(r)); } fprintf(f, "\n"); }
/* parse "n m a,b,c a,b,c ..." */
static int parse_graph(const char *line, G *g) {
    int n, m, off; if (sscanf(line, "%d %d%n", &n, &m, &off) != 2) return 0;
    if (n > MAXN || m > MAXM) return 0; g->n = n; g->m = m; const char *p = line + off;
    for (int i = 0; i < m; i++) { int a, b, c, o; if (sscanf(p, " %d,%d,%d%n", &a, &b, &c, &o) != 3) return 0; p += o; if (a == b || b == c || a == c || a >= n || b >= n || c >= n) return 0; g->e[i] = vmask(a, b, c); }
    return 1;
}
