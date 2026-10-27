// Independent C++ check of L019 computation C8 (Remark 10.3): for every stored graph F of a cell file, enumerate all
// minimum transversals, then all triples of pairwise disjoint pairs not inside an edge of F ("linear triples") that no
// minimum transversal meets; for each, k = number of F-edges meeting W (the six vertices) and tau_loc = transversal
// number of the edges of F+v meeting {v} u W.  Also counts pairs of disjoint non-edge pairs met by no minimum transversal.
// usage: nbhd26 cellfile
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int n, m, t0; vector<array<int,3>> E;
vector<u64> Tmask; // minimum transversals as vertex bitmasks (n <= 63)
void rec(vector<int>& rem, u64 chosen, int k, int t) {
    if (rem.empty()) { if (k == t) Tmask.push_back(chosen); return; }
    if (k >= t) return;
    int e = rem[0];
    for (int i = 0; i < 3; i++) {
        int v = E[e][i];
        vector<int> r2; for (int f : rem) { auto& g = E[f]; if (g[0] != v && g[1] != v && g[2] != v) r2.push_back(f); }
        rec(r2, chosen | (1ULL << v), k + 1, t);
    }
}
bool cover_le(vector<int> rem, int k) {
    if (rem.empty()) return true; if (k == 0) return false;
    int e = rem[0];
    for (int i = 0; i < 3; i++) { int v = E[e][i]; vector<int> r2; for (int f : rem) { auto& g = E[f]; if (g[0] != v && g[1] != v && g[2] != v) r2.push_back(f); } if (cover_le(r2, k - 1)) return true; }
    return false;
}
int tau_of(vector<array<int,3>>& F) { // generic small tau
    function<bool(vector<int>, int)> cl = [&](vector<int> rem, int k) -> bool {
        if (rem.empty()) return true; if (k == 0) return false;
        int e = rem[0];
        for (int i = 0; i < 3; i++) { int v = F[e][i]; vector<int> r2; for (int f : rem) { auto& g = F[f]; if (g[0] != v && g[1] != v && g[2] != v) r2.push_back(f); } if (cl(r2, k - 1)) return true; }
        return false; };
    vector<int> all(F.size()); iota(all.begin(), all.end(), 0);
    int k = 0; while (!cl(all, k)) k++; return k;
}
int main(int argc, char** argv) {
    ifstream in(argv[1]); string line; map<pair<int,int>, long> hist; long uncovered_pp = 0, pp_total = 0, triples = 0, unc = 0; int graphs = 0;
    while (getline(in, line)) {
        istringstream ss(line); if (!(ss >> n >> m >> t0)) continue; E.assign(m, {0,0,0});
        for (int i = 0; i < m; i++) ss >> E[i][0] >> E[i][1] >> E[i][2];
        graphs++;
        // tau check
        vector<int> all(m); iota(all.begin(), all.end(), 0);
        int t = 0; while (!cover_le(all, t)) t++;
        if (t != t0) { printf("TAU MISMATCH graph %d: %d vs %d\n", graphs, t, t0); return 1; }
        Tmask.clear(); rec(all, 0, 0, t);
        sort(Tmask.begin(), Tmask.end()); Tmask.erase(unique(Tmask.begin(), Tmask.end()), Tmask.end());
        int NT = Tmask.size(), W = (NT + 63) / 64;
        // adjacency
        vector<vector<char>> adj(n, vector<char>(n, 0));
        for (auto& e : E) for (int i = 0; i < 3; i++) for (int j = 0; j < 3; j++) if (i != j) adj[e[i]][e[j]] = 1;
        vector<pair<int,int>> pairs; for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if (!adj[a][b]) pairs.push_back({a, b});
        int P = pairs.size();
        vector<vector<u64>> pm(P, vector<u64>(W, 0));
        for (int p = 0; p < P; p++) for (int i = 0; i < NT; i++) if ((Tmask[i] >> pairs[p].first & 1) || (Tmask[i] >> pairs[p].second & 1)) pm[p][i / 64] |= 1ULL << (i % 64);
        vector<u64> m12(W);
        for (int p1 = 0; p1 < P; p1++) for (int p2 = p1 + 1; p2 < P; p2++) {
            auto& a = pairs[p1]; auto& b = pairs[p2];
            if (a.first == b.first || a.first == b.second || a.second == b.first || a.second == b.second) continue;
            pp_total++;
            bool any12 = false; for (int w = 0; w < W; w++) { m12[w] = pm[p1][w] & pm[p2][w]; if (m12[w]) any12 = true; }
            if (!any12) uncovered_pp++;
            for (int p3 = p2 + 1; p3 < P; p3++) {
                auto& c = pairs[p3];
                if (c.first == a.first || c.first == a.second || c.second == a.first || c.second == a.second) continue;
                if (c.first == b.first || c.first == b.second || c.second == b.first || c.second == b.second) continue;
                triples++;
                bool anyc = false; for (int w = 0; w < W; w++) if (m12[w] & pm[p3][w]) { anyc = true; break; }
                if (anyc) continue;
                unc++;
                u64 Wm = (1ULL << a.first) | (1ULL << a.second) | (1ULL << b.first) | (1ULL << b.second) | (1ULL << c.first) | (1ULL << c.second);
                vector<array<int,3>> near; for (auto& e : E) if ((Wm >> e[0] & 1) || (Wm >> e[1] & 1) || (Wm >> e[2] & 1)) near.push_back(e);
                int k = near.size(); int v = n;
                near.push_back({v, a.first, a.second}); near.push_back({v, b.first, b.second}); near.push_back({v, c.first, c.second});
                hist[{k, tau_of(near)}]++;
            }
        }
    }
    printf("%s graphs %d: pairs-of-pairs %ld (uncovered %ld); linear triples %ld, uncoverable %ld; (k,tau_loc):", argv[1], graphs, pp_total, uncovered_pp, triples, unc);
    for (auto& kv : hist) printf(" (%d,%d):%ld", kv.first.first, kv.first.second, kv.second);
    printf("\n");
}
