/* Referee L011 round 2: membership filter for the class C, from the definitions.
   Usage: rf N < lines  (formats: "TAG: (a,b,c) ..." or "m a b c ...").  Per line prints
   "tau=T maxdeg=D linear=L f7=<v;e1;e2;e3;t1;t2 or -> p3=<edge-index mask with |V(F)|<=|F|+1, or -> conn=<#components over all N points>"
   then a final "SUMMARY ..." line.  F7 = {012,034,056,135,246}: a vertex v with three edges whose pairs P1,P2,P3 are covered by
   two further edges T1, T2 each meeting every P_i once (exactly the subhypergraph copies of F7, as vertex 0 is its unique
   degree-3 vertex).  (P3): every nonempty edge set F has |V(F)| >= |F|+2 (equivalent to e(S) <= |S|-2 for all |S| >= 2). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
typedef unsigned long long u64;
static int cover(const u64 *E, int ne, u64 S, int k) { int j; for (j = 0; j < ne; j++) if (!(E[j] & S)) break;
    if (j == ne) return 1; if (k <= 0) return 0; u64 e = E[j];
    while (e) { u64 b = e & (~e + 1); e ^= b; if (cover(E, ne, S | b, k - 1)) return 1; } return 0; }
static int parse(char *line, int ed[][3]) {
    int m = 0;
    if (strchr(line, '(')) { char *p = line; while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &ed[m][0], &ed[m][1], &ed[m][2]) != 3) return -1; m++; p++; } return m; }
    char *p = line; int cnt = 0; static int vals[1000];
    while (*p) { while (*p && !isdigit((unsigned char)*p)) p++; if (!*p) break; vals[cnt++] = (int)strtol(p, &p, 10); }
    if (cnt == 0) return -2;
    m = vals[0]; if (cnt != 1 + 3*m) return -1;
    for (int k = 0; k < m; k++) for (int t = 0; t < 3; t++) ed[k][t] = vals[1 + 3*k + t];
    return m;
}
static u64 *U = 0;
int main(int argc, char **argv) {
    int N = atoi(argv[1]); static char line[1 << 20]; int ed[64][3];
    long long tot = 0, nlin = 0, nf7 = 0, np3 = 0, nf7free_p3 = 0, ninC = 0, nconn = 0, ninCconn = 0; int tmin = 99, tmax = -1, dmaxall = 0;
    U = malloc(sizeof(u64) << 22);
    while (fgets(line, sizeof line, stdin)) {
        int m = parse(line, ed); if (m == -2) continue; if (m < 0 || m > 22) { fprintf(stderr, "parse error / too many edges\n"); return 1; }
        u64 E[64]; int deg[64] = {0}; int ok = 1;
        for (int j = 0; j < m; j++) { u64 e = 0; for (int t = 0; t < 3; t++) { int v = ed[j][t]; if (v < 0 || v >= N) ok = 0; else { e |= 1ULL << v; deg[v]++; } }
            if (__builtin_popcountll(e) != 3) ok = 0; E[j] = e; }
        if (!ok) { fprintf(stderr, "bad edge\n"); return 1; }
        int lin = 1; for (int i = 0; i < m; i++) for (int j = i + 1; j < m; j++) if (__builtin_popcountll(E[i] & E[j]) >= 2) lin = 0;
        int md = 0; for (int v = 0; v < N; v++) if (deg[v] > md) md = deg[v];
        int tau = 0; while (!cover(E, m, 0, tau)) tau++;
        /* F7 */
        char f7[256] = "-";
        for (int v = 0; v < N && f7[0] == '-'; v++) {
            int at[64], na = 0; for (int j = 0; j < m; j++) if (E[j] >> v & 1) at[na++] = j;
            for (int a = 0; a < na && f7[0] == '-'; a++) for (int b = a + 1; b < na && f7[0] == '-'; b++) for (int c = b + 1; c < na && f7[0] == '-'; c++) {
                u64 P[3] = { E[at[a]] & ~(1ULL << v), E[at[b]] & ~(1ULL << v), E[at[c]] & ~(1ULL << v) };
                if ((P[0] & P[1]) || (P[0] & P[2]) || (P[1] & P[2])) continue;
                u64 all = P[0] | P[1] | P[2];
                for (int s = 0; s < 8 && f7[0] == '-'; s++) {
                    u64 T1 = 0; for (int i = 0; i < 3; i++) { u64 lo = P[i] & (~P[i] + 1), hi = P[i] ^ lo; T1 |= (s >> i & 1) ? hi : lo; }
                    u64 T2 = all ^ T1; int i1 = -1, i2 = -1;
                    for (int j = 0; j < m; j++) { if (E[j] == T1) i1 = j; if (E[j] == T2) i2 = j; }
                    if (i1 >= 0 && i2 >= 0) sprintf(f7, "%d;%d;%d;%d;%d;%d", v, at[a], at[b], at[c], i1, i2);
                }
            }
        }
        /* (P3) over all edge subsets */
        long long p3 = -1; U[0] = 0;
        for (u64 mask = 1; mask < (1ULL << m); mask++) {
            int low = __builtin_ctzll(mask); U[mask] = U[mask & (mask - 1)] | E[low];
            if (__builtin_popcountll(U[mask]) <= __builtin_popcountll(mask) + 1) { p3 = (long long)mask; break; }
        }
        /* connectivity over all N points */
        int par[64]; for (int v = 0; v < N; v++) par[v] = v;
        for (int j = 0; j < m; j++) { int r[3], k = 0; for (int v = 0; v < N; v++) if (E[j] >> v & 1) r[k++] = v;
            for (int t = 1; t < 3; t++) { int x = r[0], y = r[t]; while (par[x] != x) x = par[x]; while (par[y] != y) y = par[y]; if (x != y) par[x] = y; } }
        int ncomp = 0; for (int v = 0; v < N; v++) if (par[v] == v) ncomp++;
        printf("tau=%d maxdeg=%d linear=%d f7=%s p3=%lld conn=%d\n", tau, md, lin, f7, p3, ncomp);
        tot++; nlin += lin; if (f7[0] != '-') nf7++; if (p3 >= 0) np3++; if (f7[0] == '-' && p3 >= 0) nf7free_p3++;
        int inC = lin && f7[0] == '-' && p3 < 0; ninC += inC; nconn += (ncomp == 1); ninCconn += inC && ncomp == 1;
        if (tau < tmin) tmin = tau; if (tau > tmax) tmax = tau; if (md > dmaxall) dmaxall = md;
    }
    fprintf(stderr, "SUMMARY total=%lld linear=%lld f7=%lld p3viol=%lld f7free_p3viol=%lld inC=%lld connected=%lld inC_connected=%lld tau=[%d,%d] maxdeg=%d\n",
            tot, nlin, nf7, np3, nf7free_p3, ninC, nconn, ninCconn, tmin, tmax, dmaxall);
    return 0;
}
