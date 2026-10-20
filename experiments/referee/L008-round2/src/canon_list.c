/* canon_list.c -- referee round 2 (L008): canonical key of every 3-graph in a file of lines "TAG: (a,b,c) (d,e,f) ...".
   Vertex set = {0..NV-1} with NV given on the command line (isolated vertices allowed), or max label + 1 if NV = 0.
   Canonical form: nauty densenauty on the vertex/edge incidence graph, colour classes kept apart; key = sorted list of
   canonically relabelled edges (same construction as in bfs_enum.c).  Prints "<hex key> <|Aut|>" per graph.
   Usage: canon_list TAG NV < file */
#include "nauty.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
int main(int argc, char **argv) {
    const char *tag = argc > 1 ? argv[1] : "FOUND"; int NVfix = argc > 2 ? atoi(argv[2]) : 0;
    char line[8192]; size_t tl = strlen(tag);
    static DEFAULTOPTIONS_GRAPH(options); statsblk stats;
    options.getcanon = TRUE; options.defaultptn = FALSE;
    while (fgets(line, sizeof line, stdin)) {
        if (strncmp(line, tag, tl) || line[tl] != ':') continue;
        int ed[40][3], ne = 0, mx = -1; char *p = line + tl + 1;
        while ((p = strchr(p, '('))) {
            int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) != 3) return 2;
            ed[ne][0] = a; ed[ne][1] = b; ed[ne][2] = c; ne++;
            if (a > mx) mx = a; if (b > mx) mx = b; if (c > mx) mx = c; p++;
        }
        int nv = NVfix ? NVfix : mx + 1, n = nv + ne, m = SETWORDSNEEDED(n);
        if (n > MAXN || nv > 16) { fprintf(stderr, "too big\n"); return 3; }
        graph G[MAXN], cg[MAXN]; int lab[MAXN], ptn[MAXN], orb[MAXN];
        EMPTYGRAPH(G, m, n);
        for (int j = 0; j < ne; j++) for (int t = 0; t < 3; t++) ADDONEEDGE(G, ed[j][t], nv + j, m);
        for (int i = 0; i < n; i++) { lab[i] = i; ptn[i] = 1; }
        ptn[nv - 1] = 0; ptn[n - 1] = 0;
        densenauty(G, lab, ptn, orb, &options, &stats, m, n, cg);
        int cl[MAXN]; for (int i = 0; i < nv; i++) cl[lab[i]] = i;
        int tr[40];
        for (int j = 0; j < ne; j++) {
            int x[3] = { cl[ed[j][0]], cl[ed[j][1]], cl[ed[j][2]] };
            for (int u = 0; u < 3; u++) for (int v = u + 1; v < 3; v++) if (x[u] > x[v]) { int t = x[u]; x[u] = x[v]; x[v] = t; }
            tr[j] = (x[0] << 8) | (x[1] << 4) | x[2];
        }
        for (int i = 1; i < ne; i++) { int x = tr[i], j = i - 1; while (j >= 0 && tr[j] > x) { tr[j + 1] = tr[j]; j--; } tr[j + 1] = x; }
        double aut = stats.grpsize1; for (int e = 0; e < stats.grpsize2; e++) aut *= 10.0;
        printf("%02d:%02d:", nv, ne); for (int j = 0; j < ne; j++) printf("%03x", tr[j]); printf(" %.0f\n", aut);
    }
    return 0;
}
