/* Referee L014 round 2 -- independent extension search (written from the definitions; shares no code with ext_d/filt).
 * stdin : one graph per line: "N M a1 b1 c1 ... aM bM cM"   (vertices 0..N-1, isolated vertices allowed)
 * argv  : tp t d emax [print]
 *   tp   : tau(G) is computed exactly and must equal tp (otherwise counted in bad_tau and skipped)
 *   t    : an extension is a HIT iff tau(H) >= t, where H = G + new vertex w=N with d edges {w,a_i,b_i}
 *   d    : number of new edges (1..4)
 *   emax : endpoints must have G-degree <= emax; pairs pairwise disjoint and not inside an edge of G (linearity)
 *   print: 0 = summary only, 1 = print every HIT with its classification, 2 = print only connected members of C
 * The hit test for t = tp+1: tau(H) <= tp iff some minimum cover T of G (|T| = tp) meets every pair (T plus nothing covers H;
 * a cover of H of size tp containing w would leave tp-1 vertices covering G).  All tp-covers of G are enumerated by edge
 * branching with exclusions and every one is checked to be a cover.  For t <= tp every extension is a hit.
 * Every hit H is then classified from scratch: tau(H) recomputed by branching on H, linearity, max degree, F7 (centre +
 * 3 edges + two complementary transversal edges), (P3) by two methods (all nonempty edge subsets F: |V(F)| >= |F|+2;
 * and Hall: for every vertex pair {x,y} the edges have a matching into V-{x,y}), connectivity by union-find. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXV 32
#define MAXE 48
typedef uint64_t u64;
static int NV, NE, E[MAXE][3];
static u64 emask[MAXE];
/* ---------- tau by branching on the first uncovered edge ---------- */
static int best;
static void tau_rec(const u64 *em, int ne, u64 cov, int size) {
    if (size >= best) return;
    int i; for (i = 0; i < ne; i++) if (!(em[i] & cov)) break;
    if (i == ne) { best = size; return; }
    u64 m = em[i];
    while (m) { int v = __builtin_ctzll(m); m &= m - 1; tau_rec(em, ne, cov | (1ULL << v), size + 1); }
}
static int tau_of(const u64 *em, int ne, int nv) { best = nv + 1; tau_rec(em, ne, 0, 0); return best; }
/* ---------- enumerate all covers of size exactly k (k = tau) ---------- */
static u64 *covs; static long ncov, capcov;
static void cov_rec(const u64 *em, int ne, u64 cov, u64 excl, int size, int k) {
    int i; for (i = 0; i < ne; i++) if (!(em[i] & cov)) break;
    if (i == ne) {
        if (size == k) { if (ncov == capcov) { capcov *= 2; covs = realloc(covs, capcov * sizeof(u64)); } covs[ncov++] = cov; }
        return;  /* a cover of size < k cannot occur when tau = k */
    }
    if (size == k) return;
    u64 m = em[i] & ~excl; u64 ex = excl;
    while (m) { int v = __builtin_ctzll(m); m &= m - 1; cov_rec(em, ne, cov | (1ULL << v), ex, size + 1, k); ex |= 1ULL << v; }
}
/* ---------- classification of a hypergraph ---------- */
static int pe[MAXV][MAXV]; /* pair -> edge index or -1 */
static int has_edge(int a, int b, int c, int ne, int (*ed)[3]) {
    int e = pe[a][b]; if (e < 0) return 0;
    return ed[e][0] == c || ed[e][1] == c || ed[e][2] == c;
}
static int linear_and_index(int nv, int ne, int (*ed)[3]) {
    for (int i = 0; i < nv; i++) for (int j = 0; j < nv; j++) pe[i][j] = -1;
    for (int e = 0; e < ne; e++) {
        int a = ed[e][0], b = ed[e][1], c = ed[e][2];
        if (a == b || a == c || b == c || a < 0 || b < 0 || c < 0 || a >= nv || b >= nv || c >= nv) return 0;
        int pr[3][2] = {{a, b}, {a, c}, {b, c}};
        for (int k = 0; k < 3; k++) { int x = pr[k][0], y = pr[k][1]; if (pe[x][y] >= 0) return 0; pe[x][y] = pe[y][x] = e; }
    }
    return 1;
}
static int count_f7(int nv, int ne, int (*ed)[3]) {   /* requires pe[][] from linear_and_index */
    int cnt = 0;
    for (int c = 0; c < nv; c++) {
        int inc[MAXE], k = 0;
        for (int e = 0; e < ne; e++) if (ed[e][0] == c || ed[e][1] == c || ed[e][2] == c) inc[k++] = e;
        for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++) for (int l = j + 1; l < k; l++) {
            int P[3][2], idx[3] = {inc[i], inc[j], inc[l]};
            for (int q = 0; q < 3; q++) { int r = 0; for (int s = 0; s < 3; s++) if (ed[idx[q]][s] != c) P[q][r++] = ed[idx[q]][s]; }
            for (int ch = 0; ch < 8; ch++) {
                int u0 = P[0][ch & 1], u1 = P[1][(ch >> 1) & 1], u2 = P[2][(ch >> 2) & 1];
                int v0 = P[0][1 - (ch & 1)], v1 = P[1][1 - ((ch >> 1) & 1)], v2 = P[2][1 - ((ch >> 2) & 1)];
                if (has_edge(u0, u1, u2, ne, ed) && has_edge(v0, v1, v2, ne, ed)) cnt++;
            }
        }
    }
    return cnt / 2; /* each copy found twice (the two transversals swapped: ch and its complement) */
}
static int p3_bf_viol;
static int p3_rec(int i, int ne, const u64 *em, u64 vm, int f) {
    if (f > 0 && __builtin_popcountll(vm) < f + 2) { p3_bf_viol++; return 1; }
    if (i == ne) return 0;
    if (p3_rec(i + 1, ne, em, vm | em[i], f + 1)) return 1;
    return p3_rec(i + 1, ne, em, vm, f);
}
static int p3_bruteforce(int ne, const u64 *em) { return !p3_rec(0, ne, em, 0, 0); }
/* Hall/matching version */
static int mt_vtx[MAXV], seen_v[MAXV];
static int aug(int e, int ne, int (*ed)[3], int x, int y) {
    for (int s = 0; s < 3; s++) { int v = ed[e][s]; if (v == x || v == y || seen_v[v]) continue; seen_v[v] = 1;
        if (mt_vtx[v] < 0 || aug(mt_vtx[v], ne, ed, x, y)) { mt_vtx[v] = e; return 1; } }
    return 0;
}
static int p3_matching(int nv, int ne, int (*ed)[3]) {
    for (int x = 0; x < nv; x++) for (int y = x + 1; y < nv; y++) {
        for (int v = 0; v < nv; v++) mt_vtx[v] = -1;
        for (int e = 0; e < ne; e++) { memset(seen_v, 0, sizeof(seen_v)); if (!aug(e, ne, ed, x, y)) return 0; }
    }
    return 1;
}
static int connected_all(int nv, int ne, int (*ed)[3]) {
    int par[MAXV] = {0}; for (int v = 0; v < nv; v++) par[v] = v;
    #define FIND(z) ({ int _z = (z); while (par[_z] != _z) _z = par[_z] = par[par[_z]]; _z; })
    for (int e = 0; e < ne; e++) { int a = FIND(ed[e][0]), b = FIND(ed[e][1]), c = FIND(ed[e][2]); par[b] = a; par[FIND(c)] = a; }
    int r = FIND(0); for (int v = 1; v < nv; v++) if (FIND(v) != r) return 0;
    return 1;
}
/* ---------- main ---------- */
static long bad_deg, n_inputs, bad_tau, bad_input, n_triples, n_hits, h_nonlin, h_f7, h_p3, h_p3_f7free, h_member, h_member_conn, h_disc, h_taubad, p3_disagree, maxcov;
static int TP, T, D, EMAX, PRINT, FAST;
static int nadm_pairs, PA[600], PB[600]; static u64 pmask[600]; static u64 *miss; static int W;
static int cur[8];
static void classify_and_print(void) {
    int ed[MAXE][3]; int ne = NE + D, nv = NV + 1;
    for (int e = 0; e < NE; e++) for (int s = 0; s < 3; s++) ed[e][s] = E[e][s];
    for (int i = 0; i < D; i++) { ed[NE + i][0] = NV; ed[NE + i][1] = PA[cur[i]]; ed[NE + i][2] = PB[cur[i]]; }
    u64 em[MAXE]; for (int e = 0; e < ne; e++) em[e] = (1ULL << ed[e][0]) | (1ULL << ed[e][1]) | (1ULL << ed[e][2]);
    n_hits++;
    int lin = linear_and_index(nv, ne, ed); if (!lin) { h_nonlin++; }
    int f7 = lin ? count_f7(nv, ne, ed) : -1; if (f7 > 0) h_f7++;
    int p3a = 0, p3b = 0, tH = -1;
    if (!FAST || f7 == 0) {
        p3b = p3_matching(nv, ne, ed); p3a = FAST ? p3b : p3_bruteforce(ne, em); if (p3a != p3b) p3_disagree++;
        if (!p3a) { h_p3++; if (f7 == 0) h_p3_f7free++; }
    }
    int conn = connected_all(nv, ne, ed); if (!conn) h_disc++;
    int cand = lin && f7 == 0 && p3a && p3b;
    if (!FAST || cand) { tH = tau_of(em, ne, nv); if (tH < T) h_taubad++; }
    int member = cand && tH >= T;
    if (member) { h_member++; if (conn) h_member_conn++; }
    if (PRINT == 1 || (PRINT == 2 && member && conn)) {
        printf("%s tau=%d lin=%d f7=%d p3=%d conn=%d : %d %d", member && conn ? "MEMBER" : "HIT", tH, lin, f7, p3a, conn, nv, ne);
        for (int e = 0; e < ne; e++) printf(" %d %d %d", ed[e][0], ed[e][1], ed[e][2]);
        printf("\n");
    }
}
static void rec_pairs(int level, int start, u64 used, u64 *killed) {
    if (level == D) {
        n_triples++;
        int hit;
        if (T <= TP) hit = 1;
        else { hit = 1; for (int w = 0; w < W; w++) if (killed[w] != ~0ULL) { /* last word may be partial */
                    if (w == W - 1 && (ncov & 63)) { u64 full = (1ULL << (ncov & 63)) - 1; if ((killed[w] & full) != full) { hit = 0; break; } }
                    else { hit = 0; break; } } }
        if (hit) classify_and_print();
        return;
    }
    u64 *nk = killed + W;
    if (level == D - 1 && T > TP) {   /* last pair: alive covers after the chosen pairs; a hit needs the last pair to kill them all */
        int c0 = -1; long nal = 0;
        for (int w = 0; w < W; w++) { u64 full = (w == W - 1 && (ncov & 63)) ? ((1ULL << (ncov & 63)) - 1) : ~0ULL;
            u64 al = full & ~killed[w]; nk[w] = al; if (al) { nal++; if (c0 < 0) c0 = w * 64 + __builtin_ctzll(al); } }
        for (int p = start; p < nadm_pairs; p++) {
            if (pmask[p] & used) continue;
            n_triples++;
            if (c0 >= 0) {
                const u64 *mp = miss + (long)p * W;
                if (!((mp[c0 >> 6] >> (c0 & 63)) & 1)) continue;          /* p meets c0: c0 stays alive, no hit */
                int ok = 1; for (int w = 0; w < W; w++) if (nk[w] & ~mp[w]) { ok = 0; break; }
                if (!ok) continue;
            }
            cur[level] = p; classify_and_print();
        }
        return;
    }
    for (int p = start; p < nadm_pairs; p++) {
        if (pmask[p] & used) continue;
        for (int w = 0; w < W; w++) nk[w] = killed[w] | miss[(long)p * W + w];
        cur[level] = p;
        rec_pairs(level + 1, p + 1, used | pmask[p], nk);
    }
}
int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: myext tp t d emax [print]\n"); return 2; }
    TP = atoi(argv[1]); T = atoi(argv[2]); D = atoi(argv[3]); EMAX = atoi(argv[4]); PRINT = argc > 5 ? atoi(argv[5]) : 0; FAST = argc > 6 ? atoi(argv[6]) : 0;
    if (D < 0 || D > 4) { fprintf(stderr, "d out of range\n"); return 2; }
    capcov = 1024; covs = malloc(capcov * sizeof(u64));
    static char line[1 << 16];
    while (fgets(line, sizeof line, stdin)) {
        char *p = line; int k;
        if (sscanf(p, "%d %d%n", &NV, &NE, &k) != 2) continue;
        p += k;
        if (NV + 1 > MAXV || NE + D > MAXE) { fprintf(stderr, "too large\n"); return 3; }
        int okin = 1;
        for (int e = 0; e < NE; e++) for (int s = 0; s < 3; s++) { if (sscanf(p, "%d%n", &E[e][s], &k) != 1) okin = 0; p += k; }
        n_inputs++;
        if (!okin) { bad_input++; continue; }
        if (!linear_and_index(NV, NE, E)) { bad_input++; continue; }
        int deg[MAXV] = {0};
        for (int e = 0; e < NE; e++) { emask[e] = (1ULL << E[e][0]) | (1ULL << E[e][1]) | (1ULL << E[e][2]); for (int s = 0; s < 3; s++) deg[E[e][s]]++; }
        int dmax = 0; for (int v = 0; v < NV; v++) if (deg[v] > dmax) dmax = deg[v];
        int tg = tau_of(emask, NE, NV);
        if (D == 0) {   /* verify mode: input graph itself must be a connected member of C with tau = TP and max degree <= EMAX */
            int f7 = count_f7(NV, NE, E); int p3b = p3_matching(NV, NE, E); int p3a = FAST ? p3b : p3_bruteforce(NE, emask);
            int conn = connected_all(NV, NE, E);
            if (p3a != p3b) p3_disagree++;
            if (tg == TP && f7 == 0 && p3a && p3b && conn && dmax <= EMAX) h_member_conn++; else { bad_input++;
                printf("BADREP tau=%d f7=%d p3=%d conn=%d dmax=%d : %s", tg, f7, p3a, conn, dmax, line); }
            continue;
        }
        if (dmax > D) { bad_deg++; continue; }
        if (tg != TP) { bad_tau++; continue; }
        ncov = 0; cov_rec(emask, NE, 0, 0, 0, TP);
        for (long c = 0; c < ncov; c++) { for (int e = 0; e < NE; e++) if (!(emask[e] & covs[c])) { fprintf(stderr, "non-cover\n"); return 4; }
                                          if (__builtin_popcountll(covs[c]) != TP) { fprintf(stderr, "bad size\n"); return 4; } }
        if (ncov > maxcov) maxcov = ncov;
        W = (int)((ncov + 63) / 64); if (W == 0) W = 1;
        nadm_pairs = 0;
        for (int a = 0; a < NV; a++) for (int b = a + 1; b < NV; b++)
            if (deg[a] <= EMAX && deg[b] <= EMAX && pe[a][b] < 0) { PA[nadm_pairs] = a; PB[nadm_pairs] = b; pmask[nadm_pairs] = (1ULL << a) | (1ULL << b); nadm_pairs++; }
        miss = realloc(miss, (size_t)nadm_pairs * W * sizeof(u64) + 8);
        for (int q = 0; q < nadm_pairs; q++) for (int w = 0; w < W; w++) {
            u64 b = 0; for (int j = 0; j < 64 && w * 64 + j < ncov; j++) if (!(covs[w * 64 + j] & pmask[q])) b |= 1ULL << j;
            miss[(long)q * W + w] = b; }
        u64 *killed = calloc((size_t)W * (D + 1), sizeof(u64));
        rec_pairs(0, 0, 0, killed);
        free(killed);
    }
    printf("SUMMARY inputs=%ld bad_input=%ld bad_deg=%ld bad_tau=%ld max_min_covers=%ld dsets=%ld hits=%ld hit_tau_below_t=%ld nonlinear=%ld F7=%ld "
           "P3_violated=%ld F7free_P3_violated=%ld disconnected=%ld members_of_C=%ld connected_members=%ld p3_methods_disagree=%ld\n",
           n_inputs, bad_input, bad_deg, bad_tau, maxcov, n_triples, n_hits, h_taubad, h_nonlin, h_f7, h_p3, h_p3_f7free, h_disc, h_member, h_member_conn, p3_disagree);
    return 0;
}
