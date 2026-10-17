/* ref_filter.c: the filters of ref_ext.c applied to whole lists.
   ref_ext.c -- referee L010 round 1 (from scratch).  Vertex-extension step with a DIRECT tau test.
   Usage: ref_ext NG TG MAXDEG [printhits] < input
   input lines: "FOUND: (a,b,c) ..." or "G: (a,b,c) ..." (any tag; the edges are the (x,y,z) groups); G has vertices 0..NG-1
   (isolated vertices allowed).  For each G: requires tau(G) == TG (else counted bad_tau and skipped).
   Extensions: new vertex z = NG with three edges {z,a_i,b_i}, the pairs {a_i,b_i} pairwise disjoint, no pair inside an edge
   of G, every a_i,b_i of G-degree <= MAXDEG-1 (so that deg <= MAXDEG in H).  All unordered triples of such pairs.
   Hit iff tau(H) >= TG+1, decided by the branching cover test cov(H, TG) on H itself (no use of G's transversals).
   For every hit: linearity, F7 (method: a vertex p with three edges E1,E2,E3 through it whose other six vertices W are split
   by two disjoint edges T1,T2 contained in W, each meeting every E_i - p in one vertex), property (P3) in the form
   'every nonempty edge set F spans >= |F|+2 vertices' by recursive enumeration of all edge subsets, connectivity.
   Output: per-run summary; with printhits=1 also the hits in C ("CHIT:") and a status per hit ("HIT: <flags> edges"). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static uint32_t E[64]; static int NE, NV;
static int cov(uint64_t left, int k) {
    if (!left) return 1;
    if (k == 0) return 0;
    int i = __builtin_ctzll(left); uint32_t e = E[i];
    for (int t = 0; t < 3; t++) {
        int v = __builtin_ctz(e); e &= e - 1;
        uint64_t l2 = left;
        for (int j = 0; j < NE; j++) if ((l2 >> j & 1ULL) && (E[j] >> v & 1u)) l2 &= ~(1ULL << j);
        if (cov(l2, k - 1)) return 1;
    }
    return 0;
}
static uint64_t allm(void) { return NE >= 64 ? ~0ULL : ((1ULL << NE) - 1); }
static int tau(void) { int k = 0; while (!cov(allm(), k)) k++; return k; }
static int linear(void) { for (int i = 0; i < NE; i++) for (int j = i + 1; j < NE; j++) if (__builtin_popcount(E[i] & E[j]) > 1) return 0; return 1; }
static int f7(void) {
    for (int p = 0; p < NV; p++) {
        int at[64], k = 0; for (int i = 0; i < NE; i++) if (E[i] >> p & 1) at[k++] = i;
        for (int x = 0; x < k; x++) for (int y = x + 1; y < k; y++) for (int z = y + 1; z < k; z++) {
            uint32_t A = E[at[x]] & ~(1u << p), Bm = E[at[y]] & ~(1u << p), Cm = E[at[z]] & ~(1u << p);
            uint32_t W = A | Bm | Cm; if (__builtin_popcount(W) != 6) continue;
            int tr[64], nt = 0;
            for (int i = 0; i < NE; i++) {
                uint32_t e = E[i]; if ((e & W) != e) continue;
                if (__builtin_popcount(e & A) == 1 && __builtin_popcount(e & Bm) == 1 && __builtin_popcount(e & Cm) == 1) tr[nt++] = i;
            }
            for (int u = 0; u < nt; u++) for (int v = u + 1; v < nt; v++) if (!(E[tr[u]] & E[tr[v]])) return 1;
        }
    }
    return 0;
}
static int p3bad;
static void p3rec(int i, int cnt, uint32_t U) {   /* all edge subsets: include/exclude edge i */
    if (p3bad) return;
    if (i == NE) { if (cnt > 0 && __builtin_popcount(U) < cnt + 2) p3bad = 1; return; }
    p3rec(i + 1, cnt, U); p3rec(i + 1, cnt + 1, U | E[i]);
}
static int p3ok(void) { p3bad = 0; p3rec(0, 0, 0); return !p3bad; }
static int connected(void) {
    uint32_t all = (NV == 32) ? 0xffffffffu : ((1u << NV) - 1), c = 1u, p = 0;
    while (c != p) { p = c; for (int j = 0; j < NE; j++) if (E[j] & c) c |= E[j]; }
    return c == all;
}
static void pr(const char *tag) {
    printf("%s", tag);
    for (int j = 0; j < NE; j++) { uint32_t e = E[j]; printf(" ("); for (int c = 0; c < 3; c++) { int v = __builtin_ctz(e); e &= e - 1; printf(c ? ",%d" : "%d", v); } printf(")"); }
    printf("\n");
}

int main(int argc, char **argv) {
    /* Usage: ref_filter TAG [NVfix] < file : for every line starting with TAG: prints "INC:" + edges for members of C
       (linear, F7-free, P3), and a summary with counts, tau range, max degree. */
    const char *tag = argv[1]; int NVfix = argc > 2 ? atoi(argv[2]) : 0; size_t tl = strlen(tag);
    static char line[1 << 16];
    unsigned long long tot = 0, nonlin = 0, hf7 = 0, p3b = 0, p3b_f7free = 0, inC = 0, conn = 0; int tmin = 99, tmax = -1, dmax = 0;
    while (fgets(line, sizeof line, stdin)) {
        if (strncmp(line, tag, tl)) continue;
        char *p = strchr(line, '('); NE = 0; NV = 0;
        while (p) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) != 3) break;
            E[NE++] = (1u << a) | (1u << b) | (1u << c);
            if (a + 1 > NV) NV = a + 1; if (b + 1 > NV) NV = b + 1; if (c + 1 > NV) NV = c + 1; p = strchr(p + 1, '('); }
        if (NVfix) NV = NVfix;
        tot++;
        int lin = linear(), f = f7(), q = p3ok(), t = tau(), cn = connected();
        int d = 0; for (int v = 0; v < NV; v++) { int k = 0; for (int j = 0; j < NE; j++) if (E[j] >> v & 1) k++; if (k > d) d = k; }
        if (d > dmax) dmax = d; if (t < tmin) tmin = t; if (t > tmax) tmax = t;
        nonlin += !lin; hf7 += f; p3b += !q; p3b_f7free += (!f && !q); conn += cn;
        if (lin && !f && q) { inC++; pr("INC:"); }
    }
    printf("REFFILTER tag=%s total=%llu nonlinear=%llu contain_F7=%llu P3_violated=%llu F7free_P3bad=%llu inC=%llu connected=%llu tau=[%d,%d] maxdeg=%d\n",
           tag, tot, nonlin, hf7, p3b, p3b_f7free, inC, conn, tmin, tmax, dmax);
    return 0;
}
