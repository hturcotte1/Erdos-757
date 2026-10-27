/* ptsa.c: PT falsifier searches.  modes:
   gad N iters seed T0 T1 lam mmin mmax   : SA over graphs G = pendant hub gadget (7 vertices 0..6) + R on [7,N); minimise slack(G).
   u2  N iters seed S0 mmin mmax [start]   : SA over connected G'' (deg<=3) on N vertices maximising the number of avoided
                                             vertices of degree<=2 (and PT-candidate closeness) subject to slack(G'')<=S0 (soft). */
#include "i11core.h"
#define HOFF 60
#define HSZ 200
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


static int pick_in(const G *g, int lo, int hi) { /* random vertex in [lo,hi) with degree < DMAX */
    for (int t = 0; t < 40; t++) { int v = lo + rndint(hi - lo); if (DMAX <= 0 || degree_of(g, v) < DMAX) return v; }
    return -1;
}
static void print_edges(FILE *f, const G *g) { for (int i = 0; i < g->m; i++) { fprintf(f, " "); int k = 0; for (u64 r = g->e[i]; r; r &= r - 1) fprintf(f, k++ ? ",%d" : "%d", __builtin_ctzll(r)); } }
static void rm_edge(G *g, int i) { g->e[i] = g->e[--g->m]; }

/* ------------------- gadget mode ------------------- */
static int build_gadget_start(G *g, int N) {
    g->n = N; g->m = 0; DMAX = 3;
    u64 fx[4] = { vmask(1, 2, 3), vmask(0, 1, 4), vmask(0, 2, 5), vmask(0, 3, 6) };
    for (int i = 0; i < 4; i++) if (!try_add(g, fx[i])) return 0;
    for (int t = 0; t < 3; t++) {
        int a = 4 + t, p, q, tries = 0;
        do { p = pick_in(g, 7, N); q = pick_in(g, 7, N); tries++; } while ((p < 0 || q < 0 || p == q || !try_add(g, vmask(a, p, q))) && tries < 200);
        if (tries >= 200) return 0;
    }
    return 1;
}
static int is_movable(u64 e) { /* all vertices >= 7, or attach edge (contains exactly one of 4,5,6 and no other of 0..6) */
    u64 low = e & 127ULL; if (!low) return 1; if (__builtin_popcountll(low) == 1 && (low & 0x70)) return 1; return 0;
}
static void gad_mode(int N, long iters, u64 seed, double T0, double T1, double lam, int mmin, int mmax) {
    seed_rng(seed); G g; DMAX = 3; int tries = 0;
    while (!build_gadget_start(&g, N) && tries++ < 1000);
    if (tries >= 1000) { printf("no start\n"); return; }
    /* grow R randomly to about mmin+(mmax-mmin)/2 edges */
    int target = (mmin + mmax) / 2; int stuck = 0;
    while (g.m < target && stuck < 5000) { u64 e = 0; int ok = 1; for (int j = 0; j < 3; j++) { int v = pick_in(&g, 7, N); if (v < 0 || ((e >> v) & 1)) { ok = 0; break; } e |= 1ULL << v; } if (ok && try_add(&g, e)) stuck = 0; else stuck++; }
    double lc; int tau = tau_of(&g, 2, 1, &lc);
    double F = 11.0 * tau - 2.0 * g.m - lam * lc; int bestsl = slack_of(&g, tau); G bestg = g; int bestt = tau;
    static long hist[HSZ]; long evals = 0, acc = 0;
    for (long it = 0; it < iters; it++) {
        double T = T0 * pow(T1 / T0, (double)it / iters); G h = g; double r = rnd01(); int ok = 0;
        int idx[MAXM], nm = 0; for (int i = 0; i < h.m; i++) if (is_movable(h.e[i])) idx[nm++] = i;
        if (r < 0.40 && nm) { /* relocate */
            int i = idx[rndint(nm)]; u64 old = h.e[i]; rm_edge(&h, i); u64 low = old & 127ULL; u64 e = low; int need = 3 - __builtin_popcountll(low); int good = 1;
            for (int j = 0; j < need; j++) { int v = pick_in(&h, 7, N); if (v < 0 || ((e >> v) & 1)) { good = 0; break; } e |= 1ULL << v; }
            ok = good && try_add(&h, e);
        } else if (r < 0.75 && nm) { /* replace one free vertex */
            int i = idx[rndint(nm)]; u64 old = h.e[i]; rm_edge(&h, i); int vs[3], k = 0; for (u64 q = old; q; q &= q - 1) { int v = __builtin_ctzll(q); if (v >= 7) vs[k++] = v; }
            int j = rndint(k); int nv = pick_in(&h, 7, N); u64 e = old & ~(1ULL << vs[j]);
            ok = (nv >= 7 && nv != vs[j] && !((e >> nv) & 1)) ? try_add(&h, e | (1ULL << nv)) : 0;
        } else if (r < 0.88) { if (h.m < mmax) { u64 e = 0; int good = 1; for (int j = 0; j < 3; j++) { int v = pick_in(&h, 7, N); if (v < 0 || ((e >> v) & 1)) { good = 0; break; } e |= 1ULL << v; } ok = good && try_add(&h, e); } }
        else { if (h.m > mmin && nm) { int c = 0; for (int q = 0; q < nm; q++) if ((h.e[idx[q]] & 127ULL) == 0) c++; if (c) { int i; do i = idx[rndint(nm)]; while (h.e[i] & 127ULL); rm_edge(&h, i); ok = 1; } } }
        if (!ok) continue;
        double lc2; int t2 = tau_of(&h, 2, 1, &lc2); evals++; if (t2 < 0) continue;
        double F2 = 11.0 * t2 - 2.0 * h.m - lam * lc2;
        if (F2 >= F || rnd01() < exp((F2 - F) / T)) {
            g = h; F = F2; tau = t2; acc++; int sl = slack_of(&g, tau);
            int iso; int nc = components(&g, &iso);
            if (sl + HOFF >= 0 && sl + HOFF < HSZ && nc == 1 && iso == 0) hist[sl + HOFF]++;
            if (nc == 1 && iso == 0 && sl < bestsl) { bestsl = sl; bestg = g; bestt = tau; }
            if (sl < 0 && nc == 1 && iso == 0) { fprintf(stderr, "!!! SLACK<0 gad N=%d\n", N); printf("VIOLATOR %d %d %d slack %d edges", g.n, g.m, tau, sl); print_edges(stdout, &g); printf("\n"); fflush(stdout); }
        }
    }
    printf("GAD N=%d (n''=%d) seed=%llu iters=%ld evals=%ld acc=%ld best_slack=%d (m=%d tau=%d) hist", N, N - 7, (unsigned long long)seed, iters, evals, acc, bestsl, bestg.m, bestt);
    for (int s = 0; s < HSZ; s++) if (hist[s]) printf(" %d:%ld", s - HOFF, hist[s]); printf("\nBEST");
    print_edges(stdout, &bestg); printf("\n");
}

/* ------------------- u2 mode ------------------- */
typedef struct { int tau, slack, nU, nU2, U2[MAXN], ncand, minGood; } Ev;
static int tau_without(const G *g, int v) { G h; h.n = g->n; h.m = 0; for (int i = 0; i < g->m; i++) if (!((g->e[i] >> v) & 1)) h.e[h.m++] = g->e[i]; return tau_of(&h, 2, 0, NULL); }
static int tau_without3(const G *g, u64 X) { G h; h.n = g->n; h.m = 0; for (int i = 0; i < g->m; i++) if (!(g->e[i] & X)) h.e[h.m++] = g->e[i]; return tau_of(&h, 2, 0, NULL); }
static void evaluate(const G *g, Ev *ev, int do_pt) {
    ev->tau = tau_of(g, 2, 0, NULL); ev->slack = slack_of(g, ev->tau); ev->nU = 0; ev->nU2 = 0; ev->ncand = 0; ev->minGood = 99;
    for (int v = 0; v < g->n; v++) { int d = degree_of(g, v); if (d == 0 || d > 2) continue; if (tau_without(g, v) == ev->tau) { ev->nU2++; ev->U2[ev->nU2 - 1] = v; } }
    if (!do_pt || ev->nU2 < 6) return;
    int np = 0; static int pr[MAXN * MAXN][2];
    for (int i = 0; i < ev->nU2; i++) for (int j = i + 1; j < ev->nU2; j++) { int a = ev->U2[i], b = ev->U2[j]; int inedge = 0; for (int e = 0; e < g->m; e++) if (((g->e[e] >> a) & 1) && ((g->e[e] >> b) & 1)) { inedge = 1; break; } if (!inedge) { pr[np][0] = a; pr[np][1] = b; np++; } }
    int cnt = 0;
    for (int x = 0; x < np; x++) for (int y = x + 1; y < np; y++) {
        if (pr[x][0] == pr[y][0] || pr[x][0] == pr[y][1] || pr[x][1] == pr[y][0] || pr[x][1] == pr[y][1]) continue;
        for (int z = y + 1; z < np; z++) {
            int *A = pr[x], *B = pr[y], *C = pr[z];
            if (A[0] == C[0] || A[0] == C[1] || A[1] == C[0] || A[1] == C[1] || B[0] == C[0] || B[0] == C[1] || B[1] == C[0] || B[1] == C[1]) continue;
            if (++cnt > 40) goto done;
            ev->ncand++; int good = 0;
            for (int i = 0; i < 2; i++) for (int j = 0; j < 2; j++) for (int k = 0; k < 2; k++) { u64 X = (1ULL << A[i]) | (1ULL << B[j]) | (1ULL << C[k]); if (tau_without3(g, X) <= ev->tau - 2) good++; }
            if (good < ev->minGood) ev->minGood = good;
        }
    }
done:;
}
static double phi(const Ev *ev, int S0) {
    double p = 3.0 * (ev->nU2 < 8 ? ev->nU2 : 8);
    if (ev->ncand > 0) p += 10.0 - 1.0 * ev->minGood;
    if (ev->slack > S0) p -= 2.0 * (ev->slack - S0);
    return p;
}
static void u2_mode(int N, long iters, u64 seed, int S0, int mmin, int mmax, double T0, double T1, const char *startfile) {
    seed_rng(seed); G g; DMAX = 3; int got = 0, tau0;
    if (startfile && strcmp(startfile, "-")) { FILE *f = fopen(startfile, "r"); static char line[1 << 16]; if (f && fgets(line, sizeof line, f) && parse_graph(line, &g)) { got = 1; if (g.n < N) g.n = N; } if (f) fclose(f); }
    if (!got) { int tries = 0; while (!grow_graph(&g, N, (mmin + mmax) / 2, 4, &tau0) && tries++ < 20000); if (tries >= 20000) { printf("no start\n"); return; } }
    Ev ev; evaluate(&g, &ev, 1); double P = phi(&ev, S0);
    static long histU[HSZ][12]; static int maxU2[HSZ]; static int minslack_cfg = 999; long acc = 0, evals = 0; int bestnU[HSZ]; for (int i = 0; i < HSZ; i++) bestnU[i] = -1;
    int bestmin = 99;
    for (long it = 0; it < iters; it++) {
        double T = T0 * pow(T1 / T0, (double)it / iters); G h = g; double r = rnd01(); int ok = 0;
        if (r < 0.40) { int i = rndint(h.m); rm_edge(&h, i); u64 e = 0; int good = 1; for (int j = 0; j < 3; j++) { int v = pick_in(&h, 0, N); if (v < 0 || ((e >> v) & 1)) { good = 0; break; } e |= 1ULL << v; } ok = good && try_add(&h, e); }
        else if (r < 0.75) { int i = rndint(h.m); u64 old = h.e[i]; rm_edge(&h, i); int vs[3], k = 0; for (u64 q = old; q; q &= q - 1) vs[k++] = __builtin_ctzll(q); int j = rndint(3); int nv = pick_in(&h, 0, N); u64 e = old & ~(1ULL << vs[j]); ok = (nv >= 0 && nv != vs[j] && !((e >> nv) & 1)) ? try_add(&h, e | (1ULL << nv)) : 0; }
        else if (r < 0.88) { if (h.m < mmax) { u64 e = 0; int good = 1; for (int j = 0; j < 3; j++) { int v = pick_in(&h, 0, N); if (v < 0 || ((e >> v) & 1)) { good = 0; break; } e |= 1ULL << v; } ok = good && try_add(&h, e); } }
        else { if (h.m > mmin) { rm_edge(&h, rndint(h.m)); ok = 1; } }
        if (!ok) continue;
        int iso; if (components(&h, &iso) != 1 || iso != 0) continue;
        Ev e2; evaluate(&h, &e2, 1); evals++; double P2 = phi(&e2, S0);
        if (P2 >= P || rnd01() < exp((P2 - P) / T)) {
            g = h; ev = e2; P = P2; acc++;
            int sl = ev.slack; if (sl + HOFF >= 0 && sl + HOFF < HSZ) { int u = ev.nU2 < 11 ? ev.nU2 : 11; histU[sl + HOFF][u]++; if (ev.nU2 > maxU2[sl + HOFF]) maxU2[sl + HOFF] = ev.nU2; }
            if (ev.slack < 0) { printf("VIOLATOR(G'') n %d m %d tau %d slack %d edges", g.n, g.m, ev.tau, ev.slack); print_edges(stdout, &g); printf("\n"); fflush(stdout); }
            if (ev.ncand > 0) { if (ev.slack < minslack_cfg) minslack_cfg = ev.slack; if (ev.minGood < bestmin || ev.minGood == 0) { if (ev.minGood < bestmin) bestmin = ev.minGood; printf("CAND n %d m %d tau %d slack %d nU2 %d ncand %d minGood %d edges", g.n, g.m, ev.tau, ev.slack, ev.nU2, ev.ncand, ev.minGood); print_edges(stdout, &g); printf("\n"); fflush(stdout); } }
        }
    }
    printf("U2 N=%d seed=%llu S0=%d iters=%ld evals=%ld acc=%ld bestMinGood=%d minslack_with_cand=%d\n", N, (unsigned long long)seed, S0, iters, evals, acc, bestmin, minslack_cfg);
    for (int s = 0; s < HSZ; s++) if (maxU2[s] || histU[s][0]) { printf("SLACKROW %d maxU2 %d hist", s - HOFF, maxU2[s]); for (int u = 0; u < 12; u++) if (histU[s][u]) printf(" %d:%ld", u, histU[s][u]); printf("\n"); }
    printf("FINAL"); print_edges(stdout, &g); printf("\n");
}
int main(int argc, char **argv) {
    if (argc < 2) return 1;
    if (!strcmp(argv[1], "gad")) gad_mode(atoi(argv[2]), atol(argv[3]), (u64)atoll(argv[4]), atof(argv[5]), atof(argv[6]), atof(argv[7]), atoi(argv[8]), atoi(argv[9]));
    else if (!strcmp(argv[1], "u2")) u2_mode(atoi(argv[2]), atol(argv[3]), (u64)atoll(argv[4]), atoi(argv[5]), atoi(argv[6]), atoi(argv[7]), atof(argv[8]), atof(argv[9]), argc > 10 ? argv[10] : "-");
    return 0;
}
