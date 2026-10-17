/* ext_r2.c -- referee round 2 (L008), written from scratch.
   Mode EXT:    ext_r2 EXT NG T DMAX < graphs     (lines "FOUND: (a,b,c) ...", a 3-graph G on vertices 0..NG-1)
     For every G and every unordered triple of pairwise disjoint pairs {a_i,b_i} of V(G) such that no pair lies inside an
     edge of G and every a_i,b_i has G-degree <= DMAX-1, forms H = G + {NG,a_i,b_i} (i = 1,2,3) and decides tau(H) >= T by
     testing EVERY vertex subset of size T-1 of V(H) (no branching, no use of transversals of G).  Hits are filtered:
   Mode FILTER: ext_r2 FILTER NV < graphs        (lines "TAG: (a,b,c) ..." with TAG = FOUND or HIT; vertex set 0..NV-1)
   Filters (definitional):
     linear      : two edges share <= 1 vertex;
     F7          : an injective map f from {0..6} to V(H) sending each of 012,034,056,135,246 onto an edge of H
                   (backtracking over all vertex images; no degree-pattern lemma used);
     P3          : e(S) <= |S|-2 for EVERY vertex subset S with |S| >= 2 (all 2^NV subsets);
     survivor    = linear and F7-free and P3.
   Output: "HIT: ... | tau=.. F7=.. P3min=.." lines (EXT mode) or per-graph flags (FILTER mode, with -v), and a summary. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int NE; static uint32_t EM[64]; static int EV[64][3];
static unsigned char isedge[16][16][16];

static void build_lookup(int nv) {
    memset(isedge, 0, sizeof isedge);
    for (int j = 0; j < NE; j++) {
        int a = EV[j][0], b = EV[j][1], c = EV[j][2];
        isedge[a][b][c] = isedge[a][c][b] = isedge[b][a][c] = isedge[b][c][a] = isedge[c][a][b] = isedge[c][b][a] = 1;
    }
    (void)nv;
}
static int is_linear(void) { for (int i = 0; i < NE; i++) for (int j = i + 1; j < NE; j++) if (__builtin_popcount(EM[i] & EM[j]) > 1) return 0; return 1; }
/* F7 by injective homomorphism search */
static int f[7], NVg; static uint32_t usedv;
static int f7_rec(int i) {
    if (i == 7) return 1;
    for (int x = 0; x < NVg; x++) {
        if (usedv >> x & 1) continue;
        f[i] = x;
        int ok = 1;
        if (i == 2) ok = isedge[f[0]][f[1]][f[2]];
        else if (i == 4) ok = isedge[f[0]][f[3]][f[4]];
        else if (i == 5) ok = isedge[f[1]][f[3]][f[5]];
        else if (i == 6) ok = isedge[f[0]][f[5]][f[6]] && isedge[f[2]][f[4]][f[6]];
        if (!ok) continue;
        usedv |= 1u << x;
        if (f7_rec(i + 1)) { usedv &= ~(1u << x); return 1; }
        usedv &= ~(1u << x);
    }
    return 0;
}
static int has_F7(int nv) { NVg = nv; usedv = 0; build_lookup(nv); return f7_rec(0); }
/* P3: min over S, |S|>=2, of |S| - e(S) (must be >= 2) */
static int p3_min(int nv) {
    int best = 99;
    for (uint32_t S = 0; S < (1u << nv); S++) {
        int s = __builtin_popcount(S); if (s < 2) continue;
        int e = 0; for (int j = 0; j < NE; j++) if ((EM[j] & S) == EM[j]) e++;
        if (s - e < best) best = s - e;
    }
    return best;
}
/* tau >= T ?  by testing every (T-1)-subset of the nv vertices */
static int tau_ge(int nv, int T) {
    if (T <= 0) return 1;
    uint32_t all = (NE == 32) ? 0xffffffffu : ((1u << NE) - 1);
    uint32_t vm[32] = {0};
    for (int j = 0; j < NE; j++) for (int t = 0; t < 3; t++) vm[EV[j][t]] |= 1u << j;
    int k = T - 1;
    if (k == 0) return NE > 0;
    if (k > nv) return 0;
    uint32_t S = (1u << k) - 1;
    while (S < (1u << nv)) {
        uint32_t cov = 0; for (uint32_t s = S; s; s &= s - 1) cov |= vm[__builtin_ctz(s)];
        if (cov == all) return 0;          /* a transversal of size T-1 exists */
        uint32_t c = S & -S, r = S + c; S = (((r ^ S) >> 2) / c) | r;
    }
    return 1;
}
static int tau_exact(int nv) { int t = 0; while (tau_ge(nv, t + 1)) t++; return t; }
static int parse(char *p) {
    NE = 0; int mx = -1;
    while ((p = strchr(p, '('))) {
        int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) != 3) break;
        EV[NE][0] = a; EV[NE][1] = b; EV[NE][2] = c; EM[NE] = (1u << a) | (1u << b) | (1u << c); NE++;
        if (a > mx) mx = a; if (b > mx) mx = b; if (c > mx) mx = c; p++;
    }
    return mx;
}
int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage\n"); return 1; }
    char line[8192];
    if (!strcmp(argv[1], "FILTER")) {
        int NV = atoi(argv[2]); int verbose = argc > 3;
        unsigned long long tot = 0, lin = 0, f7 = 0, p3bad = 0, surv = 0, f7free_p3bad = 0; int tmin = 99, tmax = -1;
        while (fgets(line, sizeof line, stdin)) {
            char *c = strchr(line, ':'); if (!c) continue;
            if (strncmp(line, "FOUND", 5) && strncmp(line, "HIT", 3) && strncmp(line, "G", 1)) continue;
            int mx = parse(c + 1); if (mx < 0) continue;
            int nv = NV ? NV : mx + 1;
            tot++; int L = is_linear(); int F = has_F7(nv); int P = p3_min(nv); int t = tau_exact(nv);
            lin += L; f7 += F; p3bad += (P < 2); f7free_p3bad += (!F && P < 2); if (L && !F && P >= 2) surv++;
            if (t < tmin) tmin = t; if (t > tmax) tmax = t;
            if (verbose) printf("GRAPH %llu linear=%d F7=%d P3min=%d tau=%d\n", tot, L, F, P, t);
        }
        printf("FILTER_SUMMARY total=%llu linear=%llu F7=%llu P3_violated=%llu F7free_P3_violated=%llu survivors=%llu tau_range=[%d,%d]\n",
               tot, lin, f7, p3bad, f7free_p3bad, surv, tmin, tmax);
        return 0;
    }
    /* EXT mode */
    int NG = atoi(argv[2]), T = atoi(argv[3]), DMAX = atoi(argv[4]);
    unsigned long long graphs = 0, tested = 0, hits = 0, hf7 = 0, hp3 = 0, hsurv = 0, hf7free_p3 = 0;
    while (fgets(line, sizeof line, stdin)) {
        if (strncmp(line, "FOUND:", 6)) continue;
        parse(line + 6);
        int ne0 = NE; uint32_t EM0[64]; int EV0[64][3];
        memcpy(EM0, EM, sizeof EM); memcpy(EV0, EV, sizeof EV);
        graphs++;
        int deg[32] = {0}; for (int j = 0; j < ne0; j++) for (int t = 0; t < 3; t++) deg[EV0[j][t]]++;
        int pa[256], pb[256], np = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > DMAX - 1 || deg[b] > DMAX - 1) continue;
            int inside = 0; for (int j = 0; j < ne0; j++) if ((EM0[j] >> a & 1) && (EM0[j] >> b & 1)) inside = 1;
            if (inside) continue;
            pa[np] = a; pb[np] = b; np++;
        }
        for (int x = 0; x < np; x++) for (int y = x + 1; y < np; y++) for (int z = y + 1; z < np; z++) {
            int vs[6] = { pa[x], pb[x], pa[y], pb[y], pa[z], pb[z] }; int dis = 1;
            for (int u = 0; u < 6 && dis; u++) for (int w = u + 1; w < 6; w++) if (vs[u] == vs[w]) { dis = 0; break; }
            if (!dis) continue;
            tested++;
            NE = ne0; memcpy(EM, EM0, sizeof EM); memcpy(EV, EV0, sizeof EV);
            int pr[3][2] = { { pa[x], pb[x] }, { pa[y], pb[y] }, { pa[z], pb[z] } };
            for (int i = 0; i < 3; i++) { EV[NE][0] = NG; EV[NE][1] = pr[i][0]; EV[NE][2] = pr[i][1]; EM[NE] = (1u << NG) | (1u << pr[i][0]) | (1u << pr[i][1]); NE++; }
            if (!tau_ge(NG + 1, T)) continue;
            hits++;
            int L = is_linear(), F = has_F7(NG + 1), P = p3_min(NG + 1);
            if (!L) { fprintf(stderr, "nonlinear extension?\n"); return 4; }
            hf7 += F; hp3 += (P < 2); hf7free_p3 += (!F && P < 2); if (!F && P >= 2) hsurv++;
            printf("HIT:"); for (int j = 0; j < NE; j++) printf(" (%d,%d,%d)", EV[j][0], EV[j][1], EV[j][2]);
            printf(" | tau=%d F7=%d P3min=%d\n", tau_exact(NG + 1), F, P);
        }
    }
    printf("EXT_SUMMARY graphs=%llu tested=%llu hits=%llu F7=%llu P3_violated=%llu F7free_P3_violated=%llu survivors=%llu\n",
           graphs, tested, hits, hf7, hp3, hf7free_p3, hsurv);
    return 0;
}
