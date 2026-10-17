/* myext.c -- referee L010 round 3 (written from scratch).  Vertex-extension step.
   Usage: myext NG TG MAXDEG [verify_every] < input
   Input lines: "m a1 b1 c1 ... am bm cm" or "TAG: (a,b,c) ..." : a 3-graph G on vertex labels 0..NG-1 (isolated vertices allowed).
   For each G: (1) computes tau(G) by exact branching and requires tau(G) == TG (else counted as bad_tau and skipped);
   (2) lists all minimum transversals (size TG) by scanning the TG-subsets; (3) for every unordered triple of pairwise disjoint pairs
   {a,b} of V(G) with no pair inside an edge of G and all endpoints of G-degree <= MAXDEG-1, H = G + {NG,a,b} x 3 is a HIT iff no
   minimum transversal of G meets all three pairs (then tau(H) = TG+1; otherwise tau(H) = TG).  Every HIT is re-verified by an exact
   branching computation of tau(H) directly on H (abort on mismatch), and every verify_every-th non-hit is verified to have tau(H) <= TG.
   Output: "HIT: (edges of G) (a1,b1,NG) (a2,b2,NG) (a3,b3,NG)" lines and one SUMMARY line. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define MAXT 200000
static uint32_t E[64]; static int NE;
static int coverable(uint64_t left, int k) {   /* can edges in 'left' be met by <= k vertices? */
    if (!left) return 1;
    if (k <= 0) return 0;
    uint64_t l = left; uint32_t used = 0; int cnt = 0;
    while (l) { int i = __builtin_ctzll(l); l &= l - 1; if (!(E[i] & used)) { used |= E[i]; cnt++; } }
    if (cnt > k) return 0;
    int i = __builtin_ctzll(left); uint32_t e = E[i];
    while (e) { int v = __builtin_ctz(e); e &= e - 1; uint64_t l2 = left;
        for (int j = 0; j < NE; j++) if ((l2 >> j & 1) && (E[j] >> v & 1)) l2 &= ~(1ULL << j);
        if (coverable(l2, k - 1)) return 1; }
    return 0;
}
static uint64_t allmask(void) { return NE >= 64 ? ~0ULL : ((1ULL << NE) - 1); }
static int tau_exact(void) { int k = 0; while (!coverable(allmask(), k)) k++; return k; }
static uint64_t bs[300][(MAXT + 63) / 64];
static uint32_t tr[MAXT];
static void print_set(uint32_t s, int extra) { int f = 1; printf("("); for (int v = 0; v < 32; v++) if (s >> v & 1) { printf(f ? "%d" : ",%d", v); f = 0; } if (extra >= 0) printf(",%d", extra); printf(")"); }
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: myext NG TG MAXDEG [verify_every] < input\n"); return 1; }
    int NG = atoi(argv[1]), TG = atoi(argv[2]), MD = atoi(argv[3]); long VE = argc > 4 ? atol(argv[4]) : 100000;
    static char line[1 << 16];
    unsigned long long graphs = 0, bad_tau = 0, tested = 0, hits = 0, verified_hits = 0, verified_nonhits = 0, maxnt = 0;
    while (fgets(line, sizeof line, stdin)) {
        int ed[64][3], m = 0;
        if (strchr(line, '(')) { char *p = line; while ((p = strchr(p, '('))) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) == 3) { ed[m][0] = a; ed[m][1] = b; ed[m][2] = c; m++; } p++; } }
        else { int k; char *p = line; if (sscanf(p, "%d%n", &m, &k) != 1) continue; p += k; for (int i = 0; i < m; i++) { if (sscanf(p, "%d %d %d%n", &ed[i][0], &ed[i][1], &ed[i][2], &k) != 3) { m = -1; break; } p += k; } if (m < 0) continue; }
        if (m == 0 && !strchr(line, '(')) continue;
        graphs++;
        uint32_t g[64]; int deg[32] = {0}; uint32_t nb[32] = {0};
        for (int i = 0; i < m; i++) { int a = ed[i][0], b = ed[i][1], c = ed[i][2];
            if (a < 0 || b < 0 || c < 0 || a >= NG || b >= NG || c >= NG || a == b || a == c || b == c) { fprintf(stderr, "bad edge\n"); return 2; }
            g[i] = (1u << a) | (1u << b) | (1u << c); deg[a]++; deg[b]++; deg[c]++;
            nb[a] |= g[i]; nb[b] |= g[i]; nb[c] |= g[i]; }
        NE = m; memcpy(E, g, sizeof(uint32_t) * m);
        if (tau_exact() != TG) { bad_tau++; continue; }
        /* all TG-subsets of [NG] that meet every edge */
        int nt = 0;
        if (TG > 0) { uint32_t S = (1u << TG) - 1;
            while (S < (1u << NG)) { int ok = 1; for (int i = 0; i < m; i++) if (!(g[i] & S)) { ok = 0; break; }
                if (ok) { if (nt >= MAXT) { fprintf(stderr, "MAXT\n"); return 3; } tr[nt++] = S; }
                uint32_t c = S & -S, r = S + c; S = (((r ^ S) >> 2) / c) | r; } }
        if (nt == 0) { fprintf(stderr, "no transversal of size TG although tau==TG?\n"); return 4; }
        if ((unsigned long long)nt > maxnt) maxnt = nt;
        int words = (nt + 63) / 64;
        uint32_t pr[300]; int np = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > MD - 1 || deg[b] > MD - 1) continue;
            if (nb[a] >> b & 1) continue;               /* pair inside an edge of G */
            uint32_t p = (1u << a) | (1u << b);
            memset(bs[np], 0, sizeof(uint64_t) * words);
            for (int j = 0; j < nt; j++) if (tr[j] & p) bs[np][j >> 6] |= 1ULL << (j & 63);
            pr[np++] = p;
        }
        uint64_t and2[(MAXT + 63) / 64];
        for (int x = 0; x < np; x++) for (int y = x + 1; y < np; y++) {
            if (pr[x] & pr[y]) continue;
            int any2 = 0; for (int w = 0; w < words; w++) { and2[w] = bs[x][w] & bs[y][w]; any2 |= (and2[w] != 0); }
            for (int z = y + 1; z < np; z++) {
                if ((pr[x] | pr[y]) & pr[z]) continue;
                tested++;
                int covered = 0;
                if (any2) for (int w = 0; w < words; w++) if (and2[w] & bs[z][w]) { covered = 1; break; }
                /* verification by direct tau on H */
                int do_verify = !covered || (VE > 0 && tested % VE == 0);
                if (do_verify) {
                    NE = m + 3; memcpy(E, g, sizeof(uint32_t) * m);
                    E[m] = pr[x] | (1u << NG); E[m + 1] = pr[y] | (1u << NG); E[m + 2] = pr[z] | (1u << NG);
                    int tH = tau_exact(); NE = m;
                    if (!covered && tH != TG + 1) { fprintf(stderr, "VERIFY FAILED: hit with tau(H)=%d\n", tH); return 5; }
                    if (covered && tH != TG) { fprintf(stderr, "VERIFY FAILED: non-hit with tau(H)=%d\n", tH); return 6; }
                    if (!covered) verified_hits++; else verified_nonhits++;
                }
                if (covered) continue;
                hits++;
                printf("HIT:"); for (int i = 0; i < m; i++) { printf(" "); print_set(g[i], -1); }
                printf(" "); print_set(pr[x], NG); printf(" "); print_set(pr[y], NG); printf(" "); print_set(pr[z], NG); printf("\n");
            }
        }
    }
    printf("SUMMARY graphs=%llu bad_tau=%llu tested=%llu hits=%llu verified_hits=%llu verified_nonhits=%llu max_min_transversals=%llu\n",
           graphs, bad_tau, tested, hits, verified_hits, verified_nonhits, maxnt);
    return 0;
}
