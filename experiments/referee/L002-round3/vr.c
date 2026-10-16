/* Referee round 3 (L002): exact realizer + set verifier, written from scratch (no e757/, judge/, earlier referees).
 *
 *   ./vr set  < lines "n x_1 ... x_n"           verify sets
 *   ./vr pat N < lines "i,j,k i,j,k ..."        realize saturated ordered patterns on N vertices, then verify
 *
 * Realization: unknowns x_1..x_{N-2}, x_0 = 0, x_{N-1} = 1; one equation x_i - 2x_j + x_k = 0 per triple.
 * Solved by Gaussian elimination over exact rationals (int64 num/den, __int128 intermediates, overflow abort);
 * the solution is then checked exactly against every equation.  Failure reasons, in this order:
 *   singular | order (not strictly increasing) | extra_ap (3-AP set != pattern) | not45 | realizable
 * Set verification (both modes): distinct; (4,5) by all 4-subsets (>=5 distinct |differences|);
 *   3-APs by rank; h by exhaustive DFS over Sidon subsets (definition: all positive differences distinct);
 *   independently alpha(3-AP hypergraph) by a scan of all 2^n subsets; asserts h == alpha when the set is (4,5).
 * Output per set: "OK|BAD reason h m pattern ; normalized-set" (normal form: translate to 0, divide by gcd,
 *   lexicographic min with the reflection). Summary on stderr. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef long long ll;
typedef __int128 i128;
#define MAXN 24

static ll gcdll(ll a, ll b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { ll t = a % b; a = b; b = t; } return a; }
static void die(const char *m) { fprintf(stderr, "FATAL %s\n", m); exit(3); }
static ll fit(i128 v) { if (v > (i128)4000000000000000000LL || v < -(i128)4000000000000000000LL) die("overflow"); return (ll)v; }

typedef struct { ll p, q; } Q; /* q > 0, reduced */
static Q mkq(i128 p, i128 q) {
    if (q == 0) die("zero den");
    if (q < 0) { p = -p; q = -q; }
    i128 a = p < 0 ? -p : p, b = q;
    while (b) { i128 t = a % b; a = b; b = t; }
    if (a == 0) a = 1;
    Q r; r.p = fit(p / a); r.q = fit(q / a); return r;
}
static Q qsub(Q a, Q b) { return mkq((i128)a.p * b.q - (i128)b.p * a.q, (i128)a.q * b.q); }
static Q qmul(Q a, Q b) { return mkq((i128)a.p * b.p, (i128)a.q * b.q); }
static Q qdiv(Q a, Q b) { if (b.p == 0) die("div0"); return mkq((i128)a.p * b.q, (i128)a.q * b.p); }

static int n;
static ll X[MAXN];
static ll best_h;
/* differences are compressed to ids: did[a][b] = rank of X[b]-X[a] among the distinct positive differences */
static int did[MAXN][MAXN]; static unsigned char used[MAXN * MAXN];
static int cmpll(const void *a, const void *b) { ll x = *(const ll *)a, y = *(const ll *)b; return x < y ? -1 : x > y; }
static void build_did(void) {
    ll D[MAXN * MAXN]; int k = 0;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) D[k++] = X[b] - X[a];
    qsort(D, k, sizeof(ll), cmpll);
    int u = 0; for (int t = 0; t < k; t++) if (t == 0 || D[t] != D[t - 1]) D[u++] = D[t];
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) {
        ll d = X[b] - X[a]; int lo = 0, hi = u - 1;
        while (lo < hi) { int mid = (lo + hi) / 2; if (D[mid] < d) lo = mid + 1; else hi = mid; }
        if (D[lo] != d) die("did");
        did[a][b] = lo;
    }
    memset(used, 0, sizeof used);
}

static void sidon_dfs(int idx, int *chosen, int cnt) {
    if (cnt > best_h) best_h = cnt;
    if (cnt + (n - idx) <= best_h) return;
    for (int v = idx; v < n; v++) {
        if (cnt + (n - v) <= best_h) return;
        /* try adding v: the new differences X[v]-X[c] must be unused (and are then marked) */
        int ok = 1, t;
        for (t = 0; t < cnt; t++) { int d = did[chosen[t]][v]; if (used[d]) { ok = 0; break; } used[d] = 1; }
        if (ok) { chosen[cnt] = v; sidon_dfs(v + 1, chosen, cnt + 1); }
        for (int u = 0; u < t; u++) used[did[chosen[u]][v]] = 0;
    }
}

/* returns 1 if (4,5), fills pattern */
static int npat; static int P[MAXN * MAXN][3];
static long long cnt_reason[8]; static long long hhist[MAXN + 1];

static int verify_set(int *h_out, int *alpha_out, int *is45_out) {
    for (int i = 0; i + 1 < n; i++) if (X[i] >= X[i + 1]) return -1; /* not strictly increasing */
    /* 3-APs by rank: (a,b,c) with X_a + X_c = 2 X_b */
    npat = 0;
    for (int a = 0; a < n; a++) for (int c = a + 2; c < n; c++) {
        ll s = X[a] + X[c]; if (s & 1) continue;
        for (int b = a + 1; b < c; b++) if (2 * X[b] == s) { P[npat][0] = a; P[npat][1] = b; P[npat][2] = c; npat++; }
    }
    /* (4,5) */
    int is45 = 1;
    for (int a = 0; a < n && is45; a++) for (int b = a + 1; b < n && is45; b++)
    for (int c = b + 1; c < n && is45; c++) for (int d = c + 1; d < n && is45; d++) {
        ll D[6] = { X[b] - X[a], X[c] - X[a], X[d] - X[a], X[c] - X[b], X[d] - X[b], X[d] - X[c] };
        int distinct = 0;
        for (int u = 0; u < 6; u++) { int seen = 0; for (int w = 0; w < u; w++) if (D[w] == D[u]) seen = 1; if (!seen) distinct++; }
        if (distinct < 5) is45 = 0;
    }
    *is45_out = is45;
    /* h by DFS from the Sidon definition */
    build_did();
    int chosen[MAXN]; best_h = 0; sidon_dfs(0, chosen, 0);
    *h_out = (int)best_h;
    /* alpha of the 3-AP hypergraph by scanning all subsets */
    int al = 0;
    if (n <= 22) {
        uint32_t em[MAXN * MAXN];
        for (int t = 0; t < npat; t++) em[t] = (1u << P[t][0]) | (1u << P[t][1]) | (1u << P[t][2]);
        for (uint32_t S = 0; S < (1u << n); S++) {
            int pc = __builtin_popcount(S); if (pc <= al) continue;
            int ok = 1; for (int t = 0; t < npat; t++) if ((S & em[t]) == em[t]) { ok = 0; break; }
            if (ok) al = pc;
        }
    } else al = -1;
    *alpha_out = al;
    return 1;
}

static void print_norm(FILE *f) {
    ll Y[MAXN], R[MAXN], g = 0;
    for (int i = 0; i < n; i++) { Y[i] = X[i] - X[0]; g = gcdll(g, Y[i]); }
    for (int i = 0; i < n; i++) Y[i] /= g;
    for (int i = 0; i < n; i++) R[i] = Y[n - 1] - Y[n - 1 - i];
    int useR = 0;
    for (int i = 0; i < n; i++) { if (R[i] < Y[i]) { useR = 1; break; } if (R[i] > Y[i]) break; }
    for (int i = 0; i < n; i++) fprintf(f, "%s%lld", i ? " " : "", useR ? R[i] : Y[i]);
}

static void report(const char *tag) {
    int h, al, is45;
    int r = verify_set(&h, &al, &is45);
    if (r < 0) { printf("BAD order\n"); cnt_reason[1]++; return; }
    if (al >= 0 && is45 && al != h) die("h != alpha on a (4,5)-set");
    printf("%s %s h=%d alpha=%d m=%d pat=", tag, is45 ? "is45" : "not45", h, al, npat);
    for (int t = 0; t < npat; t++) printf("%s%d,%d,%d", t ? " " : "", P[t][0], P[t][1], P[t][2]);
    printf(" ; ");
    print_norm(stdout);
    printf("\n");
    if (is45) hhist[h]++;
}

int main(int argc, char **argv) {
    if (argc < 2) die("usage");
    char line[8192];
    if (!strcmp(argv[1], "set")) {
        long long lines = 0;
        while (fgets(line, sizeof line, stdin)) {
            char *p = line; int nn; int off;
            if (sscanf(p, "%d%n", &nn, &off) != 1) continue;
            p += off; n = nn; if (n > MAXN) die("n too big");
            for (int i = 0; i < n; i++) { if (sscanf(p, "%lld%n", &X[i], &off) != 1) die("parse"); p += off; }
            /* sort */
            for (int i = 1; i < n; i++) { ll v = X[i]; int j = i - 1; while (j >= 0 && X[j] > v) { X[j + 1] = X[j]; j--; } X[j + 1] = v; }
            lines++;
            report("SET");
        }
        fprintf(stderr, "sets=%lld nonincreasing_or_dup=%lld h_hist(4,5 only):", lines, cnt_reason[1]);
        for (int h = 0; h <= MAXN; h++) if (hhist[h]) fprintf(stderr, " %d:%lld", h, hhist[h]);
        fprintf(stderr, "\n");
        return 0;
    }
    if (!strcmp(argv[1], "pat")) {
        int N = atoi(argv[2]); n = N;
        long long lines = 0, singular = 0, order = 0, extra = 0, not45 = 0, ok = 0, residfail = 0;
        while (fgets(line, sizeof line, stdin)) {
            int E[MAXN][3], m = 0; char *p = line; int a, b, c, off;
            while (sscanf(p, " %d,%d,%d%n", &a, &b, &c, &off) == 3) { E[m][0] = a; E[m][1] = b; E[m][2] = c; m++; p += off; }
            if (m == 0) continue;
            lines++;
            if (m != N - 2) die("pattern not saturated");
            /* unknown index u = vertex-1 for vertices 1..N-2 */
            int U = N - 2; Q A[MAXN][MAXN + 1];
            for (int r = 0; r < U; r++) for (int s = 0; s <= U; s++) A[r][s] = mkq(0, 1);
            for (int r = 0; r < m; r++) {
                int v[3] = { E[r][0], E[r][1], E[r][2] }; ll co[3] = { 1, -2, 1 };
                if (!(v[0] < v[1] && v[1] < v[2])) die("bad triple");
                for (int t = 0; t < 3; t++) {
                    if (v[t] == 0) continue;                      /* x_0 = 0 */
                    if (v[t] == N - 1) { A[r][U] = qsub(A[r][U], mkq(co[t], 1)); continue; } /* move x_{N-1}=1 to rhs */
                    A[r][v[t] - 1] = qsub(A[r][v[t] - 1], mkq(-co[t], 1)); /* A += co */
                }
            }
            int sing = 0;
            for (int col = 0; col < U; col++) {
                int piv = -1; for (int r = col; r < U; r++) if (A[r][col].p != 0) { piv = r; break; }
                if (piv < 0) { sing = 1; break; }
                if (piv != col) for (int s = 0; s <= U; s++) { Q t = A[piv][s]; A[piv][s] = A[col][s]; A[col][s] = t; }
                Q iv = A[col][col];
                for (int s = 0; s <= U; s++) A[col][s] = qdiv(A[col][s], iv);
                for (int r = 0; r < U; r++) if (r != col && A[r][col].p != 0) {
                    Q f = A[r][col];
                    for (int s = 0; s <= U; s++) A[r][s] = qsub(A[r][s], qmul(f, A[col][s]));
                }
            }
            if (sing) { singular++; printf("SINGULAR\n"); continue; }
            Q x[MAXN]; x[0] = mkq(0, 1); x[N - 1] = mkq(1, 1);
            for (int u = 0; u < U; u++) x[u + 1] = A[u][U];
            /* exact residual check */
            for (int r = 0; r < m; r++) {
                Q s = qsub(qsub(x[E[r][0]], qmul(mkq(2, 1), x[E[r][1]])), mkq(-x[E[r][2]].p, x[E[r][2]].q));
                if (s.p != 0) residfail++;
            }
            /* scale to integers */
            ll L = 1; for (int i = 0; i < N; i++) { ll g = gcdll(L, x[i].q); L = fit((i128)(L / g) * x[i].q); }
            for (int i = 0; i < N; i++) X[i] = fit((i128)x[i].p * (L / x[i].q));
            int incr = 1; for (int i = 0; i + 1 < N; i++) if (X[i] >= X[i + 1]) incr = 0;
            if (!incr) { order++; printf("ORDER\n"); continue; }
            int h, al, is45; verify_set(&h, &al, &is45);
            /* compare AP set with the pattern */
            int same = (npat == m);
            if (same) for (int r = 0; r < m && same; r++) {
                int f = 0; for (int t = 0; t < npat; t++) if (P[t][0] == E[r][0] && P[t][1] == E[r][1] && P[t][2] == E[r][2]) f = 1;
                if (!f) same = 0;
            }
            if (!same) { extra++; printf("EXTRA_AP\n"); continue; }
            if (!is45) { not45++; printf("NOT45\n"); continue; }
            if (al != h) die("h != alpha");
            ok++; hhist[h]++;
            printf("REAL h=%d ; ", h); print_norm(stdout); printf("\n");
        }
        fprintf(stderr, "patterns=%lld singular=%lld residfail=%lld order=%lld extra_ap=%lld not45=%lld realizable=%lld h_hist:",
                lines, singular, residfail, order, extra, not45, ok);
        for (int h = 0; h <= MAXN; h++) if (hhist[h]) fprintf(stderr, " %d:%lld", h, hhist[h]);
        fprintf(stderr, "\n");
        return 0;
    }
    die("mode");
    return 0;
}
