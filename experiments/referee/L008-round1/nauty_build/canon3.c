/* canon3.c -- referee (L008 round 1): canonical form of 3-graphs via nauty (densenauty on the vertex-edge incidence graph with
   the partition {vertices | edges}; colour-preserving isomorphisms of the incidence graph = isomorphisms of the 3-graph, because
   no edge is repeated).  Input: lines "TAG: (a,b,c) (d,e,f) ..." ; usage: canon3 TAG NV  (NV = number of vertices, 0..NV-1).
   Output per graph: "<canonical hex string> <|Aut|> <line number>". */
#include "nauty.h"
#include <string.h>
#include <stdlib.h>
int main(int argc, char **argv) {
    const char *tag = argv[1]; int NV = atoi(argv[2]); size_t tl = strlen(tag);
    static char line[1 << 16]; long ln = 0;
    DYNALLSTAT(graph, g, g_sz); DYNALLSTAT(graph, cg, cg_sz); DYNALLSTAT(int, lab, lab_sz); DYNALLSTAT(int, ptn, ptn_sz); DYNALLSTAT(int, orbits, orbits_sz);
    static DEFAULTOPTIONS_GRAPH(options); statsblk stats;
    options.getcanon = TRUE; options.defaultptn = FALSE;
    while (fgets(line, sizeof line, stdin)) {
        ln++;
        if (strncmp(line, tag, tl) || line[tl] != ':') continue;
        int ed[64][3], ne = 0; char *p = line + tl + 1;
        while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &ed[ne][0], &ed[ne][1], &ed[ne][2]) != 3) { fprintf(stderr, "parse\n"); return 2; } ne++; p++; }
        int n = NV + ne, m = SETWORDSNEEDED(n);
        nauty_check(WORDSIZE, m, n, NAUTYVERSIONID);
        DYNALLOC2(graph, g, g_sz, m, n, "malloc"); DYNALLOC2(graph, cg, cg_sz, m, n, "malloc");
        DYNALLOC1(int, lab, lab_sz, n, "malloc"); DYNALLOC1(int, ptn, ptn_sz, n, "malloc"); DYNALLOC1(int, orbits, orbits_sz, n, "malloc");
        EMPTYGRAPH(g, m, n);
        for (int j = 0; j < ne; j++) for (int k = 0; k < 3; k++) {
            int v = ed[j][k]; if (v < 0 || v >= NV) { fprintf(stderr, "vertex out of range line %ld\n", ln); return 3; }
            ADDONEEDGE(g, v, NV + j, m);
        }
        for (int i = 0; i < n; i++) { lab[i] = i; ptn[i] = 1; }
        ptn[NV - 1] = 0; ptn[n - 1] = 0;
        densenauty(g, lab, ptn, orbits, &options, &stats, m, n, cg);
        printf("%d:%d:", NV, ne);
        for (int i = 0; i < n; i++) for (int w = 0; w < m; w++) printf("%llx.", (unsigned long long)cg[(size_t)i * m + w]);
        printf(" %.0f %ld\n", stats.grpsize1 * 1.0 * (stats.grpsize2 ? 1 : 1), ln);
        if (stats.grpsize2 != 0) { fprintf(stderr, "large group\n"); return 4; }
    }
    return 0;
}
