#include "hyp.h"
static void mk(hyp *h, int n, const char *s) { parse_found(s, h, n); }
int main(void) { hyp h; int fails = 0;
    mk(&h, 7, "FOUND: (0,1,2) (0,3,4) (0,5,6) (1,3,5) (2,4,6)"); /* F7 */
    printf("F7: linear=%d F7=%d P3=%d tau=%d conn=%d\n", hyp_linear(&h), hyp_has_F7(&h), hyp_P3(&h), hyp_tau(&h), hyp_connected(&h));
    if (!hyp_has_F7(&h) || hyp_tau(&h) != 3 || !hyp_P3(&h)) fails++;
    mk(&h, 7, "FOUND: (0,1,2) (0,3,4) (0,5,6) (1,3,5) (2,4,5)"); /* not F7 (second transversal not the complement) */
    printf("nonF7 variant: linear=%d F7=%d\n", hyp_linear(&h), hyp_has_F7(&h)); if (hyp_has_F7(&h) || hyp_linear(&h)) fails++;
    mk(&h, 7, "FOUND: (0,1,2) (0,3,4) (0,5,6) (1,3,5) (2,4,6) (1,4,6)"); printf("F7+edge: linear=%d\n", hyp_linear(&h));
    /* Fano plane: 7 points, 7 lines: linear, contains F7? Fano minus two lines... P3 fails (e(V)=7 > 5) */
    mk(&h, 7, "FOUND: (0,1,2) (0,3,4) (0,5,6) (1,3,5) (1,4,6) (2,3,6) (2,4,5)");
    printf("Fano: linear=%d F7=%d P3=%d P3brute=%d tau=%d\n", hyp_linear(&h), hyp_has_F7(&h), hyp_P3(&h), hyp_P3_brute(&h), hyp_tau(&h)); if (hyp_P3(&h) || hyp_tau(&h) != 3) fails++;
    /* A_base AP hypergraph: compute from the set */
    long A[14] = {0,136,200,243,246,249,272,286,298,323,400,528,596,1056}; h.n = 14; h.m = 0;
    for (int i = 0; i < 14; i++) for (int j = i + 1; j < 14; j++) for (int k = j + 1; k < 14; k++) if (A[i] + A[k] == 2 * A[j]) { h.e[h.m][0] = i; h.e[h.m][1] = j; h.e[h.m][2] = k; h.m++; }
    hyp_finish(&h); printf("A_base: m=%d linear=%d F7=%d P3=%d P3brute=%d tau=%d conn=%d maxdeg=%d\n", h.m, hyp_linear(&h), hyp_has_F7(&h), hyp_P3(&h), hyp_P3_brute(&h), hyp_tau(&h), hyp_connected(&h), hyp_maxdeg(&h));
    if (h.m != 12 || hyp_tau(&h) != 6 || !hyp_P3(&h) || hyp_has_F7(&h) || !hyp_linear(&h)) fails++;
    uint32_t cov[100000]; int sm; int nc = hyp_min_covers(&h, 6, cov, 100000, &sm); printf("A_base min covers of size 6: %d (smaller=%d)\n", nc, sm);
    /* brute-force check of the number of 6-covers */
    int bf = 0; for (uint32_t S = 0; S < (1u << 14); S++) if (popc(S) == 6) { int ok = 1; for (int i = 0; i < h.m; i++) if (!(h.em[i] & S)) { ok = 0; break; } bf += ok; } printf("brute force 6-covers: %d\n", bf); if (bf != nc) fails++;
    /* two disjoint edges: disconnected; 3x3 grid AG-like: rows+cols (6 edges on 9 points) linear, P3? e(V)=6<=7 ok; tau=3 */
    mk(&h, 6, "FOUND: (0,1,2) (3,4,5)"); printf("2 disjoint edges: conn=%d tau=%d P3=%d\n", hyp_connected(&h), hyp_tau(&h), hyp_P3(&h)); if (hyp_connected(&h) || hyp_tau(&h) != 2) fails++;
    mk(&h, 9, "FOUND: (0,1,2) (3,4,5) (6,7,8) (0,3,6) (1,4,7) (2,5,8)"); printf("grid: linear=%d F7=%d P3=%d brute=%d tau=%d\n", hyp_linear(&h), hyp_has_F7(&h), hyp_P3(&h), hyp_P3_brute(&h), hyp_tau(&h));
    if (hyp_P3(&h) != hyp_P3_brute(&h) || hyp_tau(&h) != 3) fails++;
    /* AG(2,3) minus one parallel class: 9 edges on 9 points: e(V)=9 > 7 so P3 fails; contains F7? */
    mk(&h, 9, "FOUND: (0,1,2) (3,4,5) (6,7,8) (0,3,6) (1,4,7) (2,5,8) (0,4,8) (1,5,6) (2,3,7)"); printf("AG minus class: linear=%d F7=%d P3=%d brute=%d tau=%d\n", hyp_linear(&h), hyp_has_F7(&h), hyp_P3(&h), hyp_P3_brute(&h), hyp_tau(&h));
    if (hyp_P3(&h) != hyp_P3_brute(&h)) fails++;
    /* relabelled F7 plus pendant edge on 9 vertices */
    mk(&h, 9, "FOUND: (8,2,7) (3,1,7) (7,4,5) (2,3,4) (8,1,5) (0,6,8)"); printf("relabelled F7 + pendant: F7=%d\n", hyp_has_F7(&h)); if (!hyp_has_F7(&h)) fails++;
    /* random P3 cross-check vs brute force on small random linear graphs */
    srand(12345); int agree = 0, tested = 0;
    for (int it = 0; it < 3000; it++) { int n = 6 + rand() % 7; h.n = n; h.m = 0; int tries = 0;
        while (h.m < n - 1 && tries < 200) { tries++; int a = rand() % n, b = rand() % n, c = rand() % n; if (a == b || b == c || a == c) continue; uint32_t em = (1u<<a)|(1u<<b)|(1u<<c); int ok = 1;
            for (int i = 0; i < h.m; i++) if (popc(h.em[i] & em) >= 2) { ok = 0; break; } if (!ok) continue; h.e[h.m][0]=a; h.e[h.m][1]=b; h.e[h.m][2]=c; h.em[h.m]=em; h.m++; if (rand()%3==0) break; }
        tested++; if (hyp_P3(&h) == hyp_P3_brute(&h)) agree++; }
    printf("P3 matching vs brute force on %d random linear graphs: agree %d\n", tested, agree); if (agree != tested) fails++;
    /* tau vs brute force */
    srand(777); agree = 0; tested = 0;
    for (int it = 0; it < 500; it++) { int n = 6 + rand() % 7; h.n = n; h.m = 0; int tries = 0;
        while (h.m < n && tries < 200) { tries++; int a = rand() % n, b = rand() % n, c = rand() % n; if (a == b || b == c || a == c) continue; uint32_t em = (1u<<a)|(1u<<b)|(1u<<c); int ok = 1;
            for (int i = 0; i < h.m; i++) if (popc(h.em[i] & em) >= 2) { ok = 0; break; } if (!ok) continue; h.e[h.m][0]=a; h.e[h.m][1]=b; h.e[h.m][2]=c; h.em[h.m]=em; h.m++; }
        int best = 99; for (uint32_t S = 0; S < (1u << n); S++) { int ok = 1; for (int i = 0; i < h.m; i++) if (!(h.em[i] & S)) { ok = 0; break; } if (ok && popc(S) < best) best = popc(S); }
        tested++; if (best == hyp_tau(&h)) agree++; }
    printf("tau vs brute force on %d random linear graphs: agree %d\n", tested, agree); if (agree != tested) fails++;
    printf("UNIT TESTS: %d failures\n", fails); return fails ? 1 : 0; }
