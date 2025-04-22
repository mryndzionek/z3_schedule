import z3
import numpy as np
import matplotlib.pyplot as plt

sol = z3.Optimize()

t_set = [(8, 2), (16, 4), (24, 12)]
# t_set = [(8, 3), (11, 3), (14, 4)]
# t_set = [(5, 2), (7, 3), (35, 6)]
# t_set = [(3, 1), (8, 1), (12, 2), (16, 3), (48, 6)]
# t_set = [
#     (4, 1),
#     (8, 3),
#     (16, 6),
# ]

util = sum([w / p for p, w in t_set])
hyper_period = np.lcm.reduce([ts[0] for ts in t_set])
print(f"Hyper period: {hyper_period}")
print(f"Utilization: {util}")


def add_task(i, p, c):
    tv = z3.BoolVector(f"tf_{i}", hyper_period)

    for j in range(0, hyper_period, p):
        sol.add(
            z3.Sum([tv[j + k] for k in range(p)]) == c
        )  # guarantee wcet in each period

    # minimize context switches
    sol.minimize(z3.Sum([tv[j] != tv[j - 1] for j in range(1, hyper_period)]))

    return tv


def count_context_switches(schedule):
    schedule = schedule.T
    d = schedule[:][1:] != schedule[:][:-1]
    return d.any(1).sum()


tvs = [add_task(i + 1, *t) for i, t in enumerate(t_set)]
for j in range(hyper_period):
    sol.add(
        z3.Sum([t[j] for t in tvs]) <= 1
    )  # each time slot is assigned to at most one task (one CPU)

if sol.check() == z3.sat:
    m = sol.model()
    schedule = []
    for t in tvs:
        schedule.append([m.eval(t[j]).py_value() for j in range(hyper_period)])
    schedule = np.array(schedule)
    cs = count_context_switches(schedule)
    print(f"Context switches: {cs}")
    plt.figure(figsize=(14, 6), dpi=300, layout="constrained")
    plt.pcolormesh(np.flip(schedule), cmap="binary")
    plt.grid(True)
    plt.xticks(range(hyper_period))
    plt.title(f"[(period, wcet)] = {t_set}")
    plt.savefig("t_set.png")
    # plt.show()
else:
    print("Unschedulable")
