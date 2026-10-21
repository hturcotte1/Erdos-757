/* refcheck N M T D < list : checks every FOUND line of a cell list: labels < N, M edges, 3 distinct vertices each, distinct edges,
   linear, F7-free, (P3), connected on N vertices, max degree <= D, tau == T exactly. Prints a count summary. */
#include "common.h"
int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: refcheck N M T D < list\n"); return 1; }
    int N = atoi(argv[1]), M = atoi(argv[2]), T = atoi(argv[3]), D = atoi(argv[4]);
    char buf[8192]; u32 E[64]; long lines = 0, found = 0, ok = 0;
    long bad_label = 0, bad_m = 0, bad_dup = 0, bad_lin = 0, bad_f7 = 0, bad_p3 = 0, bad_conn = 0, bad_deg = 0, bad_tau = 0;
    while (fgets(buf, sizeof buf, stdin)) {
        lines++; if (strncmp(buf, "FOUND", 5) != 0) continue; found++;
        int ml; int m = parse_line(buf, E, &ml); int good = 1;
        if (m < 0 || ml >= N) { bad_label++; good = 0; }
        if (m != M) { bad_m++; good = 0; }
        for (int i = 0; good && i < m; i++) for (int j = i + 1; j < m; j++) if (E[i] == E[j]) { bad_dup++; good = 0; break; }
        if (good && !is_linear(m, E)) { bad_lin++; good = 0; }
        if (good && has_f7(N, m, E)) { bad_f7++; good = 0; }
        if (good && !p3_ok(N, m, E)) { bad_p3++; good = 0; }
        if (good && ncomponents(N, m, E) != 1) { bad_conn++; good = 0; }
        if (good && maxdeg(N, m, E) > D) { bad_deg++; good = 0; }
        if (good && tau_of(m, E) != T) { bad_tau++; good = 0; }
        if (good) ok++;
    }
    printf("refcheck N=%d M=%d T=%d D=%d: lines=%ld FOUND=%ld ok=%ld bad_label=%ld bad_m=%ld bad_dup=%ld bad_linear=%ld bad_F7=%ld bad_P3=%ld bad_conn=%ld bad_deg=%ld bad_tau=%ld %s\n",
           N, M, T, D, lines, found, ok, bad_label, bad_m, bad_dup, bad_lin, bad_f7, bad_p3, bad_conn, bad_deg, bad_tau, ok == found ? "ALL-OK" : "FAILURES");
    return ok == found ? 0 : 1;
}
