cd /home/user/Erdos-757
D=experiments/20261014-0500-slack-landscape
while kill -0 $(cat $D/job1.pid) 2>/dev/null; do sleep 5; done
MOFF=1 python3 $D/driver.py op 12 12 150
BUDGET=0 MOFF=0 python3 $D/driver.py real 13 14 150
