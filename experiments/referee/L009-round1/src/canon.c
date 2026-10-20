/* Referee L009: canonical form of 3-graphs via nauty (incidence graph, colour classes vertices | edges).
   Usage: canon N < file   reads every line containing ':' followed by groups "(a,b,c)"; N = number of vertices (labels 0..N-1;
   all lines must use labels < N).  Prints one line per input: "<canonical hex string> <line number> <|Aut|>". */
#include "nauty.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: canon N\n"); return 1; }
    int N = atoi(argv[1]);
    static char line[1 << 16];
    long ln = 0;
    DYNALLSTAT(graph, g, g_sz); DYNALLSTAT(graph, cg, cg_sz);
    DYNALLSTAT(int, lab, lab_sz); DYNALLSTAT(int, ptn, ptn_sz); DYNALLSTAT(int, orbits, orbits_sz);
    static DEFAULTOPTIONS_GRAPH(options); statsblk stats;
    options.getcanon = TRUE; options.defaultptn = FALSE;
    while (fgets(line, sizeof line, stdin)) {
        ln++;
        char *p = strchr(line, ':'); if (!p) continue;
        int E[64][3], M = 0;
        while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &E[M][0], &E[M][1], &E[M][2]) != 3) { fprintf(stderr, "parse %ld\n", ln); return 2; } M++; p++; }
        int n = N + M, m = SETWORDSNEEDED(n);
        nauty_check(WORDSIZE, m, n, NAUTYVERSIONID);
        DYNALLOC2(graph, g, g_sz, m, n, "a"); DYNALLOC2(graph, cg, cg_sz, m, n, "a");
        DYNALLOC1(int, lab, lab_sz, n, "a"); DYNALLOC1(int, ptn, ptn_sz, n, "a"); DYNALLOC1(int, orbits, orbits_sz, n, "a");
        EMPTYGRAPH(g, m, n);
        for (int j = 0; j < M; j++) for (int k = 0; k < 3; k++) {
            if (E[j][k] < 0 || E[j][k] >= N) { fprintf(stderr, "label out of range line %ld\n", ln); return 3; }
            ADDONEEDGE(g, E[j][k], N + j, m);
        }
        for (int i = 0; i < n; i++) { lab[i] = i; ptn[i] = 1; }
        ptn[N - 1] = 0; ptn[n - 1] = 0;
        densenauty(g, lab, ptn, orbits, &options, &stats, m, n, cg);
        printf("%d_%d_", N, M);
        for (int i = 0; i < n; i++) { set *r = GRAPHROW(cg, i, m); for (int w = 0; w < m; w++) printf("%016llx", (unsigned long long)r[w]); }
        printf(" %ld %.0f\n", ln, stats.grpsize1 * (stats.grpsize2 ? 1e1 : 1.0)); if (stats.grpsize2) { fprintf(stderr, "large group line %ld\n", ln); }
    }
    return 0;
}
