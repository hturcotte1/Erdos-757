# Measures the frozen verifier (judge/judge.py: is_45 and max_sidon_via_aps) on K=1..5 to extrapolate its cost; run: python3 -I scaling_measure.py
import sys, json, time, importlib.util
from fractions import Fraction
spec = importlib.util.spec_from_file_location("fj", "/home/user/Erdos-757/judge/judge.py")
J = importlib.util.module_from_spec(spec); spec.loader.exec_module(J)
d = {m["K"]: m for m in json.load(open("/home/user/Erdos-757/data/reader_5_9_family.json"))["family"]}
for K in (1, 2, 3, 4, 5):
    A = J.parse_set(d[K]["set"])
    t = time.time(); ok, bad = J.is_45(A); t1 = time.time() - t
    t = time.time(); h = J.max_sidon_via_aps(A); t2 = time.time() - t
    print(K, len(A), ok, h, "is_45 %.1fs" % t1, "alpha_aps %.2fs" % t2, flush=True)
