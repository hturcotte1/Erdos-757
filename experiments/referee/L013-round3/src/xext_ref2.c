/* xext_ref NG tp t d EP [mode] < inputs ("k a b c ..." lines, NG vertices each)
   Own extension program (referee L013 round 3). For each input G (must have tau(G) == tp):
   enumerate every set of d pairwise disjoint admissible pairs {a,b} (a<b, both of G-degree <= EP, {a,b} inside no edge of G);
   H = G + new vertex w = NG with edges {w,a_i,b_i}.  If tp == t-1: tau(H) >= t  iff  no minimum cover of G meets all d pairs
   (a cover of size t-1 of H cannot contain w). If tp == t: every extension has tau(H) in {t, t+1}; keep tau(H) == t (exact).
   Enumeration: index order p1 < p2 < ... with disjointness; alive = set of minimum covers meeting all chosen pairs (bitset);
   at the last level, if alive != 0 the last pair must avoid U = union of alive covers.  mode 'brute': no pruning (every d-set
   tested against alive); mode 'validate': additionally compare the cover criterion with a direct tau(H) >= t test on random d-sets.
   Output: HIT lines (all extensions with the required tau) with flags conn/F7/P3, and SUMMARY counters. */
#include "hyp.h"
#include <time.h>
#define MAXC 300000
static hyp G; static int NG, TP, T, D, EP, brute = 0, validate = 0;
static uint32_t cov[MAXC]; static int ncov; static int W; /* words */
static uint64_t *meet; static int npairs; static int pa[600], pb[600]; static uint32_t pmask[600];
static long hits, f7free, inC, connC, nodes, cand_total; static int sel[8];
static long val_agree, val_total;
static long inC_exact, conn_all, conn_F7;
static void classify(void) { hyp H = G; H.n = NG + 1; for (int i = 0; i < D; i++) { H.e[H.m][0] = NG; H.e[H.m][1] = pa[sel[i]]; H.e[H.m][2] = pb[sel[i]]; H.m++; } hyp_finish(&H);
    hits++; int lin = hyp_linear(&H), conn = hyp_connected(&H), f7 = !hyp_has_F7(&H), p3 = f7 ? hyp_P3(&H) : 0; if (!lin) { fprintf(stderr, "NONLINEAR HIT?!\n"); } if (conn) { conn_all++; if (!f7) conn_F7++; }
    if (f7) f7free++; if (f7 && p3) { inC++; int tau = hyp_tau(&H); int exact = (tau == T); if (TP != T && !exact) fprintf(stderr, "TAU MISMATCH in C hit: %d\n", tau);
        if (exact) { inC_exact++; if (conn) connC++; printf("HIT conn=%d:", conn); for (int i = 0; i < H.m; i++) printf(" (%d,%d,%d)", H.e[i][0], H.e[i][1], H.e[i][2]); printf("\n"); } } }
static int alive_empty(const uint64_t *a) { for (int w = 0; w < W; w++) if (a[w]) return 0; return 1; }
static void rec(int level, int start, uint32_t used, uint64_t *alive) {
    nodes++;
    if (level == D) { if (TP == T || alive_empty(alive)) classify(); return; }
    if (level == D - 1 && !brute && TP != T && !alive_empty(alive)) { uint32_t U = 0; for (int w = 0; w < W; w++) { uint64_t x = alive[w]; while (x) { int b = __builtin_ctzll(x); U |= cov[w * 64 + b]; x &= x - 1; } }
        for (int p = start; p < npairs; p++) { if (pmask[p] & used) continue; if (pmask[p] & U) continue; sel[level] = p; cand_total++; classify(); } return; }
    uint64_t na[MAXC / 64 + 1];
    for (int p = start; p < npairs; p++) { if (pmask[p] & used) continue; sel[level] = p;
        if (TP != T) { int any = 0; for (int w = 0; w < W; w++) { na[w] = alive[w] & meet[(long)p * W + w]; if (na[w]) any = 1; } (void)any; }
        if (level == D - 1) cand_total++;
        rec(level + 1, p + 1, used | pmask[p], na); } }
int main(int argc, char **argv) { if (argc < 6) { fprintf(stderr, "usage: xext_ref NG tp t d EP [brute|validate]\n"); return 2; }
    NG = atoi(argv[1]); TP = atoi(argv[2]); T = atoi(argv[3]); D = atoi(argv[4]); EP = atoi(argv[5]); if (argc > 6) { if (!strcmp(argv[6], "brute")) brute = 1; if (!strcmp(argv[6], "validate")) validate = 1; }
    if (TP != T - 1 && TP != T) { fprintf(stderr, "tp must be t-1 or t\n"); return 2; }
    char line[65536]; long graphs = 0, bad_tau = 0, overflow = 0; int maxcov = 0; srand(2024);
    while (fgets(line, sizeof line, stdin)) { if (!parse_klist(line, &G, NG)) continue; graphs++;
        if (!hyp_linear(&G)) { fprintf(stderr, "input not linear\n"); continue; }
        int tauG = hyp_tau(&G); if (tauG != TP) { bad_tau++; fprintf(stderr, "bad_tau: tau(G)=%d expected %d\n", tauG, TP); continue; }
        int smaller; ncov = hyp_min_covers(&G, TP, cov, MAXC, &smaller); if (ncov < 0 || smaller) { overflow++; fprintf(stderr, "cover overflow/smaller\n"); continue; } if (ncov > maxcov) maxcov = ncov;
        W = (ncov + 63) / 64; if (W == 0) W = 1;
        int deg[MAXV]; hyp_degs(&G, deg); npairs = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) { if (deg[a] > EP || deg[b] > EP) continue; uint32_t pm = (1u << a) | (1u << b); int inside = 0;
            for (int i = 0; i < G.m; i++) if ((G.em[i] & pm) == pm) { inside = 1; break; } if (inside) continue; pa[npairs] = a; pb[npairs] = b; pmask[npairs] = pm; npairs++; }
        meet = (uint64_t*)calloc((size_t)npairs * W + 1, sizeof(uint64_t));
        for (int p = 0; p < npairs; p++) for (int j = 0; j < ncov; j++) if (cov[j] & pmask[p]) meet[(long)p * W + j / 64] |= 1ull << (j % 64);
        uint64_t all[MAXC / 64 + 1]; for (int w = 0; w < W; w++) all[w] = 0; for (int j = 0; j < ncov; j++) all[j / 64] |= 1ull << (j % 64);
        rec(0, 0, 0, all);
        if (validate && TP != T) { /* random d-sets: cover criterion vs direct tau(H) >= T */
            for (int r = 0; r < 400; r++) { uint32_t used = 0; int ok = 1; for (int i = 0; i < D; i++) { int tries = 0; while (tries++ < 50) { int p = rand() % npairs; if (!(pmask[p] & used)) { sel[i] = p; used |= pmask[p]; break; } } if (tries > 50) { ok = 0; break; } }
                if (!ok) continue; int crit = 1; for (int j = 0; j < ncov; j++) { int meets_all = 1; for (int i = 0; i < D; i++) if (!(cov[j] & pmask[sel[i]])) { meets_all = 0; break; } if (meets_all) { crit = 0; break; } }
                hyp H = G; H.n = NG + 1; for (int i = 0; i < D; i++) { H.e[H.m][0] = NG; H.e[H.m][1] = pa[sel[i]]; H.e[H.m][2] = pb[sel[i]]; H.m++; } hyp_finish(&H);
                int direct = hyp_tau_ge(&H, T); val_total++; if (crit == direct) val_agree++; else fprintf(stderr, "CRITERION DISAGREES WITH DIRECT TAU\n"); } }
        free(meet); }
    printf("SUMMARY xext_ref NG=%d tp=%d t=%d d=%d EP=%d mode=%s graphs=%ld bad_tau=%ld overflow=%ld max_min_covers=%d nodes=%ld last_level_candidates=%ld hits_all=%ld hits_F7free=%ld hits_in_C=%ld inC_tau_exact=%ld connected_in_C=%ld connected_all=%ld connected_with_F7=%ld validate=%ld/%ld\n",
        NG, TP, T, D, EP, brute ? "brute" : (validate ? "validate" : "pruned"), graphs, bad_tau, overflow, maxcov, nodes, cand_total, hits, f7free, inC, inC_exact, connC, conn_all, conn_F7, val_agree, val_total);
    return 0; }
