/* chk.c (referee L012 round 3) -- independent property report for 3-graphs on vertices 0..NV-1 given as lines with "(a,b,c)" triples
   or "m a b c ...".  Per line: n_used, m, linear, F7 (centre-based), P3 (brute force over all 2^m edge subsets), tau (brute force),
   connected on all NV vertices, max degree, degree sequence.  Summary with counts.  Usage: chk NV [WANT_TAU] < lines */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int NV; static uint32_t E[48]; static int ne;
static int is_edge(uint32_t mask) { for (int i = 0; i < ne; i++) if (E[i] == mask) return 1; return 0; }
static int has_f7(void) {
    for (int p = 0; p < NV; p++) {
        int at[16], na = 0; for (int i = 0; i < ne; i++) if (E[i] >> p & 1) { if (na < 16) at[na] = i; na++; }
        if (na < 3) continue; if (na > 16) na = 16;
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
static int p3_ok(void) {
    int cnt[32]; memset(cnt, 0, sizeof cnt); int nv = 0, nf = 0;
    unsigned long long total = 1ull << ne;
    for (unsigned long long g = 1; g < total; g++) {
        int bit = __builtin_ctzll(g); uint32_t em = E[bit]; int adding = (((g ^ (g >> 1)) >> bit) & 1);
        if (adding) { nf++; for (uint32_t r = em; r; r &= r - 1) { int v = __builtin_ctz(r); if (cnt[v]++ == 0) nv++; } }
        else { nf--; for (uint32_t r = em; r; r &= r - 1) { int v = __builtin_ctz(r); if (--cnt[v] == 0) nv--; } }
        if (nf >= 1 && nv < nf + 2) return 0;
    }
    return 1;
}
static int has_cover(int k) {
    if (k == 0) return ne == 0;
    int idx[32]; for (int i = 0; i < k; i++) idx[i] = i;
    while (1) {
        uint32_t S = 0; for (int i = 0; i < k; i++) S |= 1u << idx[i];
        int ok = 1; for (int i = 0; i < ne; i++) if (!(E[i] & S)) { ok = 0; break; }
        if (ok) return 1;
        int i = k - 1; while (i >= 0 && idx[i] == NV - k + i) i--; if (i < 0) return 0;
        idx[i]++; for (int j = i + 1; j < k; j++) idx[j] = idx[j - 1] + 1;
    }
}
static int tau(void) { for (int k = 0; k <= NV; k++) if (has_cover(k)) return k; return NV; }
static int connected_all(void) {
    int par[40]; for (int i = 0; i < NV; i++) par[i] = i;
    #define FIND(x) ({ int _x = (x); while (par[_x] != _x) _x = par[_x] = par[par[_x]]; _x; })
    for (int i = 0; i < ne; i++) { int v[3], k = 0; for (uint32_t r = E[i]; r; r &= r - 1) v[k++] = __builtin_ctz(r); par[FIND(v[1])] = FIND(v[0]); par[FIND(v[2])] = FIND(v[0]); }
    int r0 = FIND(0); for (int i = 1; i < NV; i++) if (FIND(i) != r0) return 0; return 1;
}
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: chk NV [WANT_TAU] < lines\n"); return 1; }
    NV = atoi(argv[1]); int want = argc > 2 ? atoi(argv[2]) : -1;
    static char line[1 << 15]; unsigned long long tot = 0, nlin = 0, nf7 = 0, np3 = 0, nconn = 0, ntauok = 0, inC = 0; int tmin = 99, tmax = -1, dmax_all = 0;
    while (fgets(line, sizeof line, stdin)) {
        int ed[48][3]; ne = 0;
        if (strchr(line, '(')) { char *p = line; while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &ed[ne][0], &ed[ne][1], &ed[ne][2]) == 3) ne++; p++; } }
        else { char *p = line; int k, mm; if (sscanf(p, "%d%n", &mm, &k) != 1) continue; p += k; for (int i = 0; i < mm; i++) { if (sscanf(p, "%d %d %d%n", &ed[i][0], &ed[i][1], &ed[i][2], &k) != 3) { fprintf(stderr, "bad line\n"); return 2; } p += k; } ne = mm; }
        if (ne == 0) continue;
        for (int i = 0; i < ne; i++) { for (int t = 0; t < 3; t++) if (ed[i][t] < 0 || ed[i][t] >= NV) { fprintf(stderr, "label out of range\n"); return 3; }
            if (ed[i][0] == ed[i][1] || ed[i][1] == ed[i][2] || ed[i][0] == ed[i][2]) { fprintf(stderr, "degenerate edge\n"); return 3; }
            E[i] = (1u << ed[i][0]) | (1u << ed[i][1]) | (1u << ed[i][2]); }
        tot++;
        int lin = 1; for (int i = 0; i < ne && lin; i++) for (int j = i + 1; j < ne; j++) if (__builtin_popcount(E[i] & E[j]) >= 2) { lin = 0; break; }
        int f7 = lin ? has_f7() : -1, p3 = p3_ok(), t = tau(), cn = connected_all();
        int deg[40] = {0}, dmax = 0; uint32_t used = 0; for (int i = 0; i < ne; i++) { used |= E[i]; for (uint32_t r = E[i]; r; r &= r - 1) deg[__builtin_ctz(r)]++; }
        for (int v = 0; v < NV; v++) if (deg[v] > dmax) dmax = deg[v];
        int ds[10] = {0}; for (int v = 0; v < NV; v++) ds[deg[v] > 9 ? 9 : deg[v]]++;
        nlin += lin; nf7 += (f7 == 1); np3 += !p3; nconn += cn; if (t < tmin) tmin = t; if (t > tmax) tmax = t; if (dmax > dmax_all) dmax_all = dmax;
        int c = lin && f7 == 0 && p3; inC += c; if (want >= 0 && t == want) ntauok++;
        printf("G %llu n_used=%d m=%d linear=%d F7=%d P3=%d tau=%d conn=%d maxdeg=%d degseq=", tot, __builtin_popcount(used), ne, lin, f7, p3, t, cn, dmax);
        for (int d = 0; d <= 9; d++) if (ds[d]) printf("%d^%d,", d, ds[d]); printf("\n");
    }
    printf("SUMMARY NV=%d total=%llu linear=%llu contain_F7=%llu P3_violated=%llu in_C=%llu connected=%llu tau_range=[%d,%d] tau_equals_want=%llu maxdeg_max=%d\n",
           NV, tot, nlin, nf7, np3, inC, nconn, tmin, tmax, ntauok, dmax_all);
    return 0;
}
