import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ['CELLDIR'] = os.path.join(HERE, '..', 'out', 'cells'); os.environ['ENGINELOG'] = os.path.join(HERE, '..', 'out', 'engine_fast.log')
os.environ['MD'] = '10'; os.environ['NPROC'] = '1'
sys.path.insert(0, HERE)
import engine
n, m, t, D = map(int, sys.argv[1:5])
r = engine.cell(n, m, t, D); print('RESULT', (n, m, t, D), len(r))
