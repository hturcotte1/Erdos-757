/* Referee L014 round 2 -- gfilt: filter genbg output (graph6 incidence graphs: first class n1 = hypergraph vertices,
 * second class = hyperedges) into hypergraphs and classify them from the definitions (same classifier functions as myext.c).
 * usage: genbg ... n1 n2 | gfilt n1 t [print]   -> counts by tau; members of C (linear, F7-free, (P3)) with tau == t printed
 * as 'N M a b c ...' if print=1. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXV 64
#define MAXE 64
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

int main(int argc, char **argv) {
    int n1 = atoi(argv[1]), t = atoi(argv[2]), pr = argc > 3 ? atoi(argv[3]) : 0, onlyt = argc > 4 ? atoi(argv[4]) : 0;
    static char line[4096]; long total = 0, lin_bad = 0, f7c = 0, p3v = 0, disc = 0, member = 0, member_t = 0, disagree = 0, bad3 = 0;
    long bytau[40] = {0}; long memtau[40] = {0};
    capcov = 16; covs = malloc(capcov * sizeof(u64));
    while (fgets(line, sizeof line, stdin)) {
        char *s = line; if (*s == '>') continue;
        int n = *s++ - 63; if (n > 62) { fprintf(stderr, "big\n"); return 3; }
        static int adj[64][64]; memset(adj, 0, sizeof adj);
        int k = 0; int bits = 0, cur = 0;
        for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) {
            if (bits == 0) { cur = *s++ - 63; bits = 6; }
            bits--; if ((cur >> bits) & 1) adj[i][j] = adj[j][i] = 1;
            k++;
        }
        total++;
        NV = n1; NE = n - n1; int ok = 1;
        for (int e = 0; e < NE; e++) { int c = 0; for (int v = 0; v < n1; v++) if (adj[n1 + e][v]) { if (c < 3) E[e][c] = v; c++; }
            for (int f = 0; f < NE; f++) if (adj[n1 + e][n1 + f]) ok = 0;
            if (c != 3) ok = 0; }
        for (int u = 0; u < n1; u++) for (int v = 0; v < n1; v++) if (adj[u][v]) ok = 0;
        if (!ok) { bad3++; continue; }
        for (int e = 0; e < NE; e++) emask[e] = (1ULL << E[e][0]) | (1ULL << E[e][1]) | (1ULL << E[e][2]);
        int lin = linear_and_index(NV, NE, E); if (!lin) { lin_bad++; continue; }
        int tg = tau_of(emask, NE, NV); bytau[tg]++;
        if (onlyt && tg != t) continue;   /* fast mode: classify only graphs with tau == t */
        int f7 = count_f7(NV, NE, E); if (f7) f7c++;
        int p3b = p3_matching(NV, NE, E); int p3a = onlyt ? p3b : p3_bruteforce(NE, emask); if (p3a != p3b) disagree++;
        if (!p3a) p3v++;
        int conn = connected_all(NV, NE, E); if (!conn) disc++;
        if (!f7 && p3a && p3b) { member++; memtau[tg]++; if (tg == t) { member_t++;
            if (pr) { printf("%d %d", NV, NE); for (int e = 0; e < NE; e++) printf(" %d %d %d", E[e][0], E[e][1], E[e][2]); printf("\n"); } } }
    }
    fprintf(stderr, "GFILT n1=%d t=%d total=%ld not_3uniform_bipartite=%ld nonlinear=%ld F7=%ld P3_violated=%ld disconnected=%ld members_of_C=%ld members_tau_eq_t=%ld p3_disagree=%ld",
            n1, t, total, bad3, lin_bad, f7c, p3v, disc, member, member_t, disagree);
    fprintf(stderr, " tau_hist="); for (int i = 0; i < 40; i++) if (bytau[i]) fprintf(stderr, "%d:%ld,", i, bytau[i]);
    fprintf(stderr, " member_tau_hist="); for (int i = 0; i < 40; i++) if (memtau[i]) fprintf(stderr, "%d:%ld,", i, memtau[i]);
    fprintf(stderr, "\n");
    return 0;
}
