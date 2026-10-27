"""Own realizability decision (realize_own.decide, pruned DFS over all 3^23 midpoint assignments) on X_0..X_5, plus the number of
injective midpoint labellings (certificate: 55,236, 54,164, 53,300, 53,740, 54,700, 54,260)."""
import json, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from realize_own import decide, count_injective_labellings
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'six_from_text.json')))
which = sys.argv[1:] or sorted(D)
for name in which:
    E = [tuple(e) for e in D[name]]
    t0 = time.time(); st, sols = decide(E, 25, prune=True, stop_at_first=False)
    print(name, 'REALIZABLE' if sols else 'NOT-REALIZABLE', json.dumps(st), 'secs %.1f' % (time.time() - t0),
          'injective_labellings', count_injective_labellings(E), flush=True)
