/* ref_ext.c -- referee L010 round 1 (from scratch).  Vertex-extension step with a DIRECT tau test.
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
    int NG = atoi(argv[1]), TG = atoi(argv[2]), MD = atoi(argv[3]), PH = argc > 4 ? atoi(argv[4]) : 0;
    static char line[1 << 16];
    unsigned long long graphs = 0, bad_tau = 0, tested = 0, hits = 0, h_nonlin = 0, h_f7 = 0, h_p3bad_f7free = 0, h_inC = 0, h_conn = 0, h_conn_inC = 0;
    while (fgets(line, sizeof line, stdin)) {
        char *p = strchr(line, '('); if (!p) continue;
        NE = 0; NV = NG + 1;
        while (p) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) != 3) break;
            if (a >= NG || b >= NG || c >= NG) { fprintf(stderr, "label >= NG\n"); return 2; }
            E[NE++] = (1u << a) | (1u << b) | (1u << c); p = strchr(p + 1, '('); }
        int mG = NE; graphs++;
        int deg[32] = {0}; for (int j = 0; j < mG; j++) for (int v = 0; v < NG; v++) if (E[j] >> v & 1) deg[v]++;
        { int sv = NV; NV = NG; int t = tau(); NV = sv; if (t != TG) { bad_tau++; continue; } }
        uint32_t pairs[512]; int np = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > MD - 1 || deg[b] > MD - 1) continue;
            uint32_t q = (1u << a) | (1u << b); int ok = 1;
            for (int j = 0; j < mG; j++) if ((E[j] & q) == q) { ok = 0; break; }
            if (ok) pairs[np++] = q;
        }
        uint32_t z = 1u << NG;
        for (int x = 0; x < np; x++) for (int y = x + 1; y < np; y++) {
            if (pairs[x] & pairs[y]) continue;
            for (int w = y + 1; w < np; w++) {
                if ((pairs[x] | pairs[y]) & pairs[w]) continue;
                tested++;
                E[mG] = pairs[x] | z; E[mG + 1] = pairs[y] | z; E[mG + 2] = pairs[w] | z; NE = mG + 3;
                if (cov(allm(), TG)) { NE = mG; continue; }
                hits++;
                int lin = linear(), hf = f7(), hp = p3ok(), hc = connected();
                if (!lin) h_nonlin++;
                if (hf) h_f7++; else if (!hp) h_p3bad_f7free++;
                int inC = lin && !hf && hp; h_inC += inC; h_conn += hc; h_conn_inC += hc && inC;
                if (PH) { char tg[64]; sprintf(tg, "%s%s%s%s:", inC ? "CHIT" : "HIT", hf ? "_F7" : "", hp ? "" : "_P3", hc ? "_conn" : ""); pr(tg); }
                NE = mG;
            }
        }
    }
    printf("REFEXT NG=%d TG=%d MAXDEG=%d graphs=%llu bad_tau=%llu tested=%llu hits=%llu nonlinear=%llu contain_F7=%llu F7free_P3bad=%llu inC=%llu connected=%llu connected_inC=%llu\n",
           NG, TG, MD, graphs, bad_tau, tested, hits, h_nonlin, h_f7, h_p3bad_f7free, h_inC, h_conn, h_conn_inC);
    return 0;
}
