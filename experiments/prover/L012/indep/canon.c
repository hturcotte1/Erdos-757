/* canon.c (prover, certificate L012) -- canonical form of 3-uniform hypergraphs with nauty 2.8.8 (densenauty), applied to the
   incidence bipartite graph (NV hypergraph vertices, then one vertex per edge), with the two classes as separate colour cells.
   Two inputs get the same output iff they are isomorphic as hypergraphs on NV vertices (vertices in no edge allowed).
   Usage: canon NV < lines.  Input lines: "m a1 b1 c1 ... " (edge-list format) or "TAG: (a,b,c) (d,e,f) ..." ; other lines skipped.
   Output: one line per input graph: "C <m> <canonical edges as a.b.c sorted>" (written in input order). */
#define MAXN 64
#include "nauty.h"
#include <string.h>
static int cmp3(const void *x, const void *y) { const int *a = x, *b = y; for (int i = 0; i < 3; i++) if (a[i] != b[i]) return a[i] - b[i]; return 0; }
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: canon NV < lines\n"); return 1; }
    int nv = atoi(argv[1]);
    static char line[1 << 16];
    graph g[MAXN * MAXM], cg[MAXN * MAXM]; int lab[MAXN], ptn[MAXN], orb[MAXN];
    static DEFAULTOPTIONS_GRAPH(options); statsblk stats;
    options.getcanon = TRUE; options.defaultptn = FALSE;
    long cnt = 0;
    while (fgets(line, sizeof line, stdin)) {
        int ed[40][3], ne = 0, ok = 1;
        if (strchr(line, '(')) {
            char *p = line;
            while ((p = strchr(p, '('))) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) == 3) { ed[ne][0] = a; ed[ne][1] = b; ed[ne][2] = c; ne++; } p++; }
        } else {
            char *p = line; int k, m;
            if (sscanf(p, "%d%n", &m, &k) != 1) continue;
            p += k;
            for (int i = 0; i < m; i++) { if (sscanf(p, "%d %d %d%n", &ed[i][0], &ed[i][1], &ed[i][2], &k) != 3) { ok = 0; break; } p += k; }
            if (!ok) { fprintf(stderr, "bad line\n"); return 2; }
            ne = m;
        }
        int n = nv + ne, m1 = SETWORDSNEEDED(n);
        if (n > MAXN) { fprintf(stderr, "too large\n"); return 3; }
        EMPTYGRAPH(g, m1, n);
        for (int j = 0; j < ne; j++) for (int c = 0; c < 3; c++) {
            int v = ed[j][c]; if (v < 0 || v >= nv) { fprintf(stderr, "label out of range\n"); return 4; }
            ADDONEEDGE(g, v, nv + j, m1);
        }
        for (int i = 0; i < n; i++) { lab[i] = i; ptn[i] = 1; }
        ptn[nv - 1] = 0; if (ne > 0) ptn[n - 1] = 0;
        densenauty(g, lab, ptn, orb, &options, &stats, m1, n, cg);
        int tri[40][3], t = 0;
        for (int j = nv; j < n; j++) {
            int c = 0; set *row = GRAPHROW(cg, j, m1);
            for (int v = 0; v < nv; v++) if (ISELEMENT(row, v)) { if (c < 3) tri[t][c] = v; c++; }
            if (c != 3) { fprintf(stderr, "edge of size %d\n", c); return 5; }
            t++;
        }
        qsort(tri, t, sizeof tri[0], cmp3);
        printf("C %d", t); for (int a = 0; a < t; a++) printf(" %d.%d.%d", tri[a][0], tri[a][1], tri[a][2]); printf("\n");
        cnt++;
    }
    fprintf(stderr, "canon: %ld graphs\n", cnt);
    return 0;
}
