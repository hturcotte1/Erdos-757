#include "i11core.h"
#include "ptev.h"
#define HSZ 200
#define HOFF 60
static inline u64 mix(u64 x) { x ^= x >> 31; x *= 0x9E3779B97F4A7C15ULL; x ^= x >> 29; x *= 0xBF58476D1CE4E5B9ULL; x ^= x >> 32; return x; }
static unsigned long long fp_graph(const G *g) {
    u64 vc[MAXN], ec[MAXM], nv_[MAXN];
    for (int v = 0; v < g->n; v++) vc[v] = mix(1 + degree_of(g, v));
    for (int r = 0; r < 5; r++) {
        for (int i = 0; i < g->m; i++) { u64 s = 0; for (u64 q = g->e[i]; q; q &= q - 1) s += mix(vc[__builtin_ctzll(q)]); ec[i] = mix(s); }
        for (int v = 0; v < g->n; v++) { u64 s = 0; for (int i = 0; i < g->m; i++) if ((g->e[i] >> v) & 1) s += mix(ec[i] + 77); nv_[v] = mix(vc[v] * 3 + s); }
        memcpy(vc, nv_, sizeof(u64) * g->n);
    }
    u64 h = 0; for (int v = 0; v < g->n; v++) h += mix(vc[v]); for (int i = 0; i < g->m; i++) h += mix(ec[i] ^ 0x5555); return h ^ ((u64)g->n << 56) ^ ((u64)g->m << 48);
}
#define SEEN_SZ (1 << 24)
static unsigned long long *seen_tab;
static int seen_insert(unsigned long long h) { if (!h) h = 1; unsigned i = (unsigned)(h >> 12) & (SEEN_SZ - 1); for (int k = 0; k < 64; k++) { unsigned j = (i + k) & (SEEN_SZ - 1); if (seen_tab[j] == h) return 0; if (!seen_tab[j]) { seen_tab[j] = h; return 1; } } return 1; }
static int SMAX, D, K; static long nvis = 0;
static long hist[HSZ][12]; static int maxU2[HSZ]; static int minslack_cfg = 999; static long hitcount = 0; static int minGoodAt[HSZ];
static void print_edges(FILE *f, const G *g) { for (int i = 0; i < g->m; i++) { fprintf(f, " "); int k = 0; for (u64 r = g->e[i]; r; r &= r - 1) fprintf(f, k++ ? ",%d" : "%d", __builtin_ctzll(r)); } }
static void visit(const G *g, int depth, int tau) {
    int sl = slack_of(g, tau);
    if (sl < 0) { printf("VIOLATOR n %d m %d tau %d slack %d edges", g->n, g->m, tau, sl); print_edges(stdout, g); printf("\n"); fflush(stdout); }
    if (sl <= SMAX) {
        Ev ev; evaluate(g, &ev, 1); nvis++;
        int i = sl + HOFF; if (i >= 0 && i < HSZ) { hist[i][ev.nU2 < 11 ? ev.nU2 : 11]++; if (ev.nU2 > maxU2[i]) maxU2[i] = ev.nU2;
            if (ev.ncand > 0 && ev.minGood < minGoodAt[i]) minGoodAt[i] = ev.minGood; }
        if (ev.ncand > 0) { if (ev.minGood == 0) { hitcount++; if (sl < minslack_cfg) minslack_cfg = sl; printf("HIT n %d m %d tau %d slack %d nU2 %d edges", g->n, g->m, tau, sl, ev.nU2); print_edges(stdout, g); printf("\n"); fflush(stdout); } }
        if (ev.nU2 >= 6) { printf("U2>=6 n %d m %d tau %d slack %d nU2 %d ncand %d minGood %d edges", g->n, g->m, tau, sl, ev.nU2, ev.ncand, ev.minGood); print_edges(stdout, g); printf("\n"); fflush(stdout); }
    }
    if (depth >= D) return;
    /* children: random sampling of K valid edge additions */
    int vs[MAXN], nv = 0; for (int v = 0; v < g->n; v++) if (degree_of(g, v) < 3) vs[nv++] = v;
    if (nv < 3) return;
    int got = 0;
    for (int att = 0; att < 40 * K && got < K; att++) {
        int a = vs[rndint(nv)], b = vs[rndint(nv)], c = vs[rndint(nv)]; if (a == b || b == c || a == c) continue;
        G h = *g; DMAX = 3; if (!try_add(&h, vmask(a, b, c))) continue;
        int t2 = tau_of(&h, 2, 0, NULL); int s2 = slack_of(&h, t2);
        if (s2 > SMAX) continue;
        if (!seen_insert(fp_graph(&h))) continue;
        got++; visit(&h, depth + 1, t2);
    }
}
