import glob, gzip, json, os
H = os.path.dirname(os.path.abspath(__file__)); d = glob.glob(os.path.join(H, 'out/chunks/25_19_10_D3_d3_tp9'))[0]
metas = sorted(glob.glob(d + '/c*.meta.json')); keys = set(); inp = nh = nc = 0; bad = 0; nodes = 0; secs = 0
for m in metas:
    j = json.load(open(m)); inp += j['ninputs']; nh += j['nhit']; nc += j['nsurv']; bad += j['ext'].get('bad_tau', 0); nodes += j['ext']['nodes']; secs += j['secs']
    keys.update(l for l in gzip.open(m.replace('.meta.json', '.keys.gz'), 'rt').read().splitlines() if l)
out = dict(cell='(25,19,10,3) branch d=3 tp=9', chunks_done=len(metas), chunks_total=84, chunk_size=25000, inputs_done=inp, inputs_total=2043426 + 0, hits_in_C=nh, connected_hits=nc, distinct_classes_so_far=len(keys), bad_tau=bad, ext_nodes=nodes, secs=round(secs, 1))
print(json.dumps(out)); json.dump(out, open(os.path.join(H, 'partial_25_19_10.json'), 'w'), indent=1)
