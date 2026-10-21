"""Insert the full frozen re-run result into the review (string edits only)."""
import re, sys, datetime
rev = '/home/user/Erdos-757/results/reviews/C005-lemmaE-SK6-E1__referee__20261021T040028Z.md'
log = open('/home/user/Erdos-757/experiments/referee/C005-round1/frozen_rerun.log').read()
txt = open(rev).read()
m = re.search(r'^(JUDGE: .*)$', log, re.M)
ex = re.search(r'exit=(\d+)', log)
real = re.search(r'real\s+(\S+)', log); user = re.search(r'user\s+(\S+)', log)
dates = re.findall(r'^\w{3} \w{3} +\d+ [\d:]+ UTC \d{4}$', log, re.M)
now = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S UTC')
if m and ex and ex.group(1) == '0' and 'PASS NEW-RECORD C005-lemmaE-SK6-E1 n=67 h=38 ratio=38/67' in m.group(1):
    res = (f"RESULT: `{m.group(1)}`, exit=0, real {real.group(1)}, user {user.group(1)} "
           f"(started {dates[0]}, finished {dates[-1]}). It agrees with my h = 38 and with the recorded run")
    s4 = ("4. the frozen judge's own branch and bound, re-run in full here: "
          "`JUDGE: PASS NEW-RECORD C005-lemmaE-SK6-E1 n=67 h=38 ratio=38/67`")
else:
    res = (f"RESULT: the full re-run did NOT complete or did not pass; log content: {log!r}. The recorded run")
    s4 = "4. [frozen judge full re-run: not completed, see check 10]"
txt = txt.replace("RESULT: PENDING (to be filled in below). The recorded run", res)
txt = txt.replace("claim_E1_K6.log` shows\n", "claim_E1_K6.log`, which shows\n")
txt = txt.replace("4. [frozen judge full re-run: see check 10].", s4 + ".")
txt = txt.replace("Started 2026-10-21 03:50:20 UTC.", f"Started 2026-10-21 03:50:20 UTC, finished {now}.")
open(rev, 'w').write(txt)
print(res); print(s4)
