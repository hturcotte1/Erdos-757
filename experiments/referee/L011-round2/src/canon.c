/* Referee L011 round 2: canonical form of 3-graphs (nauty densenauty on the point/edge incidence graph, partition
   [points | edges]).  Usage: canon N < lines.  A line is either "TAG: (a,b,c) (d,e,f) ..." or "m a1 b1 c1 a2 ...".
   Output per line: "<m> <hex rows of canonical graph> <|Aut|>" (|Aut| as a double; colour-preserving automorphisms). */
#include "nauty.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
int main(int argc, char **argv) {
    int N = atoi(argv[1]);
    static char line[1 << 20];
    DYNALLSTAT(graph, g, g_sz); DYNALLSTAT(graph, cg, cg_sz);
    DYNALLSTAT(int, lab, lab_sz); DYNALLSTAT(int, ptn, ptn_sz); DYNALLSTAT(int, orb, orb_sz);
    static DEFAULTOPTIONS_GRAPH(options); statsblk stats;
    options.getcanon = TRUE; options.defaultptn = FALSE;
    while (fgets(line, sizeof line, stdin)) {
        int ed[200][3], m = 0;
        if (strchr(line, '(')) {
            char *p = line;
            while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &ed[m][0], &ed[m][1], &ed[m][2]) != 3) { fprintf(stderr, "parse\n"); return 1; } m++; p++; }
        } else {
            char *p = line; int k, cnt = 0, vals[700];
            while (*p) { while (*p && !isdigit((unsigned char)*p) && *p != '-') p++; if (!*p) break; vals[cnt++] = (int)strtol(p, &p, 10); }
            if (cnt == 0) continue;
            m = vals[0]; if (cnt != 1 + 3 * m) { fprintf(stderr, "bad count %d m=%d\n", cnt, m); return 1; }
            for (k = 0; k < m; k++) { ed[k][0] = vals[1 + 3*k]; ed[k][1] = vals[2 + 3*k]; ed[k][2] = vals[3 + 3*k]; }
        }
        int n = N + m, mw = SETWORDSNEEDED(n);
        if (n > WORDSIZE) { fprintf(stderr, "too big\n"); return 1; }
        nauty_check(WORDSIZE, mw, n, NAUTYVERSIONID);
        DYNALLOC2(graph, g, g_sz, mw, n, "g"); DYNALLOC2(graph, cg, cg_sz, mw, n, "cg");
        DYNALLOC1(int, lab, lab_sz, n, "l"); DYNALLOC1(int, ptn, ptn_sz, n, "p"); DYNALLOC1(int, orb, orb_sz, n, "o");
        EMPTYGRAPH(g, mw, n);
        for (int j = 0; j < m; j++) for (int t = 0; t < 3; t++) {
            int v = ed[j][t]; if (v < 0 || v >= N) { fprintf(stderr, "vertex out of range\n"); return 1; }
            ADDONEEDGE(g, v, N + j, mw);
        }
        for (int i = 0; i < n; i++) { lab[i] = i; ptn[i] = 1; }
        ptn[N - 1] = 0; ptn[n - 1] = 0;
        densenauty(g, lab, ptn, orb, &options, &stats, mw, n, cg);
        printf("%d ", m);
        for (int i = 0; i < n; i++) printf("%016llx", (unsigned long long)cg[i]);
        printf(" %.0f\n", stats.grpsize1 * pow(10.0, stats.grpsize2));
    }
    return 0;
}
