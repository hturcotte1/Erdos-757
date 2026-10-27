/* redfree.c -- exact (Red) test for 3-graphs.  Usage: redfree NV [v] < canon-lines ("C m a.b.c ...")
   For every proper nonempty vertex subset Z, E_Z = edges meeting Z, tau(E_Z) = minimum number of vertices (anywhere) meeting all of E_Z,
   value(Z) = 3|Z| + 2|E_Z| - 11 tau(E_Z).  (Red) holds for Z iff value(Z) >= 0.  Output per input graph (tab separated):
   n m tau slack maxdeg redfree(1/0) bestval |Z| |E_Z| tau(E_Z) Zmask(hex) Tmask(hex) degseq edges
   best = argmax of value over proper nonempty Z (ties: smaller |Z|, then smaller mask).  Tmask = a minimum transversal of E_Z.
   If a second argument 'v' is given, an additional column lists the number of Z with value >= 0 (cnt_red). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int n, m; static uint32_t ed[40], inc[32]; /* inc[v]: bitmask of edges through v */
static int8_t *tauF; static uint32_t *EZ;
int main(int argc, char **argv) {
    n = atoi(argv[1]); int verbose = argc > 2;
    static char line[1 << 14];
    EZ = malloc(sizeof(uint32_t) << n);
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] != 'C') continue;
        char *p = line + 1; int k; if (sscanf(p, "%d%n", &m, &k) != 1) continue; p += k;
        memset(inc, 0, sizeof inc);
        for (int i = 0; i < m; i++) { int a, b, c; if (sscanf(p, " %d.%d.%d%n", &a, &b, &c, &k) != 3) return 2; p += k;
            ed[i] = (1u << a) | (1u << b) | (1u << c); inc[a] |= 1u << i; inc[b] |= 1u << i; inc[c] |= 1u << i; }
        /* tau of every edge subset F: tau(0)=0; tau(F) = 1 + min over v in lowest edge of F of tau(F minus edges at v) */
        uint32_t NF = 1u << m; tauF = realloc(tauF, NF);
        tauF[0] = 0;
        for (uint32_t F = 1; F < NF; F++) {
            int e = __builtin_ctz(F), best = 99;
            for (uint32_t r = ed[e]; r; r &= r - 1) { int v = __builtin_ctz(r); int t = 1 + tauF[F & ~inc[v]]; if (t < best) best = t; }
            tauF[F] = best;
        }
        int tau = tauF[NF - 1];
        int maxdeg = 0, dg[32]; for (int v = 0; v < n; v++) { dg[v] = __builtin_popcount(inc[v]); if (dg[v] > maxdeg) maxdeg = dg[v]; }
        int slack = 3 * n + 2 * m - 11 * tau;
        uint32_t NZ[32]; for (int v = 0; v < n; v++) { NZ[v] = 0; for (uint32_t r = inc[v]; r; r &= r - 1) NZ[v] |= ed[__builtin_ctz(r)]; }
        EZ[0] = 0; int bestv = -1000000, bestz = 0, bestsz = 0; long cnt = 0; int minsz = 99, mincsz = 99; uint32_t minz = 0, mincz = 0;
        for (uint32_t Z = 1; Z < (1u << n) - 1; Z++) {
            int lb = __builtin_ctz(Z); EZ[Z] = EZ[Z & (Z - 1)] | inc[lb];
            int sz = __builtin_popcount(Z), e = __builtin_popcount(EZ[Z]);
            if (3 * sz + 2 * e < 11) { /* value <= 3sz+2e-11*tau, tau>=1 when e>=1; if e=0 value=3sz>0?? handled below */ }
            int v = 3 * sz + 2 * e - 11 * tauF[EZ[Z]];
            if (v >= 0) { cnt++;
                if (sz < minsz) { minsz = sz; minz = Z; }
                if (sz < mincsz) { /* R-connected: z1 R z2 iff some edge at z1 meets some edge at z2 (then E_Z is connected as a hypergraph) */
                    uint32_t comp = Z & -Z, prev = 0; while (comp != prev) { prev = comp; for (uint32_t r = Z & ~comp; r; r &= r - 1) { int z = __builtin_ctz(r); for (uint32_t q = comp; q; q &= q - 1) if (NZ[z] & NZ[__builtin_ctz(q)]) { comp |= 1u << z; break; } } }
                if (comp == Z) { mincsz = sz; mincz = Z; } } }
            if (v > bestv || (v == bestv && sz < bestsz)) { bestv = v; bestz = Z; bestsz = sz; }
        }
        /* Z of size n-... : Z=(1<<n)-1 excluded (not proper) */
        uint32_t ez = EZ[bestz]; int tz = tauF[ez];
        /* a minimum transversal of E_Z */
        uint32_t T = 0, F = ez;
        while (F) { int e = __builtin_ctz(F); int bv = -1;
            for (uint32_t r = ed[e]; r; r &= r - 1) { int v = __builtin_ctz(r); if (tauF[F & ~inc[v]] == tauF[F] - 1) { bv = v; break; } }
            T |= 1u << bv; F &= ~inc[bv]; }
        printf("%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%x\t%x\t", n, m, tau, slack, maxdeg, bestv < 0, bestv, bestsz, __builtin_popcount(ez), tz, bestz, T);
        { int c2[40] = {0}; for (int v = 0; v < n; v++) c2[dg[v]]++; int first = 1; for (int d = 0; d < 40; d++) if (c2[d]) { printf(first ? "%d^%d" : ",%d^%d", d, c2[d]); first = 0; } }
        printf("\t%d\t%x\t%d\t%x", minsz, minz, mincsz, mincz);
        if (verbose) printf("\t%ld", cnt);
        printf("\t%s", line + 1);
    }
    return 0;
}
