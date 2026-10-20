#!/usr/bin/env python3
"""Literal 4-subset test (>= 5 distinct positive differences) for K = 9..12 (page: 119 points, 7.9M 4-sets)."""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_family import four_subset_test
from census_deep import build
out = {}
for K in (9, 10, 11, 12):
    A = build(K); t = time.time()
    ok, cnt, mn = four_subset_test(A)
    out[K] = dict(n=len(A), ok=ok, n_4subsets=cnt, min_distinct_diffs=mn, sec=round(time.time() - t, 1))
    print(K, out[K], flush=True)
Path(__file__).with_name("literal_big_results.json").write_text(json.dumps(out, indent=1))
