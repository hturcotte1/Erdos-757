/* xext.c (referee L012 round 3) -- independent re-insertion of one vertex of degree d into a 3-graph G on vertices 0..NG-1.
   Usage: xext NG T d EP < inputs   (lines "m a b c ...")
   For each G: tau(G) and ALL minimum covers by brute force over all subsets of size tau(G)-1 (none) and tau(G) (listed), using a
   combinatorial enumeration of k-subsets by index arrays (not Gosper's hack).  Requires tau(G) = T-1 (else reports and skips).
   Admissible pairs {a,b}: not inside an edge of G, both of G-degree <= EP.  Hits: d-sets of pairwise disjoint admissible pairs such
   that every minimum cover of G misses at least one pair (then tau(G + {w,a,b}) >= T; and <= T since tau(G)+1 = T).
   Search: exclusion scheme on the alive cover with the FEWEST available killing pairs (dynamic choice; ext_d uses the first alive
   cover in index order), so the search tree differs; when all covers are dead the remaining pairs are completed in increasing index
   order over the non-excluded pairs.  Every hit is produced exactly once (standard argument: a hit S is produced in the branch of its
   smallest-index pair that kills the chosen cover; no pair of S is ever excluded in that branch).
   Post-filters (own code): F7 test (centre-based: a vertex of degree >= 3, three of its edges, two disjoint transversal edges), (P3) by
   BRUTE FORCE over all 2^m edge subsets F (|V(F)| >= |F| + 2 for every nonempty F) in Gray-code order, connectivity (union-find),
   maximum degree, and (for survivors) tau(H) = T exactly by brute force over the (T-1)-subsets of the NG+1 vertices.
   Output: "HIT:" lines for survivors (in C), and a SUMMARY line with counts: hits, contain_F7, F7free_P3_violated, survivors,
   survivors_connected, tau_ok. Edges are printed as (a,b,c) with w = NG. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXC 400000
#define MAXP 512
static int NG, T, D, EP;
static uint32_t E[48]; static int ne, neG;
static int deg[32];
static uint32_t covers[MAXC]; static int K;
static int P; static uint32_t pm[MAXP]; static int pa[MAXP], pb[MAXP];
static int chosen[8], nch; static uint32_t usedv;
static unsigned long long nhits, nf7, np3, nsurv, nsurvconn, ntauok, nodes;
static int pair_in_edge(int a, int b) { uint32_t pm2 = (1u << a) | (1u << b); for (int i = 0; i < neG; i++) if ((E[i] & pm2) == pm2) return 1; return 0; }
/* ---- F7 test: some vertex p with >= 3 edges e1,e2,e3 at p (pairs {a_i,b_i}) and two disjoint edges t1,t2 not through p, each meeting
   each e_i in exactly one vertex (t1 takes one of a_i,b_i, t2 the other) */
static int is_edge(uint32_t mask) { for (int i = 0; i < ne; i++) if (E[i] == mask) return 1; return 0; }
static int has_f7(int nv) {
    for (int p = 0; p < nv; p++) {
        int at[16], na = 0; for (int i = 0; i < ne; i++) if (E[i] >> p & 1) at[na++] = i;
        if (na < 3) continue;
        for (int i = 0; i < na; i++) for (int j = i + 1; j < na; j++) for (int k = j + 1; k < na; k++) {
            int pr[3][2]; int es[3] = {at[i], at[j], at[k]};
            for (int q = 0; q < 3; q++) { uint32_t r = E[es[q]] & ~(1u << p); pr[q][0] = __builtin_ctz(r); r &= r - 1; pr[q][1] = __builtin_ctz(r); }
            for (int s2 = 0; s2 < 2; s2++) for (int s3 = 0; s3 < 2; s3++) {
                uint32_t t1 = (1u << pr[0][0]) | (1u << pr[1][s2]) | (1u << pr[2][s3]);
                uint32_t t2 = (1u << pr[0][1]) | (1u << pr[1][1 - s2]) | (1u << pr[2][1 - s3]);
                if (is_edge(t1) && is_edge(t2)) return 1;
            }
        }
    }
    return 0;
}
/* ---- (P3) brute force over all nonempty edge subsets, Gray code */
static int p3_ok_bruteforce(void) {
    int cnt[32]; memset(cnt, 0, sizeof cnt); int nv = 0, nf = 0;
    unsigned long long total = 1ull << ne;
    for (unsigned long long g = 1; g < total; g++) {
        int bit = __builtin_ctzll(g);           /* Gray code: flip edge 'bit' */
        /* gray(g) = g ^ (g>>1); the flipped bit between gray(g-1) and gray(g) is ctz(g) */
        uint32_t em = E[bit]; int adding = !((((g ^ (g >> 1)) >> bit) & 1) == 0);
        /* determine whether edge is being added or removed: state after flip */
        if (adding) { nf++; for (uint32_t r = em; r; r &= r - 1) { int v = __builtin_ctz(r); if (cnt[v]++ == 0) nv++; } }
        else { nf--; for (uint32_t r = em; r; r &= r - 1) { int v = __builtin_ctz(r); if (--cnt[v] == 0) nv--; } }
        if (nf >= 1 && nv < nf + 2) return 0;
    }
    return 1;
}
static int connected_all(int nv) {
    int par[40]; for (int i = 0; i < nv; i++) par[i] = i;
    #define FIND(x) ({ int _x = (x); while (par[_x] != _x) _x = par[_x] = par[par[_x]]; _x; })
    for (int i = 0; i < ne; i++) { int v[3], k = 0; for (uint32_t r = E[i]; r; r &= r - 1) v[k++] = __builtin_ctz(r); par[FIND(v[1])] = FIND(v[0]); par[FIND(v[2])] = FIND(v[0]); }
    int r0 = FIND(0); for (int i = 1; i < nv; i++) if (FIND(i) != r0) return 0; return 1;
}
/* exact tau by brute force: smallest k with a k-subset meeting all edges; we only need to test k = T-1 fails (then tau = T given tau <= T) */
static int no_cover_of_size(int nv, int k) {
    int idx[32]; for (int i = 0; i < k; i++) idx[i] = i;
    while (1) {
        uint32_t S = 0; for (int i = 0; i < k; i++) S |= 1u << idx[i];
        int ok = 1; for (int i = 0; i < ne; i++) if (!(E[i] & S)) { ok = 0; break; }
        if (ok) return 0;
        int i = k - 1; while (i >= 0 && idx[i] == nv - k + i) i--; if (i < 0) return 1;
        idx[i]++; for (int j = i + 1; j < k; j++) idx[j] = idx[j - 1] + 1;
    }
}
static void emit(void) {
    nhits++;
    int nv = NG + 1;
    if (has_f7(nv)) { nf7++; return; }
    if (!p3_ok_bruteforce()) { np3++; return; }
    nsurv++;
    int cn = connected_all(nv); nsurvconn += cn;
    int tauok = no_cover_of_size(nv, T - 1); ntauok += tauok;
    int dmax = 0; for (int v = 0; v < nv; v++) { int d = 0; for (int i = 0; i < ne; i++) d += E[i] >> v & 1; if (d > dmax) dmax = d; }
    printf("HIT:"); for (int i = 0; i < ne; i++) { int v[3], k = 0; for (uint32_t r = E[i]; r; r &= r - 1) v[k++] = __builtin_ctz(r); printf(" (%d,%d,%d)", v[0], v[1], v[2]); }
    printf(" #conn=%d #tauok=%d #maxdeg=%d\n", cn, tauok, dmax);
}

/* ---- search with bitsets.  Covers are re-indexed in order of increasing number of admissible killing pairs (static), and the
   branching cover is the first alive one in this order.  alive: W words over covers; excl: EW words over pairs. */
static int W, EW; static uint64_t *killb;   /* killb[p*W + w] */
static uint64_t alivebuf[12][MAXC / 64 + 1]; static uint64_t exclbuf[12][MAXP / 64 + 1];
static void complete(int start, const uint64_t *excl) {
    if (nch == D) { emit(); return; }
    for (int p = start; p < P; p++) {
        if ((excl[p >> 6] >> (p & 63) & 1) || (pm[p] & usedv)) continue;
        E[ne++] = pm[p] | (1u << NG); usedv |= pm[p]; chosen[nch++] = p;
        complete(p + 1, excl);
        nch--; usedv &= ~pm[p]; ne--;
    }
}
static void search(const uint64_t *alive, const uint64_t *excl) {
    nodes++;
    int c0 = -1; for (int w = 0; w < W; w++) if (alive[w]) { c0 = w * 64 + __builtin_ctzll(alive[w]); break; }
    if (c0 < 0) { complete(0, excl); return; }
    if (nch == D) return;
    uint64_t *ex2 = exclbuf[nch + 1], *al2 = alivebuf[nch + 1];
    memcpy(ex2, excl, sizeof(uint64_t) * EW);
    for (int p = 0; p < P; p++) {
        if (!(killb[(size_t)p * W + (c0 >> 6)] >> (c0 & 63) & 1)) continue;
        if ((ex2[p >> 6] >> (p & 63) & 1) || (pm[p] & usedv)) continue;
        E[ne++] = pm[p] | (1u << NG); usedv |= pm[p]; chosen[nch++] = p;
        for (int w = 0; w < W; w++) al2[w] = alive[w] & ~killb[(size_t)p * W + w];
        search(al2, ex2);
        nch--; usedv &= ~pm[p]; ne--;
        ex2[p >> 6] |= 1ull << (p & 63);
    }
}
int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: xext NG T d EP < inputs\n"); return 1; }
    NG = atoi(argv[1]); T = atoi(argv[2]); D = atoi(argv[3]); EP = atoi(argv[4]);
    int m; unsigned long long graphs = 0, badtau = 0;
    static char line[1 << 15];
    while (fgets(line, sizeof line, stdin)) {
        char *p = line; int k; if (sscanf(p, "%d%n", &m, &k) != 1) continue; p += k;
        ne = 0; memset(deg, 0, sizeof deg);
        for (int i = 0; i < m; i++) { int a, b, c; if (sscanf(p, "%d %d %d%n", &a, &b, &c, &k) != 3) { fprintf(stderr, "bad line\n"); return 2; } p += k;
            if (a < 0 || b < 0 || c < 0 || a >= NG || b >= NG || c >= NG) { fprintf(stderr, "label\n"); return 2; }
            E[ne++] = (1u << a) | (1u << b) | (1u << c); deg[a]++; deg[b]++; deg[c]++; }
        neG = ne; graphs++;
        /* tau(G): no (T-2)-cover, list all (T-1)-covers */
        if (!no_cover_of_size(NG, T - 2)) { badtau++; fprintf(stderr, "graph %llu: tau(G) < T-1\n", graphs); continue; }
        K = 0;
        { int kk = T - 1; int idx[32]; for (int i = 0; i < kk; i++) idx[i] = i;
          while (1) { uint32_t S = 0; for (int i = 0; i < kk; i++) S |= 1u << idx[i];
            int ok = 1; for (int i = 0; i < ne; i++) if (!(E[i] & S)) { ok = 0; break; }
            if (ok) { if (K >= MAXC) { fprintf(stderr, "MAXC\n"); return 3; } covers[K++] = S; }
            int i = kk - 1; while (i >= 0 && idx[i] == NG - kk + i) i--; if (i < 0) break;
            idx[i]++; for (int j = i + 1; j < kk; j++) idx[j] = idx[j - 1] + 1; } }
        if (K == 0) { badtau++; fprintf(stderr, "graph %llu: tau(G) > T-1\n", graphs); continue; }
        P = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > EP || deg[b] > EP || pair_in_edge(a, b)) continue;
            pa[P] = a; pb[P] = b; pm[P] = (1u << a) | (1u << b); P++;
        }
        /* static killer counts and re-indexing of covers (ascending) */
        { static int kc[MAXC], ord[MAXC]; static uint32_t cov2[MAXC];
          for (int c = 0; c < K; c++) { kc[c] = 0; for (int q = 0; q < P; q++) if (!(covers[c] & pm[q])) kc[c]++; ord[c] = c; }
          for (int i = 1; i < K; i++) { int x = ord[i], j = i - 1; while (j >= 0 && kc[ord[j]] > kc[x]) { ord[j + 1] = ord[j]; j--; } ord[j + 1] = x; }
          for (int i = 0; i < K; i++) cov2[i] = covers[ord[i]];
          memcpy(covers, cov2, sizeof(uint32_t) * K); }
        W = (K + 63) / 64; EW = (P + 63) / 64;
        killb = calloc((size_t)P * W, sizeof(uint64_t));
        for (int q = 0; q < P; q++) for (int c = 0; c < K; c++) if (!(covers[c] & pm[q])) killb[(size_t)q * W + (c >> 6)] |= 1ull << (c & 63);
        uint64_t *alive = alivebuf[0], *excl = exclbuf[0]; memset(alive, 0, sizeof(uint64_t) * W); memset(excl, 0, sizeof(uint64_t) * EW);
        for (int c = 0; c < K; c++) alive[c >> 6] |= 1ull << (c & 63);
        nch = 0; usedv = 0;
        search(alive, excl);
        free(killb);
    }
    printf("SUMMARY graphs=%llu bad_tau=%llu nodes=%llu hits=%llu contain_F7=%llu F7free_P3_violated=%llu survivors=%llu survivors_connected=%llu survivors_tau_ok=%llu\n",
           graphs, badtau, nodes, nhits, nf7, np3, nsurv, nsurvconn, ntauok);
    return 0;
}
