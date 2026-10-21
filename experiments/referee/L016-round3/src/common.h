/* Referee L016 round 3 -- own tests on 3-graphs with <= 32 vertices given as edge bitmasks. Independent of e757/, judge/, L012-L016 code. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t u32;
static int has_edge(int m, const u32 *E, u32 mask) { for (int i = 0; i < m; i++) if (E[i] == mask) return 1; return 0; }
/* linear: every two edges share at most one vertex */
static int is_linear(int m, const u32 *E) {
    for (int i = 0; i < m; i++) { if (__builtin_popcount(E[i]) != 3) return 0;
        for (int j = i + 1; j < m; j++) if (__builtin_popcount(E[i] & E[j]) >= 2) return 0; }
    return 1;
}
/* F7 = centre x with three edges {x,a_i,b_i} and two disjoint edges {a1,u2,u3}, {b1,v2,v3} with {u_i,v_i} = {a_i,b_i} */
static int has_f7(int n, int m, const u32 *E) {
    for (int x = 0; x < n; x++) {
        int at[64], k = 0; for (int i = 0; i < m; i++) if (E[i] >> x & 1) at[k++] = i;
        for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++) for (int l = j + 1; l < k; l++) {
            u32 r1 = E[at[i]] & ~(1u << x), r2 = E[at[j]] & ~(1u << x), r3 = E[at[l]] & ~(1u << x);
            int a1 = __builtin_ctz(r1), b1 = 31 - __builtin_clz(r1), a2 = __builtin_ctz(r2), b2 = 31 - __builtin_clz(r2), a3 = __builtin_ctz(r3), b3 = 31 - __builtin_clz(r3);
            for (int s2 = 0; s2 < 2; s2++) for (int s3 = 0; s3 < 2; s3++) {
                int u2 = s2 ? b2 : a2, v2 = s2 ? a2 : b2, u3 = s3 ? b3 : a3, v3 = s3 ? a3 : b3;
                if (has_edge(m, E, (1u << a1) | (1u << u2) | (1u << u3)) && has_edge(m, E, (1u << b1) | (1u << v2) | (1u << v3))) return 1;
            }
        }
    }
    return 0;
}
/* (P3) e(S) <= |S|-2 for all |S| >= 2  <=>  for every pair {x,y}: the edges have distinct representatives avoiding x,y (Hall) */
static int g_owner[32]; static u32 g_forb; static const u32 *g_E;
static int augment(int e, u32 *seen) {
    for (u32 r = g_E[e] & ~g_forb & ~*seen; r; r &= r - 1) { int v = __builtin_ctz(r); *seen |= 1u << v;
        if (g_owner[v] < 0 || augment(g_owner[v], seen)) { g_owner[v] = e; return 1; } }
    return 0;
}
static int p3_ok(int n, int m, const u32 *E) {
    g_E = E;
    for (int x = 0; x < n; x++) for (int y = x + 1; y < n; y++) {
        g_forb = (1u << x) | (1u << y); for (int v = 0; v < 32; v++) g_owner[v] = -1;
        for (int e = 0; e < m; e++) { u32 seen = 0; if (!augment(e, &seen)) return 0; }
    }
    return 1;
}
/* connectivity on all n vertices (isolated vertex = own component) */
static int uf[32]; static int uff(int x) { while (uf[x] != x) x = uf[x] = uf[uf[x]]; return x; }
static int ncomponents(int n, int m, const u32 *E) {
    for (int i = 0; i < n; i++) uf[i] = i;
    for (int i = 0; i < m; i++) { int v[3], k = 0; for (u32 r = E[i]; r; r &= r - 1) v[k++] = __builtin_ctz(r);
        uf[uff(v[1])] = uff(v[0]); uf[uff(v[2])] = uff(v[0]); }
    int c = 0; for (int i = 0; i < n; i++) if (uff(i) == i) c++; return c;
}
static int maxdeg(int n, int m, const u32 *E) { int d[32] = {0}, mx = 0; for (int i = 0; i < m; i++) for (u32 r = E[i]; r; r &= r - 1) d[__builtin_ctz(r)]++; for (int i = 0; i < n; i++) if (d[i] > mx) mx = d[i]; return mx; }
/* is there a vertex cover (transversal) with at most budget vertices?  branch on the first unmet edge */
static int cover_exists(int m, const u32 *E, u32 S, int budget) {
    int e = -1; for (int i = 0; i < m; i++) if (!(E[i] & S)) { e = i; break; }
    if (e < 0) return 1;
    if (budget == 0) return 0;
    for (u32 r = E[e]; r; r &= r - 1) if (cover_exists(m, E, S | (r & -r), budget - 1)) return 1;
    return 0;
}
static int tau_of(int m, const u32 *E) { int k = 0; while (!cover_exists(m, E, 0, k)) k++; return k; }
/* parse a line "FOUND: (a,b,c) (d,e,f) ..." or "m a b c d e f ..." into edge masks; returns m or -1 */
static int parse_line(const char *s, u32 *E, int *maxlabel) {
    int m = 0; *maxlabel = -1;
    const char *p = strchr(s, '(');
    if (p) { while ((p = strchr(p, '(')) != NULL) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) != 3) return -1;
            if (a < 0 || b < 0 || c < 0 || a > 31 || b > 31 || c > 31) return -1;
            if (a > *maxlabel) *maxlabel = a; if (b > *maxlabel) *maxlabel = b; if (c > *maxlabel) *maxlabel = c;
            E[m++] = (1u << a) | (1u << b) | (1u << c); if (m > 60) return -1; p++; } return m; }
    else { int k; char *end; long v = strtol(s, &end, 10); if (end == s) return -1; k = (int)v; if (k < 0 || k > 60) return -1;
        const char *q = end; for (int i = 0; i < k; i++) { long a = strtol(q, &end, 10); q = end; long b = strtol(q, &end, 10); q = end; long c = strtol(q, &end, 10); q = end;
            if (a < 0 || b < 0 || c < 0 || a > 31 || b > 31 || c > 31) return -1;
            if (a > *maxlabel) *maxlabel = a; if (b > *maxlabel) *maxlabel = b; if (c > *maxlabel) *maxlabel = c;
            E[m++] = (1u << a) | (1u << b) | (1u << c); } return m; }
}
