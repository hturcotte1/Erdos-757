"""Write 25 random census sets + the 3 known 12-point sets as claim files into ./spot/ (scratch only)."""
import gzip, random, json, os
random.seed(20261014)
uniq = set()
for line in gzip.open("my_realized.txt.gz", "rt"):
    a, s, h = line[1:].split("|")
    uniq.add(tuple(map(int, s.split())))
pick = random.sample(sorted(uniq), 25)
known = [[0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575], [0, 178, 198, 218, 227, 235, 272, 276, 287, 317, 356, 436],
         [-336, -168, -44, -24, -4, 0, 39, 44, 49, 80, 102, 160]]
os.makedirs("spot", exist_ok=True)
for t, S in enumerate(list(pick) + known):
    cid = "r2L002s%02d" % t
    with open(os.path.join("spot", cid + ".json"), "w") as f:
        json.dump({"id": cid, "type": "construction", "set": list(S), "claimed_h": 7, "notes": "referee spot check"}, f)
print(len(pick) + len(known))
