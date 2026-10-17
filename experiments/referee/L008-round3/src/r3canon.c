/* r3canon.c -- referee L008 round 3: canonical form and |Aut| of a 3-graph (lines "TAG: (a,b,c) ..."), via nauty's densenauty
   on the vertex/edge incidence graph with the colour classes {vertices} | {edges} fixed.  Colour-preserving automorphisms of the
   incidence graph correspond bijectively to vertex permutations preserving the edge set (edges are distinct vertex sets).
   Usage: r3canon TAG NV < file   ->  per graph one line: "<canonical string> <|Aut|>". */
#include "nauty.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
int main(int argc, char **argv) {
    const char *tag = argv[1]; int NV = atoi(argv[2]); size_t tl = strlen(tag);
    static char line[1 << 16];
    DYNALLSTAT(graph, g, g_sz); DYNALLSTAT(graph, cg, cg_sz); DYNALLSTAT(int, lab, lab_sz); DYNALLSTAT(int, ptn, ptn_sz); DYNALLSTAT(int, orb, orb_sz);
    static DEFAULTOPTIONS_GRAPH(opt); statsblk st; opt.getcanon = TRUE; opt.defaultptn = FALSE;
    while (fgets(line, sizeof line, stdin)) {
        if (strncmp(line, tag, tl) || line[tl] != ':') continue;
        int ed[64][3], ne = 0; char *p = line + tl + 1;
        while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &ed[ne][0], &ed[ne][1], &ed[ne][2]) != 3) { fprintf(stderr, "parse error\n"); return 2; } ne++; p++; }
        int n = NV + ne, m = SETWORDSNEEDED(n);
        nauty_check(WORDSIZE, m, n, NAUTYVERSIONID);
        DYNALLOC2(graph, g, g_sz, m, n, "g"); DYNALLOC2(graph, cg, cg_sz, m, n, "cg");
        DYNALLOC1(int, lab, lab_sz, n, "lab"); DYNALLOC1(int, ptn, ptn_sz, n, "ptn"); DYNALLOC1(int, orb, orb_sz, n, "orb");
        EMPTYGRAPH(g, m, n);
        for (int j = 0; j < ne; j++) for (int k = 0; k < 3; k++) { if (ed[j][k] < 0 || ed[j][k] >= NV) { fprintf(stderr, "vertex range\n"); return 3; } ADDONEEDGE(g, ed[j][k], NV + j, m); }
        for (int i = 0; i < n; i++) { lab[i] = i; ptn[i] = 1; } ptn[NV-1] = 0; ptn[n-1] = 0;
        densenauty(g, lab, ptn, orb, &opt, &st, m, n, cg);
        printf("c%d_%d_", NV, ne);
        for (int i = 0; i < n; i++) for (int w = 0; w < m; w++) printf("%llx.", (unsigned long long)cg[(size_t)i*m + w]);
        if (st.grpsize2 != 0) { fprintf(stderr, "group too large\n"); return 4; }
        printf(" %.0f\n", st.grpsize1);
    }
    return 0;
}
