"""
UniCore - Disk Scheduling: FCFS vs SSTF vs SCAN vs C-SCAN
Disk: 0-199, initial head = 53, direction = upward
"""

requests = [98, 183, 37, 122, 14, 124, 65, 67, 30, 180]
head = 53
disk_min, disk_max = 0, 199


def movement(seq):
    return sum(abs(seq[i + 1] - seq[i]) for i in range(len(seq) - 1))


def fcfs(reqs, start):
    order = list(reqs)
    return order, movement([start] + order)


def sstf(reqs, start):
    reqs = list(reqs)
    order = []
    current = start
    while reqs:
        nxt = min(reqs, key=lambda r: abs(r - current))
        order.append(nxt)
        reqs.remove(nxt)
        current = nxt
    return order, movement([start] + order)


def scan(reqs, start, disk_max):
    larger = sorted(r for r in reqs if r >= start)
    smaller = sorted((r for r in reqs if r < start), reverse=True)
    order = larger + smaller
    seq = [start] + larger
    if smaller:
        seq += [disk_max] + smaller   # sweep to the end of the disk, then reverse
    return order, movement(seq)


def cscan(reqs, start, disk_min, disk_max):
    larger = sorted(r for r in reqs if r >= start)
    smaller = sorted(r for r in reqs if r < start)
    order = larger + smaller
    seq = [start] + larger
    if smaller:
        seq += [disk_max, disk_min] + smaller   # sweep to end, jump to start, resume
    return order, movement(seq)


print("=" * 65)
print("  UniCore -- Disk Scheduling Algorithm Comparison")
print(f"  Requests = {requests}")
print(f"  Initial head position = {head}, Disk range = {disk_min}-{disk_max}, direction = upward")
print("=" * 65)

fcfs_order, fcfs_mv = fcfs(requests, head)
sstf_order, sstf_mv = sstf(requests, head)
scan_order, scan_mv = scan(requests, head, disk_max)
cscan_order, cscan_mv = cscan(requests, head, disk_min, disk_max)

algorithms = [
    ("FCFS", fcfs_order, fcfs_mv),
    ("SSTF", sstf_order, sstf_mv),
    ("SCAN", scan_order, scan_mv),
    ("C-SCAN", cscan_order, cscan_mv),
]

print(f"\n  {'Algorithm':<10}{'Seek Order'}")
for name, order, mv in algorithms:
    print(f"  {name:<10}{order}")

print(f"\n  {'Algorithm':<10}{'Total Head Movement (cylinders)'}")
print("  " + "-" * 45)
for name, order, mv in algorithms:
    print(f"  {name:<10}{mv}")

best = min(algorithms, key=lambda a: a[2])
print(f"\n[RESULT] Lowest total head movement: {best[0]} ({best[2]} cylinders)")
print("[RESULT] SCAN selected for production use -- predictable sweep pattern")
print("         and strong fairness compared to SSTF's starvation risk.")
print("=" * 65)
