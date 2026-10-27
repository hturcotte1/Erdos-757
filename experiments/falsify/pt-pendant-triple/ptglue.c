/* ptglue: M-list file, R-list file (lines "n m a,b,c ..."), params SMAX D K seed NPAIRS KMAX
   builds G'' = M u R'' + k crossing edges (each: one vertex of M, two of R''), k in 1..KMAX, evaluates PT statistics on G'' and on edge-addition closure (depth D, K samples) */
#include "ptvis.h"
static int readlist(const char *f, G *out, int cap) { FILE *fp = fopen(f, "r"); static char line[1 << 16]; int c = 0; while (c < cap && fgets(line, sizeof line, fp)) { if (parse_graph(line, &out[c])) c++; } fclose(fp); return c; }
int main(int argc, char **argv) {
    static G Ms[200000], Rs[200000]; int nM = readlist(argv[1], Ms, 200000), nR = readlist(argv[2], Rs, 200000);
    SMAX = atoi(argv[3]); D = atoi(argv[4]); K = atoi(argv[5]); seed_rng(atoll(argv[6])); long NP = atol(argv[7]); int KMAX = atoi(argv[8]);
    seen_tab = calloc(SEEN_SZ, 8); for (int i = 0; i < HSZ; i++) minGoodAt[i] = 99;
    long tried = 0, valid = 0;
    for (long it = 0; it < NP; it++) {
        G *M = &Ms[rndint(nM)], *R = &Rs[rndint(nR)]; if (M->n + R->n > 45) continue;
        G g; g.n = M->n + R->n; g.m = 0; DMAX = 3; int ok = 1;
        for (int i = 0; i < M->m; i++) g.e[g.m++] = M->e[i];
        for (int i = 0; i < R->m; i++) g.e[g.m++] = R->e[i] << M->n;
        int k = 1 + rndint(KMAX);
        for (int j = 0; j < k && ok; j++) {
            int tries = 0, done = 0;
            while (!done && tries++ < 60) {
                int u = rndint(M->n), r1 = M->n + rndint(R->n), r2 = M->n + rndint(R->n); if (r1 == r2) continue;
                done = try_add(&g, vmask(u, r1, r2));
            }
            if (!done) ok = 0;
        }
        tried++; if (!ok) continue;
        int iso; if (components(&g, &iso) != 1 || iso) continue;
        if (!seen_insert(fp_graph(&g))) continue;
        int t = tau_of(&g, 2, 0, NULL); if (slack_of(&g, t) > SMAX) continue; valid++;
        visit(&g, 0, t);
    }
    printf("GLUE tried=%ld valid=%ld visited=%ld hits=%ld minslack_with_hit=%d nM=%d nR=%d\n", tried, valid, nvis, hitcount, minslack_cfg, nM, nR);
    for (int s = 0; s < HSZ; s++) if (maxU2[s] || hist[s][0]) { printf("SLACKROW %d maxU2 %d minGoodAtCand %d hist", s - HOFF, maxU2[s], minGoodAt[s]); for (int u = 0; u < 12; u++) if (hist[s][u]) printf(" %d:%ld", u, hist[s][u]); printf("\n"); }
    return 0;
}
