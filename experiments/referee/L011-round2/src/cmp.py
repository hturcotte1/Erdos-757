"""Referee L011 r2: compare two hypergraph lists as sets of isomorphism classes (bin/canon).  Lines without '(' and without a
leading digit are skipped (e.g. enum_conn's trailer, SUMMARY lines).  Usage: python3 -I cmp.py N fileA fileB [prefixA] [prefixB]"""
import subprocess, sys, gzip, os
def lines(path, prefix=None):
    op = gzip.open if path.endswith('.gz') else open
    with op(path, 'rt') as f:
        for ln in f:
            s = ln.strip()
            if not s: continue
            if prefix is not None:
                if not s.startswith(prefix): continue
            elif not ('(' in s and ':' in s.split('(')[0] or s[0].isdigit()): continue
            if s.startswith('enum_conn') or s.startswith('SUMMARY'): continue
            yield s
def classes(N, path, prefix=None):
    L = list(lines(path, prefix))
    B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bin', 'canon')
    out = subprocess.run([B, str(N)], input='\n'.join(L) + '\n', capture_output=True, text=True, check=True).stdout.split('\n')
    cf = [o.split()[1] + ':' + o.split()[0] for o in out if o.strip()]
    assert len(cf) == len(L), (len(cf), len(L))
    return len(L), set(cf)
if __name__ == '__main__':
    N = int(sys.argv[1]); pa = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != '-' else None
    pb = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != '-' else None
    na, A = classes(N, sys.argv[2], pa); nb, B = classes(N, sys.argv[3], pb)
    print('N=%d A=%s lines=%d classes=%d | B=%s lines=%d classes=%d | %s' % (N, os.path.basename(sys.argv[2]), na, len(A),
          os.path.basename(sys.argv[3]), nb, len(B), 'IDENTICAL' if A == B else 'DIFFERENT (A-B %d, B-A %d)' % (len(A - B), len(B - A))))
