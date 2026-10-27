// Transversal richness of class-C graphs (exact).  Input lines: "n m tau a b c a b c ...".  Output: one JSON line per graph.
// For each graph F: all minimum transversals; vertex/pair coverage; pair-pair coverage; all triples of disjoint pairs:
// coverability by a min transversal, admissibility of F+v (linear, F7-free, e(S)<=|S|-2), violation classification.
#include <bits/stdc++.h>
using namespace std;
typedef uint32_t u32; typedef uint64_t u64;
static int n, m, tau_;
static u32 em[64]; static int ev[64][3];
static vector<u32> TS;           // min transversals
static bool truncated = false;
static const size_t TCAP = 400000;
static void dfs(u32 chosen, u32 forb, int cnt) {
    // find first uncovered edge; compute packing lower bound
    int first = -1; u32 used = 0; int pack = 0;
    for (int i = 0; i < m; i++) {
        if (em[i] & chosen) continue;
        if (first < 0) first = i;
        if ((em[i] & ~forb) == 0) return;
        if (!(em[i] & used)) { used |= em[i]; pack++; }
    }
    if (first < 0) { if (cnt == tau_) { if (TS.size() < TCAP) TS.push_back(chosen); else truncated = true; } return; }
    if (cnt + pack > tau_) return;
    u32 f = forb;
    for (int k = 0; k < 3; k++) {
        int v = ev[first][k];
        if (forb >> v & 1) continue;
        dfs(chosen | (1u << v), f, cnt + 1);
        f |= 1u << v;
    }
}
int main() {
    string line;
    while (getline(cin, line)) {
        istringstream is(line); int tau; is >> n >> m >> tau; tau_ = tau;
        for (int i = 0; i < m; i++) { int a, b, c; is >> a >> b >> c; ev[i][0] = a; ev[i][1] = b; ev[i][2] = c; em[i] = (1u << a) | (1u << b) | (1u << c); }
        TS.clear(); truncated = false; dfs(0, 0, 0);
        int nT = TS.size(); int W = (nT + 63) / 64; if (W == 0) W = 1;
        vector<int> deg(n, 0); for (int i = 0; i < m; i++) for (int k = 0; k < 3; k++) deg[ev[i][k]]++;
        static bool inedge[32][32]; memset(inedge, 0, sizeof inedge);
        for (int i = 0; i < m; i++) for (int a = 0; a < 3; a++) for (int b = 0; b < 3; b++) if (a != b) inedge[ev[i][a]][ev[i][b]] = true;
        vector<vector<u64>> vb(n, vector<u64>(W, 0));
        for (int t = 0; t < nT; t++) for (int v = 0; v < n; v++) if (TS[t] >> v & 1) vb[v][t >> 6] |= 1ULL << (t & 63);
        int novert = 0; for (int v = 0; v < n; v++) { bool any = false; for (u64 w : vb[v]) if (w) any = true; if (!any) novert++; }
        // P2
        long p2tot[12] = {0}, p2fail[12] = {0};
        for (int x = 0; x < n; x++) for (int y = x + 1; y < n; y++) {
            bool c = false; for (int w = 0; w < W; w++) if (vb[x][w] & vb[y][w]) { c = true; break; }
            int key = deg[x] + deg[y] - (inedge[x][y] ? 1 : 0); if (key > 11) key = 11;
            p2tot[key]++; if (!c) p2fail[key]++;
        }
        // pair meets
        int np = n * (n - 1) / 2; vector<int> pa(np), pb(np); vector<vector<u64>> mb(np, vector<u64>(W));
        vector<char> good(np); vector<u32> pm(np);
        { int k = 0; for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) { pa[k] = a; pb[k] = b; for (int w = 0; w < W; w++) mb[k][w] = vb[a][w] | vb[b][w]; good[k] = !inedge[a][b]; pm[k] = (1u << a) | (1u << b); k++; } }
        // pair-pair coverage
        long pp_all = 0, pp_all_cov = 0, pp_good = 0, pp_good_cov = 0;
        for (int p = 0; p < np; p++) for (int q = p + 1; q < np; q++) {
            if (pm[p] & pm[q]) continue;
            bool c = false; for (int w = 0; w < W; w++) if (mb[p][w] & mb[q][w]) { c = true; break; }
            pp_all++; if (c) pp_all_cov++;
            if (good[p] && good[q]) { pp_good++; if (c) pp_good_cov++; }
        }
        // subset tables
        size_t NS = (size_t)1 << n; const unsigned char INF = 255;
        bool doTriples = true;
        vector<unsigned char> s2(NS), s3(NS);
        {
            vector<unsigned char> e(NS, 0);
            vector<vector<u32>> rest(n);
            for (int i = 0; i < m; i++) for (int k = 0; k < 3; k++) rest[ev[i][k]].push_back(em[i] & ~(1u << ev[i][k]));
            e[0] = 0; s2[0] = s3[0] = INF;
            for (size_t S = 1; S < NS; S++) {
                int low = __builtin_ctz((u32)S); u32 R = (u32)S & ~(1u << low); int ee = e[R];
                // edges containing low whose other two vertices are in R: but must count each edge once: edge counted when its highest vertex is added; here low = lowest bit of S so edge counted at lowest vertex of the edge within S
                for (u32 r : rest[low]) if ((r & R) == r) ee++;
                e[S] = ee; int pc = __builtin_popcount((u32)S); int f = pc - ee;
                s2[S] = (pc >= 2 && f <= 2) ? pc : INF; s3[S] = (pc >= 2 && f <= 3) ? pc : INF;
            }
            // note: e[S] counts edges whose lowest vertex is the lowest bit at each step -> every edge contained in S counted exactly once (at its lowest vertex when that vertex is the lowest of the remaining set)
            for (int i = 0; i < n; i++) { u32 b = 1u << i; for (size_t S = 0; S < NS; S++) if (!(S & b)) { unsigned char a = s2[S | b]; if (a < s2[S]) s2[S] = a; a = s3[S | b]; if (a < s3[S]) s3[S] = a; } }
        }
        // F7 test on H = F + v (v = n) with new edges
        static bool tab[32 * 32 * 32];
        auto code = [&](int a, int b, int c) { int t; if (a > b) { t = a; a = b; b = t; } if (b > c) { t = b; b = c; c = t; } if (a > b) { t = a; a = b; b = t; } return (a * 32 + b) * 32 + c; };
        for (int i = 0; i < m; i++) tab[code(ev[i][0], ev[i][1], ev[i][2])] = true;
        auto hasF7 = [&](int NE, int (*E)[3]) -> bool {
            vector<vector<int>> at(n + 1);
            for (int i = 0; i < NE; i++) for (int k = 0; k < 3; k++) at[E[i][k]].push_back(i);
            for (int c = 0; c <= n; c++) {
                int d = at[c].size(); if (d < 3) continue;
                for (int i = 0; i < d; i++) for (int j = i + 1; j < d; j++) for (int l = j + 1; l < d; l++) {
                    int pr[3][2]; int ids[3] = {at[c][i], at[c][j], at[c][l]};
                    for (int t = 0; t < 3; t++) { int q = 0; for (int k = 0; k < 3; k++) if (E[ids[t]][k] != c) pr[t][q++] = E[ids[t]][k]; }
                    int a1 = pr[0][0], b1 = pr[0][1];
                    for (int o2 = 0; o2 < 2; o2++) for (int o3 = 0; o3 < 2; o3++) {
                        int x2 = pr[1][o2], y2 = pr[1][1 - o2], x3 = pr[2][o3], y3 = pr[2][1 - o3];
                        int vs[7] = {c, a1, b1, x2, y2, x3, y3}; bool dist = true;
                        for (int s = 0; s < 7 && dist; s++) for (int t = s + 1; t < 7; t++) if (vs[s] == vs[t]) { dist = false; break; }
                        if (!dist) continue;
                        if (tab[code(a1, x2, x3)] && tab[code(b1, y2, y3)]) return true;
                    }
                }
            }
            return false;
        };
        // tab must also contain new edges when testing: handled by temporarily setting
        long ntrip = 0, ncov = 0, nlin = 0, nadm = 0, nadm_unc = 0;
        long adm_R2 = 0, adm_R2_unc = 0, adm_R1 = 0, adm_R1_unc = 0;   // R2: all six have d_F == 2; R1: all six have d_F >= 2
        long uncA = 0, uncBonly = 0; long uncA_size[40] = {0}, uncB_size[40] = {0};
        long unc_total = 0, unc_combo[8] = {0}; long unc_P_only_size[40] = {0}; long unc_P_size[40] = {0};
        long nonadm_total = 0, nonadm_L = 0, nonadm_P = 0;
        long adm_unc_ex[64][1]; (void)adm_unc_ex;
        vector<array<int, 6>> adm_unc_list;  // sample list of admissible uncoverable triples
        vector<u64> acc(W);
        int Eh[64][3]; for (int i = 0; i < m; i++) for (int k = 0; k < 3; k++) Eh[i][k] = ev[i][k];
        for (int p1 = 0; p1 < np; p1++) for (int p2 = p1 + 1; p2 < np; p2++) {
            if (pm[p1] & pm[p2]) continue;
            for (int w = 0; w < W; w++) acc[w] = mb[p1][w] & mb[p2][w];
            u32 m12 = pm[p1] | pm[p2];
            for (int p3 = p2 + 1; p3 < np; p3++) {
                if (pm[p3] & m12) continue;
                ntrip++;
                bool cov = false; for (int w = 0; w < W; w++) if (acc[w] & mb[p3][w]) { cov = true; break; }
                if (cov) ncov++;
                bool lin = good[p1] && good[p2] && good[p3];
                if (lin) nlin++;
                u32 W6 = m12 | pm[p3];
                int minsz = INF;
                { unsigned char a = s2[m12]; if (a < minsz) minsz = a; a = s2[pm[p1] | pm[p3]]; if (a < minsz) minsz = a; a = s2[pm[p2] | pm[p3]]; if (a < minsz) minsz = a; a = s3[W6]; if (a < minsz) minsz = a; }
                bool p3ok = (minsz == INF);
                bool needF7 = (!cov) || (lin && p3ok);
                bool f7 = false;
                if (needF7) {
                    int NE = m; int pp[3] = {p1, p2, p3};
                    for (int t = 0; t < 3; t++) { Eh[NE][0] = n; Eh[NE][1] = pa[pp[t]]; Eh[NE][2] = pb[pp[t]]; tab[code(n, pa[pp[t]], pb[pp[t]])] = true; NE++; }
                    f7 = hasF7(NE, Eh);
                    for (int t = 0; t < 3; t++) tab[code(n, pa[pp[t]], pb[pp[t]])] = false;
                }
                bool adm = lin && p3ok && !f7;
                if (!lin) nonadm_L++;
                if (!p3ok) nonadm_P++;
                if (!adm) nonadm_total++;
                int vv[6] = {pa[p1], pb[p1], pa[p2], pb[p2], pa[p3], pb[p3]};
                bool r2 = true, r1 = true; for (int t = 0; t < 6; t++) { if (deg[vv[t]] != 2) r2 = false; if (deg[vv[t]] < 2) r1 = false; }
                if (adm) { nadm++; if (r2) adm_R2++; if (r1) adm_R1++; if (!cov) { nadm_unc++; if (r2) adm_R2_unc++; if (r1) adm_R1_unc++; if (adm_unc_list.size() < 20) adm_unc_list.push_back({vv[0], vv[1], vv[2], vv[3], vv[4], vv[5]}); } }
                if (!cov) {
                    unc_total++; int combo = (lin ? 0 : 1) | (f7 ? 2 : 0) | (p3ok ? 0 : 4); unc_combo[combo]++;
                    if (!p3ok) {
                        int a2 = s2[m12]; { int t = s2[pm[p1] | pm[p3]]; if (t < a2) a2 = t; t = s2[pm[p2] | pm[p3]]; if (t < a2) a2 = t; }
                        if (a2 != INF) { uncA++; int z = a2 + 1; if (z > 39) z = 39; uncA_size[z]++; }
                        else { uncBonly++; int z = s3[W6] + 1; if (z > 39) z = 39; uncB_size[z]++; }
                        int sz = minsz + 1; if (sz > 39) sz = 39; unc_P_size[sz]++; if (lin && !f7) unc_P_only_size[sz]++; }
                }
            }
        }
        // output
        printf("{\"n\":%d,\"m\":%d,\"tau\":%d,\"nT\":%d,\"trunc\":%d,\"novert\":%d,\"deg\":[", n, m, tau, nT, (int)truncated, novert);
        for (int v = 0; v < n; v++) printf("%s%d", v ? "," : "", deg[v]);
        printf("],\"p2tot\":["); for (int k = 0; k < 12; k++) printf("%s%ld", k ? "," : "", p2tot[k]);
        printf("],\"p2fail\":["); for (int k = 0; k < 12; k++) printf("%s%ld", k ? "," : "", p2fail[k]);
        printf("],\"pp_all\":%ld,\"pp_all_cov\":%ld,\"pp_good\":%ld,\"pp_good_cov\":%ld", pp_all, pp_all_cov, pp_good, pp_good_cov);
        printf(",\"ntrip\":%ld,\"ncov\":%ld,\"nlin\":%ld,\"nadm\":%ld,\"nadm_unc\":%ld,\"adm_R2\":%ld,\"adm_R2_unc\":%ld,\"adm_R1\":%ld,\"adm_R1_unc\":%ld", ntrip, ncov, nlin, nadm, nadm_unc, adm_R2, adm_R2_unc, adm_R1, adm_R1_unc);
        printf(",\"unc_total\":%ld,\"unc_combo\":[", unc_total); for (int k = 0; k < 8; k++) printf("%s%ld", k ? "," : "", unc_combo[k]);
        printf("],\"unc_P_size\":{"); bool fs = true; for (int k = 0; k < 40; k++) if (unc_P_size[k]) { printf("%s\"%d\":%ld", fs ? "" : ",", k, unc_P_size[k]); fs = false; }
        printf("},\"unc_P_only_size\":{"); fs = true; for (int k = 0; k < 40; k++) if (unc_P_only_size[k]) { printf("%s\"%d\":%ld", fs ? "" : ",", k, unc_P_only_size[k]); fs = false; }
        printf("},\"uncA\":%ld,\"uncBonly\":%ld,\"uncA_size\":{", uncA, uncBonly); fs = true; for (int k = 0; k < 40; k++) if (uncA_size[k]) { printf("%s\"%d\":%ld", fs ? "" : ",", k, uncA_size[k]); fs = false; }
        printf("},\"uncB_size\":{"); fs = true; for (int k = 0; k < 40; k++) if (uncB_size[k]) { printf("%s\"%d\":%ld", fs ? "" : ",", k, uncB_size[k]); fs = false; }
        printf("},\"nonadm_total\":%ld,\"nonadm_L\":%ld,\"nonadm_P\":%ld,\"adm_unc_sample\":[", nonadm_total, nonadm_L, nonadm_P);
        for (size_t i = 0; i < adm_unc_list.size(); i++) { printf("%s[", i ? "," : ""); for (int k = 0; k < 6; k++) printf("%s%d", k ? "," : "", adm_unc_list[i][k]); printf("]"); }
        printf("]}\n"); fflush(stdout);
        for (int i = 0; i < m; i++) tab[code(ev[i][0], ev[i][1], ev[i][2])] = false;
    }
}
