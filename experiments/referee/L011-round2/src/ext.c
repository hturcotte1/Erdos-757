/* Referee L011 round 2: extension step from the definitions (own code).
   Usage: ext NG TH D < inputs   (input line = graph G on points 0..NG-1, formats "m a b c ..." or "TAG: (a,b,c) ...").
   For each G: new point v = NG with three edges {v,a_j,b_j}, the pairs {a_j,b_j} pairwise disjoint, no pair inside an edge of G,
   every a_j, b_j of G-degree <= D-1 (isolated points allowed).  Every such unordered triple of pairs is tested; tau(H) >= TH is
   decided directly on H by exhaustive branching (no use of transversals of G).  Hits are printed as "HIT: (..) .. (a,b,v)".
   stderr: "EXT graphs=.. tested=.. hits=.." */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
typedef unsigned long long u64;
static int cover(const u64 *E, int ne, u64 S, int k) { int j; for (j = 0; j < ne; j++) if (!(E[j] & S)) break;
    if (j == ne) return 1; if (k <= 0) return 0; u64 e = E[j];
    while (e) { u64 b = e & (~e + 1); e ^= b; if (cover(E, ne, S | b, k - 1)) return 1; } return 0; }
static int parse(char *line, int ed[][3]) {
    int m = 0;
    if (strchr(line, '(')) { char *p = line; while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &ed[m][0], &ed[m][1], &ed[m][2]) != 3) return -1; m++; p++; } return m; }
    char *p = line; int cnt = 0; static int vals[1000];
    while (*p) { while (*p && !isdigit((unsigned char)*p)) p++; if (!*p) break; vals[cnt++] = (int)strtol(p, &p, 10); }
    if (cnt == 0) return -2; m = vals[0]; if (cnt != 1 + 3*m) return -1;
    for (int k = 0; k < m; k++) for (int t = 0; t < 3; t++) ed[k][t] = vals[1 + 3*k + t];
    return m;
}
int main(int argc, char **argv) {
    int NG = atoi(argv[1]), TH = atoi(argv[2]), D = atoi(argv[3]);
    static char line[1 << 20]; int ed[64][3]; long long ngraphs = 0, tested = 0, hits = 0;
    while (fgets(line, sizeof line, stdin)) {
        int m = parse(line, ed); if (m == -2) continue; if (m < 0) { fprintf(stderr, "parse error\n"); return 1; }
        ngraphs++;
        u64 E[64]; int deg[64] = {0}; u64 inedge[64] = {0};
        for (int j = 0; j < m; j++) { E[j + 3] = 0; for (int t = 0; t < 3; t++) { E[j + 3] |= 1ULL << ed[j][t]; deg[ed[j][t]]++; } }
        for (int j = 0; j < m; j++) for (int t = 0; t < 3; t++) inedge[ed[j][t]] |= E[j + 3];
        int pa[2000], pb[2000], np = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > D - 1 || deg[b] > D - 1) continue;
            if (inedge[a] >> b & 1) continue;          /* pair inside an edge of G */
            pa[np] = a; pb[np] = b; np++;
        }
        u64 v = 1ULL << NG;
        for (int i = 0; i < np; i++) for (int j = i + 1; j < np; j++) {
            u64 Pi = (1ULL << pa[i]) | (1ULL << pb[i]), Pj = (1ULL << pa[j]) | (1ULL << pb[j]);
            if (Pi & Pj) continue;
            for (int k = j + 1; k < np; k++) {
                u64 Pk = (1ULL << pa[k]) | (1ULL << pb[k]);
                if ((Pk & Pi) || (Pk & Pj)) continue;
                tested++;
                E[0] = Pi | v; E[1] = Pj | v; E[2] = Pk | v;
                if (cover(E, m + 3, 0, TH - 1)) continue;
                hits++;
                printf("HIT:");
                for (int t = 0; t < m; t++) printf(" (%d,%d,%d)", ed[t][0], ed[t][1], ed[t][2]);
                printf(" (%d,%d,%d) (%d,%d,%d) (%d,%d,%d)\n", pa[i], pb[i], NG, pa[j], pb[j], NG, pa[k], pb[k], NG);
            }
        }
    }
    fprintf(stderr, "EXT NG=%d TH=%d D=%d graphs=%lld tested=%lld hits=%lld\n", NG, TH, D, ngraphs, tested, hits);
    return 0;
}
