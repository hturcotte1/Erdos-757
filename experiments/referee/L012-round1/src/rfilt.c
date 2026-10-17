/* rfilt.c -- referee's filter for the extensions produced by rext (L012 round 1), independent of the prover's filt.c.
   Usage: rfilt NG inputs_file < rext_output     builds H = G_i + {NG, a_j, b_j} for every "X: i a1 b1 a2 b2 ..." line.
   Checks: linear (pairwise intersections <= 1); F7 by a centre-based search (a vertex p, three edges at p, and two disjoint
   transversal edges each taking one non-centre vertex from each of the three); (P3) e(S) <= |S|-2 for |S| >= 2, via: for every
   pair {x,y} of vertices, a matching of all edges into V \ {x,y} (each edge to one of its own vertices) exists -- BFS augmenting
   paths; tau(H) by branching; connectivity on all NG+1 vertices by union-find; maximum degree.
   Prints "S: (a,b,c) ..." for every H that is linear, F7-free and (P3), plus a SUMMARY. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int nv, ne, ed[64][3];
static int inG[40000][32][3], mG[40000];
static int lin(void) { for (int i = 0; i < ne; i++) for (int j = i + 1; j < ne; j++) { int c = 0;
    for (int a = 0; a < 3; a++) for (int b = 0; b < 3; b++) c += ed[i][a] == ed[j][b]; if (c > 1) return 0; } return 1; }
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
/* bipartite matching edges -> vertices (excluding x,y), BFS augmenting paths */
static int matchE[64], matchV[32];
static int bfs_aug(int src, int x, int y) {
    int prevE[32], from[64], q[64], qh = 0, qt = 0; int seenV[32]; memset(seenV, 0, sizeof seenV);
    for (int i = 0; i < 64; i++) from[i] = -2;
    q[qt++] = src; from[src] = -1;
    while (qh < qt) {
        int e = q[qh++];
        for (int k = 0; k < 3; k++) { int v = ed[e][k]; if (v == x || v == y || seenV[v]) continue; seenV[v] = 1; prevE[v] = e;
            if (matchV[v] < 0) { /* augment along the path */
                int cv = v;
                while (1) { int ce = prevE[cv]; int nxt = matchE[ce]; matchE[ce] = cv; matchV[cv] = ce; if (from[ce] == -1) break; cv = nxt; (void)0;
                    /* nxt was the vertex previously matched to ce; continue from the edge that reached it */ }
                return 1; }
            int e2 = matchV[v]; if (from[e2] == -2) { from[e2] = e; q[qt++] = e2; } }
    }
    return 0;
}
static int p3(void) {
    for (int x = 0; x < nv; x++) for (int y = x + 1; y < nv; y++) {
        for (int i = 0; i < 64; i++) matchE[i] = -1; for (int i = 0; i < 32; i++) matchV[i] = -1;
        for (int e = 0; e < ne; e++) if (!bfs_aug(e, x, y)) return 0;
    }
    return 1;
}
static int cover_k(int k, uint32_t S, int from, const uint32_t *M) {
    int e = -1; for (int i = from; i < ne; i++) if (!(M[i] & S)) { e = i; break; }
    if (e < 0) return 1; if (!k) return 0;
    for (int t = 0; t < 3; t++) if (cover_k(k - 1, S | (1u << ed[e][t]), e + 1, M)) return 1;
    return 0;
}
static int tau(void) { uint32_t M[64]; for (int i = 0; i < ne; i++) M[i] = (1u << ed[i][0]) | (1u << ed[i][1]) | (1u << ed[i][2]);
    for (int k = 0; ; k++) if (cover_k(k, 0, 0, M)) return k; }
static int par[32]; static int fnd(int x) { while (par[x] != x) x = par[x] = par[par[x]]; return x; }
static int conn(void) { for (int i = 0; i < nv; i++) par[i] = i; for (int e = 0; e < ne; e++) { par[fnd(ed[e][0])] = fnd(ed[e][1]); par[fnd(ed[e][1])] = fnd(ed[e][2]); }
    int r = fnd(0); for (int i = 1; i < nv; i++) if (fnd(i) != r) return 0; return 1; }
int main(int argc, char **argv) {
    int NG = atoi(argv[1]); FILE *fi = fopen(argv[2], "r"); int ng = 0, m;
    while (fscanf(fi, "%d", &m) == 1) { mG[ng] = m; for (int i = 0; i < m; i++) if (fscanf(fi, "%d %d %d", &inG[ng][i][0], &inG[ng][i][1], &inG[ng][i][2]) != 3) return 2; ng++; }
    nv = NG + 1; static char line[4096];
    long long tot = 0, nlin = 0, nf7 = 0, np3bad = 0, surv = 0, survconn = 0; int tmin = 99, tmax = -1, dmaxmax = 0, dminmax = 99;
    while (fgets(line, sizeof line, stdin)) {
        if (strncmp(line, "X:", 2)) continue;
        int v[40], k = 0; char *p = line + 2, *q; while (1) { long x = strtol(p, &q, 10); if (q == p) break; v[k++] = (int)x; p = q; }
        int gi = v[0]; ne = 0;
        for (int i = 0; i < mG[gi]; i++) { for (int t = 0; t < 3; t++) ed[ne][t] = inG[gi][i][t]; ne++; }
        for (int i = 1; i + 1 < k; i += 2) { ed[ne][0] = v[i]; ed[ne][1] = v[i + 1]; ed[ne][2] = NG; ne++; }
        tot++;
        memset(edge_id, 0, sizeof edge_id);
        for (int e = 0; e < ne; e++) { int a = ed[e][0], b = ed[e][1], c = ed[e][2];
            int pr[6][3] = {{a,b,c},{a,c,b},{b,a,c},{b,c,a},{c,a,b},{c,b,a}}; for (int t = 0; t < 6; t++) edge_id[pr[t][0]][pr[t][1]][pr[t][2]] = e + 1; }
        if (!lin()) continue; nlin++;
        if (f7()) { nf7++; continue; }
        if (!p3()) { np3bad++; continue; }
        int t = tau(); if (t < tmin) tmin = t; if (t > tmax) tmax = t;
        int deg[32] = {0}; for (int e = 0; e < ne; e++) for (int z = 0; z < 3; z++) deg[ed[e][z]]++;
        int dm = 0; for (int i = 0; i < nv; i++) if (deg[i] > dm) dm = deg[i]; if (dm > dmaxmax) dmaxmax = dm; if (dm < dminmax) dminmax = dm;
        int c = conn(); surv++; survconn += c;
        printf("S:"); for (int e = 0; e < ne; e++) printf(" (%d,%d,%d)", ed[e][0], ed[e][1], ed[e][2]); printf(" #conn=%d tau=%d\n", c, t);
    }
    printf("SUMMARY total=%lld linear=%lld contain_F7=%lld F7free_P3_violated=%lld survivors=%lld connected=%lld tau_range=[%d,%d] maxdeg_range=[%d,%d]\n",
           tot, nlin, nf7, np3bad, surv, survconn, tmin, tmax, dminmax, dmaxmax);
    return 0;
}
