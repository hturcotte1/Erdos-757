/* verify_cells n m t D < cellfile : re-verify every FOUND line: valid labels, exactly m edges, linear, connected on all n vertices,
   max degree <= D, F7-free, P3, tau == t. Prints counts; exit 1 if any line fails. */
#include "hyp.h"
int main(int argc, char **argv) { if (argc < 5) { fprintf(stderr, "usage\n"); return 2; }
    int n = atoi(argv[1]), m = atoi(argv[2]), t = atoi(argv[3]), D = atoi(argv[4]); char line[8192]; hyp h; int total = 0, bad = 0;
    int c_lin = 0, c_conn = 0, c_deg = 0, c_f7 = 0, c_p3 = 0, c_tau = 0;
    while (fgets(line, sizeof line, stdin)) { if (strncmp(line, "FOUND:", 6)) continue; total++;
        if (!parse_found(line, &h, n) || h.m != m || !hyp_valid(&h)) { bad++; fprintf(stderr, "BAD PARSE/VALID: %s", line); continue; }
        int lin = hyp_linear(&h), conn = hyp_connected(&h), deg = hyp_maxdeg(&h) <= D, f7 = !hyp_has_F7(&h), p3 = hyp_P3(&h), tau = hyp_tau(&h) == t;
        c_lin += lin; c_conn += conn; c_deg += deg; c_f7 += f7; c_p3 += p3; c_tau += tau;
        if (!(lin && conn && deg && f7 && p3 && tau)) { bad++; fprintf(stderr, "FAIL lin=%d conn=%d deg=%d f7free=%d p3=%d tau=%d(%d): %s", lin, conn, deg, f7, p3, hyp_tau(&h), t, line); } }
    printf("VERIFY cell(%d,%d,%d,%d): lines=%d linear=%d connected=%d degok=%d F7free=%d P3=%d tau_exact=%d bad=%d\n", n, m, t, D, total, c_lin, c_conn, c_deg, c_f7, c_p3, c_tau, bad);
    return bad ? 1 : 0; }
