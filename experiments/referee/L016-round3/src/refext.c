/* refext NG TG T d EP DMAX [gosper] [all] < inputs ("m a1 b1 c1 ...", a 3-graph G on 0..NG-1).
   Own re-implementation of the extension step: for each G with tau(G) == TG exactly (own branching), list the minimum covers (branching with
   exclusion, optionally cross-checked by a Gosper enumeration of all TG-subsets of {0..NG-1}), the admissible pairs {a,b} (not inside an edge,
   both G-degrees <= EP), and enumerate in lexicographic order every set of d pairwise disjoint admissible pairs such that H = G + {NG,a_i,b_i}
   has tau(H) >= T (for TG == T-1: every minimum cover of G misses some pair; for TG >= T: every set; for TG < T-1: none).  For every such H:
   linear (checked), F7-free, (P3), connected, max degree <= DMAX (own tests).  Counters and FOUND lines for the connected members of C
   (or, with 'all', for every H with tau >= T, tagged ALL:). */
#include "common.h"
#define MAXCOV 2000000
#define MAXPAIR 1024
static int NG, TG, T, D, EP, DMAX, GOSPER = 0, ALL = 0;
static u32 E[64]; static int m;
static u32 *covers; static long K; static int W;
static int P; static u32 pm[MAXPAIR];
static uint64_t *killb;          /* killb[p*W+w]: covers disjoint from pair p */
static int *killers; static int *killers_start;   /* per cover: list of pairs disjoint from it */
static long long nodes, hits_tau, hits_f7, hits_C, hits_conn, max_cov;
static int chosen[8];
static void collect(u32 S, int budget, u32 forb) {   /* covers with at most budget vertices, each exactly once (exclusion) */
    int e = -1; for (int i = 0; i < m; i++) if (!(E[i] & S)) { e = i; break; }
    if (e < 0) { if (K < MAXCOV) covers[K] = S; K++; return; }
    if (budget == 0) return;
    u32 r = E[e] & ~forb, f2 = forb;
    for (; r; r &= r - 1) { u32 v = r & -r; collect(S | v, budget - 1, f2); f2 |= v; }
}
static int cmpu32(const void *a, const void *b) { u32 x = *(const u32 *)a, y = *(const u32 *)b; return x < y ? -1 : x > y; }
static void final(void) {
    hits_tau++;
    u32 H[64]; int mh = m + D; memcpy(H, E, sizeof(u32) * m);
    for (int i = 0; i < D; i++) H[m + i] = pm[chosen[i]] | (1u << NG);
    if (!is_linear(mh, H)) { fprintf(stderr, "NONLINEAR extension?!\n"); exit(9); }
    int f7 = has_f7(NG + 1, mh, H); int p3 = f7 ? 0 : p3_ok(NG + 1, mh, H); int conn = ncomponents(NG + 1, mh, H) == 1; int deg = maxdeg(NG + 1, mh, H) <= DMAX;
    if (!deg) { fprintf(stderr, "DEGREE > DMAX?!\n"); exit(9); }
    if (!f7) hits_f7++;
    if (!f7 && p3) { hits_C++; if (conn) hits_conn++; }
    if (ALL || (!f7 && p3 && conn)) {
        printf(ALL ? "ALL:" : "FOUND:");
        for (int i = 0; i < mh; i++) { int v[3], k = 0; for (u32 r = H[i]; r; r &= r - 1) v[k++] = __builtin_ctz(r); printf(" (%d,%d,%d)", v[0], v[1], v[2]); }
        if (ALL) printf(" #f7=%d p3=%d conn=%d", f7, p3, conn);
        printf("\n");
    }
}
static int alive_empty(const uint64_t *al) { for (int w = 0; w < W; w++) if (al[w]) return 0; return 1; }
static uint64_t albuf[10][MAXCOV / 64 + 1];
static void rec(int k, int last, const uint64_t *alive, u32 usedv) {
    nodes++;
    if (k == D) { if (alive_empty(alive)) final(); return; }
    int c0 = -1; for (int w = 0; w < W; w++) if (alive[w]) { c0 = w * 64 + __builtin_ctzll(alive[w]); break; }
    if (c0 >= 0 && k == D - 1) {       /* the last pair must kill every remaining cover; it must kill c0 */
        for (int i = killers_start[c0]; i < killers_start[c0 + 1]; i++) { int p = killers[i];
            if (p <= last || (pm[p] & usedv)) continue;
            int ok = 1; for (int w = 0; w < W; w++) if (alive[w] & ~killb[(size_t)p * W + w]) { ok = 0; break; }
            if (ok) { chosen[k] = p; final(); } }
        return;
    }
    uint64_t *al2 = albuf[k + 1];
    for (int p = last + 1; p < P; p++) {
        if (pm[p] & usedv) continue;
        for (int w = 0; w < W; w++) al2[w] = alive[w] & ~killb[(size_t)p * W + w];
        chosen[k] = p; rec(k + 1, p, al2, usedv | pm[p]);
    }
}
int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: refext NG TG T d EP DMAX [gosper] [all] < inputs\n"); return 1; }
    NG = atoi(argv[1]); TG = atoi(argv[2]); T = atoi(argv[3]); D = atoi(argv[4]); EP = atoi(argv[5]); DMAX = atoi(argv[6]);
    for (int i = 7; i < argc; i++) { if (!strcmp(argv[i], "gosper")) GOSPER = 1; if (!strcmp(argv[i], "all")) ALL = 1; }
    if (NG > 31 || D > 8) { fprintf(stderr, "limits\n"); return 1; }
    covers = malloc(sizeof(u32) * MAXCOV); killb = NULL; size_t killb_cap = 0;
    killers_start = malloc(sizeof(int) * (MAXCOV + 1)); killers = NULL; size_t killers_cap = 0;
    long long graphs = 0, bad_tau = 0, nohit = 0, searched = 0, tn = 0, th = 0, tf = 0, tc = 0, tcc = 0, bad_input = 0;
    while (scanf("%d", &m) == 1) {
        graphs++; int deg[32] = {0}; int bad = 0;
        for (int i = 0; i < m; i++) { int a, b, c; if (scanf("%d %d %d", &a, &b, &c) != 3) { fprintf(stderr, "format\n"); return 2; }
            if (a < 0 || b < 0 || c < 0 || a >= NG || b >= NG || c >= NG || a == b || a == c || b == c) bad = 1;
            else { E[i] = (1u << a) | (1u << b) | (1u << c); deg[a]++; deg[b]++; deg[c]++; } }
        if (bad || !is_linear(m, E)) { bad_input++; continue; }
        int tau = tau_of(m, E);
        if (tau != TG) { bad_tau++; continue; }
        K = 0; collect(0, TG, 0);
        if (K > MAXCOV) { fprintf(stderr, "too many covers\n"); return 3; }
        qsort(covers, K, sizeof(u32), cmpu32);
        for (long i = 1; i < K; i++) if (covers[i] == covers[i - 1]) { fprintf(stderr, "duplicate cover (exclusion failed)\n"); return 5; }
        for (long i = 0; i < K; i++) if (__builtin_popcount(covers[i]) != TG) { fprintf(stderr, "cover of wrong size\n"); return 5; }
        if (GOSPER) {   /* independent count of the TG-subsets of {0..NG-1} meeting every edge */
            long KG = 0; u32 S = (1u << TG) - 1, lim = (NG >= 32) ? 0xffffffffu : (1u << NG) - 1;
            while (S <= lim) { int ok = 1; for (int i = 0; i < m; i++) if (!(E[i] & S)) { ok = 0; break; }
                if (ok) { if (KG < K && covers[KG] != S) { fprintf(stderr, "GOSPER MISMATCH\n"); return 6; } KG++; }
                u32 c = S & -S, r = S + c; if (r == 0) break; S = (((r ^ S) >> 2) / c) | r; }
            if (KG != K) { fprintf(stderr, "GOSPER COUNT MISMATCH %ld vs %ld\n", KG, K); return 6; }
        }
        if (TG < T - 1) { nohit++; continue; }
        if (K > max_cov) max_cov = K;
        P = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > EP || deg[b] > EP) continue;
            u32 pr = (1u << a) | (1u << b); int inside = 0; for (int i = 0; i < m; i++) if ((E[i] & pr) == pr) { inside = 1; break; }
            if (inside) continue;
            if (P >= MAXPAIR) { fprintf(stderr, "MAXPAIR\n"); return 4; }
            pm[P++] = pr;
        }
        nodes = 0; hits_tau = 0; hits_f7 = 0; hits_C = 0; hits_conn = 0;
        if (TG >= T) { W = 0; K = 0; }   /* every set is a hit: alive is empty */
        W = (K + 63) / 64;
        if ((size_t)P * W > killb_cap) { free(killb); killb_cap = (size_t)P * W + 1024; killb = malloc(sizeof(uint64_t) * killb_cap); }
        if ((size_t)K * P + 1 > killers_cap) { free(killers); killers_cap = (size_t)K * P + 1024; killers = malloc(sizeof(int) * killers_cap); }
        for (int p = 0; p < P; p++) { uint64_t *row = killb + (size_t)p * W; memset(row, 0, sizeof(uint64_t) * W);
            for (long c = 0; c < K; c++) if (!(covers[c] & pm[p])) row[c >> 6] |= 1ull << (c & 63); }
        long pos = 0; for (long c = 0; c < K; c++) { killers_start[c] = pos; for (int p = 0; p < P; p++) if (!(covers[c] & pm[p])) killers[pos++] = p; } killers_start[K] = pos;
        uint64_t *alive = albuf[0]; memset(alive, 0, sizeof(uint64_t) * (W ? W : 1)); for (long c = 0; c < K; c++) alive[c >> 6] |= 1ull << (c & 63);
        rec(0, -1, alive, 0);
        searched++; tn += nodes; th += hits_tau; tf += hits_f7; tc += hits_C; tcc += hits_conn;
    }
    printf("SUMMARY graphs=%lld bad_input=%lld bad_tau=%lld tg_too_small=%lld searched=%lld max_min_covers=%lld nodes=%lld hits_tau=%lld hits_F7free=%lld hits_in_C=%lld hits_conn_in_C=%lld\n",
           graphs, bad_input, bad_tau, nohit, searched, max_cov, tn, th, tf, tc, tcc);
    return 0;
}
