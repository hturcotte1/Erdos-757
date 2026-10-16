cd /home/user/Erdos-757
D=experiments/20261014-0500-slack-landscape
BUDGET=0 MOFF=3 python3 $D/driver.py op 13 14 120
MOFF=0 python3 $D/driver.py op 12 12 300
MOFF=4 python3 $D/driver.py real 12 12 120
