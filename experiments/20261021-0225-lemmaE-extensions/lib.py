"""Shared exact tools for the Lemma-E extension experiment (all arithmetic in Python ints)."""
import importlib.util, itertools, json, sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from e757 import core  # noqa: E402

spec = importlib.util.spec_from_file_location("cf", REPO / "experiments/20261020-1730-reader-5-9/check_family.py")
cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
O = cf.O


def family(K):
    fam = {m["K"]: m for m in json.loads((REPO / "data/reader_5_9_family.json").read_text())["family"]}
    m = fam[K]
    A = sorted(m["set"])
    scale = m["scale"]
    L = Fraction(27169, 251)
    copies = []
    for j in range(K + 1):
        cp = {int((L + Fraction(18, 269) ** j * (Fraction(x) - L)) * scale) for x in O}
        copies.append(cp)
    assert set().union(*copies) == set(A)
    return A, copies


def aps(A):
    """3-term APs (a,b,c), a<b<c, 2b=a+c, by own sum dictionary (independent of e757)."""
    S = set(A)
    A = sorted(A)
    out = []
    for i, a in enumerate(A):
        for c in A[i + 2:]:
            if (a + c) % 2 == 0 and (a + c) // 2 in S:
                out.append((a, (a + c) // 2, c))
    return out


def own_45(A):
    return cf.four_subset_test(A)  # (ok, count, min distinct diffs)


def alpha_dp(A, copy_of, remove=()):
    """Exact alpha of 3-AP hypergraph of A minus vertices `remove`, by frontier DP.
    copy_of: dict point -> sort key group (any order is correct, only affects speed)."""
    rem = set(remove)
    edges = [e for e in aps(A) if not (set(e) & rem)]
    order = sorted((v for v in A if v not in rem), key=lambda v: (copy_of[v], v))
    h, mf = cf.frontier_dp_h(order, edges)
    return h, mf


def groups_for(A, copies):
    g = {}
    for v in A:
        g[v] = min((j for j, cp in enumerate(copies) if v in cp), default=0)
    return g
