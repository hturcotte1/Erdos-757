import json, glob, os, collections
here = os.path.dirname(os.path.abspath(__file__))
meta = json.load(open(os.path.join(here, 'cells.json')))
res = {}
for k, mt in sorted(meta.items(), key=lambda kv: (kv[1]['slack'], kv[1]['n'])):
    f = os.path.join(here, 'outputs', 'cell_%s.jsonl' % k)
    if not os.path.exists(f): continue
    rows = [json.loads(l) for l in open(f)]
    n, m, tau, s = mt['n'], mt['m'], mt['tau'], mt['slack']
    nT = [r['nT'] for r in rows]
    S = lambda key: sum(r[key] for r in rows)
    p2tot = [sum(r['p2tot'][i] for r in rows) for i in range(12)]; p2fail = [sum(r['p2fail'][i] for r in rows) for i in range(12)]
    fail_keys = [i for i in range(12) if p2fail[i]]
    unc_combo = [sum(r['unc_combo'][i] for r in rows) for i in range(8)]
    sz = collections.Counter(); szo = collections.Counter()
    for r in rows:
        for a, b in r['unc_P_size'].items(): sz[int(a)] += b
        for a, b in r['unc_P_only_size'].items(): szo[int(a)] += b
    uA = S('uncA'); uB = S('uncBonly'); sA = collections.Counter(); sB = collections.Counter()
    for r in rows:
        for a, b in r['uncA_size'].items(): sA[int(a)] += b
        for a, b in r['uncB_size'].items(): sB[int(a)] += b
    maxdeg = [max(r['deg']) for r in rows]
    # classes with Delta<=3 only
    rows3 = [r for r in rows if max(r['deg']) <= 3]
    res[k] = dict(n=n, m=m, tau=tau, slack=s, D_listed=mt['D'], classes=len(rows), classes_deg_le3=len(rows3), n_minus_m=n - m, m_le_n_minus_4=(m <= n - 4),
        maxdeg_range=[min(maxdeg), max(maxdeg)], nT_min=min(nT), nT_max=max(nT), nT_mean=sum(nT) / len(nT), truncated=S('trunc'),
        vertices_in_no_min_transversal=S('novert'), max_P2_fail_key=max(fail_keys) if fail_keys else None, P2_bound_floor_s5_2=(s + 5) // 2,
        p2_pairs=sum(p2tot), p2_fail=sum(p2fail), p2_fail_by_key={i: [p2fail[i], p2tot[i]] for i in range(12) if p2fail[i]}, p2_by_key_total={i: p2tot[i] for i in range(12) if p2tot[i]},
        classes_with_P2_failure=sum(1 for r in rows if sum(r['p2fail'])),
        pp_all=S('pp_all'), pp_all_cov=S('pp_all_cov'), pp_good=S('pp_good'), pp_good_cov=S('pp_good_cov'), classes_pp_all_cov=sum(1 for r in rows if r['pp_all'] != r['pp_all_cov']),
        triples=S('ntrip'), triples_coverable=S('ncov'), triples_linear=S('nlin'), triples_admissible=S('nadm'), admissible_uncoverable=S('nadm_unc'),
        classes_with_admissible=sum(1 for r in rows if r['nadm']), classes_with_admissible_uncoverable=sum(1 for r in rows if r['nadm_unc']),
        adm_R2=S('adm_R2'), adm_R2_unc=S('adm_R2_unc'), adm_R1=S('adm_R1'), adm_R1_unc=S('adm_R1_unc'),
        adm_min_cover_count=min([r['adm_mincov'] for r in rows if r['adm_mincov']>=0] or [None]) if any(r['adm_mincov']>=0 for r in rows) else None, adm_thin_le2=S('adm_thin'), adm_min_cover_ratio=min([r['adm_minratio'] for r in rows if r['adm_minratio']>=0] or [None]) if any(r['adm_minratio']>=0 for r in rows) else None,
        uncoverable_total=S('unc_total'), uncoverable_nonadm_by_combo={'L,F,P bits (1=nonlinear,2=F7,4=P3 violated)': {str(i): unc_combo[i] for i in range(8) if unc_combo[i]}},
        uncoverable_P_violating_minS=dict(sorted(sz.items())), uncoverable_P_only_minS=dict(sorted(szo.items())),
        uncoverable_violates_A=uA, uncoverable_violates_B_only=uB, A_minS=dict(sorted(sA.items())), B_only_minS=dict(sorted(sB.items())),
        nonadm_total=S('nonadm_total'), nonadm_L=S('nonadm_L'), nonadm_P=S('nonadm_P'),
        adm_unc_sample=[(i, r['adm_unc_sample'][:3]) for i, r in enumerate(rows) if r['adm_unc_sample']][:3],
        degree_sequences=len(set(tuple(sorted(r['deg'])) for r in rows)))
json.dump(res, open(os.path.join(here, 'results.json'), 'w'), indent=1)
for k, r in res.items():
    print(k, 's=%d' % r['slack'], 'cls=%d' % r['classes'], 'nT[%d,%d]' % (r['nT_min'], r['nT_max']), 'novert', r['vertices_in_no_min_transversal'], 'P2fail %d/%d maxkey %s (bound %d)' % (r['p2_fail'], r['p2_pairs'], r['max_P2_fail_key'], r['P2_bound_floor_s5_2']),
          'pp %d/%d' % (r['pp_all_cov'], r['pp_all']), 'good %d/%d' % (r['pp_good_cov'], r['pp_good']), 'adm', r['triples_admissible'], 'adm_unc', r['admissible_uncoverable'], 'unc', r['uncoverable_total'], r['uncoverable_nonadm_by_combo'], 'minS', r['uncoverable_P_violating_minS'], 'trunc', r['truncated'])
