/* anneal_c.c -- referee L009 round 2: heuristic falsification attempt for Theorem 3 (I11 on C for n <= 18), independent of the
   induction: simulated annealing over 3-graphs on n vertices that stay in C (linear; F7-free; |U(F)| >= |F|+2 for every non-empty
   edge set F, i.e. e(S) <= |S|-2), maximising f = 11 tau - 3n - 2m.  A state with f > 0 would be a counterexample.
   Usage: anneal_c n seconds seed.   Prints the best f found and the best state.  Heuristic only (no claim of completeness). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>
static int n, NE; static uint32_t E[64]; static uint64_t INC[32];
static uint64_t rs;
static uint64_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int cover_le(uint64_t left, int k) {
    if (!left) return 1;
    if (k <= 0) return 0;
    uint64_t l = left; uint32_t used = 0; int cnt = 0;
    while (l) { int i = __builtin_ctzll(l); l &= l - 1; if (!(E[i] & used)) { used |= E[i]; if (++cnt > k) return 0; } }
    int i = __builtin_ctzll(left); uint32_t e = E[i];
    while (e) { int x = __builtin_ctz(e); e &= e - 1; if (cover_le(left & ~INC[x], k - 1)) return 1; }
    return 0;
}
static void build(void) { for (int x = 0; x < n; x++) INC[x] = 0; for (int j = 0; j < NE; j++) for (int x = 0; x < n; x++) if (E[j] >> x & 1) INC[x] |= 1ull << j; }
static int tau(void) { build(); uint64_t all = NE ? ((1ull << NE) - 1) : 0; int k = 0; while (!cover_le(all, k)) k++; return k; }
static int has_f7(void) {
    build();
    for (int c = 0; c < n; c++) {
        uint64_t at = INC[c]; int idx[64], d = 0;
        while (at) { idx[d++] = __builtin_ctzll(at); at &= at - 1; }
        for (int a = 0; a < d; a++) for (int b = a + 1; b < d; b++) for (int q = b + 1; q < d; q++) {
            uint32_t p1 = E[idx[a]] & ~(1u << c), p2 = E[idx[b]] & ~(1u << c), p3 = E[idx[q]] & ~(1u << c);
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
/* (P3) for edge sets containing the last edge (the rest was valid before) */
static int p3_last_ok(void) {
    int k = NE - 1; uint32_t last = E[k];
    for (uint32_t F = 0; F < (1u << k); F++) {
        uint32_t U = last; for (uint32_t G = F; G; G &= G - 1) U |= E[__builtin_ctz(G)];
        if (__builtin_popcount(U) < __builtin_popcount(F) + 1 + 2) return 0;
    }
    return 1;
}
static int linear_last(void) { for (int j = 0; j < NE - 1; j++) if (__builtin_popcount(E[j] & E[NE - 1]) >= 2) return 0; return 1; }
int main(int argc, char **argv) {
    n = atoi(argv[1]); double secs = atof(argv[2]); rs = 88172645463325252ull ^ (uint64_t)atoll(argv[3]) * 2654435761ull;
    int bestf = -1000; uint32_t bestE[64]; int bestNE = 0;
    clock_t st = clock(); unsigned long long it = 0;
    NE = 0; int cur = -3 * n; double T = 2.0;
    while ((double)(clock() - st) / CLOCKS_PER_SEC < secs) {
        it++;
        if ((it & 1023) == 0) { double fr = (double)(clock() - st) / CLOCKS_PER_SEC / secs; T = 2.0 * (1 - fr) + 0.05; if (rnd() % 64 == 0) { NE = 0; cur = -3 * n; } }
        uint32_t save[64]; int sNE = NE; memcpy(save, E, sizeof(uint32_t) * NE);
        int mv = rnd() % 3;
        if (mv == 0 && NE > 0) { int j = rnd() % NE; E[j] = E[NE - 1]; NE--; }
        else if (mv == 1 && NE > 0) { int j = rnd() % NE; E[j] = E[NE - 1]; NE--; mv = 2; }
        if (mv == 2 || NE == 0 || mv == 1) {
            if (NE >= n - 2) { NE = sNE; memcpy(E, save, sizeof(uint32_t) * sNE); continue; }
            int a = rnd() % n, b = rnd() % n, c = rnd() % n; if (a == b || b == c || a == c) { NE = sNE; memcpy(E, save, sizeof(uint32_t) * sNE); continue; }
            E[NE++] = (1u << a) | (1u << b) | (1u << c);
            if (!linear_last() || !p3_last_ok() || has_f7()) { NE = sNE; memcpy(E, save, sizeof(uint32_t) * sNE); continue; }
        }
        int f = 11 * tau() - 3 * n - 2 * NE;
        if (f >= cur || exp((f - cur) / T) * 4294967296.0 > (double)(rnd() & 0xffffffffu)) {
            cur = f;
            if (f > bestf) { bestf = f; bestNE = NE; memcpy(bestE, E, sizeof(uint32_t) * NE); }
        } else { NE = sNE; memcpy(E, save, sizeof(uint32_t) * sNE); }
    }
    printf("ANNEAL n=%d iters=%llu best f=11tau-3n-2m=%d (slack %d) m=%d E:", n, it, bestf, -bestf, bestNE);
    for (int j = 0; j < bestNE; j++) { printf(" ("); int f1 = 1; for (int x = 0; x < n; x++) if (bestE[j] >> x & 1) { printf(f1 ? "%d" : ",%d", x); f1 = 0; } printf(")"); }
    printf("\n");
    return 0;
}
