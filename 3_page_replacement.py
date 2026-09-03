"""
UniCore - Page Replacement: FIFO vs LRU vs Optimal
Reference string: 1 2 3 4 1 2 5 1 2 3 4 5 1 2 3 4 5
"""

ref_string = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]


def fifo(refs, n_frames):
    frames = []
    faults = 0
    trace = []
    for page in refs:
        if page not in frames:
            faults += 1
            if len(frames) >= n_frames:
                frames.pop(0)
            frames.append(page)
            trace.append((page, list(frames), "FAULT"))
        else:
            trace.append((page, list(frames), "hit"))
    return faults, trace


def lru(refs, n_frames):
    frames = []
    faults = 0
    trace = []
    for page in refs:
        if page not in frames:
            faults += 1
            if len(frames) >= n_frames:
                frames.pop(0)
            frames.append(page)
            trace.append((page, list(frames), "FAULT"))
        else:
            frames.remove(page)
            frames.append(page)
            trace.append((page, list(frames), "hit"))
    return faults, trace


def optimal(refs, n_frames):
    frames = []
    faults = 0
    trace = []
    for i, page in enumerate(refs):
        if page not in frames:
            faults += 1
            if len(frames) >= n_frames:
                future = refs[i + 1:]
                farthest, victim = -1, frames[0]
                for f in frames:
                    if f not in future:
                        victim = f
                        break
                    else:
                        idx = future.index(f)
                        if idx > farthest:
                            farthest = idx
                            victim = f
                frames.remove(victim)
            frames.append(page)
            trace.append((page, list(frames), "FAULT"))
        else:
            trace.append((page, list(frames), "hit"))
    return faults, trace


print("=" * 60)
print("  UniCore -- Page Replacement Algorithm Comparison")
print(f"  Reference string: {ref_string}")
print("=" * 60)

results = {}
for n_frames in (3, 4):
    print(f"\n--- Frames = {n_frames} ---")
    for name, func in (("FIFO", fifo), ("LRU", lru), ("Optimal", optimal)):
        faults, trace = func(ref_string, n_frames)
        results[(name, n_frames)] = faults
        print(f"  {name:<8} -> Page faults = {faults}")

print("\n" + "-" * 60)
print("  Summary Table")
print("-" * 60)
print(f"  {'Frames':<8}{'FIFO':<8}{'LRU':<8}{'Optimal':<8}")
for n_frames in (3, 4):
    print(f"  {n_frames:<8}{results[('FIFO', n_frames)]:<8}{results[('LRU', n_frames)]:<8}{results[('Optimal', n_frames)]:<8}")

if results[("FIFO", 4)] > results[("FIFO", 3)]:
    print("\n[OBSERVATION] FIFO faults INCREASED when frames grew from 3 to 4"
          " -> Belady's Anomaly confirmed.")
else:
    print("\n[OBSERVATION] No Belady's Anomaly observed for FIFO in this run.")

print("=" * 60)
