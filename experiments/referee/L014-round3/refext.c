/* refext.c -- referee (L014 round 3): independent check of the final extension step.
   usage: refext NG TG T d EP [sample_every] < inputs      (L014 top cell: refext 22 9 10 3 2)
   Input lines: "m a1 b1 c1 ... " = a 3-graph G on vertices 0..NG-1.
   For every G:  linear? labels ok?  tau(G) by exact branching (must equal TG); ALL TG-covers by branching + dedupe
   (every minimal cover is reached: branch on the vertices of the first uncovered edge);  admissible pairs {a,b}: deg<=EP, not
   inside an edge;  ALL d-sets of pairwise disjoint admissible pairs by plain nested enumeration (no kill search, no pruning);
   S is a hit iff every TG-cover of G misses some pair of S (then tau(H) = TG+1 = T, H = G + {NG,a,b}); for every hit tau(H) is
   recomputed exactly by branching.  Each hit is classified: connected on NG+1 vertices; F7 by an EXPLICIT embedding
   (centre p, three edges {p,a_i,b_i} at p, two disjoint edges each meeting every pair {a_i,b_i} in exactly one vertex);
   (P3) by Hall's test for every pair {x,y}, and on failure an explicit set S with e(S) >= |S|-1 is extracted and verified by counting.
   If sample_every > 0, for every input with index % sample_every == 0 EVERY d-set (hit or not) is also decided by the exact tau
   computation and compared with the cover criterion.  Prints one line per hit and a SUMMARY. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXE 40
#define MAXCOV 100000
static int NG, TG, T, D, EP, SAMPLE = 0;
static uint32_t E[MAXE]; static int ne;
static uint32_t covers[MAXCOV]; static int K;
/* exact: cover of size <= k containing 'chosen' (already |chosen| counted outside) */
static int cover_le(const uint32_t *Ed, int n, uint32_t chosen, int k) {
    int i; for (i = 0; i < n; i++) if (!(Ed[i] & chosen)) break;
    if (i == n) return 1;
    if (k <= 0) return 0;
    for (uint32_t r = Ed[i]; r; r &= r - 1) { int v = __builtin_ctz(r); if (cover_le(Ed, n, chosen | (1u << v), k - 1)) return 1; }
    return 0;
}
static int tau_exact(const uint32_t *Ed, int n) { int k = 0; while (!cover_le(Ed, n, 0, k)) k++; return k; }
static void enum_covers(uint32_t chosen, int cnt) {
    int i; for (i = 0; i < ne; i++) if (!(E[i] & chosen)) break;
    if (i == ne) { if (cnt == TG) { if (K >= MAXCOV) { fprintf(stderr, "MAXCOV\n"); exit(9); } covers[K++] = chosen; } return; }
    if (cnt >= TG) return;
    for (uint32_t r = E[i]; r; r &= r - 1) { int v = __builtin_ctz(r); enum_covers(chosen | (1u << v), cnt + 1); }
}
static int cmpu(const void *a, const void *b) { uint32_t x = *(const uint32_t *)a, y = *(const uint32_t *)b; return x < y ? -1 : x > y; }
/* ---- classification of H (edges HE[0..nh-1], NV vertices) ---- */
static int connected(const uint32_t *HE, int nh, int NV) {
    uint32_t all = (1u << NV) - 1, comp = 1u, prev = 0;
    while (comp != prev) { prev = comp; for (int i = 0; i < nh; i++) if (HE[i] & comp) comp |= HE[i]; }
    return comp == all;
}
static int is_edge(const uint32_t *HE, int nh, uint32_t m) { for (int i = 0; i < nh; i++) if (HE[i] == m) return 1; return 0; }
static int has_f7(const uint32_t *HE, int nh, int NV, char *why) {
    for (int p = 0; p < NV; p++) {
        int at[MAXE], na = 0; for (int i = 0; i < nh; i++) if (HE[i] >> p & 1) at[na++] = i;
        for (int i = 0; i < na; i++) for (int j = i + 1; j < na; j++) for (int k = j + 1; k < na; k++) {
            uint32_t r1 = HE[at[i]] & ~(1u << p), r2 = HE[at[j]] & ~(1u << p), r3 = HE[at[k]] & ~(1u << p);
            int a1 = __builtin_ctz(r1), b1 = 31 - __builtin_clz(r1), a2 = __builtin_ctz(r2), b2 = 31 - __builtin_clz(r2), a3 = __builtin_ctz(r3), b3 = 31 - __builtin_clz(r3);
            if (__builtin_popcount(r1 | r2 | r3) != 6) continue;   /* linear => always 6 */
            for (int s2 = 0; s2 < 2; s2++) for (int s3 = 0; s3 < 2; s3++) {
                int u2 = s2 ? b2 : a2, v2 = s2 ? a2 : b2, u3 = s3 ? b3 : a3, v3 = s3 ? a3 : b3;
                uint32_t t1 = (1u << a1) | (1u << u2) | (1u << u3), t2 = (1u << b1) | (1u << v2) | (1u << v3);
                if (is_edge(HE, nh, t1) && is_edge(HE, nh, t2)) {
                    if (why) sprintf(why, "F7 centre %d pairs (%d,%d)(%d,%d)(%d,%d) transversals {%d,%d,%d} {%d,%d,%d}", p, a1, b1, a2, b2, a3, b3, a1, u2, u3, b1, v2, v3);
                    return 1;
                }
            }
        }
    }
    return 0;
}
static int owner[32]; static uint32_t forbidv, seenv; static const uint32_t *HEg; static int nhg;
static int augment(int e) {
    for (uint32_t r = HEg[e] & ~forbidv & ~seenv; r; r &= r - 1) { int v = __builtin_ctz(r); seenv |= 1u << v;
        if (owner[v] < 0 || augment(owner[v])) { owner[v] = e; return 1; } }
    return 0;
}
/* returns 1 if (P3) holds; else 0 and writes a violating set S (with e(S) >= |S|-1 verified by counting) */
static int p3_ok(const uint32_t *HE, int nh, int NV, uint32_t *Sout) {
    HEg = HE; nhg = nh;
    for (int x = 0; x < NV; x++) for (int y = x + 1; y < NV; y++) {
        forbidv = (1u << x) | (1u << y); for (int v = 0; v < 32; v++) owner[v] = -1;
        for (int e = 0; e < nh; e++) { seenv = 0; if (!augment(e)) {
            uint32_t S = seenv | forbidv; int cnt = 0; for (int i = 0; i < nh; i++) if ((HE[i] & S) == HE[i]) cnt++;
            if (cnt < __builtin_popcount(S) - 1) { fprintf(stderr, "internal: Hall violator not verified\n"); exit(8); }
            *Sout = S; return 0; } }
    }
    return 1;
}
int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage\n"); return 1; }
    NG = atoi(argv[1]); TG = atoi(argv[2]); T = atoi(argv[3]); D = atoi(argv[4]); EP = atoi(argv[5]); if (argc > 6) SAMPLE = atoi(argv[6]);
    if (NG > 30 || D != 3) { fprintf(stderr, "this referee program handles d=3 only, NG<=30\n"); return 1; }
    int m; unsigned long long graphs = 0, hits = 0, hitsC = 0, hitsF7 = 0, hitsP3 = 0, hitsConn = 0, hitsDisc = 0, hitsF7freeConn = 0, trip = 0, badtau = 0;
    unsigned long long sampled_inputs = 0, sampled_sets = 0, sample_mismatch = 0; int maxK = 0, maxP = 0;
    static uint64_t miss[256][MAXCOV / 64 + 1];
    while (scanf("%d", &m) == 1) {
        if (m > MAXE - 8) { fprintf(stderr, "too many edges\n"); return 2; }
        ne = 0; int deg[32] = {0}; uint32_t inedge[32] = {0};
        for (int i = 0; i < m; i++) { int a, b, c; if (scanf("%d %d %d", &a, &b, &c) != 3) return 2;
            if (a < 0 || b < 0 || c < 0 || a >= NG || b >= NG || c >= NG || a == b || a == c || b == c) { fprintf(stderr, "bad label\n"); return 2; }
            E[ne++] = (1u << a) | (1u << b) | (1u << c); deg[a]++; deg[b]++; deg[c]++;
            inedge[a] |= (1u << b) | (1u << c); inedge[b] |= (1u << a) | (1u << c); inedge[c] |= (1u << a) | (1u << b); }
        for (int i = 0; i < ne; i++) for (int j = i + 1; j < ne; j++) if (__builtin_popcount(E[i] & E[j]) >= 2) { fprintf(stderr, "input not linear\n"); return 3; }
        graphs++;
        int tG = tau_exact(E, ne); if (tG != TG) { badtau++; fprintf(stderr, "bad tau %d at graph %llu\n", tG, graphs); continue; }
        K = 0; enum_covers(0, 0); qsort(covers, K, sizeof covers[0], cmpu);
        int K2 = 0; for (int i = 0; i < K; i++) if (i == 0 || covers[i] != covers[i - 1]) covers[K2++] = covers[i]; K = K2;
        if (K > maxK) maxK = K;
        for (int c = 0; c < K; c++) { if (__builtin_popcount(covers[c]) != TG) { fprintf(stderr, "cover size\n"); return 4; }
            for (int i = 0; i < ne; i++) if (!(E[i] & covers[c])) { fprintf(stderr, "not a cover\n"); return 4; } }
        int P = 0; int pa[256], pb[256]; uint32_t pm[256];
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > EP || deg[b] > EP || (inedge[a] >> b & 1)) continue;
            if (P >= 256) { fprintf(stderr, "too many pairs\n"); return 5; }
            pa[P] = a; pb[P] = b; pm[P] = (1u << a) | (1u << b); P++; }
        if (P > maxP) maxP = P;
        int W = (K + 63) / 64; uint64_t allm[MAXCOV / 64 + 1];
        for (int w = 0; w < W; w++) allm[w] = 0; for (int c = 0; c < K; c++) allm[c >> 6] |= 1ull << (c & 63);
        for (int p = 0; p < P; p++) { for (int w = 0; w < W; w++) miss[p][w] = 0; for (int c = 0; c < K; c++) if (!(covers[c] & pm[p])) miss[p][c >> 6] |= 1ull << (c & 63); }
        int dosample = SAMPLE > 0 && (graphs % SAMPLE) == 0; if (dosample) sampled_inputs++;
        for (int i = 0; i < P; i++) for (int j = i + 1; j < P; j++) { if (pm[i] & pm[j]) continue;
            for (int k = j + 1; k < P; k++) { if ((pm[i] | pm[j]) & pm[k]) continue;
                trip++;
                int hit = 1; for (int w = 0; w < W; w++) if ((miss[i][w] | miss[j][w] | miss[k][w]) != allm[w]) { hit = 0; break; }
                uint32_t HE[MAXE]; int nh = ne; memcpy(HE, E, sizeof(uint32_t) * ne);
                HE[nh++] = pm[i] | (1u << NG); HE[nh++] = pm[j] | (1u << NG); HE[nh++] = pm[k] | (1u << NG);
                if (dosample) { sampled_sets++; int tH = tau_exact(HE, nh); if ((tH >= T) != hit) sample_mismatch++; }
                if (!hit) continue;
                hits++;
                int tH = tau_exact(HE, nh); if (tH < T) { fprintf(stderr, "hit with tau(H)=%d < T\n", tH); return 6; }
                int cn = connected(HE, nh, NG + 1); char why[200] = ""; int f7 = has_f7(HE, nh, NG + 1, why); uint32_t S = 0; int p3 = p3_ok(HE, nh, NG + 1, &S);
                hitsF7 += f7; hitsP3 += !p3; hitsConn += cn; hitsDisc += !cn; if (!f7 && cn) hitsF7freeConn++;
                if (!f7 && p3 && cn) hitsC++;
                printf("HIT g=%llu pairs (%d,%d)(%d,%d)(%d,%d) tauH=%d conn=%d f7=%d p3=%d", graphs, pa[i], pb[i], pa[j], pb[j], pa[k], pb[k], tH, cn, f7, p3);
                if (f7) printf(" [%s]", why);
                if (!p3) { printf(" [P3 violator S={"); int f = 1; for (int v = 0; v < NG + 1; v++) if (S >> v & 1) { printf(f ? "%d" : ",%d", v); f = 0; } int cnt = 0; for (int q = 0; q < nh; q++) if ((HE[q] & S) == HE[q]) cnt++; printf("} |S|=%d e(S)=%d]", __builtin_popcount(S), cnt); }
                printf("\n");
            } }
    }
    printf("SUMMARY graphs=%llu bad_tau=%llu max_covers=%d max_pairs=%d disjoint_triples=%llu hits_tau_ge_T=%llu hits_F7=%llu hits_P3_violated=%llu hits_connected=%llu hits_disconnected=%llu hits_F7free_connected=%llu MEMBERS_OF_C_CONNECTED=%llu sampled_inputs=%llu sampled_sets=%llu sample_mismatch=%llu\n",
           graphs, badtau, maxK, maxP, trip, hits, hitsF7, hitsP3, hitsConn, hitsDisc, hitsF7freeConn, hitsC, sampled_inputs, sampled_sets, sample_mismatch);
    return 0;
}
