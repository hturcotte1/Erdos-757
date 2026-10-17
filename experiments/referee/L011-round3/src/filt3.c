/* Referee L011 round 3: exact filter.  Usage: filt3 NP [notau] [surv] < lines.  Per graph prints
   "R: lin f7 f7L p3worst tau maxdeg ncomp sizes" and (with 'surv') "SURV: (edges)" for linear F7-free (P3) graphs.
   Summary: totals.  NP = number of points (all labels must be < NP; isolated points count as components). */
#include "common3.h"
int main(int argc, char **argv) {
    int NP = atoi(argv[1]), notau = 0, surv = 0, quiet = 0;
    for (int i = 2; i < argc; i++) { if (!strcmp(argv[i], "notau")) notau = 1; if (!strcmp(argv[i], "surv")) surv = 1; if (!strcmp(argv[i], "quiet")) quiet = 1; }
    static char line[1 << 16]; HG h; unsigned long long tot = 0, nlin = 0, nf7 = 0, nf7L = 0, disagree = 0, np3bad = 0, nf7free_p3bad = 0, ninC = 0, nconn = 0, ninCconn = 0;
    int taumin = 999, taumax = -1, mdmax = 0; unsigned long long tauhist[40] = {0};
    while (fgets(line, sizeof line, stdin)) {
        int m = hg_parse(line, &h, NP); if (m < 0) { if (m == -2) { fprintf(stderr, "label >= NP\n"); return 5; } continue; }
        tot++;
        int lin = hg_linear(&h), f7 = hg_has_f7(&h), f7L = lin ? hg_has_f7_lemmaF(&h) : -1, w = hg_p3_worst(&h), p3 = w >= 2;
        int t = notau ? -1 : hg_tau(&h), md = hg_maxdeg(&h), sz[32], nc = hg_components(&h, sz);
        nlin += lin; nf7 += f7; if (f7L == 1) nf7L++; if (lin && f7 != f7L) disagree++; np3bad += !p3; if (!f7 && !p3) nf7free_p3bad++;
        int inC = lin && !f7 && p3; ninC += inC; nconn += (nc == 1); ninCconn += inC && nc == 1;
        if (!notau) { if (t < taumin) taumin = t; if (t > taumax) taumax = t; if (t < 40) tauhist[t]++; } if (md > mdmax) mdmax = md;
        if (!quiet) { printf("R: lin=%d f7=%d f7L=%d p3worst=%d tau=%d maxdeg=%d ncomp=%d sizes=", lin, f7, f7L, w, t, md, nc); for (int i = 0; i < nc; i++) printf("%s%d", i ? "," : "", sz[i]); printf("\n"); }
        if (surv && inC) { printf("SURV:"); hg_print(stdout, &h); printf("\n"); }
    }
    printf("FSUM total=%llu linear=%llu F7=%llu F7_lemmaF=%llu F7_disagree=%llu P3bad=%llu F7free_P3bad=%llu inC=%llu connected=%llu inC_connected=%llu tau=[%d,%d] maxdeg_max=%d tauhist=",
           tot, nlin, nf7, nf7L, disagree, np3bad, nf7free_p3bad, ninC, nconn, ninCconn, taumin, taumax, mdmax);
    for (int t = 0; t < 40; t++) if (tauhist[t]) printf("%d:%llu ", t, tauhist[t]); printf("\n");
    return 0;
}
