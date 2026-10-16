"""Regression test for experiments/20261016-0840-extremal-subsets: (a) the bitmask routine agrees with e757.core.alpha
(brute force over deletions) on stored classes; (b) a few stored summary numbers are re-derived by recomputation."""
import gzip, importlib.util, json, os

from e757 import core

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
EXP = os.path.join(ROOT, 'experiments', '20261016-0840-extremal-subsets')


def _stats():
    spec = importlib.util.spec_from_file_location('extremal_subsets_stats', os.path.join(EXP, 'stats.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _load(rel):
    d = json.load(gzip.open(os.path.join(ROOT, rel)))
    return d if isinstance(d, list) else d['real']


def test_agrees_with_core_alpha():
    import itertools
    S = _stats()
    recs = _load('experiments/20261014-1430-small-counts/results/n10_m8_real.json.gz')[:6] + \
        _load('experiments/20261014-1005-census-dfs/results/realized_n12.json.gz')[:3]
    for r in recs:
        s = sorted(r['set']); n = len(s)
        pairs, singles = S.analyse(s)
        bp = [(i, j) for i, j in itertools.combinations(range(n), 2)
              if core.alpha([v for k, v in enumerate(s) if k not in (i, j)]) == S.F[n - 2]]
        bs = [i for i in range(n) if core.alpha([v for k, v in enumerate(s) if k != i]) == S.F[n - 1]]
        assert pairs == bp and singles == bs


def test_stored_numbers_recomputed():
    S = _stats()
    res = json.load(open(os.path.join(EXP, 'results.json')))['per_source']
    for key, rel in [('n8_m6', 'n8_m6_real.json.gz'), ('n9_m7', 'n9_m7_real.json.gz'), ('n7_m5', 'n7_m5_real.json.gz')]:
        recs = _load('experiments/20261014-1430-small-counts/results/' + rel)
        out = [S.analyse(r['set']) for r in recs]
        assert len(out) == res[key]['classes']
        assert sum(1 for p, s in out if p) == res[key]['with_ext_n2']
        assert sum(1 for p, s in out if s) == res[key]['with_ext_n1']
    recs = _load('experiments/20261014-1005-census-dfs/results/realized_n12.json.gz')[:400]
    out = [S.analyse(r['set']) for r in recs]
    assert all(len(s) == 12 for p, s in out)          # every 1-point deletion extremal at even n (f(11)=f(12))
    assert res['n12_m10']['dist_singles'] == {'12': 54243} and res['n12_m10']['classes'] == 54243
