/* gfilt.c -- referee: decode genbg graph6 output (n1 hypergraph vertices, then n2 edge-vertices of degree 3) into 3-graphs and
   keep those that are F7-free, satisfy (P3) and have tau == T (and max degree <= D).  Same checks as rfilt.c.
   Usage: genbg ... n1 n2 | gfilt n1 n2 T D     prints "FOUND: (a,b,c) ..." and a SUMMARY on stderr. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int nv, ne, ed[64][3];
static int edge_id[32][32][32];
static int isedge(int a, int b, int c) { return edge_id[a][b][c] > 0; }
static int f7(void) {
    for (int p = 0; p < nv; p++) {
        int at[16], na = 0; for (int e = 0; e < ne; e++) for (int k = 0; k < 3; k++) if (ed[e][k] == p && na < 16) at[na++] = e;
        for (int i = 0; i < na; i++) for (int j = i + 1; j < na; j++) for (int k = j + 1; k < na; k++) {
            int o[3][2]; int ids[3] = {at[i], at[j], at[k]};
            for (int q = 0; q < 3; q++) { int c = 0; for (int r = 0; r < 3; r++) if (ed[ids[q]][r] != p) o[q][c++] = ed[ids[q]][r]; }
            for (int s2 = 0; s2 < 2; s2++) for (int s3 = 0; s3 < 2; s3++)
                if (isedge(o[0][0], o[1][s2], o[2][s3]) && isedge(o[0][1], o[1][1 - s2], o[2][1 - s3])) return 1;
        }
    }
    return 0;
}
static int matchE[64], matchV[32];
static int bfs_aug(int src, int x, int y) {
    int prevE[32], from[64], q[64], qh = 0, qt = 0; int seenV[32]; memset(seenV, 0, sizeof seenV);
    for (int i = 0; i < 64; i++) from[i] = -2;
    q[qt++] = src; from[src] = -1;
    while (qh < qt) {
        int e = q[qh++];
        for (int k = 0; k < 3; k++) { int v = ed[e][k]; if (v == x || v == y || seenV[v]) continue; seenV[v] = 1; prevE[v] = e;
            if (matchV[v] < 0) { int cv = v;
                while (1) { int ce = prevE[cv]; int nxt = matchE[ce]; matchE[ce] = cv; matchV[cv] = ce; if (from[ce] == -1) break; cv = nxt; }
                return 1; }
            int e2 = matchV[v]; if (from[e2] == -2) { from[e2] = e; q[qt++] = e2; } }
    }
    return 0;
}
static int p3(void) {
    for (int x = 0; x < nv; x++) for (int y = x + 1; y < nv; y++) {
        for (int i = 0; i < 64; i++) matchE[i] = -1;
        for (int i = 0; i < 32; i++) matchV[i] = -1;
        for (int e = 0; e < ne; e++) if (!bfs_aug(e, x, y)) return 0;
    }
    return 1;
}
static int cover_k(int k, uint32_t S, int from, const uint32_t *M) {
    int e = -1; for (int i = from; i < ne; i++) if (!(M[i] & S)) { e = i; break; }
    if (e < 0) return 1;
    if (!k) return 0;
    for (int t = 0; t < 3; t++) if (cover_k(k - 1, S | (1u << ed[e][t]), e + 1, M)) return 1;
    return 0;
}
static int tau(void) { uint32_t M[64]; for (int i = 0; i < ne; i++) M[i] = (1u << ed[i][0]) | (1u << ed[i][1]) | (1u << ed[i][2]);
    for (int k = 0; ; k++) if (cover_k(k, 0, 0, M)) return k; }
int main(int argc, char **argv) {
    int n1 = atoi(argv[1]), n2 = atoi(argv[2]), T = atoi(argv[3]), D = atoi(argv[4]); nv = n1;
    static char line[1 << 12]; long long tot = 0, nf7 = 0, np3 = 0, ntau = 0, out = 0, baddeg = 0;
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] == '>') continue;
        int n = line[0] - 63; if (n != n1 + n2) { fprintf(stderr, "bad n %d\n", n); return 2; }
        static int adj[64][64]; memset(adj, 0, sizeof adj);
        int bitpos = 0; const char *p = line + 1;
        for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) {
            int byte = p[bitpos / 6] - 63; int bit = (byte >> (5 - bitpos % 6)) & 1; bitpos++;
            adj[i][j] = adj[j][i] = bit; }
        ne = 0; int ok = 1;
        for (int e = n1; e < n; e++) { int c = 0; for (int v = 0; v < n1; v++) if (adj[e][v]) { if (c < 3) ed[ne][c] = v; c++; }
            for (int v = n1; v < n; v++) if (adj[e][v]) ok = 0;
            if (c != 3) ok = 0; ne++; }
        if (!ok) { fprintf(stderr, "not a 3-graph incidence graph\n"); return 3; }
        tot++;
        int deg[32] = {0}; for (int e = 0; e < ne; e++) for (int z = 0; z < 3; z++) deg[ed[e][z]]++;
        int dm = 0; for (int v = 0; v < nv; v++) if (deg[v] > dm) dm = deg[v]; if (dm > D) { baddeg++; continue; }
        memset(edge_id, 0, sizeof edge_id);
        for (int e = 0; e < ne; e++) { int a = ed[e][0], b = ed[e][1], c = ed[e][2];
            int pr[6][3] = {{a,b,c},{a,c,b},{b,a,c},{b,c,a},{c,a,b},{c,b,a}}; for (int t = 0; t < 6; t++) edge_id[pr[t][0]][pr[t][1]][pr[t][2]] = e + 1; }
        int t = tau(); if (t != T) { ntau++; continue; }
        if (f7()) { nf7++; continue; }
        if (!p3()) { np3++; continue; }
        out++; printf("FOUND:"); for (int e = 0; e < ne; e++) printf(" (%d,%d,%d)", ed[e][0], ed[e][1], ed[e][2]); printf("\n");
    }
    fprintf(stderr, "GSUM n1=%d n2=%d T=%d D=%d total=%lld deg_over=%lld tau_other=%lld F7=%lld P3bad=%lld kept=%lld\n", n1, n2, T, D, tot, baddeg, ntau, nf7, np3, out);
    return 0;
}
