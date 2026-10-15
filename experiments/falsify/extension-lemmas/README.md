# Falsification of kb/notes/extension_lemmas.md (Lemma E, U/U1/U2, Delta)

Exact integer/Fraction arithmetic throughout (e757.core ap_edges / is_45_set; own bitmask alpha). Seed fixed. Run all at nice 15.

## Scope
Sets (all tested to be (4,5)-sets): data/small_records.json (8 sets), all realized extremal classes for n=6..10 (n=9 and 10 complete,
capped at 1200 random per (n,m) file), n=11 samples, 1500 random of the 54,243 n=12 classes, 150 random of the 2,910 n=14 classes,
A_base, Fibonacci prefixes n=8,10,12,14. Total 21,994/2 = 10,997 sets. (n=13 and the 466,961 saturated n=11 classes are not on disk.)

## Commands / results
1. `python3 falsify.py 1` -> results_testsE_U.json. Lemma E numerically: both extreme points, t in {1,3,7,101,1009,1000003, 3 random in 1e6..1e12},
   A scaled by 2. 197,946 (set, a, t) triples. Wherever C is a (4,5)-set with H(C)=H(A)+{y,a,x}: h(C)=h(A)+1 (a universal) or +2 (not): 0 formula failures.
   Bad t (extra AP or not (4,5)): only t in {1,3,7,101,1009} on small-scale sets (finitely many exceptions, as claimed); never for t>=1e6.
   Lemma U/U1/U2: 5,443 universal vertices found (all in n<=11 sets and Fibonacci sets), 0 violations of 17 tau <= 5(n-1)+3(m-deg a) and of
   delta >= 5+3 deg a. U1: none of the 150 sampled n=14 classes (nor A_base) has a universal vertex.
2. `python3 test_symbolic_E.py` -> symbolic.log, results_symbolic_E.json. Test 4: t treated as formal variable (differences = linear forms in t,
   sign by lexicographic order, i.e. valid for all t beyond finitely many breakpoints). All 4-subsets containing x or y, a in {min,max}:
   21,994 cases, 0 four-subsets with <5 differences (so the (4,5) claim holds, in particular {x,y,b,c} needs b+c=2a). Negative control: a a non-extreme
   midpoint -> 21,994/21,994 fail (<5 differences), so the check has teeth.
   Universal extreme points exist (n=7,9,11 extremal sets; Fibonacci). Lemma E then gives (n+2,h+1) with D lowered by 1, but always
   h+1 = f(n+2) (ties, f(n+2)=f(n)+1 for n<=13): no new record from data (table in symbolic.log).
3. `python3 test_delta.py` -> delta.log, results_delta.json. All Delta arithmetic asserted; k=1 case examined (see below).

## Findings
- Lemma E: HOLDS-ON-DATA (proof also re-derived by hand; correct).
- Lemma U, U1: HOLDS-ON-DATA; arithmetic OK (102 > 101-3deg). U2: small ARITHMETIC-ERROR: "5+3deg a >= 8" needs deg a >= 1. A vertex in no AP is
  universal with deg 0, giving only delta >= 5 (such vertices occur: 'deg 0' rows in the table, incl. extreme ones).
- Lemma Delta main statement: arithmetic correct (m>=13 from 119<=80+3m; 102<=75+3(m-deg p) gives deg<=m-9; slack 80+42-119=3).
- Delta "consequence" paragraph: two gaps, conclusion survives.
  (i) The k=1 case {x,a,b}, y isolated: the stated condition "x universal in H(A)+{x,a,b}" is wrong: x is never universal there
      (H'-x = H(A) has alpha 8 = alpha(H')). The correct condition for h(C)=9 is h(A+x)=8, i.e. every maximum Sidon set of A contains a and b (a, b universal in H(A)).
      Correct exclusion: HY applied directly to A+x (n=15, m=13): tau=7 would need 119 <= 5*15+3*13 = 114, false; so h(A+x)>=9, h(C)>=10. (The text's
      119 > 70+36 is the right arithmetic for "U with deg x=1", just applied to the wrong hypothesis.) Checked: 2,889 one-point extensions of sampled
      n=14 classes with exactly one new AP, all had h(A+x)=9.
  (ii) k=1 with new edge containing both x,y has three roles for the old point a: midpoint (Lemma E, needs a extreme and universal) or an END point
      of (a,x,y) with x (or y) the midpoint. The latter (y=2x-a, x generic; a arbitrary) is not Lemma E and is not listed. It is also excluded by U1: h(C)=8+1 only if
      a universal (h(C)=h(A)+2 otherwise). Checked numerically: 1,708 cases, h(C)=h(A)+2, m=13, 0 exceptions (no universal vertices at n=14).
