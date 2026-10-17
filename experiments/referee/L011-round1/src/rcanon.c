/* Referee L011: canonical form of a 3-graph with nauty (bipartite incidence graph, colour classes points | hyperedges kept
   apart, so the canonical form is a complete isomorphism invariant of the 3-graph on N points, isolated points included).
   Usage: rcanon N [TAG] < file
     each input line is either "TAG: (a,b,c) (d,e,f) ..." (lines with another tag are skipped; TAG '*' = any tag) or the
     numeric format "m a1 b1 c1 ... am bm cm"; points must be < N.
   Output per graph: "<canonical hex string> <|Aut| as double> <line number>". */
#include "nauty.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage\n"); return 1; }
    int N = atoi(argv[1]); const char *tag = argc > 2 ? argv[2] : "*";
    static char line[1 << 16]; long ln = 0;
    graph g[MAXN], cg[MAXN]; int lab[MAXN], ptn[MAXN], orb[MAXN];
    DEFAULTOPTIONS_GRAPH(opt); statsblk st; opt.getcanon = TRUE; opt.defaultptn = FALSE;
    while (fgets(line, sizeof line, stdin)) {
        ln++;
        int ed[64][3], m = 0; char *p = line;
        while (*p == ' ') p++;
        if (*p >= '0' && *p <= '9') {
            int k = (int)strtol(p, &p, 10);
            for (int i = 0; i < k; i++) for (int j = 0; j < 3; j++) ed[i][j] = (int)strtol(p, &p, 10);
            m = k;
        } else {
            char *c = strchr(line, ':'); if (!c) continue;
            if (strcmp(tag, "*") && (strncmp(line, tag, strlen(tag)) || line[strlen(tag)] != ':')) continue;
            p = c + 1;
            while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &ed[m][0], &ed[m][1], &ed[m][2]) != 3) return 2; m++; p++; }
        }
        int n = N + m; if (n > MAXN) { fprintf(stderr, "too big\n"); return 3; }
        EMPTYGRAPH(g, 1, n);
        for (int i = 0; i < m; i++) for (int j = 0; j < 3; j++) {
            if (ed[i][j] < 0 || ed[i][j] >= N) { fprintf(stderr, "bad point line %ld\n", ln); return 4; }
            ADDONEEDGE(g, ed[i][j], N + i, 1);
        }
        for (int i = 0; i < n; i++) { lab[i] = i; ptn[i] = 1; }
        ptn[N - 1] = 0; if (m) ptn[n - 1] = 0;
        densenauty(g, lab, ptn, orb, &opt, &st, 1, n, cg);
        for (int i = 0; i < n; i++) printf("%016llx", (unsigned long long)cg[i]);
        printf(" %.0f %ld\n", st.grpsize1 * pow(10.0, st.grpsize2), ln);
    }
    return 0;
}
