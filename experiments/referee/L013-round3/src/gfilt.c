/* gfilt n m t D < graph6-bipartite-list : genbg output (first class = n points, second class = m edge-vertices of degree 3).
   Decodes graph6, builds the 3-graph, and keeps the graphs that are linear, connected on all n vertices, max degree <= D,
   F7-free, P3, tau == t. Prints FOUND lines of survivors and a SUMMARY. */
#include "hyp.h"
int main(int argc, char **argv) { if (argc < 5) { fprintf(stderr, "usage: gfilt n m t D\n"); return 2; }
    int n = atoi(argv[1]), m = atoi(argv[2]), t = atoi(argv[3]), D = atoi(argv[4]); int swap = (argc > 5 && !strcmp(argv[5], "swap")); char line[65536]; hyp h;
    /* swap: first class = m edge-vertices (indices 0..m-1), second class = n points (indices m..m+n-1) */
    long total = 0, c_uni = 0, c_lin = 0, c_conn = 0, c_deg = 0, c_tau = 0, c_f7 = 0, c_p3 = 0, surv = 0, bad = 0;
    while (fgets(line, sizeof line, stdin)) { if (line[0] == '\n' || line[0] == '>') continue; total++;
        int N = line[0] - 63; if (N != n + m) { bad++; fprintf(stderr, "N mismatch %d\n", N); continue; }
        /* decode upper triangle, column by column */
        int deg2[64] = {0}; int nb[64][4]; int pos = 1, bit = 5; unsigned char ch = line[pos] - 63; int ok = 1;
        for (int j = 1; j < N && ok; j++) for (int i = 0; i < j && ok; i++) { int b = (ch >> bit) & 1; if (bit == 0) { bit = 5; pos++; ch = line[pos] - 63; } else bit--;
            if (b) { int ei, pt; if (!swap) { if (i < n && j >= n) { ei = j; pt = i; } else { ok = 0; continue; } } else { if (i < m && j >= m) { ei = i; pt = j - m; } else { ok = 0; continue; } }
                if (deg2[ei] < 4) nb[ei][deg2[ei]] = pt; deg2[ei]++; } }
        if (!ok) { bad++; continue; }
        h.n = n; h.m = m; int uni = 1; for (int q = 0; q < m; q++) { int ei = swap ? q : n + q; if (deg2[ei] != 3) uni = 0; else { h.e[q][0] = nb[ei][0]; h.e[q][1] = nb[ei][1]; h.e[q][2] = nb[ei][2]; } }
        if (!uni) continue; c_uni++; hyp_finish(&h);
        if (!hyp_linear(&h)) continue; c_lin++;
        if (!hyp_connected(&h)) continue; c_conn++;
        if (hyp_maxdeg(&h) > D) continue; c_deg++;
        if (!hyp_tau_ge(&h, t)) continue; if (hyp_tau(&h) != t) continue; c_tau++;
        if (hyp_has_F7(&h)) continue; c_f7++;
        if (!hyp_P3(&h)) continue; c_p3++;
        surv++; print_found(stdout, &h); }
    printf("SUMMARY gfilt(%d,%d,%d,%d): read=%ld bad=%ld uniform=%ld linear=%ld connected=%ld deg_ok=%ld tau_exact=%ld F7free=%ld P3=%ld survivors=%ld\n", n, m, t, D, total, bad, c_uni, c_lin, c_conn, c_deg, c_tau, c_f7, c_p3, surv);
    return 0; }
