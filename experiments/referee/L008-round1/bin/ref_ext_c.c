/* ref_ext.c -- referee (L008 round 1) re-implementation of the extension step, written from scratch.
   Input lines "FOUND: (a,b,c) ..." (3-graph R or G).  Usage: ref_ext A|B < file
     A: input R on vertices 0..11 (10 edges); G = R + {12,13,14}.     B: input G on vertices 0..14 (11 edges).
   For every G: exact tau(G) (smallest k such that some k-subset of V(G) meets every edge; all subsets tried).
   Admissible pair {a,b}: a != b in V(G) = {0..14}, deg_G(a) <= 2, deg_G(b) <= 2, no edge of G contains both.
   Extension: every unordered triple of pairwise disjoint admissible pairs; H = G + {15,a_i,b_i} (i = 1..3).
   Hit: tau(H) >= 7, tested definitionally: no 6-subset of V(H) = {0..15} meets every edge of H (a superset of a transversal
   is a transversal and |V(H)| >= 6, so tau(H) <= 6 iff some 6-subset is a transversal).  The 6-subsets meeting every edge of G
   are precomputed once per G; then each extension checks the three new edges against that list.
   Output: "HIT: ..." lines (all 14 edges), and per-graph lines "GRAPH idx tauG ext hits"; final SUMMARY. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int E[32][3], ne; static uint32_t M[32];
static uint32_t six[8008]; static int nsix = 0;
static uint32_t T6[8008]; static int nT6;
static int tau_exact(uint32_t *ms, int k, int nv) {
    for (int t = 0; t <= nv; t++) {
        /* enumerate t-subsets of [nv] lexicographically by recursion-free Gosper */
        if (t == 0) { if (k == 0) return 0; continue; }
        uint32_t S = (1u << t) - 1;
        while (S < (1u << nv)) {
            int ok = 1; for (int i = 0; i < k; i++) if (!(ms[i] & S)) { ok = 0; break; }
            if (ok) return t;
            uint32_t c = S & -S, r = S + c; S = (((r ^ S) >> 2) / c) | r;
        }
    }
    return nv;
}
int main(int argc, char **argv) {
    char mode = argv[1][0]; static char line[1 << 16];
    for (uint32_t S = 0; S < (1u << 16); S++) if (__builtin_popcount(S) == 6) six[nsix++] = S;
    unsigned long long graphs = 0, ext = 0, hits = 0; int tauGmin = 99, tauGmax = -1, tauHmin = 99, tauHmax = -1;
    while (fgets(line, sizeof line, stdin)) {
        if (strncmp(line, "FOUND:", 6)) continue;
        ne = 0; char *p = line + 6;
        while ((p = strchr(p, '('))) { sscanf(p, "(%d,%d,%d)", &E[ne][0], &E[ne][1], &E[ne][2]); ne++; p++; }
        if (mode == 'A') { E[ne][0] = 12; E[ne][1] = 13; E[ne][2] = 14; ne++; }
        if (ne != 11) { fprintf(stderr, "expected 11 edges in G, got %d\n", ne); return 2; }
        int deg[16] = {0};
        for (int i = 0; i < ne; i++) { M[i] = 0; for (int k = 0; k < 3; k++) { if (E[i][k] < 0 || E[i][k] > 14) return 3; M[i] |= 1u << E[i][k]; deg[E[i][k]]++; } }
        for (int i = 0; i < ne; i++) { if (__builtin_popcount(M[i]) != 3) return 4; for (int j = i + 1; j < ne; j++) if (__builtin_popcount(M[i] & M[j]) >= 2) { fprintf(stderr, "nonlinear input\n"); return 5; } }
        for (int v = 0; v < 15; v++) if ((mode != 'C' && deg[v] == 0) || deg[v] > 3) { fprintf(stderr, "degree %d at %d\n", deg[v], v); return 6; }
        graphs++;
        int tG = tau_exact(M, ne, 15); if (tG < tauGmin) tauGmin = tG; if (tG > tauGmax) tauGmax = tG;
        nT6 = 0;
        for (int s = 0; s < nsix; s++) { int ok = 1; for (int i = 0; i < ne; i++) if (!(M[i] & six[s])) { ok = 0; break; } if (ok) T6[nT6++] = six[s]; }
        uint32_t pr[128]; int np = 0;
        for (int a = 0; a < 15; a++) for (int b = a + 1; b < 15; b++) {
            if (deg[a] > 2 || deg[b] > 2) continue;
            uint32_t q = (1u << a) | (1u << b); int ok = 1;
            for (int i = 0; i < ne; i++) if ((M[i] & q) == q) { ok = 0; break; }
            if (ok) pr[np++] = q;
        }
        unsigned long long gext = 0, ghits = 0;
        for (int x = 0; x < np; x++) for (int y = x + 1; y < np; y++) for (int z = y + 1; z < np; z++) {
            if ((pr[x] & pr[y]) || (pr[x] & pr[z]) || (pr[y] & pr[z])) continue;
            gext++;
            uint32_t n1 = pr[x] | (1u << 15), n2 = pr[y] | (1u << 15), n3 = pr[z] | (1u << 15);
            int covered = 0;
            for (int s = 0; s < nT6; s++) { uint32_t S = T6[s]; if ((S & n1) && (S & n2) && (S & n3)) { covered = 1; break; } }
            if (covered) continue;
            ghits++;
            uint32_t HM[14]; for (int i = 0; i < 11; i++) HM[i] = M[i]; HM[11] = n1; HM[12] = n2; HM[13] = n3;
            int tH = tau_exact(HM, 14, 16); if (tH < tauHmin) tauHmin = tH; if (tH > tauHmax) tauHmax = tH;
            printf("HIT:");
            for (int i = 0; i < 14; i++) { int f = 1; printf(" ("); for (int v = 0; v < 16; v++) if (HM[i] >> v & 1) { printf(f ? "%d" : ",%d", v); f = 0; } printf(")"); }
            printf("\n");
        }
        ext += gext; hits += ghits;
        printf("GRAPH %llu tauG=%d ext=%llu hits=%llu\n", graphs, tG, gext, ghits);
    }
    printf("SUMMARY mode=%c graphs=%llu tauG_range=[%d,%d] extensions=%llu hits=%llu tauH_of_hits=[%d,%d]\n", mode, graphs, tauGmin, tauGmax, ext, hits, tauHmin, tauHmax);
    return 0;
}
