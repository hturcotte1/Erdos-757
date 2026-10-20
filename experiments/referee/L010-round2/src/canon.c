/* canon.c -- referee L010 round 2.  Canonical form and automorphism-group order of 3-graphs given as lines containing
   "(a,b,c) (d,e,f) ..." (any prefix tag; text after '|' ignored) or, with -n, lines "m a b c d e f ...".
   Usage: canon NV [-n] < file   (NV = number of hypergraph vertices, so isolated vertices count).
   Builds the incidence bigraph (NV vertex nodes, then one node per edge) with the 2-cell partition {vertices | edges} and
   runs densenauty with getcanon.  Output per input line: "<hex of canonical rows> <|Aut|>".  Two 3-graphs without repeated
   edges are isomorphic iff their incidence bigraphs are isomorphic preserving the two classes iff the hex strings agree. */
#include "nauty.h"
#include <string.h>
int main(int argc, char **argv) {
    int NV = atoi(argv[1]); int numfmt = (argc > 2 && !strcmp(argv[2], "-n"));
    static char line[1 << 16];
    DYNALLSTAT(graph, g, g_sz); DYNALLSTAT(graph, cg, cg_sz);
    DYNALLSTAT(int, lab, lab_sz); DYNALLSTAT(int, ptn, ptn_sz); DYNALLSTAT(int, orb, orb_sz);
    static DEFAULTOPTIONS_GRAPH(opt); statsblk st;
    opt.getcanon = TRUE; opt.defaultptn = FALSE;
    while (fgets(line, sizeof line, stdin)) {
        int ed[64][3], me = 0;
        char *bar = strchr(line, '|'); if (bar) *bar = 0;
        if (numfmt) { char *p = line; int k, used; if (sscanf(p, "%d%n", &k, &used) != 1) continue; p += used;
            for (int i = 0; i < k; i++) { int a, b, c; if (sscanf(p, "%d %d %d%n", &a, &b, &c, &used) != 3) return 2; p += used; ed[me][0] = a; ed[me][1] = b; ed[me][2] = c; me++; } }
        else { char *p = line; while ((p = strchr(p, '('))) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) != 3) return 2; ed[me][0] = a; ed[me][1] = b; ed[me][2] = c; me++; p++; } }
        if (me == 0) continue;
        int n = NV + me, m = SETWORDSNEEDED(n);
        nauty_check(WORDSIZE, m, n, NAUTYVERSIONID);
        DYNALLOC2(graph, g, g_sz, m, n, "c"); DYNALLOC2(graph, cg, cg_sz, m, n, "c");
        DYNALLOC1(int, lab, lab_sz, n, "c"); DYNALLOC1(int, ptn, ptn_sz, n, "c"); DYNALLOC1(int, orb, orb_sz, n, "c");
        EMPTYGRAPH(g, m, n);
        for (int j = 0; j < me; j++) for (int t = 0; t < 3; t++) { if (ed[j][t] >= NV || ed[j][t] < 0) return 3; ADDONEEDGE(g, ed[j][t], NV + j, m); }
        for (int i = 0; i < n; i++) { lab[i] = i; ptn[i] = 1; }
        ptn[NV - 1] = 0; ptn[n - 1] = 0;
        densenauty(g, lab, ptn, orb, &opt, &st, m, n, cg);
        for (int i = 0; i < n; i++) { set *r = GRAPHROW(cg, i, m); for (int w = 0; w < m; w++) printf("%016llx", (unsigned long long)r[w]); }
        printf(" %.0f\n", st.grpsize1 * pow(10.0, st.grpsize2));
    }
    return 0;
}
