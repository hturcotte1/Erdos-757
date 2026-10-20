/* canon.c -- referee L010 round 3 (written from scratch).  Canonical form of 3-uniform hypergraphs via nauty (densenauty) on the
   incidence bipartite graph with the vertex class and the edge class as separate colours.  Usage: canon NV < lines
   Each input line is either "TAG: (a,b,c) (d,e,f) ... [anything]" or "m a1 b1 c1 ... am bm cm" (prover format); other lines are skipped.
   NV = number of hypergraph vertices (labels 0..NV-1; isolated vertices allowed).  Output: one line per graph: the canonical edge list
   (sorted triples of canonical labels), which is equal for two inputs iff they are isomorphic as hypergraphs on NV labelled-free vertices. */
#define MAXN 64
#include "nauty.h"
#include <string.h>
#include <ctype.h>
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: canon NV < lines\n"); return 1; }
    int nv = atoi(argv[1]);
    static char line[1 << 16];
    DYNALLSTAT(graph, g, g_sz); DYNALLSTAT(graph, cg, cg_sz); DYNALLSTAT(int, lab, lab_sz); DYNALLSTAT(int, ptn, ptn_sz); DYNALLSTAT(int, orb, orb_sz);
    static DEFAULTOPTIONS_GRAPH(options); statsblk stats;
    options.getcanon = TRUE; options.defaultptn = FALSE;
    while (fgets(line, sizeof line, stdin)) {
        int ed[64][3], ne = 0;
        if (strchr(line, '(')) {
            char *p = line; while ((p = strchr(p, '('))) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) == 3) { ed[ne][0] = a; ed[ne][1] = b; ed[ne][2] = c; ne++; } p++; }
        } else {
            int m; char *p = line; int k; if (sscanf(p, "%d%n", &m, &k) != 1) continue; p += k;
            for (int i = 0; i < m; i++) { if (sscanf(p, "%d %d %d%n", &ed[i][0], &ed[i][1], &ed[i][2], &k) != 3) { m = -1; break; } p += k; } if (m < 0) continue; ne = m;
        }
        if (ne == 0 && !strchr(line, '(') ) continue;
        int n = nv + ne, m1 = SETWORDSNEEDED(n);
        nauty_check(WORDSIZE, m1, n, NAUTYVERSIONID);
        DYNALLOC2(graph, g, g_sz, m1, n, "m"); DYNALLOC2(graph, cg, cg_sz, m1, n, "m");
        DYNALLOC1(int, lab, lab_sz, n, "m"); DYNALLOC1(int, ptn, ptn_sz, n, "m"); DYNALLOC1(int, orb, orb_sz, n, "m");
        EMPTYGRAPH(g, m1, n);
        for (int j = 0; j < ne; j++) for (int c = 0; c < 3; c++) { int v = ed[j][c]; if (v < 0 || v >= nv) { fprintf(stderr, "label out of range\n"); return 2; } ADDONEEDGE(g, v, nv + j, m1); }
        for (int i = 0; i < n; i++) { lab[i] = i; ptn[i] = 1; } ptn[nv - 1] = 0; ptn[n - 1] = 0;   /* colour classes: vertices | edges */
        densenauty(g, lab, ptn, orb, &options, &stats, m1, n, cg);
        /* canonical edge list: for each edge-vertex of cg (positions nv..n-1), its neighbours < nv */
        int tri[64][3], cnt = 0;
        for (int j = nv; j < n; j++) { int c = 0; for (int v = 0; v < nv; v++) if (ISELEMENT(GRAPHROW(cg, j, m1), v)) { if (c < 3) tri[cnt][c] = v; c++; } if (c != 3) { fprintf(stderr, "bad edge\n"); return 3; } cnt++; }
        /* sort triples lexicographically (each already ascending) */
        for (int a = 0; a < cnt; a++) for (int b = a + 1; b < cnt; b++) { int lt = tri[b][0] < tri[a][0] || (tri[b][0] == tri[a][0] && (tri[b][1] < tri[a][1] || (tri[b][1] == tri[a][1] && tri[b][2] < tri[a][2])));
            if (lt) { int t[3]; memcpy(t, tri[a], sizeof t); memcpy(tri[a], tri[b], sizeof t); memcpy(tri[b], t, sizeof t); } }
        printf("n%d", nv); for (int a = 0; a < cnt; a++) printf(" %d.%d.%d", tri[a][0], tri[a][1], tri[a][2]); printf("\n");
    }
    return 0;
}
