/* Referee L011 round 3: one-vertex extension step, independent implementation.
   Usage: ext3 NG TG MAXDEG [print] < inputs (numeric "m a b c ..." or "TAG: (a,b,c) ..."; points 0..NG-1).
   For each G: tau(G) is recomputed exactly and must equal TG (else counted bad_tau and skipped).  New point w = NG; new edges
   {w,a_i,b_i} (i=1,2,3) for every unordered triple of pairwise disjoint pairs with deg_G(a_i), deg_G(b_i) <= MAXDEG-1 and no pair
   inside an edge of G.  tau(H) >= TG+1 is decided DIRECTLY on H by branch and bound (no use of G's transversals).  Every hit is
   classified: linear, F7 (generic embedding), (P3) worst value, connectivity over all NG+1 points. */
#include "common3.h"
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage\n"); return 1; }
    int NG = atoi(argv[1]), TG = atoi(argv[2]), MD = atoi(argv[3]), pr = argc > 4;
    static char line[1 << 16]; HG g, h;
    unsigned long long graphs = 0, bad = 0, tested = 0, hits = 0, hf7 = 0, hp3 = 0, hinC = 0, hconn = 0, hinCconn = 0, hnonlin = 0; int w = NG;
    while (fgets(line, sizeof line, stdin)) {
        int m = hg_parse(line, &g, NG); if (m < 0) { if (m == -2) { fprintf(stderr, "label >= NG\n"); return 5; } continue; }
        graphs++;
        if (hg_tau(&g) != TG) { bad++; continue; }
        int deg[32]; for (int x = 0; x < NG; x++) deg[x] = __builtin_popcountll(g.INC[x]);
        uint32_t pr_[512]; int np = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > MD - 1 || deg[b] > MD - 1) continue;
            uint32_t p = (1u << a) | (1u << b); int inside = 0;
            for (int i = 0; i < m; i++) if ((g.E[i] & p) == p) { inside = 1; break; }
            if (!inside) pr_[np++] = p;
        }
        h = g; h.ne = m + 3; h.np = NG + 1;
        for (int x = 0; x < np; x++) for (int y = x + 1; y < np; y++) { if (pr_[x] & pr_[y]) continue;
            for (int z = y + 1; z < np; z++) { if ((pr_[x] | pr_[y]) & pr_[z]) continue;
                tested++;
                h.E[m] = pr_[x] | (1u << w); h.E[m + 1] = pr_[y] | (1u << w); h.E[m + 2] = pr_[z] | (1u << w);
                hg_build(&h, NG + 1);
                if (hg_cov(&h, hg_all(&h), TG)) continue;      /* tau(H) <= TG */
                hits++;
                int lin = hg_linear(&h), f7 = hg_has_f7(&h), wst = hg_p3_worst(&h), sz[32], nc = hg_components(&h, sz);
                int inC = lin && !f7 && wst >= 2;
                if (!lin) hnonlin++; if (f7) hf7++; else if (wst < 2) hp3++; if (inC) hinC++; if (nc == 1) hconn++; if (inC && nc == 1) hinCconn++;
                if (pr) { printf("HIT:"); hg_print(stdout, &h); printf(" | lin=%d f7=%d p3worst=%d ncomp=%d sizes=", lin, f7, wst, nc); for (int i = 0; i < nc; i++) printf("%s%d", i ? "," : "", sz[i]); printf("\n"); }
            } }
    }
    printf("ESUM NG=%d TG=%d MAXDEG=%d graphs=%llu bad_tau=%llu tested=%llu hits=%llu hits_nonlinear=%llu hits_F7=%llu hits_F7free_P3bad=%llu hits_inC=%llu hits_connected=%llu hits_inC_connected=%llu\n",
           NG, TG, MD, graphs, bad, tested, hits, hnonlin, hf7, hp3, hinC, hconn, hinCconn);
    return 0;
}
