/* i11.c: falsification tools for I11 (11 tau <= 3n + 2m) on class C.
   modes: selftest | eval | extend | grow | anneal | subsa      (see README / REPORT.md) */
#include "i11core.h"
#define HOFF 60
#define HSZ 400

static FILE *OUT = NULL; static int REQCONN = 0; /* slack<=1 graphs */
static inline u64 mix(u64 x) { x ^= x >> 31; x *= 0x9E3779B97F4A7C15ULL; x ^= x >> 29; x *= 0xBF58476D1CE4E5B9ULL; x ^= x >> 32; return x; }
static unsigned long long fp_graph(const G *g) { /* isomorphism-invariant fingerprint: 5 rounds of colour refinement on the incidence graph */
    u64 vc[MAXN], ec[MAXM], nv_[MAXN];
    for (int v = 0; v < g->n; v++) vc[v] = mix(1 + degree_of(g, v));
    for (int r = 0; r < 5; r++) {
        for (int i = 0; i < g->m; i++) { u64 s = 0; for (u64 q = g->e[i]; q; q &= q - 1) s += mix(vc[__builtin_ctzll(q)]); ec[i] = mix(s); }
        for (int v = 0; v < g->n; v++) { u64 s = 0; for (int i = 0; i < g->m; i++) if ((g->e[i] >> v) & 1) s += mix(ec[i] + 77); nv_[v] = mix(vc[v] * 3 + s); }
        memcpy(vc, nv_, sizeof(u64) * g->n);
    }
    u64 h = 0; for (int v = 0; v < g->n; v++) h += mix(vc[v]); for (int i = 0; i < g->m; i++) h += mix(ec[i] ^ 0x5555); return h ^ ((u64)g->n << 56) ^ ((u64)g->m << 48);
}
#define SEEN_SZ (1 << 20)
static unsigned long long seen_tab[SEEN_SZ];
static int seen_insert(unsigned long long h) { if (!h) h = 1; unsigned i = (unsigned)(h >> 12) & (SEEN_SZ - 1); for (int k = 0; k < 64; k++) { unsigned j = (i + k) & (SEEN_SZ - 1); if (seen_tab[j] == h) return 0; if (!seen_tab[j]) { seen_tab[j] = h; return 1; } } return 0; }
static void report_low(const G *g, int tau, int slack, const char *tag) {
    if (slack < 0) { fprintf(stderr, "!!! SLACK<0 %s n=%d m=%d tau=%d slack=%d\n", tag, g->n, g->m, tau, slack); }
    if (slack <= 1 && OUT) { if (!seen_insert(fp_graph(g))) return; fprintf(OUT, "%d %d %d %d %s ", slack, g->n, g->m, tau, tag); print_graph(OUT, g); fflush(OUT); }
}

/* ---------- random edge helpers ---------- */
static int pick_vertex(const G *g, int nv, int bias) {
    for (int t = 0; t < 40; t++) {
        int v;
        if (bias && rndint(2)) { int k = 0; while (k < nv - 1 && rndint(5)) k++; v = nv - 1 - k; } else v = rndint(nv);
        if (DMAX <= 0 || degree_of(g, v) < DMAX) return v;
    }
    return -1;
}
static int grow_graph(G *g, int n, int m, int K, int *tau_out) {
    g->n = n; g->m = 0; g->e[g->m++] = vmask(0, 1, 2); int nv = 3;
    while (g->m < m) {
        int Q = m - g->m, R = n - nv;
        int kmin = R - 2 * (Q - 1); if (kmin < 0) kmin = 0; int kmax = R < 2 ? R : 2;
        if (kmin > kmax) return 0;
        G best; int bestt = -1, found = 0, bestk = 0;
        double r = (double)R / Q;
        for (int c = 0, att = 0; c < K && att < 40 * K; att++) {
            double w[3], tot = 0; for (int k = kmin; k <= kmax; k++) { w[k] = exp(-1.5 * (k - r) * (k - r)); tot += w[k]; }
            double x = rnd01() * tot; int k = kmin; for (; k < kmax; k++) { if (x < w[k]) break; x -= w[k]; }
            u64 e = 0; int ok = 1;
            for (int j = 0; j < k; j++) e |= 1ULL << (nv + j);
            for (int j = 0; j < 3 - k; j++) { int v = pick_vertex(g, nv, 1); if (v < 0 || ((e >> v) & 1)) { ok = 0; break; } e |= 1ULL << v; }
            if (!ok) continue;
            G t = *g; if (!try_add(&t, e)) continue;
            c++;
            int tt = (K > 1) ? tau_of(&t, 1, 0, NULL) : 0;
            if (!found || tt > bestt || (tt == bestt && rndint(2))) { best = t; bestt = tt; found = 1; bestk = k; }
        }
        if (!found) return 0;
        *g = best; nv += bestk;
    }
    if (nv != n) return 0;
    *tau_out = tau_of(g, 3, 0, NULL);
    return 1;
}

/* ---------- selftest ---------- */
static int brute_tau(const G *g) { /* n<=22 */
    int n = g->n, best = 0;
    for (unsigned s = 0; s < (1u << n); s++) { int ok = 1; for (int i = 0; i < g->m; i++) if ((g->e[i] & s) == g->e[i]) { ok = 0; break; } if (ok) { int c = __builtin_popcount(s); if (c > best) best = c; } }
    return n - best;
}
static int slow_class(const G *g, int dmax) { /* independent slow test, n<=15: e(S)<=|S|-2 over all subsets; F7 by 5-edge subsets */
    int n = g->n;
    for (int i = 0; i < g->m; i++) for (int j = i + 1; j < g->m; j++) if (__builtin_popcountll(g->e[i] & g->e[j]) >= 2) return 2;
    if (dmax > 0 && maxdeg(g) > dmax) return 3;
    for (unsigned s = 0; s < (1u << n); s++) { int sz = __builtin_popcount(s); if (sz < 2) continue; int c = 0; for (int i = 0; i < g->m; i++) if ((g->e[i] & s) == g->e[i]) c++; if (c > sz - 2) return 5; }
    int a[5];
    for (a[0] = 0; a[0] < g->m; a[0]++) for (a[1] = a[0] + 1; a[1] < g->m; a[1]++) for (a[2] = a[1] + 1; a[2] < g->m; a[2]++) for (a[3] = a[2] + 1; a[3] < g->m; a[3]++) for (a[4] = a[3] + 1; a[4] < g->m; a[4]++) {
        u64 U = 0; for (int k = 0; k < 5; k++) U |= g->e[a[k]];
        if (__builtin_popcountll(U) != 7) continue;
        int d3 = 0, d2 = 0; for (u64 r = U; r; r &= r - 1) { int v = __builtin_ctzll(r), d = 0; for (int k = 0; k < 5; k++) d += (g->e[a[k]] >> v) & 1; if (d == 3) d3++; else if (d == 2) d2++; }
        if (d3 == 1 && d2 == 6) return 4;
    }
    return 0;
}
static int selftest(void) {
    seed_rng(12345); int bad = 0;
    /* tau DP vs brute force on random C-graphs (growth) */
    int nt = 0; for (int it = 0; it < 1500; it++) {
        int n = 6 + rndint(15); int m = 2 + rndint(n - 3); G g; int t; DMAX = 3 + rndint(3);
        if (!grow_graph(&g, n, m, 1, &t)) continue; nt++;
        int b = brute_tau(&g); double lc; int t2 = tau_of(&g, 2, 1, &lc);
        if (b != t || b != t2) { printf("TAU MISMATCH n=%d m=%d brute=%d dp=%d dp2=%d\n", n, m, b, t, t2); bad++; }
    }
    printf("tau tests on %d graphs, bad=%d\n", nt, bad);
    /* class check vs slow check on random edge soups (incl. non-C) */
    int agree = 0, inC = 0, nsoup = 0; DMAX = 0;
    for (int it = 0; it < 30000; it++) {
        G g; g.n = 8 + rndint(8); g.m = 0; int target = 3 + rndint(g.n); /* random edges, rejecting only non-3-sets */
        while (g.m < target) { int a = rndint(g.n), b = rndint(g.n), c = rndint(g.n); if (a == b || b == c || a == c) continue; g.e[g.m++] = vmask(a, b, c); }
        int sl = slow_class(&g, 0), fs = check_class(&g, 0); nsoup++;
        if ((sl == 0) != (fs == 0)) { printf("CLASS MISMATCH slow=%d fast=%d\n", sl, fs); print_graph(stdout, &g); bad++; } else agree++;
        if (fs == 0) inC++;
    }
    printf("class tests %d, in C %d, bad=%d\n", nsoup, inC, bad);
    /* incremental try_add vs full check, from growth */
    int inc_bad = 0, inc_tests = 0; DMAX = 0;
    for (int it = 0; it < 3000; it++) {
        G g; int t; int n = 8 + rndint(7); if (!grow_graph(&g, n, n - 2 - rndint(3), 1, &t)) continue;
        for (int k = 0; k < 20; k++) {
            int a = rndint(n), b = rndint(n), c = rndint(n); if (a == b || b == c || a == c) continue;
            u64 e = vmask(a, b, c); G h = g; h.e[h.m++] = e; int full = (check_class(&h, 0) == 0);
            G h2 = g; int inc = try_add(&h2, e); inc_tests++; if (full != inc) { inc_bad++; printf("INC MISMATCH full=%d inc=%d\n", full, inc); }
        }
    }
    printf("incremental tests %d bad=%d\n", inc_tests, inc_bad);
    return bad + inc_bad;
}

/* ---------- eval ---------- */
static void eval_mode(void) {
    static char line[1 << 16]; G g; long cnt = 0;
    while (fgets(line, sizeof line, stdin)) {
        if (!parse_graph(line, &g)) { printf("PARSEFAIL\n"); continue; }
        int cc = check_class(&g, 0); int iso; int nc = components(&g, &iso);
        double lc; int tau = tau_of(&g, 3, 1, &lc);
        printf("%d %d %d %d %d %d %d %d\n", g.n, g.m, tau, slack_of(&g, tau), cc, maxdeg(&g), nc, iso); cnt++;
    }
}

/* ---------- extend: all single-edge extensions ---------- */
static void extend_mode(int dmax) {
    static char line[1 << 16]; G g; static long hist[MAXN + 3][MAXM + 3][HSZ]; static int minsl[MAXN + 3][MAXM + 3]; for (int i = 0; i < MAXN + 3; i++) for (int j = 0; j < MAXM + 3; j++) minsl[i][j] = 9999;
    long nin = 0, next = 0; DMAX = dmax;
    while (fgets(line, sizeof line, stdin)) {
        if (!parse_graph(line, &g)) continue; if (check_class(&g, 0) != 0) { fprintf(stderr, "input not in C\n"); continue; } nin++;
        int n0 = g.n;
        for (int k = 0; k <= 2; k++) {
            if (n0 + k > MAXN - 1) continue;
            G h = g; h.n = n0 + k;
            if (k == 0) { for (int a = 0; a < n0; a++) for (int b = a + 1; b < n0; b++) for (int c = b + 1; c < n0; c++) { G t = h; if (try_add(&t, vmask(a, b, c))) goto emit0; continue; emit0:; int tau = tau_of(&t, 2, 0, NULL); int s = slack_of(&t, tau); next++; if (s + HOFF >= 0 && s + HOFF < HSZ) hist[t.n][t.m][s + HOFF]++; if (s < minsl[t.n][t.m]) minsl[t.n][t.m] = s; report_low(&t, tau, s, "ext"); } }
            else if (k == 1) { for (int a = 0; a < n0; a++) for (int b = a + 1; b < n0; b++) { G t = h; if (!try_add(&t, vmask(a, b, n0))) continue; int tau = tau_of(&t, 2, 0, NULL); int s = slack_of(&t, tau); next++; if (s + HOFF >= 0 && s + HOFF < HSZ) hist[t.n][t.m][s + HOFF]++; if (s < minsl[t.n][t.m]) minsl[t.n][t.m] = s; report_low(&t, tau, s, "ext"); } }
            else { for (int a = 0; a < n0; a++) { G t = h; if (!try_add(&t, vmask(a, n0, n0 + 1))) continue; int tau = tau_of(&t, 2, 0, NULL); int s = slack_of(&t, tau); next++; if (s + HOFF >= 0 && s + HOFF < HSZ) hist[t.n][t.m][s + HOFF]++; if (s < minsl[t.n][t.m]) minsl[t.n][t.m] = s; report_low(&t, tau, s, "ext"); } }
        }
    }
    printf("EXTEND inputs=%ld extensions=%ld\n", nin, next);
    for (int n = 0; n < MAXN + 3; n++) for (int m = 0; m < MAXM + 3; m++) if (minsl[n][m] < 9999) { printf("CELL %d %d minslack %d hist", n, m, minsl[n][m]); for (int s = 0; s < HSZ; s++) if (hist[n][m][s]) printf(" %d:%ld", s - HOFF, hist[n][m][s]); printf("\n"); }
}

/* ---------- grow ---------- */
static void grow_mode(int n, int mlo, int mhi, long samples, u64 seed, int K) {
    seed_rng(seed); static long hist[MAXM + 3][HSZ]; static int minsl[MAXM + 3]; static long ok[MAXM + 3], tried[MAXM + 3];
    for (int i = 0; i < MAXM + 3; i++) minsl[i] = 9999;
    for (long s = 0; s < samples; s++) {
        int m = mlo + rndint(mhi - mlo + 1); G g; int tau; tried[m]++;
        if (!grow_graph(&g, n, m, K, &tau)) continue; ok[m]++;
        if (tau < 0) { continue; }
        int sl = slack_of(&g, tau); if (sl + HOFF >= 0 && sl + HOFF < HSZ) hist[m][sl + HOFF]++; if (sl < minsl[m]) minsl[m] = sl;
        report_low(&g, tau, sl, "grow");
    }
    for (int m = mlo; m <= mhi; m++) { printf("GROW n=%d m=%d K=%d tried=%ld ok=%ld minslack=%d hist", n, m, K, tried[m], ok[m], minsl[m]); for (int s = 0; s < HSZ; s++) if (hist[m][s]) printf(" %d:%ld", s - HOFF, hist[m][s]); printf("\n"); }
}

/* ---------- anneal ---------- */
static void anneal_mode(int n, long iters, u64 seed, double T0, double T1, double lam, const char *startfile, int mmin, int mmax) {
    seed_rng(seed); G g; int tau = 0; double lc = 0;
    int got = 0;
    if (startfile && strcmp(startfile, "-")) { FILE *f = fopen(startfile, "r"); static char line[1 << 16]; if (f && fgets(line, sizeof line, f) && parse_graph(line, &g)) { got = 1; if (g.n < n) g.n = n; if (check_class(&g, DMAX) != 0) { fprintf(stderr, "start not in C\n"); return; } } if (f) fclose(f); }
    if (!got) { int tries = 0; while (!grow_graph(&g, n, (mmin + mmax) / 2, 4, &tau) && tries++ < 10000); if (tries >= 10000) { fprintf(stderr, "no start\n"); return; } }
    tau = tau_of(&g, 2, 1, &lc);
    double F = 11.0 * tau - 2.0 * g.m - lam * lc; int bestslack = slack_of(&g, tau); G bestg = g; int bestt = tau;
    static long hist[HSZ]; long evals = 0, acc = 0; long nlow = 0;
    for (long it = 0; it < iters; it++) {
        double T = T0 * pow(T1 / T0, (double)it / iters);
        G h = g; double r = rnd01(); int okmove = 0;
        if (r < 0.45) { /* relocate */
            int i = rndint(h.m); h.e[i] = h.e[--h.m]; /* removal keeps C */
            int v[3]; int ok = 1; u64 e = 0; for (int j = 0; j < 3; j++) { v[j] = pick_vertex(&h, n, 0); if (v[j] < 0 || ((e >> v[j]) & 1)) { ok = 0; break; } e |= 1ULL << v[j]; }
            okmove = ok && try_add(&h, e);
        } else if (r < 0.75) { /* replace one vertex of an edge */
            int i = rndint(h.m); u64 old = h.e[i]; h.e[i] = h.e[--h.m]; int vs[3], k = 0; for (u64 q = old; q; q &= q - 1) vs[k++] = __builtin_ctzll(q);
            int j = rndint(3); int nv_ = pick_vertex(&h, n, 0); u64 e = old & ~(1ULL << vs[j]);
            okmove = (nv_ >= 0 && !((e >> nv_) & 1) && nv_ != vs[j]) ? try_add(&h, e | (1ULL << nv_)) : 0;
        } else if (r < 0.88) { /* add */
            if (h.m < mmax) { u64 e = 0; int ok = 1; for (int j = 0; j < 3; j++) { int v = pick_vertex(&h, n, 0); if (v < 0 || ((e >> v) & 1)) { ok = 0; break; } e |= 1ULL << v; } okmove = ok && try_add(&h, e); }
        } else { /* remove */
            if (h.m > mmin) { int i = rndint(h.m); h.e[i] = h.e[--h.m]; okmove = 1; }
        }
        if (!okmove) continue;
        if (REQCONN) { int iso_; if (components(&h, &iso_) != 1 || iso_ != 0) continue; }
        double lc2; int t2 = tau_of(&h, 2, 1, &lc2); evals++; if (t2 < 0) continue;
        double F2 = 11.0 * t2 - 2.0 * h.m - lam * lc2;
        if (F2 >= F || rnd01() < exp((F2 - F) / T)) {
            g = h; F = F2; tau = t2; acc++;
            int sl = slack_of(&g, tau); if (sl + HOFF >= 0 && sl + HOFF < HSZ) hist[sl + HOFF]++;
            if (sl <= 1) nlow++;
            report_low(&g, tau, sl, "sa");
            if (sl < bestslack) { bestslack = sl; bestg = g; bestt = tau; }
        }
    }
    printf("ANNEAL n=%d iters=%ld evals=%ld accepted=%ld best_slack=%d (m=%d tau=%d) visits_slack<=1=%ld hist", n, iters, evals, acc, bestslack, bestg.m, bestt, nlow);
    for (int s = 0; s < HSZ; s++) if (hist[s]) printf(" %d:%ld", s - HOFF, hist[s]); printf("\n");
    printf("BEST "); print_graph(stdout, &bestg);
}

/* ---------- subset annealing on a big base graph (induced subhypergraphs; always in C if base is) ---------- */
static void subsa_mode(const char *file, int size, long iters, u64 seed, double T0, double T1) {
    seed_rng(seed); FILE *f = fopen(file, "r"); static char line[1 << 16]; int N = 0, M = 0; static int tri[400][3];
    if (!f || !fgets(line, sizeof line, f)) { fprintf(stderr, "cannot read base\n"); return; }
    int off; sscanf(line, "%d %d%n", &N, &M, &off); const char *p = line + off; for (int i = 0; i < M; i++) { int o; sscanf(p, " %d,%d,%d%n", &tri[i][0], &tri[i][1], &tri[i][2], &o); p += o; } fclose(f);
    int inset[200] = {0}, in[200], out[200], nin = 0, nout = 0;
    /* random start: grow a connected-ish subset by BFS from random vertex */
    int order[200]; for (int i = 0; i < N; i++) order[i] = i; for (int i = N - 1; i > 0; i--) { int j = rndint(i + 1); int t = order[i]; order[i] = order[j]; order[j] = t; }
    if (REQCONN) { int q[200], qh = 0, qt = 0, vis[200] = {0}; int s0 = order[0]; q[qt++] = s0; vis[s0] = 1; int cnt_ = 0;
        while (qh < qt && cnt_ < size) { int v = q[qh++]; inset[v] = 1; cnt_++; for (int i = 0; i < M; i++) for (int j = 0; j < 3; j++) if (tri[i][j] == v) for (int k = 0; k < 3; k++) { int u = tri[i][k]; if (!vis[u]) { vis[u] = 1; q[qt++] = u; } } }
        for (int i = 0; cnt_ < size && i < N; i++) if (!inset[order[i]]) { inset[order[i]] = 1; cnt_++; } }
    else for (int i = 0; i < size; i++) inset[order[i]] = 1;
    #define BUILD(h, tauvar, slv) { int map[200]; int k = 0; for (int v = 0; v < N; v++) map[v] = inset[v] ? k++ : -1; (h).n = size; (h).m = 0; \
        for (int i = 0; i < M; i++) if (inset[tri[i][0]] && inset[tri[i][1]] && inset[tri[i][2]]) (h).e[(h).m++] = vmask(map[tri[i][0]], map[tri[i][1]], map[tri[i][2]]); \
        tauvar = tau_of(&(h), 2, 0, NULL); slv = slack_of(&(h), tauvar); }
    G h; int tau, sl; BUILD(h, tau, sl); int best = 9999; long evals = 0; static long hist[HSZ];
    #define PEN(hh) ({ int iso_; int nc_ = components(&(hh), &iso_); (REQCONN && (nc_ != 1 || iso_)) ? 8 * (nc_ - 1 + iso_) + 4 : 0; })
    int pen = PEN(h); int obj = sl + pen; if (!pen) best = sl;
    for (long it = 0; it < iters; it++) {
        double T = T0 * pow(T1 / T0, (double)it / iters);
        nin = nout = 0; for (int v = 0; v < N; v++) { if (inset[v]) in[nin++] = v; else out[nout++] = v; }
        int a = in[rndint(nin)], b = out[rndint(nout)]; inset[a] = 0; inset[b] = 1;
        G h2; int t2, s2; BUILD(h2, t2, s2); evals++; int p2 = PEN(h2); int o2 = s2 + p2;
        if (o2 <= obj || rnd01() < exp((double)(obj - o2) / T)) { obj = o2; sl = s2; tau = t2; h = h2; pen = p2; if (!pen) { if (sl + HOFF >= 0 && sl + HOFF < HSZ) hist[sl + HOFF]++; if (sl < best) best = sl; report_low(&h, tau, sl, "sub"); } }
        else { inset[a] = 1; inset[b] = 0; }
    }
    printf("SUBSA base=%s size=%d evals=%ld best_slack=%d hist", file, size, evals, best); for (int s = 0; s < HSZ; s++) if (hist[s]) printf(" %d:%ld", s - HOFF, hist[s]); printf("\n");
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage\n"); return 1; }
    const char *mode = argv[1]; const char *outf = getenv("I11_OUT"); if (outf) OUT = fopen(outf, "a");
    const char *rc = getenv("I11_CONN"); if (rc) REQCONN = atoi(rc);
    const char *dm = getenv("I11_DMAX"); if (dm) DMAX = atoi(dm);
    if (!strcmp(mode, "selftest")) return selftest() ? 1 : 0;
    if (!strcmp(mode, "eval")) { eval_mode(); return 0; }
    if (!strcmp(mode, "extend")) { extend_mode(DMAX); return 0; }
    if (!strcmp(mode, "grow")) { grow_mode(atoi(argv[2]), atoi(argv[3]), atoi(argv[4]), atol(argv[5]), (u64)atoll(argv[6]), atoi(argv[7])); return 0; }
    if (!strcmp(mode, "anneal")) { anneal_mode(atoi(argv[2]), atol(argv[3]), (u64)atoll(argv[4]), atof(argv[5]), atof(argv[6]), atof(argv[7]), argv[8], atoi(argv[9]), atoi(argv[10])); return 0; }
    if (!strcmp(mode, "subsa")) { subsa_mode(argv[2], atoi(argv[3]), atol(argv[4]), (u64)atoll(argv[5]), atof(argv[6]), atof(argv[7])); return 0; }
    return 1;
}
