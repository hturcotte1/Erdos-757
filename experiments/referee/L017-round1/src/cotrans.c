/* Referee L017 round 1 (independent code): for each 3-graph read from stdin, compute tau exactly by a
   decision branch-and-bound, and decide co-transversality of every vertex and every pair through
   Fact 0.4: X is co-transversal iff tau(F - X) = tau(F) - |X|.  (Different method from the prover's,
   which enumerates all minimum transversals.)
   Input lines:  n m a1 b1 c1 a2 b2 c2 ...   (vertices 0..n-1, n <= 62, m <= 64)
   Output line:  tau=<t> ncv=<k> v1 v2 ... npairs=<p> x1 y1 x2 y2 ...   (non-co-transversal vertices / pairs) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64;
static int n, m;
static u64 emask[64];         /* vertex mask of edge i */
static u64 vedges[64];        /* edge mask of edges at vertex v */
static long long nodes;
/* is there a set of at most k vertices, not using vertices in 'forb', hitting all edges in 'unc'? */
static int lb_pack(u64 unc) {
    int c = 0; u64 used = 0;
    while (unc) {
        int i = __builtin_ctzll(unc); unc &= unc - 1;
        if (!(emask[i] & used)) { used |= emask[i]; c++; }
    }
    return c;
}
static int hit(u64 unc, int k, u64 forb) {
    nodes++;
    if (!unc) return 1;
    if (k == 0) return 0;
    if (lb_pack(unc) > k) return 0;
    /* choose an uncovered edge with the fewest allowed vertices */
    int best = -1, bestc = 4;
    u64 t = unc;
    while (t) {
        int i = __builtin_ctzll(t); t &= t - 1;
        int c = __builtin_popcountll(emask[i] & ~forb);
        if (c < bestc) { bestc = c; best = i; if (c <= 1) break; }
    }
    if (bestc == 0) return 0;
    u64 cand = emask[best] & ~forb;
    u64 f2 = forb;
    while (cand) {
        int v = __builtin_ctzll(cand); cand &= cand - 1;
        if (hit(unc & ~vedges[v], k - 1, f2)) return 1;
        f2 |= (1ULL << v);   /* later branches exclude v (complete: some solution uses v or avoids it) */
    }
    return 0;
}
static int tau_of(u64 unc) {
    int k = 0;
    while (!hit(unc, k, 0)) k++;
    return k;
}
int main(void) {
    char line[1 << 16];
    while (fgets(line, sizeof line, stdin)) {
        char *p = line; int off;
        if (sscanf(p, "%d %d%n", &n, &m, &off) != 2) continue;
        p += off;
        memset(vedges, 0, sizeof vedges);
        for (int i = 0; i < m; i++) {
            int a, b, c;
            if (sscanf(p, "%d %d %d%n", &a, &b, &c, &off) != 3) { fprintf(stderr, "parse error\n"); return 1; }
            p += off;
            emask[i] = (1ULL << a) | (1ULL << b) | (1ULL << c);
            vedges[a] |= 1ULL << i; vedges[b] |= 1ULL << i; vedges[c] |= 1ULL << i;
        }
        u64 all = (m == 64) ? ~0ULL : ((1ULL << m) - 1);
        int t = tau_of(all);
        /* sanity: no transversal of size t-1 */
        if (t > 0 && hit(all, t - 1, 0)) { fprintf(stderr, "tau error\n"); return 1; }
        printf("tau=%d", t);
        int ncv = 0; int cv[64];
        for (int v = 0; v < n; v++) {
            u64 unc = all & ~vedges[v];
            /* co-transversal iff tau(F - v) <= t - 1 (always >= t-1 by Fact 0.3) */
            int co = (t >= 1) && hit(unc, t - 1, 0);
            if (!co) cv[ncv++] = v;
        }
        printf(" ncv=%d", ncv);
        for (int i = 0; i < ncv; i++) printf(" %d", cv[i]);
        int np = 0; static int px[4096], py[4096];
        for (int x = 0; x < n; x++) for (int y = x + 1; y < n; y++) {
            u64 unc = all & ~vedges[x] & ~vedges[y];
            int co = (t >= 2) && hit(unc, t - 2, 0);
            if (!co) { px[np] = x; py[np] = y; np++; }
        }
        printf(" npairs=%d", np);
        for (int i = 0; i < np; i++) printf(" %d %d", px[i], py[i]);
        printf("\n");
        fflush(stdout);
    }
    fprintf(stderr, "nodes=%lld\n", nodes);
    return 0;
}
