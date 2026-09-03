"""
UniCore - Banker's Safety Algorithm
Resources: R1=Database connections, R2=File locks, R3=Printers, R4=Backup/IO channels
"""

processes = ['P0', 'P1', 'P2', 'P3']
resources = ['R1', 'R2', 'R3', 'R4']

allocation = [
    [1, 0, 0, 1],   # P0
    [1, 1, 1, 0],   # P1
    [1, 0, 1, 1],   # P2
    [0, 1, 0, 0],   # P3
]

maximum = [
    [3, 2, 2, 2],   # P0
    [2, 2, 2, 1],   # P1
    [4, 1, 3, 2],   # P2
    [2, 2, 2, 1],   # P3
]

available = [1, 1, 1, 1]

n = len(processes)
m = len(resources)

need = [[maximum[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]


def print_matrix(title, matrix):
    print(f"\n{title}")
    print("        " + "  ".join(resources))
    for i, row in enumerate(matrix):
        print(f"  {processes[i]:<4}  " + "  ".join(f"{v:2d}" for v in row))


def safety_algorithm(available, allocation, need):
    work = available.copy()
    finish = [False] * n
    safe_sequence = []
    steps = [("Initial", work.copy(), "--")]

    changed = True
    while changed:
        changed = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                work = [work[j] + allocation[i][j] for j in range(m)]
                finish[i] = True
                safe_sequence.append(processes[i])
                steps.append((f"Step {len(safe_sequence)}", work.copy(), processes[i]))
                changed = True

    is_safe = all(finish)
    return is_safe, safe_sequence, steps


print("=" * 60)
print("  UniCore -- Banker's Algorithm (Deadlock Avoidance)")
print("=" * 60)

print_matrix("Allocation Matrix:", allocation)
print_matrix("Maximum Matrix:", maximum)
print_matrix("Need Matrix (Max - Allocation):", need)
print(f"\nAvailable = {available}")

is_safe, safe_sequence, steps = safety_algorithm(available, allocation, need)

print("\nSafety Algorithm Trace:")
print(f"  {'Step':<10}{'Work Vector':<20}{'Process Chosen'}")
for step, work, proc in steps:
    print(f"  {step:<10}{str(work):<20}{proc}")

if is_safe:
    print(f"\n[RESULT] System is in a SAFE state.")
    print(f"[RESULT] Safe sequence: {' -> '.join(safe_sequence)}")
else:
    print(f"\n[RESULT] System is in an UNSAFE state -- deadlock possible.")

# Check P0 requesting [0,0,0,1]
print("\n" + "-" * 60)
print("  Additional Request Check: P0 requests [0, 0, 0, 1]")
print("-" * 60)

request = [0, 0, 0, 1]
p0 = 0

if all(request[j] <= need[p0][j] for j in range(m)) and all(request[j] <= available[j] for j in range(m)):
    tentative_available = [available[j] - request[j] for j in range(m)]
    tentative_allocation = [row.copy() for row in allocation]
    tentative_allocation[p0] = [allocation[p0][j] + request[j] for j in range(m)]
    tentative_need = [row.copy() for row in need]
    tentative_need[p0] = [need[p0][j] - request[j] for j in range(m)]

    print(f"Tentative Available = {tentative_available}")
    safe_after, seq_after, _ = safety_algorithm(tentative_available, tentative_allocation, tentative_need)

    if safe_after:
        print(f"[RESULT] Request can be GRANTED. New safe sequence: {' -> '.join(seq_after)}")
    else:
        print(f"[RESULT] Request must be DENIED -- granting it leads to an UNSAFE state.")
else:
    print("[RESULT] Request exceeds Need or Available -- request is invalid.")

print("=" * 60)
