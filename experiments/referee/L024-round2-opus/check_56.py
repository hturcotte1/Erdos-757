r"""Referee #3 (round 2): numeric test of the new closure in L024 Step 5.6 (and of the round-1 'referee remark').
Random assemblies H = R u X u E*, X = 1 or 2 disjoint induced copies of E1 / (8,5,3)#b, |E*(X)| = |X|+1 edges each
meeting V(X) (trace <= 2 on each member), other vertices in R (they form the boundary d(X)); H linear, Delta <= 3.
For each H with Claim E on all nonempty subfamilies of X:
  H1: for every e in E*(X) there are minimum transversals T_F (F in X) whose union meets E*(X) \ {e} (L021 8.1);
  if some minimum transversal T' of R contains u in d(X): tau(H) <= tau(R) + sum tau_F and P(H) >= P(R),
  with A = 27n + 35m - 132 tau and DEF computed EXACTLY over all L*-families of H and of R (all induced copies of all
  32 pieces with at most n vertices; here n <= 14, so E1, (8,5,3), (10,7,4) can occur).
Control: the same quantities when no minimum transversal of R meets d(X) (the inequality need not hold there).
Run: timeout 1800 nice -n 10 python3 -B check_56.py <trials> > check_56_output.txt"""
import sys, itertools, random
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L024-round2-opus')
from rlib2 import *

PIECES = load_pieces()
BYN = {}
for P in PIECES: BYN.setdefault(P['n'], []).append(P)

def A_val(n, m, t): return 27 * n + 35 * m - 132 * t

def copies(n, E):
    out = [(frozenset(e), 16) for e in E]
    for s, plist in BYN.items():
        if s == 3 or s > n: continue
        ms = set(len(P['edges']) for P in plist)
        for S in itertools.combinations(range(n), s):
            Ss = set(S)
            ind = [e for e in E if all(x in Ss for x in e)]
            if len(ind) not in ms: continue
            if len(components(S, ind)) != 1: continue
            lab = {x: i for i, x in enumerate(S)}
            E2 = [tuple(lab[x] for x in e) for e in ind]
            for P in plist:
                if len(P['edges']) == len(ind) and iso(s, E2, P['n'], P['edges']):
                    out.append((frozenset(S), P['W'])); break
    return out

def DEF(n, E):
    C = copies(n, E)
    best = [0]
    def rec(i, used, members, W):
        if members:
            Vx = used
            est = sum(1 for e in E if (set(e) & Vx) and not any(set(e) <= M for M in members))
            val = W - 35 * est
            if val > best[0]: best[0] = val
        for j in range(i, len(C)):
            S, w = C[j]
            if S & used: continue
            rec(j + 1, used | S, members + [S], W + w)
    rec(0, frozenset(), [], 0)
    return best[0]

def try_instance(rng):
    choices = [['(3,1,1)#0'], ['(3,1,1)#0', '(3,1,1)#0'], ['(8,5,3)#0'], ['(8,5,3)#1'],
               ['(3,1,1)#0', '(8,5,3)#0'], ['(3,1,1)#0', '(8,5,3)#1']]
    names = rng.choice(choices)
    byname = {P['name']: P for P in PIECES}
    E = []; members = []; nxt = 0; taus = []; Ws = []
    for nm in names:
        P = byname[nm]
        S = list(range(nxt, nxt + P['n'])); nxt += P['n']
        E += [tuple(x + S[0] for x in e) for e in P['edges']]
        members.append(set(S)); taus.append(P['tau']); Ws.append(P['W'])
    nX = nxt
    nR = rng.randint(2, max(2, min(6, 14 - nX)))
    if nX + nR > 14: return None
    R = list(range(nX, nX + nR)); nxt += nR
    n = nxt
    deg = degrees(n, E); pairs = set()
    for e in E:
        for p in itertools.combinations(e, 2): pairs.add(frozenset(p))
    ER = []
    for _ in range(rng.randint(0, nR)):
        e = tuple(sorted(rng.sample(R, 3))) if nR >= 3 else None
        if e is None: break
        ps = [frozenset(p) for p in itertools.combinations(e, 2)]
        if any(p in pairs for p in ps) or any(deg[x] >= 3 for x in e): continue
        ER.append(e); E.append(e)
        for p in ps: pairs.add(p)
        for x in e: deg[x] += 1
    Estar = []
    k = len(members) + 1
    for _ in range(200):
        if len(Estar) == k: break
        e = tuple(sorted(rng.sample(range(n), 3)))
        if not any(x < nX for x in e): continue
        if any(len(set(e) & M) >= 3 for M in members): continue
        if all(x >= nX for x in e): continue
        ps = [frozenset(p) for p in itertools.combinations(e, 2)]
        if any(p in pairs for p in ps) or any(deg[x] >= 3 for x in e): continue
        Estar.append(e); E.append(e)
        for p in ps: pairs.add(p)
        for x in e: deg[x] += 1
    if len(Estar) != k: return None
    return n, E, ER, members, taus, Ws, Estar, R, nX

def main(trials, seed):
    rng = random.Random(seed)
    st = dict(inst=0, claimE=0, H1_ok=0, H1_fail=0, hyp=0, tau_ok=0, P_ok=0, ctrl=0, ctrl_P_lt=0, ctrl_tau_plus1=0, bd_empty=0, edge_in_bd=0, edge_in_bd_ok=0)
    bad = 0
    for _ in range(trials):
        g = try_instance(rng)
        if g is None: continue
        n, E, ER, members, taus, Ws, Estar, R, nX = g
        st['inst'] += 1
        # Claim E on all nonempty subfamilies
        okE = True
        for r in range(1, len(members) + 1):
            for Y in itertools.combinations(range(len(members)), r):
                VY = set().union(*[members[i] for i in Y])
                if sum(1 for e in Estar if set(e) & VY) < len(Y) + 1: okE = False
        if not okE: continue
        st['claimE'] += 1
        bd = set(x for e in Estar for x in e if x >= nX)
        if not bd: st['bd_empty'] += 1; continue
        # minimum transversals of members (in H labels)
        mts = []
        for M in members:
            EM = [e for e in E if set(e) <= M]
            t, Ts = min_transversals(EM); mts.append(Ts)
        def covers_all_but(skip):
            for combo in itertools.product(*mts):
                U = set().union(*combo)
                if all(set(e) & U for e in Estar if e != skip): return True
            return False
        for e in Estar:
            if covers_all_but(e): st['H1_ok'] += 1
            else:
                st['H1_fail'] += 1; bad += 1; print('H1 FAILS', n, E, members, e)
        tR, TRs = min_transversals(ER) if ER else (0, [frozenset()])
        tH = tau(E)
        PR = A_val(len(R), len(ER), tR) + DEF_R(n, ER, R)
        PH = A_val(n, len(E), tH) + DEF(n, E)
        meets = any(T & bd for T in TRs)
        if any(set(e) <= bd for e in ER):
            st['edge_in_bd'] += 1
            if not meets: bad += 1; print('EDGE IN BD BUT NO MEETING TRANSVERSAL', n, E)
            if PH >= PR: st['edge_in_bd_ok'] += 1
        if meets:
            st['hyp'] += 1
            if tH <= tR + sum(taus): st['tau_ok'] += 1
            else: bad += 1; print('TAU FAILS', n, E)
            if PH >= PR: st['P_ok'] += 1
            else: bad += 1; print('P FAILS', n, E, PH, PR)
        else:
            st['ctrl'] += 1
            if PH < PR: st['ctrl_P_lt'] += 1
            if tH == tR + sum(taus) + 1: st['ctrl_tau_plus1'] += 1
    print('CHECK 5.6', st, 'BAD', bad, flush=True)

def DEF_R(n, ER, R):
    lab = {x: i for i, x in enumerate(R)}
    return DEF(len(R), [tuple(lab[x] for x in e) for e in ER])

if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3000, 7)
