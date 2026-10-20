/* myfilter.c -- referee L010 round 3 (written from scratch).  Class-C filter for 3-graphs given one per line
   ("TAG: (a,b,c) (d,e,f) ..." or "m a b c ..."), vertex labels 0..NV-1 (NV = max label + 1, or the optional argument).
   Tests: linear; F7 (vertex p with three edges A,B,C at p and two disjoint edges avoiding p that meet A,B,C in one vertex each);
   (P3) e(S) <= |S|-2 for all |S|>=2, tested by Hall's theorem: (P3) holds iff for every pair {x,y} the edges minus {x,y} have a
   system of distinct representatives (bipartite matching saturating the edges); for every violation the Hall violator F gives
   S = V(F), and e(S) >= |S|-1 is re-counted from the definition (abort if not); connectivity (all NV vertices in one component,
   isolated vertices count); max degree; exact tau (branching) unless 'notau'.
   Usage: myfilter TAG [NV|0] [notau] [all] < file.  Prints SURVIVOR: lines (linear, F7-free, P3) or, with 'all', every line annotated. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t E[64]; static int NE, NV;
static int linear(void) { for (int i = 0; i < NE; i++) for (int j = i + 1; j < NE; j++) if (__builtin_popcount(E[i] & E[j]) >= 2) return 0; return 1; }
static int has_f7(void) {
    for (int p = 0; p < NV; p++) {
        int at[64], na = 0; for (int j = 0; j < NE; j++) if (E[j] >> p & 1) at[na++] = j;
        if (na < 3) continue;
        for (int x = 0; x < na; x++) for (int y = x + 1; y < na; y++) for (int z = y + 1; z < na; z++) {
            uint32_t A = E[at[x]], B = E[at[y]], C = E[at[z]], U = (A | B | C) & ~(1u << p);
            for (int j = 0; j < NE; j++) { uint32_t e = E[j]; if ((e >> p & 1) || (e & U) != e) continue;
                if (__builtin_popcount(e & A) != 1 || __builtin_popcount(e & B) != 1 || __builtin_popcount(e & C) != 1) continue;
                for (int k = j + 1; k < NE; k++) { uint32_t f = E[k]; if ((f >> p & 1) || (f & U) != f || (f & e)) continue;
                    if (__builtin_popcount(f & A) == 1 && __builtin_popcount(f & B) == 1 && __builtin_popcount(f & C) == 1) return 1; } }
        }
    }
    return 0;
}
/* bipartite matching edges -> vertices avoiding x,y; returns 1 if all edges matched, else fills *viol with a Hall violator F */
static int matchv[32], matche[64], vis[64];
static uint32_t avail;
static int try_edge(int i) {
    uint32_t e = E[i] & avail;
    while (e) { int v = __builtin_ctz(e); e &= e - 1;
        if (vis[v]) continue; vis[v] = 1;
        if (matchv[v] < 0 || try_edge(matchv[v])) { matchv[v] = i; matche[i] = v; return 1; } }
    return 0;
}
static int sdr_exists(int x, int y, uint64_t *viol) {
    avail = ~0u; if (x >= 0) avail &= ~(1u << x); if (y >= 0) avail &= ~(1u << y);
    for (int v = 0; v < 32; v++) matchv[v] = -1;
    for (int i = 0; i < NE; i++) matche[i] = -1;
    for (int i = 0; i < NE; i++) { memset(vis, 0, sizeof vis); if (!try_edge(i)) {
        /* Hall violator: edges reachable from i by alternating paths = i plus matched partners of visited vertices */
        uint64_t F = 1ULL << i; for (int v = 0; v < 32; v++) if (vis[v] && matchv[v] >= 0) F |= 1ULL << matchv[v];
        *viol = F; return 0; } }
    return 1;
}
static int p3_ok(uint32_t *badS) {
    for (int x = 0; x < NV; x++) for (int y = x + 1; y < NV; y++) { uint64_t F;
        if (!sdr_exists(x, y, &F)) {
            uint32_t S = (1u << x) | (1u << y); int cntF = 0;
            for (int i = 0; i < NE; i++) if (F >> i & 1) { S |= E[i]; cntF++; }
            /* re-count from the definition: edges inside S */
            int eS = 0; for (int i = 0; i < NE; i++) if ((E[i] & S) == E[i]) eS++;
            int sz = __builtin_popcount(S);
            if (!(sz >= 2 && eS >= sz - 1)) { fprintf(stderr, "INTERNAL: Hall violator without P3 violation (|S|=%d e(S)=%d |F|=%d)\n", sz, eS, cntF); exit(9); }
            *badS = S; return 0; } }
    return 1;
}
static int coverable(uint64_t left, int k) {
    if (!left) return 1; if (k <= 0) return 0;
    uint64_t l = left; uint32_t used = 0; int cnt = 0; while (l) { int i = __builtin_ctzll(l); l &= l - 1; if (!(E[i] & used)) { used |= E[i]; cnt++; } } if (cnt > k) return 0;
    int i = __builtin_ctzll(left); uint32_t e = E[i];
    while (e) { int v = __builtin_ctz(e); e &= e - 1; uint64_t l2 = left; for (int j = 0; j < NE; j++) if ((l2 >> j & 1) && (E[j] >> v & 1)) l2 &= ~(1ULL << j); if (coverable(l2, k - 1)) return 1; }
    return 0;
}
static int tau_exact(void) { uint64_t all = NE >= 64 ? ~0ULL : ((1ULL << NE) - 1); int k = 0; while (!coverable(all, k)) k++; return k; }
static int connected(void) {
    int par[32]; for (int v = 0; v < NV; v++) par[v] = v;
    #define FIND(a) ({ int _a = (a); while (par[_a] != _a) _a = par[_a]; _a; })
    for (int i = 0; i < NE; i++) { uint32_t e = E[i]; int r = FIND(__builtin_ctz(e)); uint32_t f = e; while (f) { int v = __builtin_ctz(f); f &= f - 1; par[FIND(v)] = r; } }
    int r0 = FIND(0); for (int v = 1; v < NV; v++) if (FIND(v) != r0) return 0; return 1;
}
int main(int argc, char **argv) {
    const char *tag = argc > 1 ? argv[1] : "HIT"; int NVarg = argc > 2 ? atoi(argv[2]) : 0;
    int notau = 0, all = 0; for (int i = 3; i < argc; i++) { if (!strcmp(argv[i], "notau")) notau = 1; if (!strcmp(argv[i], "all")) all = 1; }
    static char line[1 << 16]; size_t tl = strlen(tag);
    unsigned long long tot = 0, nlin = 0, nf7 = 0, np3bad = 0, nf7free_p3bad = 0, nsurv = 0, nconn = 0, nconn_surv = 0; int taumin = 99, taumax = -1, mdmax = 0;
    while (fgets(line, sizeof line, stdin)) {
        int ed[64][3], m = 0;
        if (strchr(line, '(')) { if (strncmp(line, tag, tl) || line[tl] != ':') continue;
            char *p = line; while ((p = strchr(p, '('))) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) == 3) { ed[m][0] = a; ed[m][1] = b; ed[m][2] = c; m++; } p++; } }
        else { int k; char *p = line; if (sscanf(p, "%d%n", &m, &k) != 1) continue; p += k; for (int i = 0; i < m; i++) { if (sscanf(p, "%d %d %d%n", &ed[i][0], &ed[i][1], &ed[i][2], &k) != 3) { m = -1; break; } p += k; } if (m < 0) continue; }
        NE = m; NV = NVarg; tot++;
        for (int i = 0; i < m; i++) { E[i] = (1u << ed[i][0]) | (1u << ed[i][1]) | (1u << ed[i][2]); for (int c = 0; c < 3; c++) if (ed[i][c] + 1 > NV) NV = ed[i][c] + 1; }
        int lin = linear(); nlin += lin; int f7 = has_f7(); nf7 += f7; uint32_t badS = 0; int p3 = p3_ok(&badS); np3bad += !p3; if (!f7 && !p3) nf7free_p3bad++;
        int conn = connected(); nconn += conn; int md = 0; for (int v = 0; v < NV; v++) { int d = 0; for (int i = 0; i < m; i++) if (E[i] >> v & 1) d++; if (d > md) md = d; } if (md > mdmax) mdmax = md;
        int t = notau ? -1 : tau_exact(); if (t < taumin) taumin = t; if (t > taumax) taumax = t;
        int surv = lin && !f7 && p3; nsurv += surv; if (surv && conn) nconn_surv++;
        if (all) { printf("%s lin=%d f7=%d p3=%d conn=%d maxdeg=%d tau=%d nv=%d badS=%u | %s", surv ? "SURVIVOR" : "REJECT", lin, f7, p3, conn, md, t, NV, badS, line); }
        else if (surv) { printf("SURVIVOR: "); for (int i = 0; i < m; i++) printf("(%d,%d,%d) ", ed[i][0], ed[i][1], ed[i][2]); printf("\n"); }
    }
    printf("MYSUMMARY tag=%s total=%llu linear=%llu contain_F7=%llu P3_violated=%llu F7free_and_P3_violated=%llu survivors=%llu connected=%llu connected_survivors=%llu tau_range=[%d,%d] maxdeg_max=%d\n",
           tag, tot, nlin, nf7, np3bad, nf7free_p3bad, nsurv, nconn, nconn_surv, taumin, taumax, mdmax);
    return 0;
}
