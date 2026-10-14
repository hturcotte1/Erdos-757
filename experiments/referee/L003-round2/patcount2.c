/* patcount2.c -- referee L003 round 2: count SATURATED class-O patterns (every interior rank j has exactly one AP (L[j],j,R[j]),
 * linear, K30, F7-free) with alpha <= T, labelled and reflection-symmetric.  Independent of e757/ and of the round-1 code.
 * F7 = {012,034,056,135,246}: a centre v with three edges {v,a1,a2},{v,b1,b2},{v,c1,c2} and two further edges {a,b,c},
 * {a',b',c'} taking one point from each pair and the complementary points (sub-hypergraph containment).
 * alpha <= T  iff  no (T+1)-subset is independent (contains no edge).
 * usage: ./patcount2 n T     -> "PAT n T labelled=.. symmetric=.. up_to_reflection=.. (f7 rejected=.., alpha rejected=..)" */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 14
static int n, T, L[MAXN], R[MAXN];
static long long lab = 0, sym = 0, f7rej = 0, alpharej = 0, leaves = 0;
static int subs[5000], nsubs = 0;

static int has_edge(int a, int b, int c) {
    /* edge with these three vertices? each edge is (L[j], j, R[j]) for interior j */
    int s[3] = { a, b, c };
    for (int u = 0; u < 3; u++) { int j = s[u]; if (j >= 1 && j <= n - 2) {
        int o1 = s[(u + 1) % 3], o2 = s[(u + 2) % 3];
        if ((L[j] == o1 && R[j] == o2) || (L[j] == o2 && R[j] == o1)) return 1; } }
    return 0;
}

static int has_f7(void) {
    for (int v = 0; v < n; v++) {
        int pa[MAXN][2], np = 0;
        for (int j = 1; j <= n - 2; j++) {
            int e[3] = { L[j], j, R[j] };
            for (int u = 0; u < 3; u++) if (e[u] == v) { pa[np][0] = e[(u + 1) % 3]; pa[np][1] = e[(u + 2) % 3]; np++; }
        }
        for (int x = 0; x < np; x++) for (int y = x + 1; y < np; y++) for (int z = y + 1; z < np; z++)
            for (int bx = 0; bx < 2; bx++) for (int by = 0; by < 2; by++) for (int bz = 0; bz < 2; bz++)
                if (has_edge(pa[x][bx], pa[y][by], pa[z][bz]) && has_edge(pa[x][1 - bx], pa[y][1 - by], pa[z][1 - bz])) return 1;
    }
    return 0;
}

static void leaf(void) {
    leaves++;
    if (has_f7()) { f7rej++; return; }
    int em[MAXN];
    for (int j = 1; j <= n - 2; j++) em[j] = (1 << L[j]) | (1 << j) | (1 << R[j]);
    for (int s = 0; s < nsubs; s++) {
        int ind = 1;
        for (int j = 1; j <= n - 2; j++) if ((subs[s] & em[j]) == em[j]) { ind = 0; break; }
        if (ind) { alpharej++; return; }
    }
    lab++;
    /* reflection: rank i -> n-1-i; the AP with midpoint j maps to the AP with midpoint n-1-j and endpoints n-1-R[j], n-1-L[j] */
    int s = 1;
    for (int j = 1; j <= n - 2 && s; j++) { int jj = n - 1 - j; if (!(L[jj] == n - 1 - R[j] && R[jj] == n - 1 - L[j])) s = 0; }
    sym += s;
}

static void dfs(int j) {
    if (j == n - 1) { leaf(); return; }
    for (int l = 0; l < j; l++) for (int r = j + 1; r <= n - 1; r++) {
        int bad = 0;
        for (int i = 1; i < j && !bad; i++) {
            if (l <= L[i] && r <= R[i]) bad = 1;
            int e1[3] = { L[i], i, R[i] }, e2[3] = { l, j, r }, c = 0;
            for (int u = 0; u < 3; u++) for (int w = 0; w < 3; w++) if (e1[u] == e2[w]) c++;
            if (c >= 2) bad = 1;
        }
        if (bad) continue;
        L[j] = l; R[j] = r; dfs(j + 1);
    }
}

int main(int argc, char **argv) {
    n = atoi(argv[1]); T = atoi(argv[2]);
    for (int s = 0; s < (1 << n); s++) if (__builtin_popcount(s) == T + 1) subs[nsubs++] = s;
    dfs(1);
    printf("PAT n=%d T=%d K30+lin leaves=%lld f7_rejected=%lld alpha_rejected=%lld labelled=%lld symmetric=%lld up_to_reflection=%lld\n",
           n, T, leaves, f7rej, alpharej, lab, sym, (lab + sym) / 2);
    return 0;
}
