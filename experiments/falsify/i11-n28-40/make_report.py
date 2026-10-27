import json, glob, gzip, collections, os, re
R = json.load(open('results.json'))
low = [json.loads(l) for l in gzip.open('low_graphs.jsonl.gz', 'rt')]
conn = [d for d in low if d['connected']]
S2 = json.load(open('out/structure2.json')) if os.path.exists('out/structure2.json') else []
val = json.load(open('out/validate_tau.json')) if os.path.exists('out/validate_tau.json') else None
rr = json.load(open('out/realize_rand.json')) if os.path.exists('out/realize_rand.json') else {}
# per-n minimum CONNECTED slack by method
best = collections.defaultdict(dict)
def upd(n, meth, s):
    if s is None: return
    if meth not in best[n] or s < best[n][meth]: best[n][meth] = s
for n, s in R['glue']['min_connected_slack_by_n'].items(): upd(int(n), 'gluing', s)
for n, s in R['extend_min_slack_by_n'].items(): upd(int(n), 'glue+1edge', s)
for run, d in R['beam'].items():
    if run.startswith('mut') or run.startswith('t3'): continue
    for n, v in d.items(): upd(int(n), 'beam', v['min_connected_slack'])
for d in conn: upd(d['n'], 'beam', d['slack'])
for x in R['subsa']:
    if x['best_slack'] < 9999: upd(x['size'], 'subset-SA', x['best_slack'])
for x in R['sa_polish']: upd(x['n'], 'SA-polish', x.get('best_slack'))
for x in (R['sa_cells'] if isinstance(R['sa_cells'], list) else []): upd(x['n'], 'SA-cells', x['best_slack'])
for k, d in R.get('real', {}).items():
    for n, s in d['best_slack_by_n'].items(): upd(int(n), 'real-walk', s)
for n in range(28, 41):
    for K in (1, 4, 10):
        g = R['growth'].get('%d_K%d' % (n, K))
        if g: upd(n, 'growth', g['minslack'])
out = []
P = out.append
P("FALSIFIER: HOLDS-ON-DATA\n")
P("# Falsification of I11 (11 tau <= 3n + 2m) on the class C, n = 28..40\n")
P("Tags: [verified-here] = computation in this folder; NONE-FOUND is evidence, not proof.  Notation: slack = 3n + 2m - 11 tau; I11 <=> slack >= 0.  All arithmetic is integer (exact tau by a frontier DP; every tau validated, see section 6).\n")
P("## 0. Statement tested and verdict\n")
P("Statement: for every linear, F7-free 3-uniform hypergraph H on n vertices with e(S) <= |S| - 2 for all vertex subsets S (|S| >= 2), 11 tau(H) <= 3n + 2m (class C), here at n = 28..40 where I11 is not proved (it is proved on C for n <= 27: L007-L016).\n")
P("**Verdict: no counterexample found.  Minimum slack over all searches, restricted to CONNECTED graphs (a violator can be taken connected, slack is additive over components): see the table in section 3; no graph with slack < 0 was produced by any method (every run prints '!!! NEGATIVE SLACK' on a hit; none occurred in the production runs).  Disconnected graphs reach slack 0 trivially (disjoint unions of the tight pieces), which says nothing.**\n")
P("Class membership is tested by (i) linearity, (ii) max degree cap (3 for the minimal-counterexample runs; 4-5 in the runs that allow A_base-type pieces), (iii) F7 as a subhypergraph (vertex v with three edges and two disjoint edges taking one vertex of each pair), (iv) the Hall form of e(S) <= |S|-2: for every pair {x,y} of vertices the edges have an SDR avoiding x,y (incremental: when an edge is added to a graph in C only the 3 pairs inside the new edge need testing; proof in i11core.h comments / section 6).\n")
P("## 1. Tools (all in this folder)\n")
P("`i11core.h` (class C test, tau DP), `i11.c` (modes selftest / eval / extend / grow / anneal / subsa), `vext.c` (exact vertex-extension operator: all ways to add one vertex with 1..4 disjoint pairs so that tau rises by 1, i.e. the pairs hit every maximum independent set), `beam.py beam2.py beam3.py beam4.py beam5.py` (beam search over vext), `glue.py glue_exh.py pieces.py` (gluings), `real.py realize_rand.py` (realizable sets), `run_grow*.sh run_sa.py run_sa2.py run_subsa.py`, `classify_low.py structure.py structure2.py aggregate.py make_report.py`.  Raw outputs in `out/`, machine-readable summary `results.json`, slack<=1 graphs in `low_graphs.jsonl.gz` (fields: slack, n, m, tau, connected, components (n,m,tau,slack), wl_hash (colour-refinement hash used with an exact networkx isomorphism test for dedup), edges).\n")
P("## 2. Tests, ranges and counts\n")
tot_g = R['growth_samples_K1_total']
P("| # | method | range | objects | min slack (connected) |\n|---|---|---|---|---|")
P("| A | random edge-by-edge growth in C (each new edge adds 0/1/2 new vertices, degree <= 3, incremental class test), K=1 | n=28..40, m=ceil((n-1)/2)..n-2 | %d valid graphs (200,000 attempts per n) | %d |" % (tot_g, min(R['growth']['%d_K1' % n]['minslack'] for n in range(28, 41))))
k4 = sum(R['growth']['%d_K4' % n]['ok'] for n in range(28, 41)); k10 = sum(R['growth']['%d_K10' % n]['ok'] for n in range(28, 41))
P("| A' | same, greedy: best of K=4 / K=10 random candidate edges by exact tau at every step | n=28..40 | %d (K=4) + %d (K=10) | %d |" % (k4, k10, min(min(R['growth']['%d_K%d' % (n, K)]['minslack'] for n in range(28, 41)) for K in (4, 10))))
gt = R['glue']
P("| B | random gluings of 2-4 tight pieces / A_base / 2,910 saturated 14-point classes / records, identifying 1-3 vertices per added copy (pieces: the 16 connected induced subgraphs with slack <= 1 of the record sets, see pieces.json) | n=20..56 | %d graphs generated (%d generated in n=28..40), all re-checked in C | %s |" % (gt['total_generated'], sum(v['generated'] for n, v in gt['per_n'].items() if 28 <= int(n) <= 40), min(v for n, v in gt['min_connected_slack_by_n'].items() if 28 <= int(n) <= 40)))
ge = R['glue_exhaustive']
P("| B' | exhaustive 1- and 2-vertex identifications of A_base with itself and with each of the 16 tight pieces | n=15..27 | %d graphs | 5 (A_base+A_base: 8 for 1 vertex, 16 for 2 vertices) |" % sum(sum(x['count'] for x in v.values()) for v in ge.values()))
P("| C | all single-edge extensions (0, 1 or 2 new vertices) of 2,385 low-slack gluing results | n=20..41 | %s | %d |" % (R['extend_summary'].split('extensions=')[1] + " extensions", min(v for n, v in R['extend_min_slack_by_n'].items() if 28 <= int(n) <= 40)))
P("| D | beam search over exact tau-raising vertex extensions (vext), degree cap 3 and 5, seeds = unions of tight pieces (+ gluing results); parent pools chosen by slack | n=3..40 (see section 4 for the reached depth) | see section 4 | see section 3 |")
sm = [x for x in R['subsa'] if x['best_slack'] < 9999]
P("| E | simulated annealing over induced vertex subsets of size 28..40 of the (4,5)-set hypergraphs S_3..S_8 (reader family), C003, C004, C005 and A+A+12 (disjoint union), connected subsets only | sizes 28..40 | %d runs x 150,000 SA steps (each step an exact tau) | %d |" % (len(R['subsa']), min(x['best_slack'] for x in sm)))
sc = R['sa_cells'] if isinstance(R['sa_cells'], list) else []
P("| F | SA over edge moves per window cell (n,m) (class C kept incrementally, connected, objective 11 tau - 2m - lambda log #max independent sets) | n=28..29 only (5 cells, killed to free CPU) + n=14 calibration | 5 cells x 350,000 moves | 9 (n=28), 16 (n=29): much weaker than B/D |")
sp = R['sa_polish']
P("| G | SA polishing of the best gluing graphs (m within +-2, degree cap 5) | n=28..32 | %d runs x 700,000 moves | no improvement over the start (%s) |" % (len(sp), ", ".join("%d:%d" % (x['n'], x['best_slack']) for x in sp[:6])))
rl = R.get('real', {}).get('real_main.json', {})
P("| H | realizable (4,5)-sets: random/greedy one-point extensions (new point in a new 3-AP, (4,5) verified exactly, tau exact) of generic-scale gluings of the records and of sub-selections of S_2..S_5 | n=23..40 | %s walks, %s steps | %d |" % (rl.get('iterations'), rl.get('steps'), min(rl['best_slack_by_n'].values()) if rl else -1))
P("| I | random saturated C-graphs (m=n-2) from growth with a random midpoint assignment, solved exactly (e757.saturated) and checked as (4,5)-sets | n=10,12,14,16,20 | 4,000 each | realized: %s |" % ", ".join("n=%s: %d" % (n, v['realized']) for n, v in rr.items()))
P("")
P("## 3. Minimum slack of CONNECTED graphs found, by n and method\n")
meths = ['growth', 'gluing', 'glue+1edge', 'beam', 'subset-SA', 'SA-cells', 'SA-polish', 'real-walk']
P("| n | " + " | ".join(meths) + " | overall min |\n|" + "---|" * (len(meths) + 2))
for n in range(14, 41):
    row = [str(best[n].get(m, '')) for m in meths]
    vals = [best[n][m] for m in meths if m in best[n]]
    P("| %d | %s | %s |" % (n, " | ".join(row), min(vals) if vals else ''))
P("\n(the beam column also includes the slack<=1 connected graphs of section 5; for n < 28 the table is shown for context; blank = no connected graph found by that method.)\n")
P("## 4. Beam search (exact vertex extension) details\n")
P("Operator: given a parent graph G in C and the set of all its maximum independent sets, `vext` enumerates every set of d <= 4 disjoint pairs {a_i,b_i} (degrees < cap) such that every maximum independent set contains some pair; adding a new vertex v with edges {v,a_i,b_i} then raises tau by exactly 1 (tau(G+v) = tau(G)+1) and changes the slack by 2d - 8 (d=1: -6, d=2: -4, d=3: -2, d=4: 0).  Non-raising additions change the slack by 2d+3 > 0 and are not generated.  Children are tested for class C and for tau by the DP.  Pools per n are kept (dedupe by colour-refinement fingerprint); parents are drawn from graphs with slack <= 7 (connected) and slack <= 1 (disconnected unions of tight pieces).\n")
P("Runs (log files out/beam_*.log, stats out/beam_*_stats.json): d3a-d3c (degree cap 3), d5a-d5e (cap 5, pieces+gluing seeds), d5f-d5i (cap 5, d up to 4, extra connected pieces).  Per-level lines show parents / children / pool size / minimum slack.  Runs d5f/d5g/d5h were stopped when the time limit per level made them too slow; d5i is the one reported for depth.\n")
for run in ['d5b', 'd5e', 'd5i']:
    if run in R['beam']:
        P("%s: min connected slack per n: %s" % (run, ", ".join("%s:%s" % (n, v['min_connected_slack']) for n, v in R['beam'][run].items() if int(n) >= 20)))
P("")
P("Power check (mutation tests, out/beam_mutH.log, beam_mutF.log): with the Hall condition switched off the same beam immediately returns the known (9,8,4) slack -1 graph (and (12,9,5) slack -1); with the F7 test switched off it returns F7 itself (7,5,3, slack -2) and its extensions (10,6,4), (13,7,5).  So the search machinery does detect violations of I11 when the hypotheses of C are weakened.\n")
P("## 5. Slack-0 and slack-1 graphs at n >= 15 (connected)\n")
P("`low_graphs.jsonl.gz` holds every graph with slack <= 1 found by any method (%d graphs up to isomorphism-hash+exact isomorphism, n >= 15; %d connected)." % (len(low), len(conn)))
c = collections.Counter((d['slack'], d['n'], d['m'], d['tau']) for d in conn)
P("\nConnected graphs with slack <= 1 (slack, n, m, tau): number of non-isomorphic classes found\n")
P("| slack | n | m | tau | classes found |\n|---|---|---|---|---|")
for k in sorted(c, key=lambda k: (k[1], k[0])): P("| %d | %d | %d | %d | %d |" % (k[0], k[1], k[2], k[3], c[k]))
P("\nHub decomposition (structure2.py; up to 25 sampled classes per cell): the smallest vertex set H whose deletion leaves only components with slack <= 1, and the types of those components (n,m,tau,slack):\n")
for key, found, v in sorted(S2, key=lambda x: (x[0][0], x[0][2])):
    P("- %d classes, cell (n,m,slack) = %s: %s" % (v, tuple(key), "hub set size %d with degrees %s, components %s" % (found[0], found[1], [tuple(x) for x in found[2]]) if found else "no decomposition with |H|<=4"))
P("\nReading: every connected slack<=1 graph found at n >= 15 is assembled from the tight pieces AP (3,1,1;0), C8 (8,5,3;1), C10 (10,7,4;0), C12 (12,10,5;1), A_base-type (14,12,6;0) and previously found connected pieces ((15,11,6;1), (17,13,7;0), (19,16,8;1), ...) by ONE hub vertex whose d edges raise tau by 1 (slack = sum of component slacks + 2d - 8).  Hubs of degree 4 leave the slack unchanged; hubs of degree 3 lower it by 2 and are only possible when the components carry slack >= 2 in total (e.g. two C8's: 1+1-2 = 0 gives (17,13,7)).  This is the 'tight gluing' mechanism a violator would need (two hubs of degree 3 on pieces of total slack <= 3), and the exact enumeration finds no such configuration; compare L009 (n=18) where the cell (18,16,8) = two C8 + two hubs is proved empty.\n")
P("## 6. Validation\n")
P("- tau DP vs brute force over all 2^n subsets: 874 random class-C graphs with n=6..20, 0 mismatches (`./i11 selftest`).")
P("- class test (fast, incremental) vs an independent slow test (all subsets for e(S) <= |S|-2, all 5-edge subsets for F7): 30,000 random edge sets on 8..15 vertices (3,346 in C), 0 mismatches; incremental try_add vs full check: 43,588 trials, 0 mismatches.")
if val: P("- at n=28..40: tau of %d graphs (gluing and beam pools) recomputed with OR-tools CP-SAT (%d not proved optimal within 30 s, values still equal), class membership of %d of them recomputed independently in Python (networkx bipartite matching for every pair, direct F7 search): %d mismatches." % (val['graphs'], val['cpsat_not_optimal'], val['class_checked'], val['mismatches']))
P("- the equality graph A_base (14,12,6) and slack 0 at (3,1,1), (10,7,4), (13,8,5) are recovered; SA at n=14 finds slack 0.\n")
P("## 7. Honest scope and limits\n")
P("- This is NONE-FOUND evidence, not a proof.  The searches are heuristic except the single-edge and single-vertex extension operators (exhaustive for their parent sets) and the exhaustive 1-/2-vertex identifications.")
P("- Annealing from scratch (F) is far weaker than the constructive methods: it reaches slack 9-18 at n=28-29 where gluing reaches 2-3; so the 'high-tau local search' evidence is weak.  The beam and gluing evidence concerns graphs built from the known tight pieces and their hub compositions, which is exactly where equality-type structures live.")
P("- Realizability was not used as a filter: all searches are in the abstract class C.  Section 2 row I shows that many random saturated C-graphs do realize at small n (so realizability is not a rare obstruction there), but no violating abstract graph appeared, so no realization was needed.")
P("- Degree: runs with cap 3 (minimal-counterexample reduction) and cap 5 (allows A_base) were both made; the cap-3 runs hardly produce connected low-slack graphs (all 2,910 tight 14-point classes have a vertex of degree >= 4), which is why most beam evidence comes from the cap-5 runs.")
open('REPORT.md', 'w').write("\n".join(out) + "\n")
print("REPORT.md written", len(out))
