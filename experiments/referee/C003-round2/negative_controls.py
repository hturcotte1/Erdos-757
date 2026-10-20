#!/usr/bin/env python3
"""Negative controls: the referee's checkers must FLAG known bad inputs."""
import itertools, sys
sys.path.insert(0, "/home/user/Erdos-757/experiments/referee/C003-round2")
from reflib import *

def is45(B):
    B = sorted(B)
    return all(len({b-a, c-a, d-a, c-b, d-b, d-c}) >= 5 for a, b, c, d in itertools.combinations(B, 4))

A, raw = load_claim_set()
print("{0,1,2,3} (4-AP)            is45 =", is45([0,1,2,3]), "(expect False)")
print("{1,2,3,5}                   is45 =", is45([1,2,3,5]), "(expect False)")
print("{0,1,3,4} (parallelogram)   is45 =", is45([0,1,3,4]), "(expect False)")
print("{0,1,3,7} (Sidon)           is45 =", is45([0,1,3,7]), "(expect True)")
# perturb one point of the claim set to create a parallelogram a+b=c+d with 4 distinct points
B = list(A); B[10] = A[3] + A[7] - A[20]
print("claim set with point 10 := A3+A7-A20   is45 =", is45(B), "(expect False); weak Sidon =", len(set(x+y for x,y in itertools.combinations(sorted(B),2))) == 65*64//2, "(expect False)")
# conflicts of the perturbed set must include a 4-point conflict
conf = conflicts_from_definition(sorted(B))
print("perturbed set: conflict sizes", sorted(set(map(len, conf))), "(expect includes 4)")
# add a point creating a 4-AP (two APs sharing two points) -> not (4,5), but still weak Sidon possible
C = list(A) + [2*A[1] - A[0]]            # 0, A1, 2*A1: AP with midpoint A1; and A0,A1 are in AP {0,A1,2A1}
print("claim set + {2*A1-A0}: is45 =", is45(C), "(expect False, since {A0,A1,2A1} u a common AP of A1 ... at least check it reports something)")
# the DP/SAT/brute must give n for a Sidon set and known values on small sets
S = [0, 1, 3, 7, 12, 20]            # Sidon
conf = conflicts_from_definition(S)
print("Sidon set: conflicts", len(conf), "DP h =", frontier_dp(len(S), conf, list(range(len(S))))[0], "brute h =", brute_force_h(S)[0], "(expect 6, 6)")
S = list(range(10))                  # 0..9: h = max Sidon subset of {0..9} is 5 ({0,1,3,7,9}?) brute will tell
conf = conflicts_from_definition(S)
print("{0..9}: conflicts", len(conf), "DP h =", frontier_dp(len(S), conf, list(range(len(S))))[0], "brute h =", brute_force_h(S)[0], "SAT>=h", sat_atleast(10, conf, brute_force_h(S)[0])[0], "SAT>=h+1", sat_atleast(10, conf, brute_force_h(S)[0]+1)[0])
