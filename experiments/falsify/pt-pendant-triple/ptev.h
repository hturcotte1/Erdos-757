/* shared evaluation: avoided deg<=2 vertices and PT candidate triples (needs i11core.h) */
typedef struct { int tau, slack, nU, nU2, U2[MAXN], ncand, minGood; } Ev;
static int tau_without(const G *g, int v) { G h; h.n = g->n; h.m = 0; for (int i = 0; i < g->m; i++) if (!((g->e[i] >> v) & 1)) h.e[h.m++] = g->e[i]; return tau_of(&h, 2, 0, NULL); }
static int tau_without3(const G *g, u64 X) { G h; h.n = g->n; h.m = 0; for (int i = 0; i < g->m; i++) if (!(g->e[i] & X)) h.e[h.m++] = g->e[i]; return tau_of(&h, 2, 0, NULL); }
static void evaluate(const G *g, Ev *ev, int do_pt) {
    ev->tau = tau_of(g, 2, 0, NULL); ev->slack = slack_of(g, ev->tau); ev->nU = 0; ev->nU2 = 0; ev->ncand = 0; ev->minGood = 99;
    for (int v = 0; v < g->n; v++) { int d = degree_of(g, v); if (d == 0 || d > 2) continue; if (tau_without(g, v) == ev->tau) { ev->nU2++; ev->U2[ev->nU2 - 1] = v; } }
    if (!do_pt || ev->nU2 < 6) return;
    int np = 0; static int pr[MAXN * MAXN][2];
    for (int i = 0; i < ev->nU2; i++) for (int j = i + 1; j < ev->nU2; j++) { int a = ev->U2[i], b = ev->U2[j]; int inedge = 0; for (int e = 0; e < g->m; e++) if (((g->e[e] >> a) & 1) && ((g->e[e] >> b) & 1)) { inedge = 1; break; } if (!inedge) { pr[np][0] = a; pr[np][1] = b; np++; } }
    int cnt = 0;
    for (int x = 0; x < np; x++) for (int y = x + 1; y < np; y++) {
        if (pr[x][0] == pr[y][0] || pr[x][0] == pr[y][1] || pr[x][1] == pr[y][0] || pr[x][1] == pr[y][1]) continue;
        for (int z = y + 1; z < np; z++) {
            int *A = pr[x], *B = pr[y], *C = pr[z];
            if (A[0] == C[0] || A[0] == C[1] || A[1] == C[0] || A[1] == C[1] || B[0] == C[0] || B[0] == C[1] || B[1] == C[0] || B[1] == C[1]) continue;
            if (++cnt > 40) goto done;
            ev->ncand++; int good = 0;
            for (int i = 0; i < 2; i++) for (int j = 0; j < 2; j++) for (int k = 0; k < 2; k++) { u64 X = (1ULL << A[i]) | (1ULL << B[j]) | (1ULL << C[k]); if (tau_without3(g, X) <= ev->tau - 2) good++; }
            if (good < ev->minGood) ev->minGood = good;
        }
    }
done:;
}
