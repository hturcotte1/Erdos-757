/* g6filt N1 N2 T < graph6 lines from genbg (first class = N1 hypergraph vertices, second class = N2 edges of size 3).
   Own tests: each edge-vertex has exactly 3 neighbours, linear, connected, max degree; counts graphs with tau == T, and those that are
   moreover F7-free and (P3) (= members of C(N1,N2,T,.)); prints a tau histogram and the FOUND lines of the members. */
#include "common.h"
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: g6filt N1 N2 T < g6\n"); return 1; }
    int N1 = atoi(argv[1]), N2 = atoi(argv[2]), T = atoi(argv[3]);
    char buf[4096]; u32 E[64]; long total = 0, bad = 0, nonlin = 0, disc = 0, tauT = 0, members = 0; long hist[40] = {0}; int maxd = 0;
    while (fgets(buf, sizeof buf, stdin)) {
        if (buf[0] == '>' || buf[0] == '\n') continue;
        int n = buf[0] - 63; if (n != N1 + N2) { bad++; continue; }
        total++;
        /* graph6: bits of the upper triangle, column by column: for j=1..n-1, i=0..j-1 */
        int bitpos = 0; const char *p = buf + 1;
        for (int j = 0; j < N2; j++) E[j] = 0;
        int degv[64] = {0};
        for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) {
            int ch = p[bitpos / 6] - 63; int bit = (ch >> (5 - bitpos % 6)) & 1; bitpos++;
            if (bit) { if (j >= N1 && i < N1) { E[j - N1] |= 1u << i; degv[j]++; } else if (i >= N1 || j >= N1) { } else { bad++; } }
        }
        int ok = 1; for (int j = 0; j < N2; j++) if (__builtin_popcount(E[j]) != 3) ok = 0;
        if (!ok) { bad++; continue; }
        if (!is_linear(N2, E)) { nonlin++; continue; }
        if (ncomponents(N1, N2, E) != 1) { disc++; continue; }
        int md = maxdeg(N1, N2, E); if (md > maxd) maxd = md;
        int t = tau_of(N2, E); if (t < 40) hist[t]++;
        if (t == T) { tauT++; if (!has_f7(N1, N2, E) && p3_ok(N1, N2, E)) { members++;
                printf("FOUND:"); for (int i = 0; i < N2; i++) { int v[3], k = 0; for (u32 r = E[i]; r; r &= r - 1) v[k++] = __builtin_ctz(r); printf(" (%d,%d,%d)", v[0], v[1], v[2]); } printf("\n"); } }
    }
    printf("g6filt N1=%d N2=%d T=%d: graphs=%ld bad=%ld nonlinear=%ld disconnected=%ld maxdeg=%d tau==T:%ld MEMBERS(tau==T,F7-free,P3)=%ld  tau histogram:", N1, N2, T, total, bad, nonlin, disc, maxd, tauT, members);
    for (int t = 0; t < 40; t++) if (hist[t]) printf(" %d:%ld", t, hist[t]); printf("\n");
    return 0;
}
