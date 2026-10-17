/* cfilter_r2.c -- referee L009 round 2: standalone membership test for the class C (same algorithms as r2hooks.c, validated there
   against the definitional networkx/brute-force checker defcheck.py).  Reads hypergraph lines with "(a,b,c)" tuples (vertices 0..31),
   prints for each:  "CF n=.. m=.. lin=.. f7=.. p3=.. C=.. conn=.. tau=.. maxdeg=.. comps=<sizes> E: (..) ...".
   linear: pairs of edges share <= 1 vertex; F7: centre c, three edges at c, two disjoint edges avoiding c inside the six other points,
   each meeting each of the three edges once; P3: e(S) <= |S|-2 for all vertex subsets S with |S| >= 2 (brute force over 2^n);
   tau exact by branching; connectivity of the vertex set 0..n-1 (n = max label + 1) by the edges.                                   */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static int NE, NV; static uint32_t E[64]; static uint64_t INC[32];
static int cover_le(uint64_t left, int k) {
    if (!left) return 1;
    if (k <= 0) return 0;
    uint64_t l = left; uint32_t used = 0; int cnt = 0;
    while (l) { int i = __builtin_ctzll(l); l &= l - 1; if (!(E[i] & used)) { used |= E[i]; if (++cnt > k) return 0; } }
    int i = __builtin_ctzll(left); uint32_t e = E[i];
    while (e) { int x = __builtin_ctz(e); e &= e - 1; if (cover_le(left & ~INC[x], k - 1)) return 1; }
    return 0;
}
static int has_f7(void) {
    for (int c = 0; c < NV; c++) {
        uint64_t at = INC[c]; int idx[64], d = 0;
        while (at) { idx[d++] = __builtin_ctzll(at); at &= at - 1; }
        for (int a = 0; a < d; a++) for (int b = a + 1; b < d; b++) for (int q = b + 1; q < d; q++) {
            uint32_t p1 = E[idx[a]] & ~(1u << c), p2 = E[idx[b]] & ~(1u << c), p3 = E[idx[q]] & ~(1u << c);
            if ((p1 & p2) || (p1 & p3) || (p2 & p3)) continue;
            uint32_t P = p1 | p2 | p3, tr[64]; int nt = 0;
            for (int j = 0; j < NE; j++) { uint32_t f = E[j];
                if (f & (1u << c)) continue; if (f & ~P) continue;
                if (__builtin_popcount(f & p1) != 1 || __builtin_popcount(f & p2) != 1 || __builtin_popcount(f & p3) != 1) continue;
                tr[nt++] = f; }
            for (int u = 0; u < nt; u++) for (int v = u + 1; v < nt; v++) if (!(tr[u] & tr[v])) return 1;
        }
    }
    return 0;
}
static int p3_ok(void) {
    uint32_t full = (NV >= 32) ? 0xffffffffu : ((1u << NV) - 1);
    for (uint32_t S = 0;; S++) {
        int sz = __builtin_popcount(S);
        if (sz >= 2) { int e = 0; for (int j = 0; j < NE; j++) if ((E[j] & S) == E[j]) e++; if (e > sz - 2) return 0; }
        if (S == full) break;
    }
    return 1;
}
int main(void) {
    static char line[1 << 16];
    unsigned long long tot = 0, nC = 0, nCconn = 0;
    while (fgets(line, sizeof line, stdin)) {
        NE = 0; NV = 0; char *p = line;
        while ((p = strchr(p, '('))) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) == 3) {
                if (NE >= 60 || a > 31 || b > 31 || c > 31 || a < 0 || b < 0 || c < 0) { fprintf(stderr, "range\n"); return 2; }
                E[NE++] = (1u << a) | (1u << b) | (1u << c);
                int mx = a > b ? (a > c ? a : c) : (b > c ? b : c); if (mx + 1 > NV) NV = mx + 1; } p++; }
        if (!NE) continue;
        tot++;
        for (int x = 0; x < NV; x++) INC[x] = 0;
        for (int j = 0; j < NE; j++) for (int x = 0; x < NV; x++) if (E[j] >> x & 1) INC[x] |= 1ull << j;
        int lin = 1; for (int i = 0; i < NE; i++) for (int j = i + 1; j < NE; j++) if (__builtin_popcount(E[i] & E[j]) >= 2) lin = 0;
        int f7 = has_f7(), p3 = p3_ok();
        uint64_t all = (1ull << NE) - 1; int t = 0; while (!cover_le(all, t)) t++;
        int md = 0; for (int x = 0; x < NV; x++) { int d = __builtin_popcountll(INC[x]); if (d > md) md = d; }
        /* components over vertices 0..NV-1 */
        uint32_t seen = 0; int cs[32], nc = 0;
        for (int x = 0; x < NV; x++) { if (seen >> x & 1) continue;
            uint32_t comp = 1u << x, prev = 0;
            while (comp != prev) { prev = comp; for (int j = 0; j < NE; j++) if (E[j] & comp) comp |= E[j]; }
            seen |= comp; cs[nc++] = __builtin_popcount(comp); }
        int C = lin && !f7 && p3; nC += C; if (C && nc == 1) nCconn++;
        printf("CF n=%d m=%d lin=%d f7=%d p3=%d C=%d conn=%d tau=%d maxdeg=%d comps=", NV, NE, lin, f7, p3, C, nc == 1, t, md);
        for (int i = 0; i < nc; i++) printf(i ? ",%d" : "%d", cs[i]);
        printf(" E:");
        for (int j = 0; j < NE; j++) { printf(" ("); int f = 1; for (int x = 0; x < NV; x++) if (E[j] >> x & 1) { printf(f ? "%d" : ",%d", x); f = 0; } printf(")"); }
        printf("\n");
    }
    fprintf(stderr, "CFILTER total=%llu inC=%llu inC_connected=%llu\n", tot, nC, nCconn);
    return 0;
}
