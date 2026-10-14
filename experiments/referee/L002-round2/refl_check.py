"""The 2,226,490 census patterns: closed under reflection i -> 11-i, no self-symmetric pattern; canonical count."""
N = 12
def refl(s):
    E = [tuple(map(int, t.split(","))) for t in s.split()]
    R = sorted((N - 1 - k, N - 1 - j, N - 1 - i) for i, j, k in E)
    return " ".join("%d,%d,%d" % e for e in R)
S = set(l.rstrip("\n") for l in open("my_n12_m10_f7free_sorted.txt"))
missing = selfsym = canon = 0
for s in S:
    r = refl(s)
    if r not in S: missing += 1
    if r == s: selfsym += 1
    if tuple(tuple(map(int, t.split(","))) for t in s.split()) <= tuple(tuple(map(int, t.split(","))) for t in r.split()): canon += 1
print("patterns", len(S), "reflection missing", missing, "self-symmetric", selfsym, "canonical (es<=refl)", canon)
