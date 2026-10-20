/* ext_d.c (prover, certificate L012) -- re-insertion of one vertex of degree d.
   Usage: ext_d NG TG T d EP [noprune] < input        input lines "m a1 b1 c1 ... " (a 3-graph G on vertices 0..NG-1)
   For each G: checks tau(G) = TG exactly (no (TG-1)-subset of the NG vertices meets every edge, some TG-subset does; Gosper
   enumeration of all subsets of these two sizes) and lists ALL TG-subsets meeting every edge (the minimum covers).  Admissible pairs:
   {a,b}, a<b<NG, not inside an edge of G, both of G-degree <= EP.  A d-set S of pairwise disjoint admissible pairs defines
   H = G + {NG,a,b} ({a,b} in S); H is linear.
   - if TG >= T: every S is a hit (tau(H) >= tau(G) >= T);
   - if TG == T-1: S is a hit iff every minimum cover of G is disjoint from some pair of S (a cover of H of size <= TG cannot contain
     NG, so it is a TG-cover of G meeting every pair of S);
   - if TG < T-1: no hit.
   Enumeration ("kill" search with exclusion): at a node, let c0 be the first minimum cover not yet disjoint from a chosen pair; the
   hit must contain a pair disjoint from c0; branch over these pairs p_1 < p_2 < ... (disjoint from the chosen pairs), and in branch i
   forbid p_1..p_{i-1} in the whole subtree; when no cover is left, the remaining pairs are chosen freely (increasing index, not
   forbidden).  Every hit S is produced exactly once (in the branch of the smallest-index pair of S disjoint from c0, inductively).
   Pruning (unless 'noprune'): a branch is cut when the new edge lies in a copy of F7 (incremental test; valid because F7-containment
   is inherited by supersets and G is F7-free).  Finals: (P3) by the Hall test (as in filt.c); prints the hits in C as "HIT:" lines
   (with 'noprune': all hits, no P3 test) and a SUMMARY. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXC 262144
#define MAXP 256
static int NG, TG, T, D, EP, PRUNE = 1;
static uint32_t E[40]; static int ne;                 /* current edge masks (G edges, then new edges) */
static signed char pe[32][32];                         /* pair -> edge index, -1 if none (linear graphs) */
static uint32_t covers[MAXC]; static int K, W;
static int P; static int pa[MAXP], pb[MAXP]; static uint32_t pm[MAXP];
static uint64_t *killb;                                /* killb[p*W + w]: covers disjoint from pair p */
static unsigned long long nodes, nfinal, nfinalC, tested_graphs, bad_tau, nohit_graphs, ncovmax;
static int chosen[8], nch;
static void add_edge(uint32_t m) { int v[3], k = 0; for (uint32_t r = m; r; r &= r - 1) v[k++] = __builtin_ctz(r);
    pe[v[0]][v[1]] = pe[v[1]][v[0]] = pe[v[0]][v[2]] = pe[v[2]][v[0]] = pe[v[1]][v[2]] = pe[v[2]][v[1]] = (signed char)ne; E[ne++] = m; }
static void del_edge(void) { uint32_t m = E[--ne]; int v[3], k = 0; for (uint32_t r = m; r; r &= r - 1) v[k++] = __builtin_ctz(r);
    pe[v[0]][v[1]] = pe[v[1]][v[0]] = pe[v[0]][v[2]] = pe[v[2]][v[0]] = pe[v[1]][v[2]] = pe[v[2]][v[1]] = -1; }
static int is_edge3(int x, int y, int z) { int f = pe[x][y]; return f >= 0 && (E[f] >> z & 1); }
static int third(int f, int u, int v) { uint32_t r = E[f] & ~(1u << u) & ~(1u << v); return __builtin_ctz(r); }
/* does the LAST edge of E lie in a copy of F7 inside E? */
static int f7_last(void) {
    int e = ne - 1; uint32_t me = E[e]; int x[3], k = 0; for (uint32_t r = me; r; r &= r - 1) x[k++] = __builtin_ctz(r);
    /* case A: e passes through the centre p */
    for (int i = 0; i < 3; i++) {
        int p = x[i], a1 = x[(i + 1) % 3], b1 = x[(i + 2) % 3];
        int at[8], na = 0; for (int f = 0; f < ne; f++) if (f != e && (E[f] >> p & 1)) at[na++] = f;
        for (int s = 0; s < na; s++) for (int t = s + 1; t < na; t++) {
            uint32_t r2 = E[at[s]] & ~(1u << p), r3 = E[at[t]] & ~(1u << p);
            int a2 = __builtin_ctz(r2), b2 = 31 - __builtin_clz(r2), a3 = __builtin_ctz(r3), b3 = 31 - __builtin_clz(r3);
            for (int s2 = 0; s2 < 2; s2++) for (int s3 = 0; s3 < 2; s3++) {
                int u2 = s2 ? b2 : a2, v2 = s2 ? a2 : b2, u3 = s3 ? b3 : a3, v3 = s3 ? a3 : b3;
                if (is_edge3(a1, u2, u3) && is_edge3(b1, v2, v3)) return 1;
            }
        }
    }
    /* case B: e is a transversal {x1,x2,x3}; centre p outside e, edges {p,x_i,y_i}, and {y1,y2,y3} an edge */
    for (int f = 0; f < ne; f++) {
        if (f == e || !(E[f] >> x[0] & 1)) continue;
        uint32_t r = E[f] & ~(1u << x[0]);
        for (; r; r &= r - 1) {
            int p = __builtin_ctz(r); if (me >> p & 1) continue;
            int f2 = pe[p][x[1]], f3 = pe[p][x[2]]; if (f2 < 0 || f3 < 0) continue;
            int y1 = third(f, p, x[0]), y2 = third(f2, p, x[1]), y3 = third(f3, p, x[2]);
            uint32_t all = (1u << p) | me | (1u << y1) | (1u << y2) | (1u << y3);
            if (__builtin_popcount(all) != 7) continue;
            if (is_edge3(y1, y2, y3)) return 1;
        }
    }
    return 0;
}
static int owner[32]; static uint32_t forbidv;
static int augment(int e, uint32_t *seen) {
    for (uint32_t r = E[e] & ~forbidv & ~*seen; r; r &= r - 1) { int v = __builtin_ctz(r); *seen |= 1u << v;
        if (owner[v] < 0 || augment(owner[v], seen)) { owner[v] = e; return 1; } }
    return 0;
}
static int p3_ok(void) {
    uint32_t used = 0; for (int i = 0; i < ne; i++) used |= E[i];
    for (int x = 0; x < 32; x++) if (used >> x & 1) for (int y = x + 1; y < 32; y++) if (used >> y & 1) {
        forbidv = (1u << x) | (1u << y); for (int v = 0; v < 32; v++) owner[v] = -1;
        for (int e = 0; e < ne; e++) { uint32_t seen = 0; if (!augment(e, &seen)) return 0; } }
    return 1;
}
static int neG;
static void emit(void) {
    nfinal++;
    if (PRUNE) { if (!p3_ok()) return; nfinalC++; } else nfinalC++;
    printf("HIT:");
    for (int i = 0; i < ne; i++) { int v[3], k = 0; for (uint32_t r = E[i]; r; r &= r - 1) v[k++] = __builtin_ctz(r); printf(" (%d,%d,%d)", v[0], v[1], v[2]); }
    printf("\n");
}
static uint32_t usedv;
static int forb_has(const uint64_t *fb, int p) { return fb[p >> 6] >> (p & 63) & 1; }
static void freecomp(int start, const uint64_t *fb) {
    if (nch == D) { emit(); return; }
    for (int p = start; p < P; p++) {
        if (forb_has(fb, p) || (pm[p] & usedv)) continue;
        add_edge(pm[p] | (1u << NG)); usedv |= pm[p]; chosen[nch++] = p;
        if (!PRUNE || !f7_last()) freecomp(p + 1, fb);
        nch--; usedv &= ~pm[p]; del_edge();
    }
}
static uint64_t alivebuf[10][MAXC / 64];
static void kill(const uint64_t *alive, const uint64_t *fb) {
    nodes++;
    int c0 = -1; for (int w = 0; w < W; w++) if (alive[w]) { c0 = w * 64 + __builtin_ctzll(alive[w]); break; }
    if (c0 < 0) { freecomp(0, fb); return; }
    if (nch == D) return;
    uint64_t fb2[MAXP / 64]; memcpy(fb2, fb, sizeof fb2);
    uint64_t *al2 = alivebuf[nch + 1];
    for (int p = 0; p < P; p++) {
        if (!(killb[(size_t)p * W + (c0 >> 6)] >> (c0 & 63) & 1)) continue;   /* p must be disjoint from c0 */
        if (forb_has(fb2, p) || (pm[p] & usedv)) continue;
        add_edge(pm[p] | (1u << NG)); usedv |= pm[p]; chosen[nch++] = p;
        if (!PRUNE || !f7_last()) {
            for (int w = 0; w < W; w++) al2[w] = alive[w] & ~killb[(size_t)p * W + w];
            kill(al2, fb2);
        }
        nch--; usedv &= ~pm[p]; del_edge();
        fb2[p >> 6] |= 1ull << (p & 63);                /* forbid p in the later sibling branches */
    }
}
int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: ext_d NG TG T d EP [noprune]\n"); return 1; }
    NG = atoi(argv[1]); TG = atoi(argv[2]); T = atoi(argv[3]); D = atoi(argv[4]); EP = atoi(argv[5]);
    if (argc > 6 && !strcmp(argv[6], "noprune")) PRUNE = 0;
    if (NG > 31 || D > 8) { fprintf(stderr, "limits\n"); return 1; }
    killb = malloc(sizeof(uint64_t) * (size_t)MAXP * (MAXC / 64));
    int m; unsigned long long graphs = 0, totnodes = 0, totfinal = 0, totC = 0;
    while (scanf("%d", &m) == 1) {
        graphs++; ne = 0; memset(pe, -1, sizeof pe); int deg[32] = {0};
        for (int i = 0; i < m; i++) { int a, b, c; if (scanf("%d %d %d", &a, &b, &c) != 3) return 2;
            if (a >= NG || b >= NG || c >= NG) { fprintf(stderr, "label\n"); return 2; }
            add_edge((1u << a) | (1u << b) | (1u << c)); deg[a]++; deg[b]++; deg[c]++; }
        neG = ne;
        /* tau(G) = TG exactly, and all TG-covers */
        int small = 0; K = 0;
        for (int s = TG - 1; s <= TG; s++) {
            if (s < 0) continue;
            if (s == 0) { if (m == 0) { if (s == TG - 1) small = 1; else covers[K++] = 0; } continue; }
            uint32_t S = (1u << s) - 1, lim = (1u << NG) - 1;
            while (S <= lim) {
                int ok = 1; for (int i = 0; i < m; i++) if (!(E[i] & S)) { ok = 0; break; }
                if (ok) { if (s == TG - 1) { small = 1; break; } if (K >= MAXC) { fprintf(stderr, "MAXC\n"); return 3; } covers[K++] = S; }
                uint32_t c = S & -S, r = S + c; if (r == 0) break; S = (((r ^ S) >> 2) / c) | r;
            }
            if (small) break;
        }
        if (small || K == 0) { bad_tau++; continue; }
        if (TG < T - 1) { nohit_graphs++; continue; }
        if ((unsigned long long)K > ncovmax) ncovmax = K;
        P = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > EP || deg[b] > EP || pe[a][b] >= 0) continue;
            if (P >= MAXP) { fprintf(stderr, "MAXP\n"); return 4; }
            pa[P] = a; pb[P] = b; pm[P] = (1u << a) | (1u << b); P++;
        }
        uint64_t fb[MAXP / 64]; memset(fb, 0, sizeof fb);
        nodes = 0; nfinal = 0; nfinalC = 0; nch = 0; usedv = 0;
        if (TG >= T) { freecomp(0, fb); }
        else {
            W = (K + 63) / 64;
            for (int p = 0; p < P; p++) { uint64_t *row = killb + (size_t)p * W; memset(row, 0, sizeof(uint64_t) * W);
                for (int c = 0; c < K; c++) if (!(covers[c] & pm[p])) row[c >> 6] |= 1ull << (c & 63); }
            uint64_t *alive = alivebuf[0]; memset(alive, 0, sizeof(uint64_t) * W); for (int c = 0; c < K; c++) alive[c >> 6] |= 1ull << (c & 63);
            kill(alive, fb);
        }
        tested_graphs++; totnodes += nodes; totfinal += nfinal; totC += nfinalC;
    }
    printf("SUMMARY graphs=%llu bad_tau=%llu tg_too_small=%llu searched=%llu max_min_covers=%llu nodes=%llu hits%s=%llu %s=%llu\n",
           graphs, bad_tau, nohit_graphs, tested_graphs, ncovmax, totnodes, PRUNE ? "_F7free" : "_all", totfinal, PRUNE ? "hits_in_C" : "printed", totC);
    return 0;
}
