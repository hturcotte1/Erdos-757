/* Referee L011 round 3: canonical form of a 3-graph on N points (isolated points included) via nauty on the bipartite
   incidence graph (points | edges as two colour classes).  Input lines: "TAG: (a,b,c) ..." (any tag; optional trailing text)
   or numeric "m a1 b1 c1 ... am bm cm".  Output: "<canonical hex> <|Aut|> <lineno>".  Usage: canon3 N < file */
#include "nauty.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
int main(int argc, char **argv) {
    if (argc < 2) return 1;
    int N = atoi(argv[1]); static char line[1 << 16]; long ln = 0;
    graph g[MAXN], cg[MAXN]; int lab[MAXN], ptn[MAXN], orb[MAXN];
    DEFAULTOPTIONS_GRAPH(opt); statsblk st; opt.getcanon = TRUE; opt.defaultptn = FALSE;
    while (fgets(line, sizeof line, stdin)) {
        ln++; int ed[64][3], m = 0; char *p = line; while (*p == ' ') p++;
        if (*p >= '0' && *p <= '9') { int k = (int)strtol(p, &p, 10); for (int i = 0; i < k; i++) for (int j = 0; j < 3; j++) ed[i][j] = (int)strtol(p, &p, 10); m = k; }
        else { char *c = strchr(line, ':'); if (!c) continue; p = c + 1;
               while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &ed[m][0], &ed[m][1], &ed[m][2]) != 3) return 2; m++; p++; } }
        int n = N + m; if (n > MAXN) return 3;
        EMPTYGRAPH(g, 1, n);
        for (int i = 0; i < m; i++) for (int j = 0; j < 3; j++) { if (ed[i][j] < 0 || ed[i][j] >= N) { fprintf(stderr, "bad point at line %ld\n", ln); return 4; } ADDONEEDGE(g, ed[i][j], N + i, 1); }
        for (int i = 0; i < n; i++) { lab[i] = i; ptn[i] = 1; }
        ptn[N - 1] = 0; if (m) ptn[n - 1] = 0;
        densenauty(g, lab, ptn, orb, &opt, &st, 1, n, cg);
        for (int i = 0; i < n; i++) printf("%016llx", (unsigned long long)cg[i]);
        printf(" %.0f %ld\n", st.grpsize1 * pow(10.0, st.grpsize2), ln);
    }
    return 0;
}
