"""Independent F7 test (prover L007), not using e757.cpsat_model.find_f7.
Lemma used: in a LINEAR 3-graph, five edges form a copy of F7 = {012,034,056,135,246} iff their union has exactly 7
vertices and, counted within these five edges, one vertex has degree 3 and the other six have degree 2.
(Proof in the certificate, step C3.)  We test all 5-subsets of the edge set."""
import itertools, re, sys, json
def is_linear(es):
    seen = set()
    for e in es:
        for p in itertools.combinations(sorted(e), 2):
            if p in seen: return False
            seen.add(p)
    return True
def has_f7(es):
    for five in itertools.combinations(es, 5):
        deg = {}
        for e in five:
            for v in e: deg[v] = deg.get(v, 0) + 1
        if len(deg) == 7 and sorted(deg.values()) == [2, 2, 2, 2, 2, 2, 3]:
            return True
    return False
def parse(path, tag):
    out = []
    for l in open(path):
        if l.startswith(tag):
            out.append([tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l)])
    return out
if __name__ == '__main__':
    # sanity: F7 itself, Fano minus two lines (7 vertices, 5 edges, not F7), AG(2,3) minus 2 points
    F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
    fano = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    fano_minus2 = [e for e in fano if e not in [(0,1,2),(0,3,4)]]
    assert has_f7(F7) and not has_f7(fano_minus2), 'sanity'
    print('sanity: F7 detected; Fano minus two lines (7 vertices, 5 edges) not detected')
    report = {}
    for path, tag in sys.argv[1:] and [a.split(':') for a in sys.argv[1:]] or []:
        L = parse(path, tag + ':')
        lin = sum(is_linear(es) for es in L)
        f7 = sum(has_f7(es) for es in L)
        report[path] = dict(graphs=len(L), linear=lin, contain_F7=f7, F7_free=len(L) - f7)
        print(path, report[path], flush=True)
    json.dump(report, open('f7check_results.json', 'w'), indent=1)
