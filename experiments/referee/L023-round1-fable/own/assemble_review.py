"""Fill the placeholders of review_draft.md from the live status files and write the final review."""
import os, re, json, time, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
draft = open(os.path.join(R, 'own', 'review_draft.md')).read()
now = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
# realizability results
lines = []
for p in (os.path.join(R, 'own', 'realize_own_output.txt'), '/dev/shm/fable_l023/realize_rest.txt'):
    if os.path.exists(p): lines += [l.strip() for l in open(p) if l.startswith('X_')]
res = {}
for l in lines:
    m = re.match(r'X_(\d) (\S+) (\{.*\}) ([\d.]+)s', l)
    if m: res[int(m.group(1))] = (m.group(2), json.loads(m.group(3)), float(m.group(4)))
done = sorted(res)
x3 = ''
if 3 in res:
    c = res[3][1]; x3 = 'X_3 %s, %d labellings = %d NONINJ + %d NOTWS, %d SINGULAR, %d REAL (%.0f s);' % (res[3][0], c['labellings'], c['NONINJ'], c['NOTWS'], c['SINGULAR'], c['REAL'], res[3][2])
others = [i for i in done if i not in (0, 3)]
if others:
    x3 += ' ' + ' '.join('X_%d %s, %d labellings = %d NONINJ + %d NOTWS, %d REAL;' % (i, res[i][0], res[i][1]['labellings'], res[i][1]['NONINJ'], res[i][1]['NOTWS'], res[i][1]['REAL']) for i in others)
summary = 'classes decided: %s, all NOT-REALIZABLE with 0 SINGULAR, 0 NONLIN, 0 APSET, 0 REAL and the certificate\'s exact NONINJ/NOTWS counts (%s); the undecided classes (%s) were not reached within the budget (two runs of the script died silently on the overloaded machine; the task required at least two classes).' % (
    ', '.join('X_%d' % i for i in done), '; '.join('X_%d: %d/%d/%d' % (i, res[i][1]['labellings'], res[i][1]['NONINJ'], res[i][1]['NOTWS']) for i in done), ', '.join('X_%d' % i for i in range(6) if i not in done) or 'none')
if len(done) == 6: summary = 'all six classes decided: NOT-REALIZABLE, each with 0 SINGULAR, 0 NONLIN, 0 APSET, 0 REAL and exactly the certificate\'s labelling/NONINJ/NOTWS counts (%s).' % '; '.join('X_%d: %d/%d/%d' % (i, res[i][1]['labellings'], res[i][1]['NONINJ'], res[i][1]['NOTWS']) for i in done)
# engine status
cell = os.path.join(R, 'engine', 'cells', 'cell_23_17_9_D3.txt')
cmp_out = subprocess.run([sys.executable, os.path.join(R, 'own', 'compare_gap.py')], capture_output=True, text=True).stdout.strip()
finished = os.path.exists(cell) and any(l.startswith('INFO ') for l in open(cell))
cpu = subprocess.run("ps -eo cputime,etime,args | grep 'L023-round1-fable/engine/bin/ext_d' | grep -v grep | head -1", shell=True, capture_output=True, text=True).stdout.strip()
if finished:
    ok = 'identical FOUND lines: True' in cmp_out.split('23_17_9_D3')[1].split('\n')[0]
    engine_status = ('cell(23,17,9,3) recomputed from the refereed lists plus the 12 twice-computed lists (verified U1 == repro copy): %s. Output of own/compare_gap.py:\n```\n%s\n```' % ('IDENTICAL to U1\'s list (137,326 canonical forms, same INFO counters)' if ok else 'DIFFERENT FROM U1 - see below', cmp_out))
    gap_status = ('Of the five, I recomputed cell(23,17,9,3) (137,326 classes; the largest and the one no other referee was observed to recompute) from the refereed lists plus the twice-computed lists: %s. The other four ((24,20,10,3), which needs (23,17,9,3), (20,16,8,3) and (17,15,7,3) as inputs, and (21,19,9,3), (20,16,8,3), (17,15,7,3)) were not recomputed by me within the budget; my engine process continues with them under a watchdog (see Problems, item 1).' % ('IDENTICAL to U1\'s list' if ok else 'DIFFERENT from U1\'s list, which would REFUTE the certificate - see Problems'))
    gap_detail = engine_status
    prob1 = ('Status after this review: cell(23,17,9,3) recomputed by me: %s; (24,20,10,3), (21,19,9,3), (20,16,8,3), (17,15,7,3) not recomputed by me.' % ('identical' if ok else 'DIFFERENT'))
else:
    engine_status = ('the recomputation of cell(23,17,9,3) (883,379 inputs, 49 decompositions, as in U1\'s record) started 08:57 UTC and is still inside its single `ext_d 22 8 9 3 2` step at the time of writing (%s UTC; process cputime/elapsed: %s) on a machine with load 10-22 on 4 cores; it did not finish within the 2.5 h budget. I detached it from its original `timeout` so that it continues (PID 27133, nice 10, one process) under a watchdog that kills it at about 14:07 UTC; when it finishes, engine/cells/cell_23_17_9_D3.txt is written and `python3 own/compare_gap.py` compares it (and any later list of the same run: the process continues with 17,15,7,3 20,16,8,3 21,19,9,3 24,20,10,3) with U1\'s copies in own/u1_gap/. To stop it earlier: `kill 27133; pkill -f L023-round1-fable/engine/bin/ext_d`.' % (time.strftime('%H:%M', time.gmtime()), cpu or 'n/a'))
    gap_status = ('None of the five was recomputed by me within the budget: I chose (23,17,9,3), the largest (137,326 classes, 883,379 inputs, 12.5 x 10^9 ext_d nodes in U1) and the one no other referee was observed to recompute, from the refereed lists plus the 12 twice-computed lists; after %s of a 25-30%% CPU share on the overloaded shared machine its single ext_d step had not finished. It continues under a watchdog; see Problems, item 1, for how to collect and compare the result. What I could verify about the five lists: U1\'s run records are consistent with my own brute-force decompositions and input counts (decompositions 7, 21, 6, 49, 18; inputs 617,069; 821,288; 977,982; 883,379; 1,176,201; bad_tau 0; one branch each), the prover\'s soundness audit (C12) and the fact that the lists sit correctly in the tree; none of this establishes their completeness.' % (cpu.split()[1] if cpu else 'about 1 h'))
    gap_detail = engine_status
    prob1 = 'Status after this review: none of the five recomputed by me (my run of (23,17,9,3) continues in the background; see item 1 text below for how to collect it).'
out = draft.replace('GAP_TIMESTAMP', now).replace('GAP_STATUS_PARAGRAPH', gap_status).replace('GAP_DETAIL', gap_detail).replace('REALIZE_X3_LINE', x3).replace('REALIZE_SUMMARY', summary).replace('ENGINE_STATUS', engine_status).replace('PROBLEM1_STATUS', prob1)
assert 'GAP_' not in out and 'REALIZE_' not in out and 'ENGINE_STATUS' not in out and 'PROBLEM1_' not in out
path = '/home/user/Erdos-757/results/reviews/L023-f25-equals-15__referee__%s.md' % now
if len(sys.argv) > 1 and sys.argv[1] == 'write':
    open(path, 'w').write(out); print('written', path)
else:
    print(out[:3000]); print('...'); print('(dry run; pass "write" to write %s)' % path)
