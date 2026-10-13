import json
import random
from pathlib import Path

from e757.anneal import (FastEval, evaluate, extend_map, is45_ints, is_linear_map, map_from_set,
                         propose, random_linear_map, solve_exact)
from e757.core import is_45_set

SETS = json.load(open(Path(__file__).resolve().parent.parent / "data" / "small_records.json"))["sets"]


def test_base_map_alpha8():
    m = map_from_set(SETS["14"]["set"])
    ev = evaluate(m)
    assert ev["alpha"] == 8 and ev["extra_ap"] == 0 and ev["repeated"] == 0 and ev["is45"]
    assert FastEval(14).score(m)[1:] == (8, 0)


def test_12pt_map_alpha7():
    for k in ("12", "12b", "12c"):
        ev = evaluate(map_from_set(SETS[k]["set"]))
        assert ev["alpha"] == 7 and ev["extra_ap"] == 0 and ev["repeated"] == 0 and ev["is45"]


def test_moves_preserve_linearity_and_is45_agrees():
    rng = random.Random(0)
    m = random_linear_map(16, rng)
    for _ in range(300):
        q = propose(m, rng)
        if q is not None:
            assert is_linear_map(q.mid)
            m = q
    for _ in range(100):
        A = sorted(rng.sample(range(45), 9))
        assert is45_ints(A) == is_45_set(A)


def test_extend_and_free_vertex_solve():
    rng = random.Random(1)
    m = extend_map(map_from_set(SETS["14"]["set"]), 2, rng)
    assert m.n == 16 and is_linear_map(m.mid)
    mf = random_linear_map(16, rng, nfree=1)
    v = solve_exact(mf)
    if v is not None:
        assert all(2 * v[j] == v[i] + v[k] for j, (i, k) in mf.mid.items())
