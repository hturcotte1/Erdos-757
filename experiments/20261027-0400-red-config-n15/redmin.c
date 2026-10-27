/* redmin.c -- exact (Red) test, streaming summary version of ../20261027-0230-red-config/redfree.c.
   Usage: redmin N hitsfile minsz_out_threshold < canon-lines ("C m a.b.c ...")   (all graphs on N vertices)
   For each graph: tau (min transversal), slack = 3n+2m-11tau, and the smallest |Z| (Z proper nonempty vertex set) with
   value(Z) = 3|Z| + 2 e(Z) - 11 tau(E_Z) >= 0, where E_Z = edges meeting Z.  Z is scanned by increasing size (Gosper), stops at the first
   size with a Red set (exact: minsz = min |Z| over all (Red) Z; none => (Red)-free, minsz=0 recorded as 99).
   Graphs with minsz >= threshold (or Red-free) are appended to hitsfile as "n m tau slack minsz Zmask graph".
   Summary on stdout (one line per cell, fields: cls redfree maxminsz minslack maxslack, then hist minsz x slack as "ms:sl:count"). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int n, m; static uint32_t ed[40], inc[32];
static uint8_t *tauF;
static long hist[100][80]; /* [minsz][slack+8] ; slack range -8..71 */
int main(int argc, char **argv) {
    n = atoi(argv[1]); FILE *hf = fopen(argv[2], "a"); int thr = atoi(argv[3]);
    static char line[1 << 14];
    long cls = 0, redfree = 0; int maxms = 0, minsl = 1000, maxsl = -1000;
    tauF = malloc(1 << 20);
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] != 'C') continue;
        char *p = line + 1; int k; if (sscanf(p, "%d%n", &m, &k) != 1) continue; p += k;
        memset(inc, 0, sizeof inc);
        for (int i = 0; i < m; i++) { int a, b, c; if (sscanf(p, " %d.%d.%d%n", &a, &b, &c, &k) != 3) return 2; p += k;
            ed[i] = (1u << a) | (1u << b) | (1u << c); inc[a] |= 1u << i; inc[b] |= 1u << i; inc[c] |= 1u << i; }
        uint32_t NF = 1u << m;
        tauF[0] = 0;
        for (uint32_t F = 1; F < NF; F++) {
            int e = __builtin_ctz(F), best = 99;
            for (uint32_t r = ed[e]; r; r &= r - 1) { int v = __builtin_ctz(r); int t = 1 + tauF[F & ~inc[v]]; if (t < best) best = t; }
            tauF[F] = best;
        }
        int tau = tauF[NF - 1];
        int slack = 3 * n + 2 * m - 11 * tau;
        int ms = 99; uint32_t zf = 0;
        for (int sz = 1; sz < n && ms == 99; sz++) {
            uint32_t Z = (1u << sz) - 1, lim = 1u << n;
            while (Z < lim) {
                uint32_t E = 0; for (uint32_t r = Z; r; r &= r - 1) E |= inc[__builtin_ctz(r)];
                if (3 * sz + 2 * __builtin_popcount(E) - 11 * tauF[E] >= 0) { ms = sz; zf = Z; break; }
                uint32_t c = Z & -Z, r2 = Z + c; Z = (((r2 ^ Z) >> 2) / c) | r2;
            }
        }
        cls++; if (ms == 99) redfree++;
        if (ms != 99 && ms > maxms) maxms = ms;
        if (slack < minsl) minsl = slack; if (slack > maxsl) maxsl = slack;
        int sli = slack + 8; if (sli < 0) sli = 0; if (sli > 79) sli = 79;
        hist[ms][sli]++;
        if (ms >= thr) { fprintf(hf, "%d\t%d\t%d\t%d\t%d\t%x\t%s", n, m, tau, slack, ms, zf, line + 1); }
    }
    fclose(hf);
    printf("cls=%ld redfree=%ld maxminsz=%d minslack=%d maxslack=%d hist=", cls, redfree, maxms, minsl, maxsl);
    for (int a = 0; a < 100; a++) for (int b = 0; b < 80; b++) if (hist[a][b]) printf("%d:%d:%ld,", a, b - 8, hist[a][b]);
    printf("\n");
    return 0;
}
