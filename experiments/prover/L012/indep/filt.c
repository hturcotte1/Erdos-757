/* filt.c (prover, certificate L012) -- filters for 3-graphs given as lines "TAG: (a,b,c) (d,e,f) ...", on the vertex set {0..NV-1}.
   Tests: linearity; F7 by Lemma F of L007 (five edges of a linear 3-graph form F7 iff their union has 7 vertices with within-degrees
   3,2,2,2,2,2,2; all 5-subsets of edges); (P3) e(S)<=|S|-2 for all |S|>=2, tested in the equivalent Hall form: for every pair {x,y}
   of non-isolated vertices the edges have distinct representatives (each edge -> one of its own vertices, all different) avoiding x
   and y (augmenting paths); exact tau (smallest k with a k-subset of the NV vertices meeting all edges; Gosper enumeration), unless
   TAUMODE is 'notau'; maximum degree; connectivity on all NV vertices (a vertex in no edge is its own component).
   Usage: filt TAG NV [tau|notau] [WANTTAU]   Prints "SURVIVOR:" lines (linear, F7-free, P3; and tau == WANTTAU if WANTTAU given)
   with the connectivity flag appended as " #conn=0/1", and one SUMMARY line. Up to 32 vertices and 40 edges. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t M[40]; static int ne, NV;
static int linear(void) { for (int i = 0; i < ne; i++) for (int j = i + 1; j < ne; j++) if (__builtin_popcount(M[i] & M[j]) >= 2) return 0; return 1; }
static int has_f7(void) {
    int a[5];
    for (a[0] = 0; a[0] < ne; a[0]++) for (a[1] = a[0] + 1; a[1] < ne; a[1]++) {
        if (!(M[a[0]] & M[a[1]])) {} /* no shortcut: test every 5-subset */
        for (a[2] = a[1] + 1; a[2] < ne; a[2]++) for (a[3] = a[2] + 1; a[3] < ne; a[3]++) for (a[4] = a[3] + 1; a[4] < ne; a[4]++) {
            uint32_t U = M[a[0]] | M[a[1]] | M[a[2]] | M[a[3]] | M[a[4]];
            if (__builtin_popcount(U) != 7) continue;
            int d3 = 0, d2 = 0;
            for (uint32_t r = U; r; r &= r - 1) { int v = __builtin_ctz(r), d = 0; for (int k = 0; k < 5; k++) d += (M[a[k]] >> v) & 1; if (d == 3) d3++; else if (d == 2) d2++; }
            if (d3 == 1 && d2 == 6) return 1;
        }
    }
    return 0;
}
static int owner[32]; static uint32_t forbid;
static int augment(int e, uint32_t *seen) {
    for (uint32_t r = M[e] & ~forbid & ~*seen; r; r &= r - 1) {
        int v = __builtin_ctz(r); *seen |= 1u << v;
        if (owner[v] < 0 || augment(owner[v], seen)) { owner[v] = e; return 1; }
    }
    return 0;
}
static int p3_ok(void) {
    uint32_t used = 0; for (int i = 0; i < ne; i++) used |= M[i];
    for (int x = 0; x < 32; x++) if (used >> x & 1) for (int y = x + 1; y < 32; y++) if (used >> y & 1) {
        forbid = (1u << x) | (1u << y); for (int v = 0; v < 32; v++) owner[v] = -1;
        for (int e = 0; e < ne; e++) { uint32_t seen = 0; if (!augment(e, &seen)) return 0; }
    }
    return 1;
}
static int tau(void) {
    if (ne == 0) return 0;
    for (int k = 1; k <= NV; k++) {
        uint32_t S = (1u << k) - 1, lim = (NV == 32) ? 0xFFFFFFFFu : ((1u << NV) - 1);
        while (1) {
            int ok = 1; for (int i = 0; i < ne; i++) if (!(M[i] & S)) { ok = 0; break; }
            if (ok) return k;
            uint32_t c = S & -S, r = S + c; if (r == 0 || r > lim) break; S = (((r ^ S) >> 2) / c) | r; if (S > lim) break;
        }
    }
    return NV;
}
static int connected(void) {
    uint32_t all = (NV == 32) ? 0xFFFFFFFFu : ((1u << NV) - 1), comp = 1u, prev = 0;
    while (comp != prev) { prev = comp; for (int i = 0; i < ne; i++) if (M[i] & comp) comp |= M[i]; }
    return comp == all;
}
int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: filt TAG NV [tau|notau] [WANTTAU]\n"); return 1; }
    const char *tag = argv[1]; NV = atoi(argv[2]); int dotau = !(argc > 3 && !strcmp(argv[3], "notau")); int want = argc > 4 ? atoi(argv[4]) : -1;
    if (want >= 0 && !dotau) { fprintf(stderr, "WANTTAU needs tau\n"); return 1; }
    static char line[1 << 14]; size_t tl = strlen(tag);
    unsigned long long tot = 0, nlin = 0, nf7 = 0, np3 = 0, nf7free_p3 = 0, nsurv = 0, nsurvconn = 0, nconn = 0, badlabel = 0, wrongtau = 0;
    int tmin = 99, tmax = -1, dmax = 0;
    while (fgets(line, sizeof line, stdin)) {
        if (strncmp(line, tag, tl) || line[tl] != ':') continue;
        ne = 0; char *p = line + tl + 1; int bad = 0;
        while ((p = strchr(p, '('))) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) != 3) return 2;
            if (a < 0 || b < 0 || c < 0 || a >= NV || b >= NV || c >= NV || a == b || b == c || a == c) bad = 1;
            if (ne >= 40) return 3;
            M[ne++] = (1u << a) | (1u << b) | (1u << c); p++; }
        tot++; if (bad) { badlabel++; continue; }
        int lin = linear(); nlin += lin;
        int f7 = lin ? has_f7() : 1; nf7 += f7;
        int p3 = p3_ok(); np3 += !p3; if (!f7 && !p3) nf7free_p3++;
        int t = dotau ? tau() : -1; if (t < tmin) tmin = t; if (t > tmax) tmax = t;
        for (int v = 0; v < NV; v++) { int d = 0; for (int i = 0; i < ne; i++) d += (M[i] >> v) & 1; if (d > dmax) dmax = d; }
        int cn = connected(); nconn += cn;
        if (lin && !f7 && p3) {
            if (want >= 0 && t != want) { wrongtau++; continue; }
            nsurv++; nsurvconn += cn;
            char *nl = strchr(line, '\n'); if (nl) *nl = 0;
            printf("SURVIVOR:%s #conn=%d\n", line + tl + 1, cn);
        }
    }
    printf("SUMMARY tag=%s NV=%d total=%llu bad_labels=%llu linear=%llu contain_F7=%llu P3_violated=%llu F7free_and_P3_violated=%llu "
           "survivors=%llu survivors_connected=%llu wrong_tau_dropped=%llu connected_all=%llu tau_range=[%d,%d] maxdeg_max=%d\n",
           tag, NV, tot, badlabel, nlin, nf7, np3, nf7free_p3, nsurv, nsurvconn, wrongtau, nconn, tmin, tmax, dmax);
    return 0;
}
