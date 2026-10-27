"""Stream a stored cell list file as 'n m tau edges...' lines to stdout."""
import sys,re,gzip,os
def stream(path):
    base=os.path.basename(path)
    mm=re.match(r'cell_(\d+)_(\d+)_(\d+)',base)
    op=gzip.open if path.endswith('.gz') else open
    try:
        with op(path,'rt') as f:
            for line in f:
                line=line.strip()
                if not line or line[0]=='#' or line.startswith('INFO'): continue
                if line.startswith('FOUND:'):
                    n,m,t=map(int,mm.groups())
                    tri=re.findall(r'\((\d+),(\d+),(\d+)\)',line)
                    assert len(tri)==m
                    yield '%d %d %d %s'%(n,m,t,' '.join(' '.join(x) for x in tri))
                elif line[0].isdigit():
                    yield line
    except EOFError:
        sys.stderr.write('TRUNCATED '+path+'\n')
if __name__=='__main__':
    for l in stream(sys.argv[1]): print(l)
