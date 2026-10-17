/* ref_filter.c -- referee (L008 round 1) definitional filters, written from scratch.
   For each line "TAG: (a,b,c) ...":
     linear     : no two edges share >= 2 vertices;
     F7         : DEFINITIONAL subgraph test: for every 5-set of edges whose union has exactly 7 vertices, try all 7! bijections
                  phi from {0..6} to that union and test whether phi maps the 5 edges of F7 = {012,034,056,135,246} onto edges of
                  the hypergraph (5 distinct images inside the chosen 5 edges <=> equality);
     P3         : for EVERY vertex subset S with |S| >= 2 (all 2^nv subsets), e(S) <= |S|-2 (e(S) = number of edges inside S);
     tau        : exact, smallest k with a k-subset meeting all edges;  maxdeg; connectivity (primal graph on used vertices).
   Prints summary and one "SURVIVOR:" line for each linear, F7-free, P3-satisfying hypergraph.  Usage: ref_filter TAG [nv] < file
   (nv = number of vertices; default = 1 + largest label). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int E[64][3], ne, nv; static uint32_t M[64];
static const int F7[5][3] = {{0,1,2},{0,3,4},{0,5,6},{1,3,5},{2,4,6}};
static int perm[7], used7[7], verts[7], cand[5]; static uint32_t candM[5]; static int found;
static void tryperm(int k) {
    if (found) return;
    if (k == 7) {
        for (int f = 0; f < 5; f++) {
            uint32_t img = (1u << verts[perm[F7[f][0]]]) | (1u << verts[perm[F7[f][1]]]) | (1u << verts[perm[F7[f][2]]]);
            int ok = 0; for (int c = 0; c < 5; c++) if (candM[c] == img) { ok = 1; break; }
            if (!ok) return;
        }
        found = 1; return;
    }
    for (int i = 0; i < 7; i++) if (!used7[i]) { used7[i] = 1; perm[k] = i; tryperm(k + 1); used7[i] = 0; if (found) return; }
}
static int has_f7(void) {
    int c[5];
    for (c[0] = 0; c[0] < ne; c[0]++) for (c[1] = c[0] + 1; c[1] < ne; c[1]++) for (c[2] = c[1] + 1; c[2] < ne; c[2]++)
    for (c[3] = c[2] + 1; c[3] < ne; c[3]++) for (c[4] = c[3] + 1; c[4] < ne; c[4]++) {
        uint32_t U = 0; for (int k = 0; k < 5; k++) U |= M[c[k]];
        if (__builtin_popcount(U) != 7) continue;
        int t = 0; for (int v = 0; v < 32; v++) if (U >> v & 1) verts[t++] = v;
        for (int k = 0; k < 5; k++) candM[k] = M[c[k]];
        found = 0; memset(used7, 0, sizeof used7); tryperm(0);
        if (found) return 1;
    }
    return 0;
}
static int p3_ok(int *worstS) {
    int worst = 1000;
    for (uint32_t S = 0; S < (1u << nv); S++) {
        int s = __builtin_popcount(S); if (s < 2) continue;
        int e = 0; for (int i = 0; i < ne; i++) if ((M[i] & S) == M[i]) e++;
        if (e > 0 && s - e < worst) worst = s - e;     /* only sets containing an edge can violate (|S|>=2 => |S|-2 >= 0) */
    }
    *worstS = worst; return worst >= 2;
}
static int tau_exact(void) {
    for (int t = 1; t <= nv; t++) {
        uint32_t S = (1u << t) - 1;
        while (S < (1u << nv)) { int ok = 1; for (int i = 0; i < ne; i++) if (!(M[i] & S)) { ok = 0; break; } if (ok) return t;
            uint32_t c = S & -S, r = S + c; S = (((r ^ S) >> 2) / c) | r; }
    }
    return nv;
}
static int connected(void) {
    uint32_t used = 0; for (int i = 0; i < ne; i++) used |= M[i];
    uint32_t comp = M[0], prev = 0; while (comp != prev) { prev = comp; for (int i = 0; i < ne; i++) if (M[i] & comp) comp |= M[i]; }
    return comp == used;
}
int main(int argc, char **argv) {
    const char *tag = argv[1]; size_t tl = strlen(tag); int NVfix = argc > 2 ? atoi(argv[2]) : 0;
    static char line[1 << 16];
    unsigned long long tot = 0, lin = 0, f7 = 0, p3bad = 0, f7free_p3bad = 0, surv = 0, conn = 0; int tmin = 99, tmax = -1, dmax = 0, wmin = 99, wmax = -99;
    while (fgets(line, sizeof line, stdin)) {
        if (strncmp(line, tag, tl) || line[tl] != ':') continue;
        ne = 0; nv = 0; char *p = line + tl + 1;
        while ((p = strchr(p, '('))) { sscanf(p, "(%d,%d,%d)", &E[ne][0], &E[ne][1], &E[ne][2]); M[ne] = (1u << E[ne][0]) | (1u << E[ne][1]) | (1u << E[ne][2]);
            for (int k = 0; k < 3; k++) if (E[ne][k] + 1 > nv) nv = E[ne][k] + 1; ne++; p++; }
        if (NVfix) nv = NVfix;
        tot++;
        int L = 1; for (int i = 0; i < ne; i++) for (int j = i + 1; j < ne; j++) if (__builtin_popcount(M[i] & M[j]) >= 2) L = 0;
        lin += L;
        int F = has_f7(); f7 += F;
        int w; int P = p3_ok(&w); p3bad += !P; if (!F && !P) f7free_p3bad++;
        if (w < wmin) wmin = w; if (w > wmax) wmax = w;
        int t = tau_exact(); if (t < tmin) tmin = t; if (t > tmax) tmax = t;
        int deg[32] = {0}; for (int i = 0; i < ne; i++) for (int k = 0; k < 3; k++) deg[E[i][k]]++;
        for (int v = 0; v < 32; v++) if (deg[v] > dmax) dmax = deg[v];
        conn += connected();
        if (getenv("VERBOSE")) printf("FLAGS lin=%d f7=%d p3=%d tau=%d minSlack=%d\n", L, F, P, t, w);
        if (L && !F && P) { surv++; printf("SURVIVOR:%s", line + tl + 1); }
    }
    printf("SUMMARY tag=%s total=%llu linear=%llu contain_F7=%llu P3_violated=%llu F7free_and_P3_violated=%llu survivors=%llu connected=%llu tau=[%d,%d] maxdeg=%d min(|S|-e(S))=[%d,%d]\n",
           tag, tot, lin, f7, p3bad, f7free_p3bad, surv, conn, tmin, tmax, dmax, wmin, wmax);
    return 0;
}
