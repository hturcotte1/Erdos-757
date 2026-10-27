import cProfile, pstats, sys, io, itertools, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L024')
sys.argv = ['x', 'none']
import pattern_a as pa
from hyp24 import *
P = [pa.byname['(3,1,1)#0'], pa.byname['(10,7,4)#1'], pa.byname['(17,13,7)#0']]
def run():
    Ps = P
    offs = [0, Ps[0]['n'], Ps[0]['n'] + Ps[1]['n']]
    N = sum(p['n'] for p in Ps)
    E0 = []
    for p, o in zip(Ps, offs): E0 += [tuple(x + o for x in e) for e in p['edges']]
    d0 = degrees(N, E0)
    MT = [[T << o for T in p['mts']] for p, o in zip(Ps, offs)]
    gcand = [pa.orbit_reps(p, [x for x in range(p['n']) if p['deg'][x] <= 2]) for p in Ps]
    print('gcand sizes', [len(c) for c in gcand])
    tU = tH = tS = 0; ncfg = 0; nC = []
    for gl in list(itertools.product(*gcand))[:6]:
        g = tuple(x + o for x, o in zip(gl, offs))
        E1 = E0 + [tuple(sorted(g))]
        d1 = list(d0)
        for x in g: d1[x] += 1
        Lmask = sum(1 << x for x in range(N) if d1[x] <= 2)
        inside = set()
        for e in E1:
            for a, b in itertools.combinations(e, 2): inside.add((min(a, b), max(a, b)))
        low = [x for x in range(N) if Lmask >> x & 1]
        valid = [(1 << a) | (1 << b) for a, b in itertools.combinations(low, 2) if (a, b) not in inside]
        t1 = time.time()
        Us = set()
        for i0 in range(3):
            parts = []
            for i in range(3):
                if i == i0: parts.append(pa.maximal([T & Lmask for T in MT[i] if T >> g[i] & 1]))
                else: parts.append(pa.maximal([T & Lmask for T in MT[i]]))
            for a in parts[0]:
                for b in parts[1]:
                    for c in parts[2]: Us.add(a | b | c)
        Cs = pa.minimal([Lmask & ~U for U in Us])
        t2 = time.time(); tU += t2 - t1
        sols = pa.hitting_triples(Cs, valid)
        t3 = time.time(); tS += t3 - t2
        nC.append((len(Us), len(Cs), len(sols)))
        for sol in sols:
            E = list(E1)
            for p in sol:
                a, b = [x for x in range(N) if p >> x & 1]
                E.append(tuple(sorted((a, b, N))))
            r = pa.check_H(N + 1, E, 0, None); ncfg += 1
        tH += time.time() - t3
    print('U time', tU, 'search time', tS, 'check time', tH, 'configs', ncfg, nC)
cProfile.run('run()', 'prof.out')
s = io.StringIO(); pstats.Stats('prof.out', stream=s).sort_stats('cumulative').print_stats(15); print(s.getvalue()[:3000])
