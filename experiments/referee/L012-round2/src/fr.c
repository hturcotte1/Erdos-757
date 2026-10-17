/* fr.c -- referee round 2 (L012): independent membership filter for C.
   Usage: fr NV [print] < lines ("TAG: (a,b,c) ..." or "m a b c ...").
   (P1) linear: any two edges share <= 1 vertex (and no repeated edge).
   (P2) F7-free: F7={012,034,056,135,246} has a unique degree-3 vertex; a copy = centre c, three edges {c,x_i,y_i} at c and two edges
        {z_1,z_2,z_3}, {z'_1,z'_2,z'_3} with {z_i,z'_i} = {x_i,y_i}.  Tested for every centre, every 3 edges at it, all 4 splittings.
   (P3) e(S) <= |S|-2 for all |S|>=2  <=>  for every vertex pair {x,y} the edges have a system of distinct representatives in
        V \ {x,y} (Hall).  Kuhn augmenting paths for every pair.
   Also: tau (exact, branching), connectivity on all NV vertices, max degree.
   Prints "SURV tau=.. conn=.. maxdeg=..: <line>" for members of C when 'print' is given; summary at the end. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n, m, ed[64][3], pe[64][64], deg[64], inc[64][16];
static unsigned long long em[64];
static int tau_rec(unsigned long long sel, int k, int best) {
    if (k >= best) return best;
    int e; for (e = 0; e < m; e++) if (!(sel & em[e])) break;
    if (e == m) return k;
    for (int t = 0; t < 3; t++) { int r = tau_rec(sel | (1ULL << ed[e][t]), k + 1, best); if (r < best) best = r; }
    return best;
}
static int is_edge(int a, int b, int c) { int e = pe[a][b]; if (e < 0) return 0; return ed[e][0] == c || ed[e][1] == c || ed[e][2] == c; }
static int has_f7(void) {
    for (int c = 0; c < n; c++) {
        int d = deg[c]; if (d < 3) continue;
        for (int i = 0; i < d; i++) for (int j = i + 1; j < d; j++) for (int k = j + 1; k < d; k++) {
            int E3[3] = { inc[c][i], inc[c][j], inc[c][k] }, X[3], Y[3];
            for (int q = 0; q < 3; q++) { int e = E3[q], t = 0; int o[2]; for (int r = 0; r < 3; r++) if (ed[e][r] != c) o[t++] = ed[e][r]; X[q] = o[0]; Y[q] = o[1]; }
            for (int s = 0; s < 4; s++) {   /* choice for edge 0 fixed to X[0] (the complement covers the other half) */
                int z1 = X[0], z2 = (s & 1) ? Y[1] : X[1], z3 = (s & 2) ? Y[2] : X[2];
                int w1 = Y[0], w2 = (s & 1) ? X[1] : Y[1], w3 = (s & 2) ? X[2] : Y[2];
                if (is_edge(z1, z2, z3) && is_edge(w1, w2, w3)) return 1;
            }
        }
    }
    return 0;
}
static int matchv[64], visv[64], bx, by, stamp;
static int aug(int e) {
    for (int t = 0; t < 3; t++) { int v = ed[e][t]; if (v == bx || v == by || visv[v] == stamp) continue; visv[v] = stamp;
        if (matchv[v] < 0 || aug(matchv[v])) { matchv[v] = e; return 1; } }
    return 0;
}
static int p3_ok(void) {
    for (bx = 0; bx < n; bx++) for (by = bx + 1; by < n; by++) {
        for (int v = 0; v < n; v++) matchv[v] = -1;
        for (int e = 0; e < m; e++) { stamp++; if (!aug(e)) return 0; }
    }
    return 1;
}
static int par[64]; static int fnd(int x) { while (par[x] != x) x = par[x] = par[par[x]]; return x; }
int main(int argc, char **argv) {
    if (argc < 2) return 1;
    n = atoi(argv[1]); int PRINT = argc > 2;
    static char line[1 << 16];
    long tot = 0, nonlin = 0, f7 = 0, p3 = 0, surv = 0, conn = 0; int tmin = 99, tmax = -1, dmin = 99, dmax = -1;
    while (fgets(line, sizeof line, stdin)) {
        m = 0;
        if (strchr(line, '(')) { char *p = line; while ((p = strchr(p, '('))) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) == 3) { ed[m][0] = a; ed[m][1] = b; ed[m][2] = c; m++; } p++; } }
        else { char *p = line; int k, mm; if (sscanf(p, "%d%n", &mm, &k) != 1) continue; p += k; for (int i = 0; i < mm; i++) { if (sscanf(p, "%d %d %d%n", &ed[i][0], &ed[i][1], &ed[i][2], &k) != 3) return 2; p += k; } m = mm; }
        if (m == 0) continue;
        tot++;
        for (int a = 0; a < n; a++) { deg[a] = 0; for (int b = 0; b < n; b++) pe[a][b] = -1; }
        int lin = 1;
        for (int e = 0; e < m && lin; e++) {
            em[e] = 0;
            for (int t = 0; t < 3; t++) { int v = ed[e][t]; if (v < 0 || v >= n) { fprintf(stderr, "label\n"); return 3; } em[e] |= 1ULL << v; }
            if (__builtin_popcountll(em[e]) != 3) { lin = 0; break; }
            for (int s = 0; s < 3; s++) for (int t = 0; t < 3; t++) if (s != t) { int a = ed[e][s], b = ed[e][t]; if (pe[a][b] >= 0) lin = 0; pe[a][b] = e; }
            for (int t = 0; t < 3; t++) { int v = ed[e][t]; if (deg[v] >= 16) { fprintf(stderr, "deg\n"); return 3; } inc[v][deg[v]++] = e; }
        }
        if (!lin) { nonlin++; continue; }
        if (has_f7()) { f7++; continue; }
        if (!p3_ok()) { p3++; continue; }
        surv++;
        int tau = tau_rec(0, 0, 64);
        for (int v = 0; v < n; v++) par[v] = v;
        for (int e = 0; e < m; e++) { int a = fnd(ed[e][0]), b = fnd(ed[e][1]), c = fnd(ed[e][2]); par[a] = b; par[fnd(c)] = fnd(b); }
        int comps = 0; for (int v = 0; v < n; v++) if (fnd(v) == v) comps++;
        int md = 0; for (int v = 0; v < n; v++) if (deg[v] > md) md = deg[v];
        if (comps == 1) conn++;
        if (tau < tmin) tmin = tau; if (tau > tmax) tmax = tau; if (md < dmin) dmin = md; if (md > dmax) dmax = md;
        if (PRINT) { line[strcspn(line, "\n")] = 0; printf("SURV tau=%d conn=%d maxdeg=%d: %s\n", tau, comps == 1, md, line); }
    }
    printf("FRSUMMARY total=%ld nonlinear=%ld F7=%ld P3violated=%ld survivors=%ld connected=%ld tau=[%d,%d] maxdeg=[%d,%d]\n", tot, nonlin, f7, p3, surv, conn, tmin, tmax, dmin, dmax);
    return 0;
}
