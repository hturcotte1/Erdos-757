/* ref_g6filt.c -- referee (L014 round 3): filter genbg output (graph6, bipartite: first n1 vertices = hypergraph vertices,
   next n2 = edges, each of degree 3) for membership in C(n,m,t,D): linear (2 edges share <= 1 vertex), connected on all n
   vertices, max degree <= D, F7-free (explicit embedding), (P3) (Hall test, witness verified), tau == t (exact branching).
   usage: ref_g6filt n m t D < graph6 > survivors(graph6, unchanged lines)    ; counts to stderr */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int n, m, t, D;
static uint32_t E[64]; static int ne;
static int cover_le(uint32_t chosen, int k) {
    int i; for (i = 0; i < ne; i++) if (!(E[i] & chosen)) break;
    if (i == ne) return 1;
    if (k <= 0) return 0;
    for (uint32_t r = E[i]; r; r &= r - 1) { int v = __builtin_ctz(r); if (cover_le(chosen | (1u << v), k - 1)) return 1; }
    return 0;
}
static int tau_exact(void) { int k = 0; while (!cover_le(0, k)) k++; return k; }
static int is_edge(uint32_t x) { for (int i = 0; i < ne; i++) if (E[i] == x) return 1; return 0; }
static int has_f7(void) {
    for (int p = 0; p < n; p++) {
        int at[64], na = 0; for (int i = 0; i < ne; i++) if (E[i] >> p & 1) at[na++] = i;
        for (int i = 0; i < na; i++) for (int j = i + 1; j < na; j++) for (int k = j + 1; k < na; k++) {
            uint32_t r1 = E[at[i]] & ~(1u << p), r2 = E[at[j]] & ~(1u << p), r3 = E[at[k]] & ~(1u << p);
            if (__builtin_popcount(r1 | r2 | r3) != 6) continue;
            int a1 = __builtin_ctz(r1), b1 = 31 - __builtin_clz(r1), a2 = __builtin_ctz(r2), b2 = 31 - __builtin_clz(r2), a3 = __builtin_ctz(r3), b3 = 31 - __builtin_clz(r3);
            for (int s2 = 0; s2 < 2; s2++) for (int s3 = 0; s3 < 2; s3++) {
                int u2 = s2 ? b2 : a2, v2 = s2 ? a2 : b2, u3 = s3 ? b3 : a3, v3 = s3 ? a3 : b3;
                if (is_edge((1u << a1) | (1u << u2) | (1u << u3)) && is_edge((1u << b1) | (1u << v2) | (1u << v3))) return 1;
            }
        }
    }
    return 0;
}
static int owner[32]; static uint32_t forbidv, seenv;
static int augment(int e) {
    for (uint32_t r = E[e] & ~forbidv & ~seenv; r; r &= r - 1) { int v = __builtin_ctz(r); seenv |= 1u << v;
        if (owner[v] < 0 || augment(owner[v])) { owner[v] = e; return 1; } }
    return 0;
}
static int p3_ok(void) {
    for (int x = 0; x < n; x++) for (int y = x + 1; y < n; y++) {
        forbidv = (1u << x) | (1u << y); for (int v = 0; v < 32; v++) owner[v] = -1;
        for (int e = 0; e < ne; e++) { seenv = 0; if (!augment(e)) {
            uint32_t S = seenv | forbidv; int cnt = 0; for (int i = 0; i < ne; i++) if ((E[i] & S) == E[i]) cnt++;
            if (cnt < __builtin_popcount(S) - 1) { fprintf(stderr, "internal: violator\n"); exit(8); }
            return 0; } }
    }
    return 1;
}
int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: ref_g6filt n m t D\n"); return 1; }
    n = atoi(argv[1]); m = atoi(argv[2]); t = atoi(argv[3]); D = atoi(argv[4]);
    static char line[100000]; unsigned long long tot = 0, nonlin = 0, disc = 0, degbad = 0, f7 = 0, p3 = 0, wrongtau = 0, surv = 0, badfmt = 0;
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] == '>' || line[0] == '\n') continue;
        tot++;
        int N = line[0] - 63; if (N != n + m || line[0] < 63) { badfmt++; continue; }
        /* graph6: bits of upper triangle, column by column: for j in 1..N-1, for i in 0..j-1 */
        uint32_t adj[64] = {0}; int bit = 0; const char *p = line + 1; int bad = 0;
        for (int j = 1; j < N; j++) for (int i = 0; i < j; i++) {
            int ch = p[bit / 6]; if (ch < 63) { bad = 1; break; }
            int b = ((ch - 63) >> (5 - bit % 6)) & 1; bit++;
            if (b) { adj[i] |= 1u << j; adj[j] |= 1u << i; }
        }
        if (bad) { badfmt++; continue; }
        ne = 0; int ok = 1;
        for (int j = n; j < N; j++) { uint32_t row = adj[j] & ((1u << n) - 1); if (__builtin_popcount(row) != 3 || (adj[j] >> n)) { ok = 0; break; } E[ne++] = row; }
        if (!ok) { badfmt++; continue; }
        int lin = 1; for (int i = 0; i < ne && lin; i++) for (int j = i + 1; j < ne; j++) if (__builtin_popcount(E[i] & E[j]) >= 2) { lin = 0; break; }
        if (!lin) { nonlin++; continue; }
        int dmax = 0; for (int v = 0; v < n; v++) { int d = 0; for (int i = 0; i < ne; i++) d += E[i] >> v & 1; if (d > dmax) dmax = d; }
        if (dmax > D) { degbad++; continue; }
        uint32_t comp = 1u, prev = 0; while (comp != prev) { prev = comp; for (int i = 0; i < ne; i++) if (E[i] & comp) comp |= E[i]; }
        if (comp != (1u << n) - 1) { disc++; continue; }
        if (has_f7()) { f7++; continue; }
        if (!p3_ok()) { p3++; continue; }
        if (tau_exact() != t) { wrongtau++; continue; }
        surv++; fputs(line, stdout);
    }
    fprintf(stderr, "REF_G6FILT n=%d m=%d t=%d D=%d total=%llu badfmt=%llu nonlinear=%llu deg_gt_D=%llu disconnected=%llu F7=%llu P3_violated=%llu wrong_tau=%llu survivors=%llu\n", n, m, t, D, tot, badfmt, nonlin, degbad, disc, f7, p3, wrongtau, surv);
    return 0;
}
