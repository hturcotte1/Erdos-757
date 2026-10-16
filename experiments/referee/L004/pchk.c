/* Referee L004: independent pattern checker (written from scratch; shares no code with e757/).
 * Input (stdin): one pattern per line: "i,j,k i,j,k ..." (any order, any whitespace); N given as argv[1].
 *   Optional leading tag token not containing ',' is copied to the output.
 * Output (stdout) per line:  <tag> sat lin k30 f7 alpha canon sym  <canonical-key>
 *   sat   = 1 iff exactly N-2 triples, i<j<k, every interior vertex 1..N-2 is the middle of exactly one triple
 *   lin   = 1 iff no two triples share two vertices
 *   k30   = 1 iff no triples (i,j,k),(a,b,c) with j<b, i>=a, k>=c   (monotone midpoints)
 *   f7    = 1 iff some 5 triples span exactly 7 vertices with degree multiset {3,2,2,2,2,2,2}
 *           (for a linear hypergraph this is exactly a copy of F7 = {012,034,056,135,246})
 *   alpha = independence number (largest vertex set containing no triple), by scanning all 2^N subsets
 *   canon = 1 iff sorted(P) <= sorted(refl P) lexicographically, refl: (i,j,k) -> (N-1-k, N-1-j, N-1-i)
 *   sym   = 1 iff P == refl P
 *   key   = min(sorted P, sorted refl P) printed as i,j,k;... (reflection-orbit key)
 *   and   own = sorted P printed the same way (exact labelled key)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXE 64
static int N;

static int cmp3(const void *a, const void *b) {
    const int *x = a, *y = b;
    for (int t = 0; t < 3; t++) if (x[t] != y[t]) return x[t] < y[t] ? -1 : 1;
    return 0;
}

static void put(int e[][3], int m, char *buf) {
    char *p = buf; *p = 0;
    for (int t = 0; t < m; t++) p += sprintf(p, "%s%d,%d,%d", t ? ";" : "", e[t][0], e[t][1], e[t][2]);
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: pchk N < patterns\n"); return 2; }
    N = atoi(argv[1]);
    static char line[8192];
    long long lines = 0;
    /* subsets of {0..N-1} grouped by popcount, for the alpha scan */
    int full = 1 << N;
    while (fgets(line, sizeof line, stdin)) {
        int e[MAXE][3], m = 0; char tag[256] = "-";
        char *tok = strtok(line, " \t\r\n");
        int first = 1;
        while (tok) {
            if (first && !strchr(tok, ',')) { snprintf(tag, sizeof tag, "%s", tok); }
            else {
                if (m >= MAXE) { fprintf(stderr, "too many edges\n"); return 3; }
                if (sscanf(tok, "%d,%d,%d", &e[m][0], &e[m][1], &e[m][2]) != 3) { fprintf(stderr, "bad token %s\n", tok); return 3; }
                m++;
            }
            first = 0;
            tok = strtok(NULL, " \t\r\n");
        }
        if (m == 0) continue;
        lines++;
        qsort(e, m, sizeof e[0], cmp3);
        /* sat */
        int sat = (m == N - 2), midcnt[64] = {0};
        for (int t = 0; t < m; t++) {
            if (!(0 <= e[t][0] && e[t][0] < e[t][1] && e[t][1] < e[t][2] && e[t][2] < N)) sat = 0;
            else midcnt[e[t][1]]++;
        }
        for (int v = 1; v <= N - 2; v++) if (midcnt[v] != 1) sat = 0;
        /* masks */
        uint32_t mk[MAXE];
        for (int t = 0; t < m; t++) mk[t] = (1u << e[t][0]) | (1u << e[t][1]) | (1u << e[t][2]);
        /* lin */
        int lin = 1;
        for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++) if (__builtin_popcount(mk[a] & mk[b]) >= 2) lin = 0;
        /* k30 */
        int k30 = 1;
        for (int a = 0; a < m; a++) for (int b = 0; b < m; b++) {
            if (a == b) continue;
            if (e[a][1] < e[b][1] && e[a][0] >= e[b][0] && e[a][2] >= e[b][2]) k30 = 0;
        }
        /* f7 via 5-subsets of edges */
        int f7 = 0;
        if (m >= 5) {
            int idx[5];
            for (idx[0] = 0; idx[0] < m && !f7; idx[0]++)
            for (idx[1] = idx[0] + 1; idx[1] < m && !f7; idx[1]++)
            for (idx[2] = idx[1] + 1; idx[2] < m && !f7; idx[2]++)
            for (idx[3] = idx[2] + 1; idx[3] < m && !f7; idx[3]++)
            for (idx[4] = idx[3] + 1; idx[4] < m && !f7; idx[4]++) {
                uint32_t U = 0; int deg[64] = {0};
                for (int t = 0; t < 5; t++) { U |= mk[idx[t]]; for (int s = 0; s < 3; s++) deg[e[idx[t]][s]]++; }
                if (__builtin_popcount(U) != 7) continue;
                int d3 = 0, d2 = 0;
                for (int v = 0; v < N; v++) { if (deg[v] == 3) d3++; else if (deg[v] == 2) d2++; }
                if (d3 == 1 && d2 == 6) f7 = 1;
            }
        }
        /* alpha by full subset scan: S independent iff no edge mask inside S */
        int alpha = 0;
        for (int S = 0; S < full; S++) {
            int pc = __builtin_popcount(S);
            if (pc <= alpha) continue;
            int ok = 1;
            for (int t = 0; t < m; t++) if ((mk[t] & (uint32_t)S) == mk[t]) { ok = 0; break; }
            if (ok) alpha = pc;
        }
        /* reflection */
        int r[MAXE][3];
        for (int t = 0; t < m; t++) { r[t][0] = N - 1 - e[t][2]; r[t][1] = N - 1 - e[t][1]; r[t][2] = N - 1 - e[t][0]; }
        qsort(r, m, sizeof r[0], cmp3);
        int c = 0;
        for (int t = 0; t < m && c == 0; t++) c = cmp3(e[t], r[t]);
        int canon = (c <= 0), sym = (c == 0);
        static char k1[8192], k2[8192];
        put(canon ? e : r, m, k1);
        put(e, m, k2);
        printf("%s %d %d %d %d %d %d %d %s %s\n", tag, sat, lin, k30, f7, alpha, canon, sym, k1, k2);
    }
    fprintf(stderr, "pchk: %lld patterns\n", lines);
    return 0;
}
