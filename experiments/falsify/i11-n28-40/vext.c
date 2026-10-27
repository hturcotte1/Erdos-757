/* vext.c: exact vertex-extension operator.  For each parent graph G (in C) enumerate every way to add ONE new vertex v with d<=3 edges
   {v,a_i,b_i} (disjoint pairs, deg<=3) such that tau(G+v) = tau(G)+1, i.e. the pairs {a_i,b_i} hit every maximum independent set of G
   (each max independent set contains some pair).  Children (checked to lie in C, exact tau by DP) are printed:  slack n m tau fp edges.
   usage: vext [maxchildren_per_parent] [extras_per_core] < parents ; env I11_SEED. */
#include "i11core.h"
static inline u64 mix(u64 x) { x ^= x >> 31; x *= 0x9E3779B97F4A7C15ULL; x ^= x >> 29; x *= 0xBF58476D1CE4E5B9ULL; x ^= x >> 32; return x; }
static u64 fp_graph(const G *g) {
    u64 vc[MAXN], ec[MAXM], nv_[MAXN];
    for (int v = 0; v < g->n; v++) vc[v] = mix(1 + degree_of(g, v));
    for (int r = 0; r < 5; r++) {
        for (int i = 0; i < g->m; i++) { u64 s = 0; for (u64 q = g->e[i]; q; q &= q - 1) s += mix(vc[__builtin_ctzll(q)]); ec[i] = mix(s); }
        for (int v = 0; v < g->n; v++) { u64 s = 0; for (int i = 0; i < g->m; i++) if ((g->e[i] >> v) & 1) s += mix(ec[i] + 77); nv_[v] = mix(vc[v] * 3 + s); }
        memcpy(vc, nv_, sizeof(u64) * g->n);
    }
    u64 h = 0; for (int v = 0; v < g->n; v++) h += mix(vc[v]); for (int i = 0; i < g->m; i++) h += mix(ec[i] ^ 0x5555); return h ^ ((u64)g->n << 56) ^ ((u64)g->m << 48);
}
#define SEEN_SZ (1 << 22)
static u64 seen_tab[SEEN_SZ];
static int seen_insert(u64 h) { if (!h) h = 1; unsigned i = (unsigned)(h >> 12) & (SEEN_SZ - 1); for (int k = 0; k < 128; k++) { unsigned j = (i + k) & (SEEN_SZ - 1); if (seen_tab[j] == h) return 0; if (!seen_tab[j]) { seen_tab[j] = h; return 1; } } return 0; }

#define CAPS 60000
static u64 sets[CAPS]; static int nsets;
static G R; /* relabelled parent */
static int DM = 3; static int A, sufA[MAXN + 1]; static u64 endO[MAXN][MAXDEG]; static int nend[MAXN];
static void rec(int i, u64 cur, int sz) {
    if (nsets >= CAPS) return;
    if (sz + sufA[i] < A) return;
    if (i == R.n) { if (sz == A) sets[nsets++] = cur; return; }
    int ok = 1; for (int k = 0; k < nend[i]; k++) if ((cur & endO[i][k]) == endO[i][k]) { ok = 0; break; }
    if (ok) rec(i + 1, cur | (1ULL << i), sz + 1);
    rec(i + 1, cur, sz);
}
static u64 *cov; static int W; static int pairs_ok[MAXN][MAXN];
static int cores[200000][3], ncore[200000], ncores = 0; /* pair indices a*64+b */
static void dfs(int depth, const u64 *U, u64 used, int *chosen, int dmax) {
    int idx = -1; for (int w = 0; w < W; w++) if (U[w]) { idx = w * 64 + __builtin_ctzll(U[w]); break; }
    if (idx < 0) return;
    u64 S = sets[idx]; int vs[MAXN], k = 0; for (u64 r = S; r; r &= r - 1) vs[k++] = __builtin_ctzll(r);
    u64 U2[(CAPS + 63) / 64];
    for (int x = 0; x < k; x++) { int a = vs[x]; if ((used >> a) & 1) continue; for (int y = x + 1; y < k; y++) { int b = vs[y]; if ((used >> b) & 1) continue; if (!pairs_ok[a][b]) continue;
        const u64 *c = cov + (size_t)(a * R.n + b) * W; int empty = 1;
        for (int w = 0; w < W; w++) { U2[w] = U[w] & ~c[w]; if (U2[w]) empty = 0; }
        chosen[depth] = a * 64 + b;
        if (empty) { if (ncores < 200000) { ncore[ncores] = depth + 1; for (int t = 0; t <= depth; t++) cores[ncores][t] = chosen[t]; ncores++; } }
        else if (depth + 1 < dmax) dfs(depth + 1, U2, used | (1ULL << a) | (1ULL << b), chosen, dmax);
    } }
}
int main(int argc, char **argv) {
    int maxchild = argc > 1 ? atoi(argv[1]) : 1000; int extras = argc > 2 ? atoi(argv[2]) : 2;
    const char *dme = getenv("I11_DM"); if (dme) DM = atoi(dme); DMAX = DM;
    const char *sd = getenv("I11_SEED"); seed_rng(sd ? atoll(sd) : 1);
    static char line[1 << 16]; G P; long nparents = 0, nchild = 0, skipped = 0;
    while (fgets(line, sizeof line, stdin)) {
        if (!parse_graph(line, &P) || P.n >= MAXN - 1) continue;
        if (check_class(&P, DM) != 0) { skipped++; continue; }
        nparents++;
        /* relabel by DP order */
        int ord[MAXN], pos[MAXN]; make_order(&P, ord, 0); for (int i = 0; i < P.n; i++) pos[ord[i]] = i;
        R.n = P.n; R.m = P.m; for (int i = 0; i < P.m; i++) { u64 x = 0; for (u64 r = P.e[i]; r; r &= r - 1) x |= 1ULL << pos[__builtin_ctzll(r)]; R.e[i] = x; }
        int tauP = tau_of(&R, 2, 0, NULL); if (tauP < 0) { skipped++; continue; } A = R.n - tauP;
        for (int i = 0; i <= R.n; i++) { G Q; Q.n = R.n - i; Q.m = 0; for (int j = 0; j < R.m; j++) if (!(R.e[j] & ((1ULL << i) - 1))) Q.e[Q.m++] = R.e[j] >> i; sufA[i] = Q.n - (Q.n ? tau_of(&Q, 1, 0, NULL) : 0); }
        memset(nend, 0, sizeof nend);
        for (int j = 0; j < R.m; j++) { int mx = 63 - __builtin_clzll(R.e[j]); endO[mx][nend[mx]++] = R.e[j] & ~(1ULL << mx); }
        nsets = 0; rec(0, 0, 0);
        if (nsets >= CAPS) { skipped++; fprintf(stderr, "cap hit\n"); continue; }
        W = (nsets + 63) / 64; int n = R.n;
        cov = calloc((size_t)n * n * W, sizeof(u64));
        for (int s = 0; s < nsets; s++) { int vs[MAXN], k = 0; for (u64 r = sets[s]; r; r &= r - 1) vs[k++] = __builtin_ctzll(r); for (int x = 0; x < k; x++) for (int y = x + 1; y < k; y++) cov[(size_t)(vs[x] * n + vs[y]) * W + (s >> 6)] |= 1ULL << (s & 63); }
        for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) { pairs_ok[a][b] = (a < b) && degree_of(&R, a) < DM && degree_of(&R, b) < DM; if (pairs_ok[a][b]) for (int j = 0; j < R.m; j++) if (((R.e[j] >> a) & 1) && ((R.e[j] >> b) & 1)) pairs_ok[a][b] = 0; }
        u64 U[(CAPS + 63) / 64]; for (int w = 0; w < W; w++) U[w] = ~0ULL; if (nsets & 63) U[W - 1] = (1ULL << (nsets & 63)) - 1;
        int chosen[4]; ncores = 0; dfs(0, U, 0, chosen, 3);
        int emitted = 0;
        for (int c = 0; c < ncores && emitted < maxchild; c++) {
            for (int d = ncore[c]; d <= 3; d++) for (int rep = 0; rep < (d == ncore[c] ? 1 : extras); rep++) {
                G H = R; H.n = n + 1; u64 usedm = 0;
                for (int t = 0; t < ncore[c]; t++) { int a = cores[c][t] >> 6, b = cores[c][t] & 63; H.e[H.m++] = vmask(a, b, n); usedm |= (1ULL << a) | (1ULL << b); }
                int ok = 1;
                for (int t = ncore[c]; t < d && ok; t++) { int tries = 0; ok = 0; while (tries++ < 60) { int a = rndint(n), b = rndint(n); if (a == b) continue; if (a > b) { int x = a; a = b; b = x; } if (!pairs_ok[a][b] || ((usedm >> a) & 1) || ((usedm >> b) & 1)) continue; H.e[H.m++] = vmask(a, b, n); usedm |= (1ULL << a) | (1ULL << b); ok = 1; break; } }
                if (!ok) continue;
                if (check_class(&H, DM) != 0) continue;
                if (!seen_insert(fp_graph(&H))) continue;
                int tau = tau_of(&H, 2, 0, NULL); if (tau < 0) continue;
                printf("%d %d %d %d %llx ", slack_of(&H, tau), H.n, H.m, tau, (unsigned long long)fp_graph(&H)); print_graph(stdout, &H); emitted++; nchild++;
            }
        }
        free(cov);
    }
    fprintf(stderr, "vext: parents=%ld skipped=%ld children=%ld\n", nparents, skipped, nchild);
    return 0;
}
