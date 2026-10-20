/* Referee L014 r1: convert lines containing "(a,b,c)" triples (FOUND:/HIT:/SURVIVOR: lines) of a 3-graph on N vertices into
   graph6 of its incidence graph (vertices 0..N-1, then edge-nodes N..N+M-1).  Usage: hg2g6 N < in > out.g6 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv) {
  int N = atoi(argv[1]); static char line[1 << 16]; long cnt = 0;
  while (fgets(line, sizeof line, stdin)) {
    int ev[64][3], M = 0; char *p = line;
    if (line[0] == 'I' || line[0] == 'S' && strncmp(line, "SURVIVOR", 8) && 1) { if (!strchr(line, '(')) continue; }
    while ((p = strchr(p, '(')) != NULL) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) == 3) { ev[M][0] = a; ev[M][1] = b; ev[M][2] = c; M++; } p++; }
    if (M == 0) continue;
    int n = N + M; if (n > 62) { fprintf(stderr, "too big\n"); return 2; }
    static unsigned char adj[64][64]; memset(adj, 0, sizeof adj);
    for (int e = 0; e < M; e++) for (int j = 0; j < 3; j++) { int v = ev[e][j]; if (v < 0 || v >= N) { fprintf(stderr, "bad v\n"); return 3; } adj[v][N + e] = adj[N + e][v] = 1; }
    char out[1024]; int k = 0; out[k++] = (char)(63 + n);
    int bits = 0, nb = 0;
    for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) { bits = bits << 1 | adj[i][j]; nb++; if (nb == 6) { out[k++] = (char)(63 + bits); bits = 0; nb = 0; } }
    if (nb) { bits <<= (6 - nb); out[k++] = (char)(63 + bits); }
    out[k] = 0; puts(out); cnt++;
  }
  fprintf(stderr, "hg2g6: %ld graphs\n", cnt);
  return 0;
}
