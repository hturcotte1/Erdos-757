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
