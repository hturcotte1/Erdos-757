/* Referee L014 round 2: hypergraph lines -> graph6 of the vertex/edge incidence graph (vertex nodes 0..n-1, then edge nodes).
 * Accepts 'N M a b c ...', 'MEMBER ... : N M a b c ...' and 'FOUND: (a,b,c) (d,e,f) ...' (then N must be given as argv[1]).
 * Other lines are skipped (counted on stderr). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv) {
    int NFIX = argc > 1 ? atoi(argv[1]) : -1; static char line[1 << 16]; long nin = 0, nskip = 0;
    while (fgets(line, sizeof line, stdin)) {
        int n, m, ed[64][3], k; char *p = line;
        if (!strncmp(line, "FOUND:", 6)) {
            n = NFIX; m = 0; p = line + 6;
            while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &ed[m][0], &ed[m][1], &ed[m][2]) != 3) return 2; m++; p++; }
        } else {
            char *c = strchr(line, ':'); if (!strncmp(line, "MEMBER", 6) || !strncmp(line, "HIT", 3)) { if (!c) return 2; p = c + 1; }
            else if (!(line[0] >= '0' && line[0] <= '9')) { nskip++; continue; }
            if (sscanf(p, "%d %d%n", &n, &m, &k) != 2) return 2; p += k;
            for (int e = 0; e < m; e++) { int a, b, cc; if (sscanf(p, "%d %d %d%n", &a, &b, &cc, &k) != 3) return 2; p += k; ed[e][0] = a; ed[e][1] = b; ed[e][2] = cc; }
        }
        int N = n + m; if (N > 62) return 3;
        long nbits = (long)N * (N - 1) / 2; int nbytes = (int)((nbits + 5) / 6); unsigned char b[2048]; memset(b, 0, nbytes);
        for (int j = 0; j < m; j++) { long col = n + j, base = col * (col - 1) / 2;
            for (int s = 0; s < 3; s++) { int v = ed[j][s]; if (v < 0 || v >= n) return 4; long pos = base + v; b[pos / 6] |= 1 << (5 - pos % 6); } }
        putchar(N + 63); for (int i = 0; i < nbytes; i++) putchar(b[i] + 63); putchar('\n'); nin++;
    }
    fprintf(stderr, "hg2g6: %ld graphs, %ld lines skipped\n", nin, nskip);
    return 0;
}
