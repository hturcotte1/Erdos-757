/*
 * C port of the hot loop of e757/ordered_dfs.py (independent exact DFS over the ordered-midpoint class
 * O(n)).  Same mathematics, see the docstring of ordered_dfs.py for the soundness arguments:
 *   - monotone midpoints as the staircase M[i] (new edge (i,j,k) legal iff k > M[i]);
 *   - alpha look-ahead: an independent set of size T+1 in V minus (still-feasible midpoints), w.r.t. the
 *     current edges, kills the subtree;
 *   - forced-none budget check; optional F7-freeness; optional Henning-Yeo m bound (hy=1).
 *
 * Usage: ordered_dfs n=16 T=9 m_min=13 [m_exact=-1] [f7=0] [mode=enum|min|count|estimate] [tl=seconds]
 *                    [hy=0] [refl=0] [mono=1] [probes=2000] [seed=1] [limit=0] [progress=1]
 * Output (stdout, one item per line):
 *   SOL <alpha> i,j,k i,j,k ...      (mode enum / min; in min mode every improving solution)
 *   PROG ...                         progress (level-1 / level-2 completion, elapsed seconds)
 *   EST ...                          estimator result (mode estimate)
 *   DONE nodes=.. leaves=.. solutions=.. timed_out=0|1 time=..
 * n <= 32.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <math.h>

typedef uint32_t u32;
#define MAXN 32

static int maxdeg = 99;
static int n, T, m_min, m_exact = -1, f7 = 0, hy = 0, refl = 0, mono = 1, limit = 0, progress = 1;
static double tl = 0;
static int mode_enum = 1, mode_min = 0, mode_count = 0, mode_est = 0;
static long long nodes = 0, leaves = 0, solutions = 0;
static int stopped = 0, timed_out = 0;
static double t0;
/* prefix split: pre=i-k,i-k,x,... fixes the choice at midpoints 1..plen (x = no edge); mode=prefixes depth=d prints
 * every surviving node at level d+1 as "PRE <choices>" (same syntax), without searching below. */
static int plen = 0, pre_i[MAXN], pre_k[MAXN], pdepth = 0, mode_pref = 0;
static int cur_i[MAXN], cur_k[MAXN];

/* edge stack */
static int E_i[MAXN], E_j[MAXN], E_k[MAXN], ne = 0;
static u32 E_mask[MAXN];
/* by-vertex lists of "other two" masks */
static u32 ev[MAXN][MAXN];
static int evn[MAXN];

static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

static int hy_need(int T_) { /* ceil((12n - 17T)/3), >= 0 */
    int x = 12 * n - 17 * T_;
    if (x <= 0) return 0;
    return (x + 2) / 3;
}
static int m_need(void) {
    int m = m_min;
    if (hy && f7 && hy_need(T) > m) m = hy_need(T);
    return m;
}

/* branch and bound for an independent set; returns best size found, early exit at stop_at */
static int ind_search(u32 cand, u32 chosen, int size, int best, int stop_at) {
    if (size > best) { best = size; if (best >= stop_at) return best; }
    while (cand) {
        if (size + __builtin_popcount(cand) <= best) return best;
        int v = __builtin_ctz(cand);
        cand &= cand - 1;
        u32 cand2 = cand;
        for (int t = 0; t < evn[v]; t++) {
            u32 om = ev[v][t], inter = om & chosen;
            if (inter) cand2 &= ~(om ^ inter);
        }
        best = ind_search(cand2, chosen | (1u << v), size + 1, best, stop_at);
        if (best >= stop_at) return best;
    }
    return best;
}


/* refined bound: value(S) = |S| - #{r in S cap Rf : some feasible triple {i,r,k} lies inside S}.
 * pm[r][t] = {i,k} mask of the t-th currently feasible edge with midpoint r (r in Rf). */
static u32 pm[MAXN][MAXN * MAXN / 2];
static int pmn[MAXN];
static u32 g_rf;
static int refine = 1;

static int is_killed(int r, u32 chosen) {
    for (int t = 0; t < pmn[r]; t++) if ((pm[r][t] & ~chosen) == 0) return 1;
    return 0;
}

static int ind_search2(u32 cand, u32 chosen, int size, u32 killed, int best, int stop_at) {
    int val = size - __builtin_popcount(killed);
    if (val > best) { best = val; if (best >= stop_at) return best; }
    while (cand) {
        if (val + __builtin_popcount(cand) <= best) return best;
        int v = __builtin_ctz(cand);
        cand &= cand - 1;
        u32 cand2 = cand;
        for (int t = 0; t < evn[v]; t++) {
            u32 om = ev[v][t], inter = om & chosen;
            if (inter) cand2 &= ~(om ^ inter);
        }
        u32 ch2 = chosen | (1u << v), k2 = killed;
        u32 todo = ch2 & g_rf & ~killed;
        while (todo) { int r = __builtin_ctz(todo); todo &= todo - 1; if (is_killed(r, ch2)) k2 |= 1u << r; }
        best = ind_search2(cand2, ch2, size + 1, k2, best, stop_at);
        if (best >= stop_at) return best;
    }
    return best;
}

static void push_edge(int i, int j, int k) {
    E_i[ne] = i; E_j[ne] = j; E_k[ne] = k;
    E_mask[ne] = (1u << i) | (1u << j) | (1u << k);
    ne++;
    ev[i][evn[i]++] = (1u << j) | (1u << k);
    ev[j][evn[j]++] = (1u << i) | (1u << k);
    ev[k][evn[k]++] = (1u << i) | (1u << j);
}
static void pop_edge(void) {
    ne--;
    evn[E_i[ne]]--; evn[E_j[ne]]--; evn[E_k[ne]]--;
}

static int has_edge_mask(u32 m) { for (int t = 0; t < ne; t++) if (E_mask[t] == m) return 1; return 0; }

static int has_f7(void) {
    if (ne < 5) return 0;
    for (int c = 0; c < n; c++) {
        if (evn[c] < 3) continue;
        for (int a = 0; a < evn[c]; a++) for (int b = a + 1; b < evn[c]; b++) {
            if (ev[c][a] & ev[c][b]) continue;
            for (int d = b + 1; d < evn[c]; d++) {
                if ((ev[c][a] | ev[c][b]) & ev[c][d]) continue;
                int p[3][2];
                u32 ms[3] = { ev[c][a], ev[c][b], ev[c][d] };
                for (int t = 0; t < 3; t++) { p[t][0] = __builtin_ctz(ms[t]); p[t][1] = 31 - __builtin_clz(ms[t]); }
                for (int s2 = 0; s2 < 2; s2++) for (int s3 = 0; s3 < 2; s3++) {
                    u32 P = (1u << p[0][0]) | (1u << p[1][s2]) | (1u << p[2][s3]);
                    u32 Q = (1u << p[0][1]) | (1u << p[1][1 - s2]) | (1u << p[2][1 - s3]);
                    if (has_edge_mask(P) && has_edge_mask(Q)) return 1;
                }
            }
        }
    }
    return 0;
}

static int cmp_edge(const void *a, const void *b) {
    const int *x = a, *y = b;
    for (int t = 0; t < 3; t++) if (x[t] != y[t]) return x[t] - y[t];
    return 0;
}

static int refl_ok(int (*es)[3], int m) { /* es sorted lex; keep iff es <= reflection(es) */
    int rs[MAXN][3];
    for (int t = 0; t < m; t++) { rs[t][0] = n - 1 - es[t][2]; rs[t][1] = n - 1 - es[t][1]; rs[t][2] = n - 1 - es[t][0]; }
    qsort(rs, m, sizeof(rs[0]), cmp_edge);
    for (int t = 0; t < m; t++) { int c = cmp_edge(es[t], rs[t]); if (c < 0) return 1; if (c > 0) return 0; }
    return 1;
}

static void report_leaf(void) {
    int es[MAXN][3];
    for (int t = 0; t < ne; t++) { es[t][0] = E_i[t]; es[t][1] = E_j[t]; es[t][2] = E_k[t]; }
    qsort(es, ne, sizeof(es[0]), cmp_edge);
    if (refl && !refl_ok(es, ne)) return;
    int a = ind_search((n >= 32 ? 0xFFFFFFFFu : ((1u << n) - 1)), 0, 0, 0, n + 1);
    if (a > T) return;
    solutions++;
    if (mode_enum || mode_min) {
        printf("SOL %d", a);
        for (int t = 0; t < ne; t++) printf(" %d,%d,%d", es[t][0], es[t][1], es[t][2]);
        printf("\n"); fflush(stdout);
    }
    if (mode_min) T = a - 1;
    if (limit && solutions >= limit) stopped = 1;
}

static u32 range_above(int lo) { /* bits > lo, within n bits */
    u32 full = (n >= 32) ? 0xFFFFFFFFu : ((1u << n) - 1);
    if (lo + 1 >= 32) return 0;
    return full & ~((1u << (lo + 1)) - 1);
}

typedef struct { u32 nb[MAXN]; int M[MAXN]; } State;

static int feasible_mid(int r, const State *s) {
    for (int i = 0; i < r; i++) {
        if ((s->nb[r] >> i) & 1) continue;
        int lo = mono ? (s->M[i] > r ? s->M[i] : r) : r;
        if (range_above(lo) & ~(s->nb[i] | s->nb[r])) return 1;
    }
    return 0;
}

/* entry checks of a node at level j (midpoint j undecided). Returns 1 if the node survives. */
static int entry_ok(int j, const State *s, int nones, int *is_leaf) {
    int need = m_need();
    int budget = (n - 2) - (m_exact >= 0 ? m_exact : need);
    u32 rf = 0; int forced = 0;
    for (int r = j; r <= n - 2; r++) { if (feasible_mid(r, s)) rf |= 1u << r; else forced++; }
    if (nones + forced > budget) return 0;
    u32 full = (n >= 32) ? 0xFFFFFFFFu : ((1u << n) - 1);
    if (refine && rf) {
        g_rf = rf;
        for (int r = j; r <= n - 2; r++) {
            pmn[r] = 0;
            if (!((rf >> r) & 1)) continue;
            for (int i = 0; i < r; i++) {
                if ((s->nb[r] >> i) & 1) continue;
                int lo = mono ? (s->M[i] > r ? s->M[i] : r) : r;
                u32 ak = range_above(lo) & ~(s->nb[i] | s->nb[r]);
                while (ak) { int k = __builtin_ctz(ak); ak &= ak - 1; pm[r][pmn[r]++] = (1u << i) | (1u << k); }
            }
        }
        if (ind_search2(full, 0, 0, 0, 0, T + 1) > T) return 0;
    } else if (ind_search(full & ~rf, 0, 0, 0, T + 1) > T) return 0;
    *is_leaf = (j == n - 1);
    return 1;
}

static void check_time(void) {
    if (tl > 0 && (nodes & 4095) == 0 && now() - t0 > tl) { stopped = 1; timed_out = 1; }
}

static long long lvl1_done = 0;

static void rec(int j, const State *s, int nones) {
    if (stopped) return;
    nodes++;
    check_time();
    if (stopped) return;
    int leaf;
    if (!entry_ok(j, s, nones, &leaf)) return;
    if (leaf) {
        leaves++;
        if (ne >= m_need() && (m_exact < 0 || ne == m_exact)) report_leaf();
        return;
    }
    if (mode_pref && j == pdepth + 1) {
        printf("PRE");
        for (int l = 1; l <= pdepth; l++) { if (cur_k[l] < 0) printf("%sx", l > 1 ? "," : " "); else printf("%s%d-%d", l > 1 ? "," : " ", cur_i[l], cur_k[l]); }
        printf("\n");
        return;
    }
    int budget = (n - 2) - (m_exact >= 0 ? m_exact : m_need());
    for (int i = 0; i < j; i++) {
        if ((s->nb[j] >> i) & 1) continue;
        if (j <= plen && i != pre_i[j]) continue;
        int lo = mono ? (s->M[i] > j ? s->M[i] : j) : j;
        u32 ak = range_above(lo) & ~(s->nb[i] | s->nb[j]);
        while (ak) {
            int k = __builtin_ctz(ak); ak &= ak - 1;
            if (j <= plen && k != pre_k[j]) continue;
            cur_i[j] = i; cur_k[j] = k;
            push_edge(i, j, k);
            if (evn[i] > maxdeg || evn[j] > maxdeg || evn[k] > maxdeg) { pop_edge(); continue; }
            if (f7 && has_f7()) { pop_edge(); continue; }
            State s2 = *s;
            s2.nb[i] |= (1u << j) | (1u << k);
            s2.nb[j] |= (1u << i) | (1u << k);
            s2.nb[k] |= (1u << i) | (1u << j);
            if (mono) for (int i2 = 0; i2 <= i; i2++) if (s2.M[i2] < k) s2.M[i2] = k;
            rec(j + 1, &s2, nones);
            pop_edge();
            if (stopped) return;
        }
        if (progress && j == 2 && i + 1 == 2) { /* nothing */ }
    }
    if (nones + 1 <= budget && !(j <= plen && pre_k[j] != -1)) { cur_k[j] = -1; rec(j + 1, s, nones + 1); }
    if (progress && j <= 2) {
        printf("PROG level=%d midpoint=%d done t=%.1f nodes=%lld sols=%lld\n", j, j, now() - t0, nodes, solutions);
        fflush(stdout);
    }
}

/* ---------------- Knuth estimator ---------------- */
static double lvl_surv[MAXN+2];
static uint64_t rng_s = 88172645463325252ULL;
static uint64_t rnd(void) { rng_s ^= rng_s << 13; rng_s ^= rng_s >> 7; rng_s ^= rng_s << 17; return rng_s; }

typedef struct { int i, k; /* k = -1: none */ } Child;

static void estimate(int probes) {
    /* estimates (a) number of calls of rec (nodes), (b) number of surviving nodes, over random descents */
    double sum_calls = 0, sum_calls2 = 0, sum_surv = 0;
    for (int p = 0; p < probes; p++) {
        State s; memset(&s, 0, sizeof s);
        int nones = 0, j = 1; double w = 1, calls = 1, surv = 0;
        ne = 0; memset(evn, 0, sizeof evn);
        int leaf;
        if (!entry_ok(1, &s, 0, &leaf)) { sum_calls += 1; sum_calls2 += 1; continue; }
        surv = 1;
        int depth_edges = 0;
        while (1) {
            if (j == n - 1) break;
            int budget = (n - 2) - (m_exact >= 0 ? m_exact : m_need());
            Child ch[MAXN * MAXN]; int nc = 0, gen = 0;
            State cs[1]; (void)cs;
            /* enumerate children, test entry for each */
            static State st_arr[MAXN * MAXN];
            static int none_arr[MAXN * MAXN];
            for (int i = 0; i < j; i++) {
                if ((s.nb[j] >> i) & 1) continue;
                int lo = mono ? (s.M[i] > j ? s.M[i] : j) : j;
                u32 ak = range_above(lo) & ~(s.nb[i] | s.nb[j]);
                while (ak) {
                    int k = __builtin_ctz(ak); ak &= ak - 1;
                    push_edge(i, j, k);
                    int bad = (evn[i] > maxdeg || evn[j] > maxdeg || evn[k] > maxdeg) || (f7 && has_f7());
                    gen++;
                    if (!bad) {
                        State s2 = s;
                        s2.nb[i] |= (1u << j) | (1u << k);
                        s2.nb[j] |= (1u << i) | (1u << k);
                        s2.nb[k] |= (1u << i) | (1u << j);
                        if (mono) for (int i2 = 0; i2 <= i; i2++) if (s2.M[i2] < k) s2.M[i2] = k;
                        int lf;
                        if (entry_ok(j + 1, &s2, nones, &lf)) { ch[nc].i = i; ch[nc].k = k; st_arr[nc] = s2; none_arr[nc] = nones; nc++; }
                    }
                    pop_edge();
                }
            }
            if (nones + 1 <= budget) {
                gen++;
                int lf;
                if (entry_ok(j + 1, &s, nones + 1, &lf)) { ch[nc].i = -1; ch[nc].k = -1; st_arr[nc] = s; none_arr[nc] = nones + 1; nc++; }
            }
            calls += w * gen;
            if (nc == 0) break;
            int pick = (int)(rnd() % (uint64_t)nc);
            w *= nc; surv += w; lvl_surv[j+1] += w;
            if (ch[pick].k >= 0) { push_edge(ch[pick].i, j, ch[pick].k); depth_edges++; }
            s = st_arr[pick]; nones = none_arr[pick];
            j++;
        }
        while (ne > 0) pop_edge();
        sum_calls += calls; sum_calls2 += calls * calls; sum_surv += surv;
    }
    double mean = sum_calls / probes, var = sum_calls2 / probes - mean * mean;
    printf("EST_LEVELS"); for (int l = 1; l < n; l++) printf(" %d:%.3g", l, lvl_surv[l] / probes); printf("\n");
    printf("EST probes=%d est_calls=%.4g stderr=%.3g est_surviving=%.4g\n", probes, mean, sqrt(var / probes), sum_surv / probes);
}

int main(int argc, char **argv) {
    int probes = 2000; long seed = 1; char mode[32] = "enum";
    n = 0; T = -1; m_min = 0;
    for (int a = 1; a < argc; a++) {
        char *eq = strchr(argv[a], '=');
        if (!eq) { fprintf(stderr, "bad arg %s\n", argv[a]); return 2; }
        *eq = 0; const char *key = argv[a], *val = eq + 1;
        if (!strcmp(key, "n")) n = atoi(val);
        else if (!strcmp(key, "T")) T = atoi(val);
        else if (!strcmp(key, "m_min")) m_min = atoi(val);
        else if (!strcmp(key, "m_exact")) m_exact = atoi(val);
        else if (!strcmp(key, "f7")) f7 = atoi(val);
        else if (!strcmp(key, "hy")) hy = atoi(val);
        else if (!strcmp(key, "refl")) refl = atoi(val);
        else if (!strcmp(key, "mono")) mono = atoi(val);
        else if (!strcmp(key, "limit")) limit = atoi(val);
        else if (!strcmp(key, "progress")) progress = atoi(val);
        else if (!strcmp(key, "refine")) refine = atoi(val);
        else if (!strcmp(key, "maxdeg")) maxdeg = atoi(val);
        else if (!strcmp(key, "probes")) probes = atoi(val);
        else if (!strcmp(key, "seed")) seed = atol(val);
        else if (!strcmp(key, "tl")) tl = atof(val);
        else if (!strcmp(key, "depth")) pdepth = atoi(val);
        else if (!strcmp(key, "pre")) {
            char buf[512]; snprintf(buf, sizeof buf, "%s", val);
            for (char *tok = strtok(buf, ","); tok; tok = strtok(NULL, ",")) {
                plen++;
                if (!strcmp(tok, "x")) { pre_i[plen] = -1; pre_k[plen] = -1; }
                else if (sscanf(tok, "%d-%d", &pre_i[plen], &pre_k[plen]) != 2) { fprintf(stderr, "bad pre\n"); return 2; }
            }
        }
        else if (!strcmp(key, "mode")) snprintf(mode, sizeof mode, "%s", val);
        else { fprintf(stderr, "unknown key %s\n", key); return 2; }
    }
    if (n < 3 || n > MAXN) { fprintf(stderr, "n must be in 3..32\n"); return 2; }
    if (T < 0) T = n;
    mode_enum = !strcmp(mode, "enum"); mode_min = !strcmp(mode, "min");
    mode_count = !strcmp(mode, "count"); mode_est = !strcmp(mode, "estimate");
    mode_pref = !strcmp(mode, "prefixes");
    if (m_exact >= 0) m_min = m_exact;
    rng_s ^= (uint64_t)seed * 0x9E3779B97F4A7C15ULL; for (int t = 0; t < 10; t++) rnd();
    t0 = now();
    if (mode_est) { estimate(probes); printf("DONE nodes=0 leaves=0 solutions=0 timed_out=0 time=%.2f\n", now() - t0); return 0; }
    State s; memset(&s, 0, sizeof s);
    rec(1, &s, 0);
    printf("DONE nodes=%lld leaves=%lld solutions=%lld timed_out=%d time=%.2f\n", nodes, leaves, solutions, timed_out, now() - t0);
    return 0;
}
