/* Fast filter of ordered midpoint patterns: independent re-statement of K30, K31, and forbidden cores
 * (same semantics as e757.cpsat_model.core_hit / constraint_violations).
 * Usage: filter cores.txt < sols (lines "SOL a i,j,k ...") > out
 * cores.txt: first line N; then per core: kind(0 plain,1 extra_ap) v ne  (i j k)*ne  [r0 r1 r2 if kind 1]
 * Output per canonical-up-to-reflection solution (es <= refl(es)): "k30 k31 c4 call i,j,k ..." (flags 0/1)
 * where c4 = no core hit among cores with <=4 edges, call = no core hit among all cores. Final line "N total canon".
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXC 400
#define NV 12
typedef struct { int kind, v, ne; int ed[8][3]; int rel[3]; } Core;
static Core cores[2*MAXC]; static int nc = 0;
static int E[16][3], ne;
static int Eset[NV][NV][NV];
static int mp[16], used[NV];

static int rec(const Core *c, int t) {
    if (t == c->ne) {
        int prev = -1;
        for (int a = 0; a < c->v; a++) if (mp[a] >= 0) { if (prev >= 0 && mp[a] <= prev) return 0; prev = mp[a]; }
        if (c->kind == 1 && Eset[mp[c->rel[0]]][mp[c->rel[1]]][mp[c->rel[2]]]) return 0;
        return 1;
    }
    for (int e = 0; e < ne; e++) {
        int saved[3], setm[3] = {0,0,0}, ok = 1;
        for (int x = 0; x < 3; x++) {
            int a = c->ed[t][x], b = E[e][x];
            if (mp[a] >= 0) { if (mp[a] != b) { ok = 0; break; } }
            else { if (used[b]) { ok = 0; break; } mp[a] = b; used[b] = 1; setm[x] = 1; }
        }
        int hit = 0;
        if (ok) hit = rec(c, t + 1);
        for (int x = 2; x >= 0; x--) if (setm[x]) { int a = c->ed[t][x]; used[mp[a]] = 0; mp[a] = -1; }
        (void)saved;
        if (hit) return 1;
    }
    return 0;
}
static int core_hit(const Core *c) { for (int a = 0; a < 16; a++) mp[a] = -1; memset(used, 0, sizeof used); return rec(c, 0); }
static int cmp3(const void *a, const void *b) { const int *x=a,*y=b; for (int t=0;t<3;t++) if (x[t]!=y[t]) return x[t]-y[t]; return 0; }
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); int N; fscanf(f, "%d", &N);
    int kind, v, k;
    while (fscanf(f, "%d %d %d", &kind, &v, &k) == 3) {
        Core *c = &cores[nc]; c->kind = kind; c->v = v; c->ne = k;
        for (int t = 0; t < k; t++) fscanf(f, "%d %d %d", &c->ed[t][0], &c->ed[t][1], &c->ed[t][2]);
        if (kind) fscanf(f, "%d %d %d", &c->rel[0], &c->rel[1], &c->rel[2]);
        qsort(c->ed, k, sizeof c->ed[0], cmp3);
        nc++;
    }
    static char line[4096]; long total = 0, canon = 0;
    while (fgets(line, sizeof line, stdin)) {
        if (strncmp(line, "SOL", 3)) continue;
        char *p = line + 3; strtol(p, &p, 10); ne = 0;
        while (1) { char *q; long i = strtol(p, &q, 10); if (q == p) break; p = q + 1; long j = strtol(p, &q, 10); p = q + 1; long kk = strtol(p, &q, 10); p = q; E[ne][0]=i;E[ne][1]=j;E[ne][2]=kk; ne++; }
        total++;
        qsort(E, ne, sizeof E[0], cmp3);
        int R[16][3];
        for (int t = 0; t < ne; t++) { R[t][0]=N-1-E[t][2]; R[t][1]=N-1-E[t][1]; R[t][2]=N-1-E[t][0]; }
        qsort(R, ne, sizeof R[0], cmp3);
        int cmp = 0; for (int t = 0; t < ne && !cmp; t++) cmp = cmp3(E[t], R[t]);
        if (cmp > 0) continue;
        canon++;
        memset(Eset, 0, sizeof Eset);
        for (int t = 0; t < ne; t++) Eset[E[t][0]][E[t][1]][E[t][2]] = 1;
        /* K30 */
        int k30 = 1;
        for (int a = 0; a < ne; a++) for (int b = 0; b < ne; b++)
            if (E[a][0] <= E[b][0] && E[a][2] <= E[b][2] && !(E[a][0]==E[b][0] && E[a][2]==E[b][2]) && !(E[a][1] < E[b][1])) k30 = 0;
        int k31 = 1;
        for (int a = 0; a < ne; a++) for (int b = 0; b < ne; b++)
            if (E[b][0] == E[a][0] && E[b][2] > E[a][2] && E[b][1] != E[a][1])
                for (int c = 0; c < ne; c++) if (E[c][0] == E[a][2] && E[c][2] == E[b][2]) k31 = 0;
        int c4 = 1, call = 1;
        for (int ci = 0; ci < nc && call; ci++) {
            if (core_hit(&cores[ci])) { call = 0; if (cores[ci].ne <= 4) c4 = 0; }
        }
        /* c4 needs all small cores evaluated even when a bigger one hit: redo */
        if (!call && c4) { for (int ci = 0; ci < nc; ci++) if (cores[ci].ne <= 4 && core_hit(&cores[ci])) { c4 = 0; break; } }
        printf("%d %d %d %d", k30, k31, c4, call);
        for (int t = 0; t < ne; t++) printf(" %d,%d,%d", E[t][0], E[t][1], E[t][2]);
        printf("\n");
    }
    fprintf(stderr, "total=%ld canon=%ld\n", total, canon);
    return 0;
}
