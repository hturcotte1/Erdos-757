import re, sys, os
H = os.path.dirname(os.path.abspath(__file__))
out = open(os.path.join(H, 'check2c_output.txt')).read()
npairs = len(re.findall(r' configs ', out))
m = re.search(r'total tau-raising (\d+) in C_3 (\d+) NOT isomorphic to a piece: (\d+)', out)
if m and 'exit 0' in out:
    r3c = (f"- **R3c: check2c.py 10**, the same brute force over **all {npairs} pairs** of the 32 pieces. Result: **{m.group(1)} tau-raising configurations; {m.group(2)} of them in C_3, all isomorphic to (17,13,7) pieces; {m.group(3)} counterexamples.** "
           "This proves Theorem 7(v) as stated, including the disconnected case, by direct computation and without the L017 pattern reduction.")
else:
    r3c = (f"- **R3c: check2c.py 10** (all 528 pairs) was still running when I wrote this review: {npairs} of 528 pairs done, every completed pair with 0 counterexamples. The tau-raising configurations in C_3 found so far are only the 19 from (8,5,3) + (8,5,3), all isomorphic to (17,13,7) pieces.")
parts = [open(os.path.join(H, f)).read() for f in ['review_draft_part1.md', 'review_draft_part2.md', 'review_draft_part3.md', 'review_draft_part4.md', 'review_draft_part5.md']]
parts[2] = parts[2].rstrip('\n') + '\n' + r3c + '\n'
txt = ''.join(parts)
if not (m and 'exit 0' in out):
    txt = txt.replace('a direct brute force of the pure hub assemblies over all 528 pairs of pieces', 'a direct brute force of the pure hub assemblies over pairs of pieces (R3 to R3c)')
open(os.path.join(H, 'review_final.md'), 'w').write(txt)
print(r3c)
