import json, os, random
from fractions import Fraction as F
from e757.core import is_45_set, alpha

A = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
P = os.path.join(os.path.dirname(__file__), '..', 'experiments', '20261014-0640-abase-extensions', 'results.json')


def test_sample_extensions():
    R = json.load(open(P))
    st = R['stored']
    assert len(st) == R['n_stored'] and len(st) >= 50
    rng = random.Random(0)
    for xs, ys, h in rng.sample(st, 50):
        B = [F(a) for a in A] + [F(xs), F(ys)]
        assert len(set(B)) == 16
        assert is_45_set(B)
        assert alpha(B) == 10 and h == 10


def test_stored_witnesses_direct():
    W = json.load(open(os.path.join(os.path.dirname(P), 'witnesses.json')))
    AF = {F(a) for a in A}
    assert len(W['pairs']) == 1743 and len(W['generic_y']) == 50
    rng = random.Random(1)
    for w in rng.sample(W['pairs'], 50):
        S = [F(v) for v in w['S']]
        assert len(S) == 10 and len(set(S)) == 10
        assert set(S) <= AF | {F(w['x']), F(w['y'])}
        assert all(2 * q != a + b for a in S for b in S if a != b for q in S)   # 3-AP-free
    for w in W['generic_y']:
        S = [F(v) for v in w['S9']]
        assert len(set(S)) == 9 and set(S) <= AF | {F(w['x'])}
        assert all(2 * q != a + b for a in S for b in S if a != b for q in S)
