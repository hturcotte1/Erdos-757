/* rext.c -- referee (L016 round 2) own program; written from scratch, shares no code with ext_d.c / filt.c / canon.c.
   Hypergraphs: 3-uniform, vertices 0..n-1 (n <= 31), at most 48 edges, stored as 32-bit vertex masks.

   rext ext NG TG d EP        stdin: lines "m a1 b1 c1 ..." (graph G on 0..NG-1)
       For each G: tau(G) computed exactly (iterative deepening, edge branching); if != TG -> counted bad_tau, skipped.
       All minimum covers of G enumerated (edge branching without exclusion, then sort+unique).
       Admissible pairs {a,b}: a<b<NG, not both in one edge of G, deg_G(a), deg_G(b) <= EP.
       Lists EVERY set of d pairwise disjoint admissible pairs such that every minimum cover of G misses some pair
       (<=> tau(X) = TG+1 for X = G + {NG,a,b}), such that X is connected; for these X tests F7-freeness and (P3)
       (full Hall test over all vertex pairs) and prints graph6 of the vertex-edge incidence graph of each survivor.
       Search: branch on the first not-yet-killed cover over the pairs killing it (siblings excluded later); free completion
       when all covers are killed; pruning only by connectivity (untouched components > 2*(pairs left)).
   rext filt n D              stdin: "FOUND: (a,b,c) ..." lines (or "m a b c ..." lines with 'raw' as 4th arg)
       prints per graph: "n m tau maxdeg linear f7free p3 connected" and a summary.
   rext g6 n                  stdin: FOUND lines -> graph6 of incidence graphs (vertex classes 0..n-1, n..n+m-1)
   rext gb n1 n2 t D          stdin: graph6 bipartite graphs of genbg (class 1 = vertices, class 2 = edges) -> filter:
       linear, F7-free, P3, connected, tau == t, maxdeg <= D; prints survivors as graph6 (same graph) and a summary. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXE 48
#define MAXCOV 400000
#define MAXPAIRS 700
typedef uint32_t u32; typedef uint64_t u64;

static int pc(u32 x) { return __builtin_popcount(x); }

/* ---------- covers ---------- */
static u32 *gE; static int gm;
static int lb_unhit(u32 S) {      /* greedy number of pairwise disjoint edges not met by S */
    u32 used = 0; int c = 0;
    for (int i = 0; i < gm; i++) if (!(gE[i] & S) && !(gE[i] & used)) { used |= gE[i]; c++; }
    return c;
}
static int exists_cover(u32 S, int b) {
    int e = -1; for (int i = 0; i < gm; i++) if (!(gE[i] & S)) { e = i; break; }
    if (e < 0) return 1;
    if (b == 0) return 0;
    if (lb_unhit(S) > b) return 0;
    for (u32 r = gE[e]; r; r &= r - 1) if (exists_cover(S | (r & -r), b - 1)) return 1;
    return 0;
}
static int tau_of(u32 *E, int m) {
    gE = E; gm = m;
    for (int b = 0; b <= 31; b++) if (exists_cover(0, b)) return b;
    return -1;
}
static u32 *cov; static long ncov; static int covovf;
static void all_cov(u32 S, int b) {
    int e = -1; for (int i = 0; i < gm; i++) if (!(gE[i] & S)) { e = i; break; }
    if (e < 0) { if (ncov >= MAXCOV) { covovf = 1; return; } cov[ncov++] = S; return; }
    if (b == 0) return;
    if (lb_unhit(S) > b) return;
    for (u32 r = gE[e]; r; r &= r - 1) all_cov(S | (r & -r), b - 1);
}
static int cmpu(const void *a, const void *b) { u32 x = *(const u32 *)a, y = *(const u32 *)b; return x < y ? -1 : x > y; }
static long min_covers(u32 *E, int m, int t) {  /* all covers of size exactly t (assumes tau = t) */
    gE = E; gm = m; ncov = 0; covovf = 0; all_cov(0, t);
    if (covovf) { fprintf(stderr, "cover overflow\n"); exit(3); }
    qsort(cov, ncov, sizeof(u32), cmpu);
    long k = 0; for (long i = 0; i < ncov; i++) { if (pc(cov[i]) != t) { fprintf(stderr, "cover size error\n"); exit(3); }
        if (k == 0 || cov[i] != cov[k - 1]) cov[k++] = cov[i]; }
    ncov = k; return k;
}

/* ---------- properties ---------- */
static int is_linear(u32 *E, int m) { for (int i = 0; i < m; i++) for (int j = i + 1; j < m; j++) if (pc(E[i] & E[j]) > 1) return 0; return 1; }
static int has_f7(u32 *E, int m, int n) {
    for (int x = 0; x < n; x++) {
        int at[MAXE], k = 0; for (int i = 0; i < m; i++) if (E[i] >> x & 1) at[k++] = i;
        for (int a = 0; a < k; a++) for (int b = a + 1; b < k; b++) for (int c = b + 1; c < k; c++) {
            u32 A1 = E[at[a]] & ~(1u << x), A2 = E[at[b]] & ~(1u << x), A3 = E[at[c]] & ~(1u << x);
            u32 U = A1 | A2 | A3; if (pc(U) != 6) continue;
            for (int f = 0; f < m; f++) {
                u32 F = E[f]; if (F & ~U) continue;
                if (pc(F & A1) != 1 || pc(F & A2) != 1 || pc(F & A3) != 1) continue;
                u32 G = U & ~F;
                for (int g = 0; g < m; g++) if (E[g] == G) return 1;
            }
        }
    }
    return 0;
}
/* (P3): e(S) <= |S|-2 for all S, |S|>=2  <=>  for all vertex pairs {x,y}: the edges have a system of distinct representatives
   avoiding x and y (Hall).  */
static int mt_owner[32]; static u32 mt_avoid; static u32 *mE;
static int aug(int e, u32 *seen) {
    for (u32 r = mE[e] & ~mt_avoid & ~*seen; r; r &= r - 1) { int v = __builtin_ctz(r); *seen |= 1u << v;
        if (mt_owner[v] < 0 || aug(mt_owner[v], seen)) { mt_owner[v] = e; return 1; } }
    return 0;
}
static int sdr_avoiding(u32 *E, int m, u32 avoid) {
    mE = E; mt_avoid = avoid; for (int v = 0; v < 32; v++) mt_owner[v] = -1;
    for (int e = 0; e < m; e++) { u32 seen = 0; if (!aug(e, &seen)) return 0; }
    return 1;
}
static int p3_ok(u32 *E, int m, int n) {
    if (m == 0) return 1;
    if (m > n - 2) return 0;
    for (int x = 0; x < n; x++) for (int y = x + 1; y < n; y++) if (!sdr_avoiding(E, m, (1u << x) | (1u << y))) return 0;
    return 1;
}
static int find(int *p, int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; }
static int ncomp_of(u32 *E, int m, int n, int *comp) {
    int p[32]; for (int i = 0; i < n; i++) p[i] = i;
    for (int i = 0; i < m; i++) { int v[3], k = 0; for (u32 r = E[i]; r; r &= r - 1) v[k++] = __builtin_ctz(r);
        int a = find(p, v[0]), b = find(p, v[1]), c = find(p, v[2]); p[b] = a; c = find(p, c); p[c] = a; }
    int lab[32], nc = 0; for (int i = 0; i < n; i++) lab[i] = -1;
    for (int i = 0; i < n; i++) { int r = find(p, i); if (lab[r] < 0) lab[r] = nc++; comp[i] = lab[r]; }
    return nc;
}
static void put_g6(u32 *E, int m, int n) {
    int N = n + m; char buf[2048]; int k = 0; buf[k++] = (char)(N + 63);
    int acc = 0, nb = 0;
    for (int j = 1; j < N; j++) for (int i = 0; i < j; i++) {
        int bit = 0;
        if (i < n && j >= n) bit = E[j - n] >> i & 1;
        acc = (acc << 1) | bit; nb++;
        if (nb == 6) { buf[k++] = (char)(acc + 63); acc = 0; nb = 0; }
    }
    if (nb) { acc <<= (6 - nb); buf[k++] = (char)(acc + 63); }
    buf[k++] = '\n'; fwrite(buf, 1, k, stdout);
}
static int maxdeg(u32 *E, int m, int n) { int d[32] = {0}, M = 0; for (int i = 0; i < m; i++) for (u32 r = E[i]; r; r &= r - 1) d[__builtin_ctz(r)]++;
    for (int i = 0; i < n; i++) if (d[i] > M) M = d[i]; return M; }

/* ---------- parsing ---------- */
static int read_found(char *line, u32 *E) {  /* "(a,b,c) ..." anywhere in the line */
    int m = 0; char *p = line;
    while ((p = strchr(p, '('))) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) == 3) { E[m++] = (1u << a) | (1u << b) | (1u << c); } p++; }
    return m;
}

/* ---------- extension search ---------- */
static int NG, TG, Dd, EP;
static u32 GE[MAXE]; static int Gm;
static int P; static u32 pm[MAXPAIRS]; static u64 *killb; static int W;
static int comp[32], ncompG;
static unsigned long long n_nodes, n_sol, n_conn, n_f7, n_out;
static int chosen[8];
static int comp_of_pair_mask(int p) { int a = __builtin_ctz(pm[p]), b = 31 - __builtin_clz(pm[p]); return (1 << comp[a]) | (1 << comp[b]); }
static int allcomp; static int NOCONN = 0; static unsigned long long u_f7free, u_p3, u_conn;
static void leaf(int nch) {
    n_sol++;
    int touched = 0; for (int i = 0; i < nch; i++) touched |= comp_of_pair_mask(chosen[i]);
    if (NOCONN) { u32 Y[MAXE]; int mm = Gm; memcpy(Y, GE, sizeof(u32) * Gm); for (int i = 0; i < nch; i++) Y[mm++] = pm[chosen[i]] | (1u << NG);
        if (touched == allcomp) u_conn++; if (!has_f7(Y, mm, NG + 1)) { u_f7free++; if (p3_ok(Y, mm, NG + 1)) u_p3++; } }
    if (touched != allcomp) return;
    n_conn++;
    u32 X[MAXE]; int m = Gm; memcpy(X, GE, sizeof(u32) * Gm);
    for (int i = 0; i < nch; i++) X[m++] = pm[chosen[i]] | (1u << NG);
    if (has_f7(X, m, NG + 1)) return;
    n_f7++;
    if (!p3_ok(X, m, NG + 1)) return;
    n_out++; put_g6(X, m, NG + 1);
}
static int popc_int(int x) { return __builtin_popcount((unsigned)x); }
/* free completion: choose (Dd - nch) further pairs from index >= start, not forbidden, disjoint */
static void freec(int nch, int start, u32 usedv, const u64 *forb, int touched) {
    if (nch == Dd) { leaf(nch); return; }
    if (!NOCONN && popc_int(allcomp & ~touched) > 2 * (Dd - nch)) return;
    for (int p = start; p < P; p++) {
        if (forb[p >> 6] >> (p & 63) & 1) continue;
        if (pm[p] & usedv) continue;
        chosen[nch] = p; freec(nch + 1, p + 1, usedv | pm[p], forb, touched | comp_of_pair_mask(p));
    }
}
static u64 alv[10][MAXCOV / 64 + 1];
static void search(int nch, const u64 *alive, u32 usedv, const u64 *forb, int touched) {
    n_nodes++;
    int c0 = -1; for (int w = 0; w < W; w++) if (alive[w]) { c0 = w * 64 + __builtin_ctzll(alive[w]); break; }
    if (c0 < 0) { freec(nch, 0, usedv, forb, touched); return; }
    if (nch == Dd) return;
    if (!NOCONN && popc_int(allcomp & ~touched) > 2 * (Dd - nch)) return;
    u64 f2[MAXPAIRS / 64 + 1]; memcpy(f2, forb, sizeof f2);
    u64 *a2 = alv[nch + 1];
    for (int p = 0; p < P; p++) {
        if (!(killb[(size_t)p * W + (c0 >> 6)] >> (c0 & 63) & 1)) continue;
        if (f2[p >> 6] >> (p & 63) & 1) continue;
        if (pm[p] & usedv) continue;
        chosen[nch] = p;
        if (nch + 1 == Dd) {   /* last pair: must kill everything alive */
            int ok = 1; for (int w = 0; w < W; w++) if (alive[w] & ~killb[(size_t)p * W + w]) { ok = 0; break; }
            if (ok) { n_nodes++; leaf(nch + 1); }
        } else {
            for (int w = 0; w < W; w++) a2[w] = alive[w] & ~killb[(size_t)p * W + w];
            search(nch + 1, a2, usedv | pm[p], f2, touched | comp_of_pair_mask(p));
        }
        f2[p >> 6] |= 1ull << (p & 63);
    }
}
static int mode_ext(int argc, char **argv) {
    NG = atoi(argv[2]); TG = atoi(argv[3]); Dd = atoi(argv[4]); EP = atoi(argv[5]); if (argc > 6 && !strcmp(argv[6], "noconn")) NOCONN = 1;
    if (NG > 30 || Dd > 6) { fprintf(stderr, "limits\n"); return 1; }
    cov = malloc(sizeof(u32) * MAXCOV);
    killb = malloc(sizeof(u64) * (size_t)MAXPAIRS * (MAXCOV / 64 + 1));
    unsigned long long ninp = 0, nbad = 0, maxcov = 0, totcov = 0;
    int m;
    while (scanf("%d", &m) == 1) {
        ninp++; Gm = m; int deg[32] = {0};
        for (int i = 0; i < m; i++) { int a, b, c; if (scanf("%d %d %d", &a, &b, &c) != 3) return 2;
            if (a < 0 || b < 0 || c < 0 || a >= NG || b >= NG || c >= NG || a == b || a == c || b == c) { fprintf(stderr, "bad label\n"); return 2; }
            GE[i] = (1u << a) | (1u << b) | (1u << c); deg[a]++; deg[b]++; deg[c]++; }
        int t = tau_of(GE, m);
        if (t != TG) { nbad++; continue; }
        long K = min_covers(GE, m, t);
        if ((unsigned long long)K > maxcov) maxcov = K; totcov += K;
        ncompG = ncomp_of(GE, m, NG, comp); allcomp = (ncompG >= 31) ? -1 : ((1 << ncompG) - 1);
        if (!NOCONN && ncompG > 2 * Dd) continue;   /* cannot be connected */
        P = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > EP || deg[b] > EP) continue;
            u32 pr = (1u << a) | (1u << b); int inside = 0;
            for (int i = 0; i < m; i++) if ((GE[i] & pr) == pr) { inside = 1; break; }
            if (inside) continue;
            if (P >= MAXPAIRS) { fprintf(stderr, "pairs\n"); return 4; }
            pm[P++] = pr;
        }
        W = (int)((K + 63) / 64);
        for (int p = 0; p < P; p++) { u64 *row = killb + (size_t)p * W; memset(row, 0, sizeof(u64) * W);
            for (long c = 0; c < K; c++) if (!(cov[c] & pm[p])) row[c >> 6] |= 1ull << (c & 63); }
        u64 *alive = alv[0]; memset(alive, 0, sizeof(u64) * W); for (long c = 0; c < K; c++) alive[c >> 6] |= 1ull << (c & 63);
        u64 forb[MAXPAIRS / 64 + 1]; memset(forb, 0, sizeof forb);
        search(0, alive, 0, forb, 0);
    }
    fflush(stdout);
    fprintf(stderr, "RSUMMARY inputs=%llu bad_tau=%llu max_covers=%llu sum_covers=%llu nodes=%llu killsets=%llu connected=%llu f7free=%llu out=%llu\n",
            ninp, nbad, maxcov, totcov, n_nodes, n_sol, n_conn, n_f7, n_out);
    if (NOCONN) fprintf(stderr, "UNPRUNED all_extensions_tau_ge_T=%llu connected=%llu f7free=%llu f7free_and_p3=%llu\n", n_sol, u_conn, u_f7free, u_p3);
    return 0;
}
static int mode_filt(int argc, char **argv) {
    int n = atoi(argv[2]), D = atoi(argv[3]); int raw = argc > 4 && !strcmp(argv[4], "raw");
    char line[8192]; u32 E[MAXE]; unsigned long long cnt = 0, bad = 0;
    while (fgets(line, sizeof line, stdin)) {
        int m;
        if (raw) { char *p = line; int k; if (sscanf(p, "%d%n", &m, &k) != 1) continue; p += k;
            for (int i = 0; i < m; i++) { int a, b, c; sscanf(p, "%d %d %d%n", &a, &b, &c, &k); p += k; E[i] = (1u << a) | (1u << b) | (1u << c); } }
        else { if (strncmp(line, "FOUND", 5)) continue; m = read_found(line, E); }
        cnt++;
        int lin = is_linear(E, m), f7 = !has_f7(E, m, n), p3 = p3_ok(E, m, n);
        int cp[32]; int nc = ncomp_of(E, m, n, cp); int t = tau_of(E, m); int md = maxdeg(E, m, n);
        u32 all = 0; for (int i = 0; i < m; i++) all |= E[i];
        int lab = (n == 32) ? 1 : ((all >> n) == 0);
        int ok = lin && f7 && p3 && nc == 1 && md <= D && lab;
        if (!ok) bad++;
        printf("%d %d %d %d %d %d %d %d\n", n, m, t, md, lin, f7, p3, nc == 1);
    }
    fprintf(stderr, "FSUMMARY graphs=%llu failing=%llu\n", cnt, bad);
    return 0;
}
static int mode_g6(int argc, char **argv) {
    int n = atoi(argv[2]); char line[8192]; u32 E[MAXE];
    while (fgets(line, sizeof line, stdin)) { if (!strchr(line, '(')) continue; int m = read_found(line, E); put_g6(E, m, n); }
    return 0;
}
static int decode_bip(const char *s, int n1, int n2, u32 *E) {
    int N = s[0] - 63; if (N != n1 + n2) return -1;
    const char *p = s + 1; int bitpos = 0;
    for (int j = 0; j < n2; j++) E[j] = 0;
    for (int j = 1; j < N; j++) for (int i = 0; i < j; i++) {
        int byte = p[bitpos / 6] - 63; int bit = (byte >> (5 - bitpos % 6)) & 1; bitpos++;
        if (bit) { if (i < n1 && j >= n1) E[j - n1] |= 1u << i; else return -2; }
    }
    for (int j = 0; j < n2; j++) if (pc(E[j]) != 3) return -3;
    return n2;
}
static int mode_gb(int argc, char **argv) {
    int n1 = atoi(argv[2]), n2 = atoi(argv[3]), t = atoi(argv[4]), D = atoi(argv[5]);
    char line[4096]; u32 E[MAXE]; unsigned long long cnt = 0, nl = 0, nf7 = 0, np3 = 0, nconn = 0, ntau = 0, nd = 0, nerr = 0;
    while (fgets(line, sizeof line, stdin)) {
        line[strcspn(line, "\n")] = 0; if (!line[0]) continue;
        cnt++;
        int m = decode_bip(line, n1, n2, E); if (m != n2) { nerr++; continue; }
        if (!is_linear(E, m)) continue; nl++;
        if (has_f7(E, m, n1)) continue; nf7++;
        if (!p3_ok(E, m, n1)) continue; np3++;
        int cp[32]; if (ncomp_of(E, m, n1, cp) != 1) continue; nconn++;
        if (maxdeg(E, m, n1) > D) continue; nd++;
        if (tau_of(E, m) != t) continue; ntau++;
        put_g6(E, m, n1);
    }
    fprintf(stderr, "GSUMMARY read=%llu decode_err=%llu linear=%llu f7free=%llu p3=%llu connected=%llu deg_ok=%llu tau_eq=%llu\n", cnt, nerr, nl, nf7, np3, nconn, nd, ntau);
    return 0;
}
int main(int argc, char **argv) {
    if (argc < 2) return 1;
    if (!strcmp(argv[1], "ext") && argc >= 6) return mode_ext(argc, argv);
    if (!strcmp(argv[1], "filt") && argc >= 4) return mode_filt(argc, argv);
    if (!strcmp(argv[1], "g6") && argc >= 3) return mode_g6(argc, argv);
    if (!strcmp(argv[1], "gb") && argc >= 6) return mode_gb(argc, argv);
    fprintf(stderr, "usage\n"); return 1;
}
