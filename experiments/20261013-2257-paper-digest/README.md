# Paper digest (2026-10-13)
Question: digest Gyarfas-Lehel 1995 and Henning-Yeo (2017 EJC, 2018 arXiv) for the lower-bound track; try to obtain Henning-Yeo 2021.
Method: `pdftotext -layout` for the two Henning-Yeo PDFs (text files here). The Gyarfas-Lehel PDF is a scan without text layer; pages rendered with `pdftoppm -r 130 -png` and read visually (PNGs deleted afterwards, regenerate with that command).
Scripts: chk_fibonacci_F7_AG.py (Fibonacci sets are (4,5), tau=floor(2(n-1)/5), F7/F8/AG(2,3) tau and HY slack), chk_L13_L8.py (L(8)=F8, L(13) linear F7-free tau=6), hy_tight_search.py (random search for small HY slack, heuristic). Run with `python3 <script>` from repo root.
Results: see kb/notes/gyarfas_lehel_1995.md, kb/notes/henning_yeo_2021_affine.md. HY 2021 full text NOT obtainable (closed access).

## Exact commands
From the repo root (all three scripts are small and deterministic, no randomness except `hy_tight_search.py`, which draws random hypergraphs):
`python3 experiments/20261013-2257-paper-digest/chk_fibonacci_F7_AG.py`, `python3 experiments/20261013-2257-paper-digest/chk_L13_L8.py`,
`python3 experiments/20261013-2257-paper-digest/hy_tight_search.py` (random search, output not stored in the folder).
Text extraction: `pdftotext -layout <pdf> <txt>` gave `henning_yeo_1802.01825.txt`, `henning_yeo_ejc_2017.txt` and `mt.txt` (Ma-Tang).

## Results (re-run on 2026-10-15 for this README; outputs reproduced from the scripts)
- `chk_fibonacci_F7_AG.py` [verified-here]: for n = 4..14 the set {2,3,5,8,...} (n terms, from F_3) is a (4,5)-set (`is_45_set` True; n = 15 not tested, printed None),
  with h = 3,4,4,5,6,6,7,7,8,9,9 for n = 4..14 (h = 10 at n = 15), tau = floor(2(n-1)/5) for every n = 4..15 (equal to the printed "GL tau formula"),
  and n-3 3-APs (1, 2, ..., 12 edges for n = 4..15). `is_45_set([1,2,3,5])` is False and `is_45_set([2,3,5,8])` is True (the caveat in kb/00_START_HERE.md section 6).
  Henning-Yeo slack check: AG(2,3) has 12 lines (n = 9, m = 12, tau = 5: 17*5 = 85 > 5n+3m = 81); AG(2,3) minus a point (n = 8, m = 8, tau = 4: 68 > 64);
  F7 (n = 7, m = 5, tau = 3: 51 > 50). So the three configurations violate 17 tau <= 5n+3m, which is why F7-freeness is a hypothesis of the theorem
  (F7 and F8 have 4 tau = n+m = 12 and 16, AG(2,3) has 4 tau = 20 < n+m = 21; the script prints these values).
- `chk_L13_L8.py` [verified-here]: the cyclic hypergraph with edges {i, i+1, i+3} mod n is linear with tau = 4 for n = 8 and tau = 6 for n = 13;
  L(8) is isomorphic to AG(2,3) minus a point (F8) and contains F7; L(13) contains no F7.
- `hy_tight_search.py` [heuristic]: random search for small Henning-Yeo slack; no output is stored, so no number can be quoted from this folder.
- The digests of the papers are in kb/notes/gyarfas_lehel_1995.md, kb/notes/henning_yeo_2021_affine.md, kb/notes/henning_yeo_transversals.md and
  kb/notes/ma_tang_2026.md. Henning-Yeo 2021 (Graphs Combin. 37) could not be obtained (closed access); only the 2017 EJC paper and the 2018 arXiv version are on disk.

## Conclusion
Reading and sanity-check folder: it feeds K7-K10 and K21 (published facts, recorded with the test cases `test_fibonacci_caveat`, `test_f7_not_realizable`) and
the Fibonacci / F7 / AG(2,3) facts quoted in kb/00_START_HERE.md. It produced no new result. Tags: the script outputs above are [verified-here]; the
paper content itself is [published] (via kb/notes digests); `hy_tight_search.py` is [heuristic].
