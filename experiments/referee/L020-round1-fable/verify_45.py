"""Referee check of the 45 classes of L020 Theorem 1 (input: the prover's K29_classes.json, used only as data) and of
the 120 labelled graphs (pattern_e_found_cell_20_15_8.json): own membership/tau checks and own canonical forms;
nauty labelg (independent binary) on the augmented incidence graph as a second canonical form."""
import sys, time, json, subprocess, itertools, random
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-fable')
import ref3 as R

LABELG = '/home/user/Erdos-757/experiments/referee/L013-round2/out/nauty_build/labelg'
P = '/home/user/Erdos-757/experiments/prover/L020/'

def main():
    cls = json.load(open(P + 'K29_classes.json'))
    lab = json.load(open(P + 'pattern_e_found_cell_20_15_8.json'))
    print('classes file:', len(cls), '| labelled file:', len(lab))
    # the certificate's K29 must be the first class
    K29 = [(0,1,14),(1,2,15),(2,16,17),(3,4,13),(3,10,18),(4,11,18),(5,8,9),(5,15,16),(6,7,16),(6,8,17),(7,9,17),(10,11,19),(12,14,15),(12,18,19),(13,14,19),(20,21,22),(21,25,26),(22,24,27),(23,24,26),(23,25,27),(1,12,28),(21,23,28),(0,20,28)]
    E0 = [tuple(sorted(e)) for e in cls[0]['edges']]
    print('certificate K29 == class 0 edge set:', set(map(frozenset, K29)) == set(map(frozenset, E0)))
    t0 = time.time()
    allok = True
    certs = []
    g6 = []
    random.seed(1)
    p3c_idx = set(random.sample(range(len(cls)), 10))
    for i, d in enumerate(cls):
        n = d['n']; E = [tuple(sorted(e)) for e in d['edges']]
        ok = R.is_3uniform_distinct(n, E) and n == 29 and len(E) == 23
        deg = R.degrees(n, E)
        hist = tuple(sorted((k, deg.count(k)) for k in set(deg)))
        lin = R.is_linear(E); f7 = R.contains_F7_direct(n, E); p3 = R.p3_hall(n, E); con = R.connected(n, E)
        masks = R.edge_masks(E)
        T12 = R.min_transversal(masks, 12)
        ex11 = R.exists_transversal(masks, 11)
        tau = 12 if (T12 is not None and not ex11) else R.tau(n, E)
        p3c = R.p3_complete(n, E) if i in p3c_idx else None
        s = 3 * n + 2 * len(E) - 11 * tau
        row_ok = ok and lin and not f7 and p3 and con and max(deg) == 3 and tau == 12 and s == 1 and hist == ((2, 18), (3, 11)) and (p3c is None or p3c)
        allok = allok and row_ok
        c = R.canon(n, E); certs.append(c)
        g6.append(R.graph6_augmented(n, E))
        print('class %2d: lin %s F7 %s P3hall %s P3complete %s conn %s deg %s tau %d slack %d OK %s (%.0fs)' % (
            i, lin, f7, p3, p3c, con, hist, tau, s, row_ok, time.time() - t0), flush=True)
    print('ALL 45 OK:', allok)
    print('distinct own canonical forms among the 45:', len(set(certs)))
    # labelg
    out = subprocess.run([LABELG, '-q'], input='\n'.join(g6) + '\n', capture_output=True, text=True)
    canon_g6 = [l for l in out.stdout.split('\n') if l.strip()]
    print('labelg: lines', len(canon_g6), 'distinct', len(set(canon_g6)), 'stderr:', out.stderr.strip()[:200])
    # consistency: own canon equal <=> labelg canon equal
    mism = 0
    for i in range(len(cls)):
        for j in range(i + 1, len(cls)):
            if (certs[i] == certs[j]) != (canon_g6[i] == canon_g6[j]):
                mism += 1
    print('own-canon vs labelg disagreements:', mism)
    # the 120 labelled graphs
    t0 = time.time()
    certs120 = []
    bad = 0
    for d in lab:
        n = d['n']; E = [tuple(sorted(e)) for e in d['edges']]
        certs120.append(R.canon(n, E))
        if not (n == 29 and len(E) == 23 and d['tau'] == 12):
            bad += 1
    S120 = set(certs120)
    print('120 labelled graphs: distinct own canonical forms', len(S120), '| equal to the set of the 45:', S120 == set(certs), '| bad params', bad, '(%.0fs)' % (time.time() - t0))
    # sanity of own canon: random relabelling of class 0 gives the same certificate
    n = 29; E = [tuple(sorted(e)) for e in cls[0]['edges']]
    perm = list(range(n)); random.shuffle(perm)
    E2 = [tuple(sorted(perm[x] for x in e)) for e in E]
    random.shuffle(E2)
    print('own canon invariant under random relabelling:', R.canon(n, E2) == certs[0])
    # and distinguishes a modified graph
    E3 = list(E); E3[0] = (0, 1, 13) if (0, 1, 13) not in E3 else (0, 1, 15)
    print('own canon distinguishes a modified graph:', R.canon(n, E3) != certs[0])

if __name__ == '__main__':
    main()
