/* myext.c -- referee L016 round 1 (own code, written from scratch for this review).
   Extension of a 3-graph G (vertices 0..NG-1) by one new vertex w = NG of degree d.
   Usage: myext NG TG d EP DMAX [all] [same] < input  (same: keep the extensions with tau = TG instead of tau >= TG+1) ; input lines "m a1 b1 c1 a2 b2 c2 ..."
   For each G:
     1. tau(G) is computed exactly (own branch and bound); if tau(G) != TG the graph is counted as 'badtau' and skipped.
     2. All covers of size TG (= all minimum covers) are enumerated by edge branching (smallest-candidate edge first,
        earlier siblings excluded); the list is sorted and checked for duplicates and for being covers of size TG.
     3. Admissible pairs: {a,b}, a<b<NG, deg_G(a) <= EP, deg_G(b) <= EP, {a,b} not contained in an edge of G.
     4. All d-sets of pairwise disjoint admissible pairs such that every minimum cover of G is disjoint from at least one
        pair of the set (equivalently tau(G + w) >= TG+1, since a cover of size TG of G+w cannot contain w).
        Enumeration: branch on the pairs killing the first live cover (earlier siblings excluded in the subtree); when no
        cover is alive the remaining pairs are chosen freely as a combination of non-excluded pairs.
     5. For each such X = G + {w,a,b}: F7 test (own), (P3) test by Hall with surplus 2 (each edge tripled), connectivity of
        all NG+1 vertices, maximum degree <= DMAX.
   Counters: sol (tau-hits), f7free, inC (f7free and P3), conn (inC, connected, maxdeg <= DMAX).
   Prints "X: (a,b,c) ..." for every hit of the last category (with 'all': every tau-hit, prefixed by its category). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int NG, TG, DD, EP, DMAX, PRINTALL = 0, SAME = 0;
static int m; static uint32_t E[64]; static int degG[32];
static uint32_t *cov; static int ncov, capcov;
static unsigned long long c_graphs, c_badtau, c_sol, c_f7free, c_inC, c_conn, c_maxcov, c_dup;

static void addcov(uint32_t S) {
    if (ncov == capcov) { capcov = capcov ? 2 * capcov : 1024; cov = realloc(cov, sizeof(uint32_t) * capcov); if (!cov) exit(9); }
    cov[ncov++] = S;
}
/* lower bound: a greedy set of pairwise disjoint edges not met by S needs that many new vertices */
static int lbound(uint32_t S) {
    uint32_t used = 0; int k = 0;
    for (int i = 0; i < m; i++) if (!(E[i] & S) && !(E[i] & used)) { used |= E[i]; k++; }
    return k;
}
/* covers C with S <= C, C disjoint from forb, |C \ S| <= budget, by branching on the non-forbidden vertices of the
   unmet edge with fewest candidates (earlier siblings forbidden in the subtree).  mode 0: return 1 at the first cover;
   mode 1: store every leaf. */
static int covrec(uint32_t S, int budget, uint32_t forb, int mode) {
    int best = -1, bc = 4;
    for (int i = 0; i < m; i++) if (!(E[i] & S)) { int c = __builtin_popcount(E[i] & ~forb); if (c < bc) { bc = c; best = i; if (c == 0) break; } }
    if (best < 0) { if (mode == 0) return 1; addcov(S); return 0; }
    if (bc == 0 || budget == 0) return 0;
    if (lbound(S) > budget) return 0;
    uint32_t f2 = forb;
    for (uint32_t r = E[best] & ~forb; r; r &= r - 1) { uint32_t v = r & -r; if (covrec(S | v, budget - 1, f2, mode) && mode == 0) return 1; f2 |= v; }
    return 0;
}
static int cmpu(const void *a, const void *b) { uint32_t x = *(const uint32_t *)a, y = *(const uint32_t *)b; return x < y ? -1 : x > y; }

/* pairs */
static int P; static uint32_t pm[600]; static uint64_t *killrow; static int W;
static int chosen[8];

/* ---------- checks on X ---------- */
static uint32_t XE[64]; static int XM;
static int isedge(uint32_t mask) { for (int i = 0; i < XM; i++) if (XE[i] == mask) return 1; return 0; }
static int has_f7(void) {
    int nv = NG + 1;
    for (int v = 0; v < nv; v++) {
        int at[64], na = 0;
        for (int i = 0; i < XM; i++) if (XE[i] >> v & 1) at[na++] = i;
        if (na < 3) continue;
        for (int i = 0; i < na; i++) for (int j = i + 1; j < na; j++) for (int k = j + 1; k < na; k++) {
            uint32_t A[3] = { XE[at[i]] & ~(1u << v), XE[at[j]] & ~(1u << v), XE[at[k]] & ~(1u << v) };
            if ((A[0] & A[1]) || (A[0] & A[2]) || (A[1] & A[2])) continue;
            int a0 = __builtin_ctz(A[0]), a1 = 31 - __builtin_clz(A[0]);
            int b0 = __builtin_ctz(A[1]), b1 = 31 - __builtin_clz(A[1]);
            int c0 = __builtin_ctz(A[2]), c1 = 31 - __builtin_clz(A[2]);
            /* choice x = (a0, bX, cY); complement (a1, other b, other c) */
            for (int sb = 0; sb < 2; sb++) for (int sc = 0; sc < 2; sc++) {
                int bx = sb ? b1 : b0, by = sb ? b0 : b1, cx = sc ? c1 : c0, cy = sc ? c0 : c1;
                uint32_t f = (1u << a0) | (1u << bx) | (1u << cx), g = (1u << a1) | (1u << by) | (1u << cy);
                if (__builtin_popcount(f) == 3 && __builtin_popcount(g) == 3 && isedge(f) && isedge(g)) return 1;
            }
        }
    }
    return 0;
}
static uint32_t Lm[80]; static int mr[32];
static int aug(int i, uint32_t *vis) {
    for (uint32_t r = Lm[i] & ~*vis; r; r &= r - 1) {
        int v = __builtin_ctz(r); *vis |= 1u << v;
        if (mr[v] < 0 || aug(mr[v], vis)) { mr[v] = i; return 1; }
    }
    return 0;
}
/* (P3): every nonempty edge set F spans >= |F|+2 vertices  <=>  for every edge e, the edge-vertex incidence system with e
   tripled has a matching saturating all edge copies (Hall). */
static int p3ok(void) {
    int base[32];
    for (int v = 0; v < 32; v++) mr[v] = -1;
    for (int i = 0; i < XM; i++) Lm[i] = XE[i];
    for (int i = 0; i < XM; i++) { uint32_t vis = 0; if (!aug(i, &vis)) return 0; }
    memcpy(base, mr, sizeof base);
    for (int e = 0; e < XM; e++) {
        memcpy(mr, base, sizeof base);
        Lm[XM] = XE[e]; Lm[XM + 1] = XE[e];
        uint32_t vis = 0; if (!aug(XM, &vis)) return 0;
        vis = 0; if (!aug(XM + 1, &vis)) return 0;
    }
    return 1;
}
static int connected_all(void) {
    int nv = NG + 1; uint32_t seen = 1u, frontier = 1u;   /* start from vertex 0 */
    while (frontier) {
        uint32_t nf = 0;
        for (int i = 0; i < XM; i++) if (XE[i] & frontier) nf |= XE[i];
        nf &= ~seen; seen |= nf; frontier = nf;
    }
    uint32_t all = (nv == 32) ? 0xffffffffu : ((1u << nv) - 1);
    return seen == all;
}
static int maxdeg(void) {
    int dg[32] = {0}, mx = 0;
    for (int i = 0; i < XM; i++) for (uint32_t r = XE[i]; r; r &= r - 1) { int v = __builtin_ctz(r); if (++dg[v] > mx) mx = dg[v]; }
    return mx;
}
static void printX(const char *tag) {
    printf("%s", tag);
    for (int i = 0; i < XM; i++) { int v[3], k = 0; for (uint32_t r = XE[i]; r; r &= r - 1) v[k++] = __builtin_ctz(r); printf(" (%d,%d,%d)", v[0], v[1], v[2]); }
    printf("\n");
}
static uint64_t *allcov;
static int same_ok(int nch) {   /* is some minimum cover of G meeting every chosen pair? (then tau(X) = TG) */
    for (int w = 0; w < W; w++) { uint64_t a = allcov[w]; for (int i = 0; i < nch; i++) a &= ~killrow[(size_t)chosen[i] * W + w]; if (a) return 1; }
    return 0;
}
static void emit(int nch) {
    if (SAME && !same_ok(nch)) return;
    c_sol++;
    XM = 0; for (int i = 0; i < m; i++) XE[XM++] = E[i];
    for (int i = 0; i < nch; i++) XE[XM++] = pm[chosen[i]] | (1u << NG);
    int f7 = has_f7();
    int p3 = 0, cn = 0, dg = 0;
    if (!f7) { c_f7free++; p3 = p3ok(); if (p3) { c_inC++; cn = connected_all(); dg = maxdeg() <= DMAX; if (cn && dg) c_conn++; } }
    if (PRINTALL) {
        char tag[64]; snprintf(tag, sizeof tag, "H f7=%d p3=%d conn=%d degok=%d:", f7, p3, cn, dg); printX(tag);
    } else if (!f7 && p3 && cn && dg) printX("X:");
}
static void freepick(int nch, int start, const uint64_t *fb, uint32_t used) {
    if (nch == DD) { emit(nch); return; }
    for (int p = start; p < P; p++) {
        if ((fb[p >> 6] >> (p & 63)) & 1) continue;
        if (pm[p] & used) continue;
        chosen[nch] = p; freepick(nch + 1, p + 1, fb, used | pm[p]);
    }
}
static uint64_t *alivebuf;  /* (DD+1) * W words */
static void search(int nch, const uint64_t *alive, const uint64_t *fb, uint32_t used) {
    int c0 = -1;
    for (int w = 0; w < W; w++) if (alive[w]) { c0 = w * 64 + __builtin_ctzll(alive[w]); break; }
    if (c0 < 0) { freepick(nch, 0, fb, used); return; }
    if (nch == DD) return;
    uint64_t fb2[10]; memcpy(fb2, fb, sizeof fb2);
    uint64_t *al = alivebuf + (size_t)(nch + 1) * W;
    for (int p = 0; p < P; p++) {
        if (pm[p] & cov[c0]) continue;           /* must kill c0: disjoint from it */
        if ((fb2[p >> 6] >> (p & 63)) & 1) continue;
        if (pm[p] & used) continue;
        const uint64_t *kr = killrow + (size_t)p * W;
        for (int w = 0; w < W; w++) al[w] = alive[w] & ~kr[w];
        chosen[nch] = p;
        search(nch + 1, al, fb2, used | pm[p]);
        fb2[p >> 6] |= 1ull << (p & 63);
    }
}
int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: myext NG TG d EP DMAX [all]\n"); return 1; }
    NG = atoi(argv[1]); TG = atoi(argv[2]); DD = atoi(argv[3]); EP = atoi(argv[4]); DMAX = atoi(argv[5]);
    for (int i = 6; i < argc; i++) { if (!strcmp(argv[i], "all")) PRINTALL = 1; if (!strcmp(argv[i], "same")) SAME = 1; }
    if (NG > 31 || DD > 7 || DD < 1) { fprintf(stderr, "limits\n"); return 1; }
    while (scanf("%d", &m) == 1) {
        c_graphs++;
        if (m > 56) { fprintf(stderr, "too many edges\n"); return 2; }
        memset(degG, 0, sizeof degG);
        for (int i = 0; i < m; i++) {
            int a, b, c; if (scanf("%d %d %d", &a, &b, &c) != 3) { fprintf(stderr, "parse\n"); return 2; }
            if (a < 0 || b < 0 || c < 0 || a >= NG || b >= NG || c >= NG || a == b || a == c || b == c) { fprintf(stderr, "label\n"); return 2; }
            E[i] = (1u << a) | (1u << b) | (1u << c); degG[a]++; degG[b]++; degG[c]++;
        }
        /* tau(G) == TG ? */
        ncov = 0;
        if (TG < 1 || covrec(0, TG - 1, 0, 0)) { c_badtau++; continue; }
        covrec(0, TG, 0, 1);
        if (ncov == 0) { c_badtau++; continue; }
        qsort(cov, ncov, sizeof(uint32_t), cmpu);
        for (int i = 0; i < ncov; i++) {
            if (__builtin_popcount(cov[i]) != TG) { fprintf(stderr, "cover size\n"); return 5; }
            for (int j = 0; j < m; j++) if (!(E[j] & cov[i])) { fprintf(stderr, "not a cover\n"); return 5; }
            if (i && cov[i] == cov[i - 1]) c_dup++;
        }
        if (c_dup) { fprintf(stderr, "duplicate covers\n"); return 5; }
        if ((unsigned long long)ncov > c_maxcov) c_maxcov = ncov;
        /* pairs */
        P = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (degG[a] > EP || degG[b] > EP) continue;
            uint32_t pmask = (1u << a) | (1u << b); int inside = 0;
            for (int j = 0; j < m; j++) if ((E[j] & pmask) == pmask) { inside = 1; break; }
            if (inside) continue;
            if (P >= 600) { fprintf(stderr, "P\n"); return 4; }
            pm[P++] = pmask;
        }
        W = (ncov + 63) / 64;
        killrow = realloc(killrow, sizeof(uint64_t) * (size_t)(P ? P : 1) * W);
        alivebuf = realloc(alivebuf, sizeof(uint64_t) * (size_t)(DD + 2) * W);
        for (int p = 0; p < P; p++) { uint64_t *kr = killrow + (size_t)p * W; memset(kr, 0, sizeof(uint64_t) * W);
            for (int c = 0; c < ncov; c++) if (!(cov[c] & pm[p])) kr[c >> 6] |= 1ull << (c & 63); }
        uint64_t *alive = alivebuf; memset(alive, 0, sizeof(uint64_t) * W);
        for (int c = 0; c < ncov; c++) alive[c >> 6] |= 1ull << (c & 63);
        uint64_t fb[10]; memset(fb, 0, sizeof fb);
        if (SAME) { allcov = realloc(allcov, sizeof(uint64_t) * (size_t)W); memcpy(allcov, alive, sizeof(uint64_t) * W); freepick(0, 0, fb, 0); }
        else search(0, alive, fb, 0);
    }
    printf("MYSUMMARY graphs=%llu badtau=%llu maxcov=%llu sol=%llu f7free=%llu inC=%llu conn=%llu\n",
           c_graphs, c_badtau, c_maxcov, c_sol, c_f7free, c_inC, c_conn);
    return 0;
}
