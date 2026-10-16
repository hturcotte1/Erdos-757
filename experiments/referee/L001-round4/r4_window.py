"""Route W (referee round 4): recount the half-integer window numbers quoted in the proof text with new numpy
code (doubled coordinates, int64).  (4,5) for a quadruple <=> at most one equal pair among its 6 distances."""
import itertools, json, sys, time
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001-round4')
from r4_lib import A_BASE, is45_full

EXP = '/home/user/Erdos-757/experiments/20261014-0640-abase-extensions/'
A2 = np.array(sorted(2 * a for a in A_BASE), dtype=np.int64)
A2set = set(int(a) for a in A2)
P2 = set()
for p, q in itertools.combinations(A2.tolist(), 2):
    P2 |= {(p + q) // 2, 2 * p - q, 2 * q - p}
P2 -= A2set
P2arr = np.array(sorted(P2), dtype=np.int64)
assert len(P2) == 223


def eqcount(ds, shape):
    eq = np.zeros(shape, dtype=np.int8)
    for p, q in itertools.combinations(range(len(ds)), 2):
        eq += (ds[p] == ds[q])
    return eq


def singles(LO, HI):
    v = np.array([u for u in range(LO, HI) if u not in A2set], dtype=np.int64)
    T = np.array(list(itertools.combinations(A2.tolist(), 3)), dtype=np.int64)   # (364,3)
    a, b, c = T[:, 0][None, :], T[:, 1][None, :], T[:, 2][None, :]
    vv = v[:, None]
    ds = (np.abs(vv - a), np.abs(vv - b), np.abs(vv - c), np.abs(a - b), np.abs(a - c), np.abs(b - c))
    ok = (eqcount(ds, (len(v), len(T))) <= 1).all(axis=1)
    return v[ok]


def window(LO, HI, stored=None, verify_sample=0):
    t0 = time.time()
    vals = singles(LO, HI)
    ia, ib = zip(*itertools.combinations(range(14), 2))
    PA, PB = A2[list(ia)][None, :], A2[list(ib)][None, :]
    DAB = np.abs(PA - PB)
    tot = both = lineg = 0
    nonline = []
    sample = []
    for i in range(len(vals) - 1):
        x = int(vals[i])
        ys = vals[i + 1:]
        Y = ys[:, None]
        ds = (np.abs(Y - x), np.abs(x - PA), np.abs(x - PB), np.abs(Y - PA), np.abs(Y - PB), DAB)
        ok = (eqcount(ds, (len(ys), 91)) <= 1).all(axis=1)
        yo = ys[ok]
        tot += len(yo)
        if verify_sample and i % verify_sample == 0 and len(yo):
            sample.append((x, int(yo[len(yo) // 2])))
        kx = x in P2
        ky = np.isin(yo, P2arr)
        cross = ((2 * A2[None, :] == (x + yo)[:, None]).sum(1) + (2 * x == A2[None, :] + yo[:, None]).sum(1)
                 + ((2 * yo)[:, None] == A2[None, :] + x).sum(1))
        inx = kx | (cross > 0)
        iny = ky | (cross > 0)
        bb = inx & iny
        lg = bb & (~ky) & (cross == 1) & (not kx)
        both += int(bb.sum())
        lineg += int(lg.sum())
        for y in yo[bb & ~lg].tolist():
            nonline.append(frozenset((Fr(x, 2), Fr(y, 2))))
    res = {'window_doubled': [LO, HI], 'valid singles': len(vals), '(4,5) pairs': tot,
           'both points in 3-APs': both, 'line-generic': lineg, 'non-line-generic': len(nonline)}
    if stored is not None:
        def inwin(q):
            return (2 * q).denominator == 1 and LO <= 2 * q < HI
        sw = {k for k in stored if all(inwin(q) for q in k)}
        nl = set(nonline)
        res.update({'stored in window': len(sw), 'non-line-generic missing from stored': len(nl - sw),
                    'stored-in-window not found': len(sw - nl)})
    if sample:
        A = [Fr(a) for a in A_BASE]
        res['pure-python re-check of sampled (4,5) decisions'] = [len(sample), all(is45_full(A + [Fr(x, 2), Fr(y, 2)]) for x, y in sample)]
    res['seconds'] = round(time.time() - t0, 1)
    return res


if __name__ == '__main__':
    R = json.load(open(EXP + 'results.json'))
    stored = {frozenset((Fr(a), Fr(b))) for a, b, h in R['stored']}
    out = []
    for LO, HI in [(-600, 3400), (-120, 2241), (-120, 2240)]:
        r = window(LO, HI, stored, verify_sample=40 if LO == -600 else 0)
        print(json.dumps(r), flush=True)
        out.append(r)
    json.dump(out, open('/home/user/Erdos-757/experiments/referee/L001-round4/r4_window_out.json', 'w'), indent=1)
