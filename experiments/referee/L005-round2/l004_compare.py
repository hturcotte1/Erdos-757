import gzip, json, sys
sys.path.insert(0, '.')
from check_data import normal_form
mine = {normal_form(json.loads(l)['set']) for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt')}
theirs = set()
for l in gzip.open('/home/user/Erdos-757/experiments/referee/L004/my_realizable.txt.gz', 'rt'):
    if l.strip():
        theirs.add(normal_form([int(v) for v in l.split('\t')[1].split(',')]))
print('census classes', len(mine), 'L004-referee classes', len(theirs), 'equal', mine == theirs)
