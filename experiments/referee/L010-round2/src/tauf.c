/* tauf.c -- referee L010 r2: per line "TAG: (a,b,c) ..." print exact tau (branching) and F7 flag (method B). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static uint32_t E[64]; static int ne, NV = 32;
static int cov(uint64_t left, int k) { if (!left) return 1; if (k <= 0) return 0; int i = __builtin_ctzll(left); uint32_t e = E[i];
    while (e) { int v = __builtin_ctz(e); e &= e - 1; uint64_t l2 = left; for (int j = i; j < ne; j++) if ((l2 >> j & 1) && (E[j] >> v & 1)) l2 &= ~(1ull << j); if (cov(l2, k - 1)) return 1; } return 0; }
static int f7(void) { for (int i = 0; i < ne; i++) for (int j = i + 1; j < ne; j++) { if (E[i] & E[j]) continue; uint32_t U = E[i] | E[j];
    for (int p = 0; p < NV; p++) { if (U >> p & 1) continue; int c = 0; for (int t = 0; t < ne; t++) if ((E[t] >> p & 1) && __builtin_popcount(E[t] & E[i]) == 1 && __builtin_popcount(E[t] & E[j]) == 1) c++; if (c >= 3) return 1; } } return 0; }
int main(void) { static char line[1 << 16]; long hist[40][2]; memset(hist, 0, sizeof hist);
    while (fgets(line, sizeof line, stdin)) { char *bar = strchr(line, '|'); if (bar) *bar = 0; ne = 0; char *p = line;
        while ((p = strchr(p, '('))) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) != 3) return 2; E[ne++] = (1u << a) | (1u << b) | (1u << c); p++; }
        if (!ne) continue; int t = 0; while (!cov((1ull << ne) - 1, t)) t++; hist[t][f7()]++; }
    for (int t = 0; t < 40; t++) if (hist[t][0] || hist[t][1]) printf("tau=%d: F7-free %ld, with F7 %ld\n", t, hist[t][0], hist[t][1]);
    return 0; }
