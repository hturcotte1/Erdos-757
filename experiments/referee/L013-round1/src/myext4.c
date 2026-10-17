/* Referee L013 round 1: own extension program (independent of ext_d).
   Usage: myext NG t d D < inputs     (input lines: "k a1 b1 c1 ... ak bk ck", vertices 0..NG-1)
   For each input G (tau(G) is recomputed and must be t-1): enumerate ALL sets of d pairwise disjoint pairs {a,b} of vertices of G
   with {a,b} not inside an edge of G and deg_G(a), deg_G(b) <= d-1, such that X = G + w + {w,a_i,b_i} has tau(X) >= t
   (equivalently every (t-1)-cover of G misses some pair; all (t-1)-covers of G are enumerated, then a branching on the
   first not-yet-missed cover); each such X has tau(X) = t, which is re-checked by an exact cover search.
   Then: connected?, F7-free?, (P3)?, Delta <= D?  Prints HIT lines for X connected, in C, tau = t, Delta <= D, and a summary. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXV 32
#define MAXE 48
typedef unsigned int u32;
static int NG, T, d, Dmax;
static int nE; static int E[MAXE][3];
static u32 emask[MAXE];          /* vertex mask of edge */
static int degG[MAXV];
/* covers */
static u32 *covers; static int ncov, capcov;
static u32 *hs; static unsigned long hcap;
static int hins(u32 x) { unsigned long h = (x * 2654435761u) & (hcap - 1); while (hs[h]) { if (hs[h] == x) return 0; h = (h + 1) & (hcap - 1); } hs[h] = x; return 1; }
static void gen_covers(u32 chosen, int k) {
    /* find first edge not hit by chosen */
    int e; for (e = 0; e < nE; e++) if (!(emask[e] & chosen)) break;
    if (e == nE) { if (__builtin_popcount(chosen) == T - 1) { if (hins(chosen + 1)) { if (ncov == capcov) { capcov = capcov ? 2 * capcov : 1024; covers = realloc(covers, capcov * sizeof(u32)); } covers[ncov++] = chosen; } } return; }
    if (k == 0) return;
    for (int i = 0; i < 3; i++) gen_covers(chosen | (1u << E[e][i]), k - 1);
}
static int has_cover_X(int nx, int ne, int (*X)[3], u32 mask_edges_unc_dummy, int k);
/* generic exact cover check on edge list */
static int XE[MAXE][3]; static int nXE; static unsigned long long vinc[MAXV + 1];
static int hc(unsigned long long mask, int k) {
    if (!mask) return 1; if (!k) return 0;
    /* greedy disjoint lower bound */
    u32 used = 0; int c = 0;
    for (int e = 0; e < nXE; e++) if (mask >> e & 1) { u32 vs = (1u << XE[e][0]) | (1u << XE[e][1]) | (1u << XE[e][2]); if (!(vs & used)) { used |= vs; c++; } }
    if (c > k) return 0;
    int e = __builtin_ctzll(mask);
    for (int i = 0; i < 3; i++) if (hc(mask & ~vinc[XE[e][i]], k - 1)) return 1;
    return 0;
}
static int tauX(int nv) {
    memset(vinc, 0, sizeof vinc);
    for (int e = 0; e < nXE; e++) for (int i = 0; i < 3; i++) vinc[XE[e][i]] |= 1ULL << e;
    unsigned long long all = (nXE == 64) ? ~0ULL : ((1ULL << nXE) - 1);
    for (int k = 0; k <= nXE; k++) if (hc(all, k)) return k;
    return nXE;
}
static int isedgeX(int a, int b, int c) { return (vinc[a] & vinc[b] & vinc[c]) != 0; }
static int hasF7X(int nv) {
    for (int c = 0; c < nv; c++) {
        int inc[MAXE], ni = 0;
        for (int e = 0; e < nXE; e++) if (vinc[c] >> e & 1) inc[ni++] = e;
        for (int x = 0; x < ni; x++) for (int y = x + 1; y < ni; y++) for (int z = y + 1; z < ni; z++) {
            int P[3][2]; int es[3] = {inc[x], inc[y], inc[z]};
            for (int r = 0; r < 3; r++) { int q = 0; for (int i = 0; i < 3; i++) if (XE[es[r]][i] != c) P[r][q++] = XE[es[r]][i]; }
            for (int a = 0; a < 2; a++) for (int b = 0; b < 2; b++) for (int g = 0; g < 2; g++)
                if (isedgeX(P[0][a], P[1][b], P[2][g]) && isedgeX(P[0][1 - a], P[1][1 - b], P[2][1 - g])) return 1;
        }
    }
    return 0;
}
static int matchV[MAXV + 1], seenV[MAXV + 1], stampc, fu, fv;
static int tryE(int e) { for (int i = 0; i < 3; i++) { int v = XE[e][i]; if (v == fu || v == fv || seenV[v] == stampc) continue; seenV[v] = stampc; if (matchV[v] < 0 || tryE(matchV[v])) { matchV[v] = e; return 1; } } return 0; }
static int P3X(int nv) {
    if (nXE > nv - 2) return 0;
    for (fu = 0; fu < nv; fu++) for (fv = fu + 1; fv < nv; fv++) {
        for (int i = 0; i < nv; i++) matchV[i] = -1;
        for (int e = 0; e < nXE; e++) { stampc++; if (!tryE(e)) return 0; }
    }
    return 1;
}
static int connX(int nv) {
    int seen[MAXV + 1] = {0}, st[MAXV + 1], sp = 0, cnt = 1; seen[0] = 1; st[sp++] = 0;
    while (sp) { int v = st[--sp]; for (int e = 0; e < nXE; e++) if (vinc[v] >> e & 1) for (int i = 0; i < 3; i++) { int w = XE[e][i]; if (!seen[w]) { seen[w] = 1; cnt++; st[sp++] = w; } } }
    return cnt == nv;
}
static int linX(void) { for (int a = 0; a < nXE; a++) for (int b = a + 1; b < nXE; b++) { int c = 0; for (int i = 0; i < 3; i++) for (int j = 0; j < 3; j++) if (XE[a][i] == XE[b][j]) c++; if (c > 1) return 0; } return 1; }
/* pairs */
static int np; static int PA[600], PB[600]; static u32 PM[600];
static int chosen[8];
static long long cnt_connF7free, cnt_connP3fail; static long long cnt_sets, cnt_conn, cnt_f7free, cnt_inC, cnt_hit, cnt_tauerr, cnt_dup;
static long long ginputs, gbadtau;
/* dedupe of found d-sets per input: store sorted index tuples */
#define HS2 (1u << 23)
static unsigned int *usedslots; static unsigned int nused;
static unsigned long long *hs2; static int hs2n;
static int h2ins(unsigned long long key) { unsigned long long h = (key * 11400714819323198485ull) >> 41; h &= (HS2 - 1); while (hs2[h]) { if (hs2[h] == key) return 0; h = (h + 1) & (HS2 - 1); } hs2[h] = key; hs2n++; usedslots[nused++] = (unsigned int)h; if (hs2n > HS2 / 2) { fprintf(stderr, "dedupe table full\n"); exit(6); } return 1; }
static int curline; static int printall; static int allow_eq;
static void process_set(int *idx) {
    /* idx: d pair indices; dedupe */
    int s[8]; for (int i = 0; i < d; i++) s[i] = idx[i];
    for (int i = 0; i < d; i++) for (int j = i + 1; j < d; j++) if (s[j] < s[i]) { int t = s[i]; s[i] = s[j]; s[j] = t; }
    unsigned long long key = 1; for (int i = 0; i < d; i++) key = key * 1024 + s[i];
    if (!h2ins(key)) { cnt_dup++; return; }
    cnt_sets++;
    if (printall) { printf("SET: line=%d", curline); for (int i = 0; i < d; i++) printf(" %d-%d", PA[s[i]], PB[s[i]]); printf("\n"); }
    nXE = 0; for (int e = 0; e < nE; e++) { XE[nXE][0] = E[e][0]; XE[nXE][1] = E[e][1]; XE[nXE][2] = E[e][2]; nXE++; }
    for (int i = 0; i < d; i++) { XE[nXE][0] = NG; XE[nXE][1] = PA[s[i]]; XE[nXE][2] = PB[s[i]]; nXE++; }
    int nv = NG + 1;
    int ta = tauX(nv);
    if (ta != T) { cnt_tauerr++; }
    if (!linX()) { fprintf(stderr, "nonlinear extension?!\n"); exit(5); }
    int dm = 0; int dg[MAXV + 1] = {0}; for (int e = 0; e < nXE; e++) for (int i = 0; i < 3; i++) dg[XE[e][i]]++; for (int v = 0; v < nv; v++) if (dg[v] > dm) dm = dg[v];
    int cn = connX(nv); if (cn) cnt_conn++;
    int f7 = hasF7X(nv); if (!f7) cnt_f7free++;
    int p3 = (!f7) ? P3X(nv) : 0; if (!f7 && p3) cnt_inC++;
    if (cn && !f7) { cnt_connF7free++; if (!p3) cnt_connP3fail++; }
    if (cn && !f7 && p3 && ta == T && dm <= Dmax) { cnt_hit++; printf("HIT: line=%d", curline); for (int e = 0; e < nXE; e++) printf(" (%d,%d,%d)", XE[e][0], XE[e][1], XE[e][2]); printf("\n"); }
}
static void free_complete(int depth, int start, u32 used, int *idx) {
    if (depth == d) { process_set(idx); return; }
    for (int p = start; p < np; p++) if (!(PM[p] & used)) { idx[depth] = p; free_complete(depth + 1, p + 1, used | PM[p], idx); }
}
static void branch(int depth, u32 used, int *idx) {
    /* first cover not missed by chosen pairs */
    int c;
    for (c = 0; c < ncov; c++) { int missed = 0; for (int i = 0; i < depth; i++) if (!(PM[idx[i]] & covers[c])) { missed = 1; break; } if (!missed) break; }
    if (c == ncov) { free_complete(depth, 0, used, idx); return; }
    if (depth == d) return;
    for (int p = 0; p < np; p++) if (!(PM[p] & used) && !(PM[p] & covers[c])) { idx[depth] = p; branch(depth + 1, used | PM[p], idx); }
}
int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: myext NG t d D\n"); return 2; }
    NG = atoi(argv[1]); T = atoi(argv[2]); d = atoi(argv[3]); Dmax = atoi(argv[4]); printall = (argc > 5 && argv[5][0] == 'a'); allow_eq = (argc > 5 && argv[5][0] == 'e');
    if (NG + 1 > MAXV || d > 6) return 2;
    hcap = 1u << 22; hs = calloc(hcap, sizeof(u32)); hs2 = calloc(HS2, sizeof(unsigned long long)); usedslots = malloc(sizeof(unsigned int) * (HS2 / 2 + 2));
    static char line[1 << 16]; long long maxcov = 0;
    while (fgets(line, sizeof line, stdin)) {
        char *p = line; int k = strtol(p, &p, 10); if (k <= 0 && *p == 0) continue;
        curline++; ginputs++;
        nE = k; memset(degG, 0, sizeof degG);
        for (int e = 0; e < k; e++) { for (int i = 0; i < 3; i++) { E[e][i] = strtol(p, &p, 10); if (E[e][i] < 0 || E[e][i] >= NG) { fprintf(stderr, "bad vertex\n"); return 3; } degG[E[e][i]]++; } emask[e] = (1u << E[e][0]) | (1u << E[e][1]) | (1u << E[e][2]); }
        /* tau(G) */
        nXE = 0; for (int e = 0; e < nE; e++) { XE[e][0] = E[e][0]; XE[e][1] = E[e][1]; XE[e][2] = E[e][2]; nXE++; }
        int tg = tauX(NG);
        if (tg != T - 1 && !(allow_eq && tg == T)) { gbadtau++; continue; }
        /* all (t-1)-covers (none needed when tau(G) = T: every extension has tau >= T; HITs keep tau == T) */
        memset(hs, 0, hcap * sizeof(u32)); ncov = 0; if (tg == T - 1) gen_covers(0, T - 1);
        if (ncov > maxcov) maxcov = ncov;
        if ((unsigned long)ncov * 2 > hcap) { fprintf(stderr, "too many covers\n"); return 4; }
        /* admissible pairs */
        np = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (degG[a] > d - 1 || degG[b] > d - 1) continue;
            int inside = 0; for (int e = 0; e < nE; e++) if ((emask[e] >> a & 1) && (emask[e] >> b & 1)) { inside = 1; break; }
            if (inside) continue;
            PA[np] = a; PB[np] = b; PM[np] = (1u << a) | (1u << b); np++;
        }
        for (unsigned int i = 0; i < nused; i++) hs2[usedslots[i]] = 0; nused = 0; hs2n = 0;
        int idx[8]; branch(0, 0, idx);
    }
    printf("SUMMARY NG=%d t=%d d=%d D=%d inputs=%lld bad_tau_G=%lld max_covers=%lld dsets_tau_ge_t=%lld connected=%lld F7free=%lld F7free_and_P3=%lld connected_F7free=%lld connected_F7free_P3fail=%lld tau_recheck_errors=%lld HITS(connected,inC,tau=t,Delta<=D)=%lld\n",
           NG, T, d, Dmax, ginputs, gbadtau, maxcov, cnt_sets, cnt_conn, cnt_f7free, cnt_inC, cnt_connF7free, cnt_connP3fail, cnt_tauerr, cnt_hit);
    return 0;
}
