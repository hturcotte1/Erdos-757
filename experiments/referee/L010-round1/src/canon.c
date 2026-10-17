/* canon.c -- referee L010 round 1.  Canonical form of 3-graphs (hypergraph isomorphism classes) with nauty densenauty on
   the vertex-edge incidence graph, colour classes kept apart (vertices first, edges second).
   Input lines: either "TAG: (a,b,c) (d,e,f) ..." (lines without '(' are skipped) or "m a1 b1 c1 ... " (mode -n).
   Number of vertices: max label + 1 (or argv NV if given > 0).
   Output per graph: "<nv>_<ne>_<hex rows of the canonical incidence graph>" on its own line. */
#include "nauty.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
int main(int argc, char **argv) {
    int numeric = (argc > 1 && strcmp(argv[1], "-n") == 0);
    int NVfix = (argc > 2) ? atoi(argv[2]) : 0;
    static char line[1 << 16];
    DYNALLSTAT(graph, g, g_sz); DYNALLSTAT(graph, cg, cg_sz);
    int lab[128], ptn[128], orbits[128];
    static DEFAULTOPTIONS_GRAPH(options); statsblk stats;
    options.getcanon = TRUE; options.defaultptn = FALSE;
    while (fgets(line, sizeof line, stdin)) {
        int ed[64][3], ne = 0, nv = 0;
        if (numeric) {
            char *p = line; int m, k; if (sscanf(p, "%d%n", &m, &k) != 1) continue; p += k;
            for (int i = 0; i < m; i++) for (int j = 0; j < 3; j++) { sscanf(p, "%d%n", &ed[i][j], &k); p += k; }
            ne = m;
        } else {
            char *p = strchr(line, '('); if (!p) continue;
            while (p && *p == '(') {
                if (sscanf(p, "(%d,%d,%d)", &ed[ne][0], &ed[ne][1], &ed[ne][2]) != 3) { fprintf(stderr, "parse\n"); return 2; }
                ne++; p = strchr(p, ')'); p++; while (*p == ' ') p++;
            }
        }
        for (int i = 0; i < ne; i++) for (int j = 0; j < 3; j++) if (ed[i][j] + 1 > nv) nv = ed[i][j] + 1;
        if (NVfix > 0) { if (nv > NVfix) { fprintf(stderr, "nv\n"); return 3; } nv = NVfix; }
        int n = nv + ne, m = SETWORDSNEEDED(n);
        nauty_check(WORDSIZE, m, n, NAUTYVERSIONID);
        DYNALLOC2(graph, g, g_sz, m, n, "g"); DYNALLOC2(graph, cg, cg_sz, m, n, "cg");
        EMPTYGRAPH(g, m, n);
        for (int i = 0; i < ne; i++) for (int j = 0; j < 3; j++) ADDONEEDGE(g, ed[i][j], nv + i, m);
        for (int i = 0; i < n; i++) { lab[i] = i; ptn[i] = 1; }
        ptn[nv - 1] = 0; ptn[n - 1] = 0;
        densenauty(g, lab, ptn, orbits, &options, &stats, m, n, cg);
        printf("%d_%d_", nv, ne);
        for (int i = 0; i < n; i++) { set *row = GRAPHROW(cg, i, m); for (int w = 0; w < m; w++) printf("%016llx", (unsigned long long)row[w]); }
        printf(" %.0f\n", stats.grpsize1 * pow(10.0, stats.grpsize2));
    }
    return 0;
}
