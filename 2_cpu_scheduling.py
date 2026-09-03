"""
UniCore - CPU Scheduling: FCFS vs Round Robin (q=2)
"""

processes = [
    {"pid": "P1", "cls": "Interactive", "at": 0, "bt": 4},
    {"pid": "P2", "cls": "Interactive", "at": 1, "bt": 3},
    {"pid": "P3", "cls": "Interactive", "at": 2, "bt": 2},
    {"pid": "P4", "cls": "Interactive", "at": 3, "bt": 5},
    {"pid": "P5", "cls": "Background",  "at": 0, "bt": 8},
    {"pid": "P6", "cls": "Background",  "at": 0, "bt": 10},
    {"pid": "P7", "cls": "Interactive", "at": 4, "bt": 2},
    {"pid": "P8", "cls": "Background",  "at": 2, "bt": 6},
]


def fcfs(procs):
    procs = sorted([p.copy() for p in procs], key=lambda p: (p["at"], p["pid"]))
    time = 0
    gantt = []
    for p in procs:
        start = max(time, p["at"])
        end = start + p["bt"]
        p["start"] = start
        p["completion"] = end
        p["response"] = start - p["at"]
        p["turnaround"] = end - p["at"]
        p["waiting"] = p["turnaround"] - p["bt"]
        gantt.append((p["pid"], start, end))
        time = end
    return procs, gantt


def round_robin(procs, quantum=2):
    procs = [p.copy() for p in procs]
    for p in procs:
        p["remaining"] = p["bt"]
        p["response"] = None
        p["completion"] = None
    procs_sorted = sorted(procs, key=lambda p: (p["at"], p["pid"]))

    time = 0
    queue = []
    gantt = []
    arrived = [False] * len(procs_sorted)

    def enqueue_arrivals(current_time):
        for idx, p in enumerate(procs_sorted):
            if not arrived[idx] and p["at"] <= current_time:
                queue.append(p)
                arrived[idx] = True

    enqueue_arrivals(time)
    if not queue:
        time = min(p["at"] for p in procs_sorted)
        enqueue_arrivals(time)

    while queue:
        p = queue.pop(0)
        if p["response"] is None:
            p["response"] = time - p["at"]
        run = min(quantum, p["remaining"])
        start = time
        time += run
        p["remaining"] -= run
        gantt.append((p["pid"], start, time))
        enqueue_arrivals(time)
        if p["remaining"] > 0:
            queue.append(p)
        else:
            p["completion"] = time

    for p in procs_sorted:
        p["turnaround"] = p["completion"] - p["at"]
        p["waiting"] = p["turnaround"] - p["bt"]

    return procs_sorted, gantt


def print_gantt(gantt):
    line = " | ".join(f"{pid}({s}-{e})" for pid, s, e in gantt)
    print(line)


def print_results(title, procs, gantt):
    print(f"\n{title}")
    print_gantt(gantt)
    print(f"\n  {'PID':<5}{'Class':<13}{'AT':<4}{'BT':<4}{'WT':<5}{'TAT':<5}{'RT':<5}")
    total_wt = total_tat = total_rt = 0
    for p in sorted(procs, key=lambda x: x["pid"]):
        print(f"  {p['pid']:<5}{p['cls']:<13}{p['at']:<4}{p['bt']:<4}{p['waiting']:<5}{p['turnaround']:<5}{p['response']:<5}")
        total_wt += p["waiting"]
        total_tat += p["turnaround"]
        total_rt += p["response"]
    n = len(procs)
    print(f"\n  Average Waiting Time    = {total_wt / n:.3f}")
    print(f"  Average Turnaround Time = {total_tat / n:.3f}")
    print(f"  Average Response Time   = {total_rt / n:.3f}")
    return total_wt / n, total_tat / n, total_rt / n


print("=" * 65)
print("  UniCore -- CPU Scheduling: FCFS vs Round Robin (q=2)")
print("=" * 65)

fcfs_procs, fcfs_gantt = fcfs(processes)
fcfs_wt, fcfs_tat, fcfs_rt = print_results("FCFS Schedule:", fcfs_procs, fcfs_gantt)

rr_procs, rr_gantt = round_robin(processes, quantum=2)
rr_wt, rr_tat, rr_rt = print_results("Round Robin (q=2) Schedule:", rr_procs, rr_gantt)

print("\n" + "-" * 65)
print(f"  Comparison: FCFS avg RT = {fcfs_rt:.3f}  |  RR avg RT = {rr_rt:.3f}")
print(f"  Round Robin reduces average response time by "
      f"{fcfs_rt - rr_rt:.3f} time units for interactive services.")
print("=" * 65)
