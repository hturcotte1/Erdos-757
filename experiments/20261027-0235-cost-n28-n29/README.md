# Cost estimate for extending the I11 window-cell induction to n = 28, 29 and for the record cell (25,23,11)

Date 2026-10-27 (UTC 02:40-03:25). Question: what would it cost (compute) to run the exact I11 induction of L013/L016 (class C, engine `ext_d`, streamed driver) for n = 28 and n = 29 (consequence f(29) = 17: no 29-point record), and to decide the record cell (25,23,11) with Delta <= 4? Tags: arithmetic [derived-here]; class counts of cells that exist or were computed here [verified-here] (computations, not refereed, the concurrent worker's lists agree on the 3 cells both computed); every cost / class-count estimate for cells NOT computed [heuristic].

## Method and commands (all under `nice -n 10`, one process, `timeout`)
- `arith_base.py` = `experiments/20261017-1720-i11-n26/arith.py` run for n = 28, 29 (`python3 arith_base.py`, output `arith_output.txt`, `arith_results_n28_29.json`).
- `plan2.py` (copy of the n=27 `plan.py`, generalised; uses `engine.decompositions` unchanged and the seeded cell directory `../20261017-2150-i11-n27/out/cells`, read only) builds the full recursion DAG of every target (`python3 plan2.py n28|n29full|n29rec|rec25`, outputs `plan_*_out.txt`, `plan_*.json`). `dag.py` prints branches and input counts with unknown components (`dag_*.txt`).
- `driver.py` (bottom-up, exact, budget 1080 s, 120 s per cell) computed the cheap missing cells with the real engine (`run_cell.py`); the heavy engine was run for about 15 min in total plus 280 s for a fast-binary probe of cell(16,12,6,3) (budget 20 min respected). The machine was shared with other agents (load 9-11 on 4 cores), so timeouts are pessimistic.
- `harvest.py` collects class counts / inputs / ext_d nodes / seconds from all INFO lines (271 lists: the n=27 folder, this folder, and `../20261027-0300-tight-cells-d4/out/cells`, a concurrent worker, read only). `model.py` = cost model; `tables.py`, `branches.py`, `existing.py` write `cells_table.tsv`, `branches.txt`, `existing_cells_used.tsv`; `backtest.txt` = backtest of the node-count cost model.

## (1) Arithmetic for n = 28 and 29 [derived-here] (window 1 <= tau <= m <= n-2, connected n <= 2m+1, K8, slack < 0; dmax = floor((s+8)/2); counting 3m <= dmax*n)
| n | cell (n,m,tau) | slack | dmax | status |
|---|---|---|---|---|
| 28 | (28,16,11) | -5 | 1 | excluded (counting) |
| 28 | (28,17,11) | -3 | 2 | OPEN, Delta<=2 |
| 28 | (28,18,11) | -1 | 3 | OPEN, Delta<=3 |
| 28 | (28,22,12) | -4 | 2 | excluded (counting 66>56) |
| 28 | (28,23,12) | -2 | 3 | OPEN, Delta<=3 |
| 29 | (29,14,11) -6, (29,20,12) -5, (29,21,12) -3, (29,26,13) -4 | | 1,1,2,2 | excluded (counting) |
| 29 | (29,15,11) | -4 | 2 | OPEN |
| 29 | (29,16,11) | -2 | 3 | OPEN |
| 29 | (29,22,12) | -1 | 3 | OPEN |
| 29 | (29,27,13) | -2 | 3 | OPEN: the only cell with h <= 16 (tau >= 13: m=26 is excluded, m=27 open), 81 <= 3*29=87 |

So I11 at n=28 = 3 open cells; the record claim at n=29 needs I11 for n<=28 plus the single cell (29,27,13,3); full I11 at n=29 adds only (29,15,11,2), (29,16,11,3), (29,22,12,3) (all three cost ~0, see below). Branches (d, tau', S') of every top cell and the decompositions are in `branches.txt`; summary:
- (28,17,11,2): d=2, tau'=10, remainder (27,15) slack 1; 16 decompositions, 1 input (needs new cell (27,15,10,2) ~ empty).
- (28,18,11,3): d=2, tau'=10, (27,16) slack 3 (47 decs, ~3 inputs; new (27,16,10,2), (24,15,9,2)); d=3, tau'=10, (27,15) slack 1 (16 decs, 176 inputs, dominated by 5x(3,1,1)+(12,10,5,3) = 149; new (27,15,10,3)).
- (28,23,12,3): d=3, tau'=11, (27,20) slack 0 (6 decs, 33 inputs; new (27,20,11,3), which needs new (26,17,10,3)).
- (29,27,13,3): d=3, tau'=12, (28,24) slack 0, 3 decompositions: 2x(14,12,6,3) [old, 2 classes -> 3 inputs], (3,1,1)+(25,23,11,3) [NEW, tight Delta<=3 version of the 25-point record cell], (28,24,12,3) [NEW tight cell]; ~6 inputs + those classes.
- (29,15,11,2): d=2, (28,13) slack 0, 0 inputs; (29,16,11,3): d=2 (28,14) s2, d=3 (28,13) s0, ~5 inputs; (29,22,12,3): d=3, (28,19) s1, 974 inputs (components all old).
The (28,24,12,3) cell (slack 0) needs d=3, tau'=11, (27,21) slack 2: 11 decs, ~22k inputs + the classes of (21,19,9,3), (24,20,10,3), (27,21,11,3).

## (2) The record cell (25,23,11) with Delta <= 4 [derived-here]
For H with (n,m,tau)=(25,23,11), deleting a vertex of degree d: tau'=10 (tau'=11 has S'=-3-2d<0), slack(H-v)=8-2d >= 0 so d<=4; counting 3m=69<=3*25 allows Delta=3 or 4; d ranges over ceil(69/25)=3..4. Branches: **d=3**: remainder (24,20,10), slack 2, 4 decompositions, ~1.7e4 inputs (11,175 = 2x(12,10,5,3)=149 classes each; 3000 est. for (3,1,1)+(21,19,9,3); ~2.7e3 est. for (24,20,10,3)); **d=4**: remainder (24,19,10), slack 0, 3 decompositions, ~67 inputs: (10,7,4,3)x(14,12,6,3)-type products 55 (old counts 5 and 11 at Delta<=4), (3,1,1)+(21,18,9,4) = 12 (computed: 12 classes), (24,19,10,4) = 0 classes (computed by the concurrent worker; my own run timed out at 120 s under load). Existing (old) components: (12,10,5,3), (14,12,6,3/4), (10,7,4,3/4), (13,10,5,3) etc. (full list `existing_cells_used.tsv`, 192 cells, 178 old). New component cells: chain (13,11,5,3)=65,771 [computed here, = d4 worker], (16,12,6,3) [probe: 6163 inputs, 2.56e7 ext_d nodes (only 4.2e3/input) but 8.36e6 hits_in_C, filt/canon did not finish in the 280 s probe, so est. classes ~1e5-2e5], (17,15,7,3), (18,10,6,3) (direct, `enum_conn`, >120 s under load, est. 5e3 classes), (19,13,7,3), (20,16,8,3), (22,14,8,3), (23,17,9,3), (21,19,9,3), (24,20,10,3), D=4 side cells (21,18,9,4)=12, (23,15,9,4)=0, (20,14,8,4)=0, (22,11,8,4)=0, (24,19,10,4)=0, (17,13,7,4)=10 (all small, computed). The Delta<=4 lists are larger than Delta<=3 (L012: cell(22,17,9,4) = 95 vs 37) but here the d=4 branch has slack 0 and is tiny; the cost is the d=3 chain. After the lists: for non-empty cell(25,23,11,4) each class needs the L012 realization test (`realize`, injective midpoint maps), est. tens of classes (est. 8) if the pattern of (23,21,10,4)=699 [d4 worker] does not repeat; this is cheap.

## (3) Cost estimates [heuristic]
Model: classes(cell) = inputs x yield(n,s,D) (log-linear fit on 27 recursed Delta<=3 cells, rms 0.92 in ln, i.e. factor 2.5; Delta=4 yield x3, Delta=2 capped); cost = inputs x nodes/input / rate x 1.2 with nodes/input = 300 / 1e4 / 3e4 for Delta = 2/3/4 (measured range 4e2-1e5; the L016 value 1.1e4 for cell(25,19,10,3)), rate 1e6 nodes/s/core (central, high) or 3e6 (low: `ext_d_fast` on an idle core: L016 measured 3.2e6 for cell(25,19,10,3) with 3 procs); D=2 cells 0.05 s per input. Overrides by interpolation on the saturated chain m=n-2 (counts 65,771 (13), 949,522 (15), ? (17), 29,898 (19), ? (21), 0 (23)): (17,15,7,3)=2e5, (21,19,9,3)=3e3, (25,23,11,3)=2 classes. Scenarios: low = yield/2.7, nodes/3, rate 3e6; high = yield x2.7, nodes x3, rate 1e6 (the factors compound over the 6-level chain). Backtest (`backtest.txt`): central cost within 0.3-1.2x for 5 of 9 heavy cells, 3-24x too high for the saturated dense ones ((19,17,8,3), (22,18,9,3), (23,21,10,3)), 3x too low for the hit-heavy (24,16,9,3). The filt/canon time on hit-heavy low-n cells is not separated in the model (cell(16,12,6,3): 8.4M hits for 6163 inputs).

| target | new cells (estimated) | core-hours low | central | high |
|---|---|---|---|---|
| n = 28 (3 open cells) | 11 | 0.03 | 0.08 | 0.2 |
| n = 29 record (cell (29,27,13,3) only, given n=28) | 16 | 0.9 | 9.9 | 89 |
| n = 29 full I11 (4 open cells) | 25 | 0.9 | 10.0 | 89 |
| record cell (25,23,11,4) | 10 | 0.75 | 6.9 | 60 |
| union n28 + n29 record + (25,23,11,4) (shared chain counted once) | 36 | 0.95 | 10.1 | 90 |
Biggest items (central, core-h): (27,21,11,3) 1.7, (24,20,10,3) 1.6, (21,19,9,3) 1.3, (26,18,10,3) 1.3, (23,17,9,3) 1.2, (20,16,8,3) 1.1, (17,15,7,3) 0.9, (18,10,6,3) 0.4 (direct), (25,23,11,4) 0.2; all others < 0.1. Not counted: the 15 min of exact work done here (all cells with fewer inputs), driver overhead, streaming/chunking, the prover's and referees' recomputation (each referee recomputes the chain: roughly the same compute again).
4 cores x 36 h = 144 core-h (3 cores: 108 core-h): all three targets fit even in the high scenario (90 core-h), with little slack for referee recomputation; central needs about 3.4 wall-hours on 3 cores.

## Recommendation
1. Order: (a) n = 28 first (about 5-10 minutes of compute beyond the lists already computed; no new mathematics, but it unlocks n = 29); (b) in the same run the shared dense chain (16,12,6,3) -> (17,15,7,3) -> (18,10,6,3) -> (19,13,7,3) -> (20,16,8,3) -> (22,14,8,3) -> (23,17,9,3) -> (21,19,9,3) -> (24,20,10,3), then the D=4 side cells, then (25,23,11,4) (record cell decided at that point: expected a handful of classes to realization-test) and (25,23,11,3); (c) then (26,18,10,3) -> (27,21,11,3) -> (28,24,12,3) -> (29,27,13,3). So the record cell and n = 29 are one computation (the record cell is a by-product of the n=29 chain; n = 29 only adds three cells, ~2 core-h central).
2. Affordable: all three, in 36 h on 3 cores (central ~10 core-h; high ~90 core-h still fits). Use the streamed chunked driver of L014/L016 (several chains have 3e5-5e5 inputs and 1e5-2e5 classes; 15 GB RAM suffices; the non-streamed `engine.py` held 8.4M hits in memory in the probe).
3. Risks: (i) class counts of (16,12,6,3), (17,15,7,3), (20,16,8,3), (23,17,9,3), (26,18,10,3) are extrapolated (could be 3-10x larger; the cost scales with them and compounds along the chain: high scenario 90 core-h); (ii) the hit-processing (filt/canon) of high-yield cells is under-modelled; (iii) a new engine pitfall at n = 28, 29: MAXP 640 is enough (P <= C(28,2)=378), Lemma E' needs n <= 31 (OK); (iv) non-emptiness of a tight cell ((25,23,11,3/4), (28,24,12,3)) would require extra realization work; (v) the refereeing of a new certificate (L017-type) costs more wall time than the computation; (vi) the concurrent worker `experiments/20261027-0300-tight-cells-d4` is already computing overlapping cells (its 24 new lists agree with mine on (13,11,5,3), (12,8,4,3), (15,9,5,3)); coordinate to avoid duplicate work.

## Caveats
Only 15 min of heavy engine here, on a loaded machine; the class-count extrapolation is the weak point; no claim about the mathematical outcome (emptiness of cells) is made, only about cost.
