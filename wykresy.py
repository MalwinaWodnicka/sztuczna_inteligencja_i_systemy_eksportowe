import os
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


resultsDir = "analysis_results"


def plot_grouped_bars(grouped_data, metric_name, title, ylabel, filename):
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(title)

    for i, (data_dict, variants, plot_title, subplot_idx) in enumerate(grouped_data):
        ax = axs[subplot_idx[0]][subplot_idx[1]]

        depths = sorted(data_dict.keys())
        width = 0.1
        x = np.arange(len(depths))

        for j, variant in enumerate(variants):
            means = []
            for d in depths:
                values = [entry[metric_name] for entry in data_dict[d][variant] if metric_name in entry]
                mean = sum(values) / len(values) if values else 0
                means.append(mean)
            ax.bar(x + j * width, means, width, label=variant.upper())

        ax.set_title(plot_title)
        ax.set_xlabel("Głębokość")
        ax.set_ylabel(ylabel)
        ax.set_xticks(x + width * (len(variants) - 1) / 2)
        ax.set_xticklabels(depths)
        ax.legend()

        if subplot_idx == (0, 0) and (metric_name == "searchTime" or "visitedStates" or "processedStates"):
            ax.set_yscale('log')

    plt.tight_layout(rect=(0, 0, 1, 0.96))
    os.makedirs("plots", exist_ok=True)
    plt.savefig(filename)
    plt.close()


data = []

bfs = []
dfs = []
astr = []

bfs_by_depth_perm = {
    i: {perm: [] for perm in ["RDLU", "RDUL", "DRUL", "DRLU", "LURD","LUDR","ULRD", "ULDR"]} for i in
    range(1, 8)}
dfs_by_depth_perm = {
    i: {perm: [] for perm in ["RDLU", "RDUL", "DRUL", "DRLU", "LURD","LUDR","ULRD", "ULDR"]} for i in
    range(1, 8)}
astr_by_depth_heur = {i: {heur: [] for heur in ["manh", "hamm"]} for i in range(1, 8)}

bfs_by_depth = {i: [] for i in range(1, 8)}
dfs_by_depth = {i: [] for i in range(1, 8)}
astr_by_depth = {i: [] for i in range(1, 8)}
strategies_by_depth = {
    i: {
        "bfs": bfs_by_depth[i],
        "dfs": dfs_by_depth[i],
        "astr": astr_by_depth[i]
    } for i in range(1, 8)
}

for filename in os.listdir(resultsDir):
    if not filename.endswith("_stats.txt"):
        continue

    parts = filename.split("_")
    depth = int(parts[1])
    alg = parts[3]
    variant = parts[4].split(".")[0]

    with open(os.path.join(resultsDir, filename)) as f:
        lines = f.read().strip().split("\n")
        if len(lines) != 5:
            continue

        result = {
            "depth": depth,
            "alg": alg,
            "variant": variant,
            "filename": filename,
            "solutionLength": int(lines[0]),
            "visitedStates": int(lines[1]),
            "processedStates": int(lines[2]),
            "maxDepthRecursion": int(lines[3]),
            "searchTime": float(lines[4])
        }

        data.append(result)

        if alg == "bfs":
            bfs.append(result)
            bfs_by_depth[depth].append(result)
            if variant in bfs_by_depth_perm[depth]:
                bfs_by_depth_perm[depth][variant].append(result)

        elif alg == "dfs":
            dfs.append(result)
            dfs_by_depth[depth].append(result)
            if variant in dfs_by_depth_perm[depth]:
                dfs_by_depth_perm[depth][variant].append(result)

        elif alg == "astr":
            astr.append(result)
            astr_by_depth[depth].append(result)
            if variant in astr_by_depth_heur[depth]:
                astr_by_depth_heur[depth][variant].append(result)




plot_grouped_bars(
    grouped_data=[
        (
            {i: {"bfs": bfs_by_depth[i], "dfs": dfs_by_depth[i], "astr": astr_by_depth[i]} for i in range(1, 8)},
            ["bfs", "dfs", "astr"],
            "Porównanie strategii",
            (0, 0)
        ),
        (astr_by_depth_heur, ["manh", "hamm"], "A* - heurystyki", (0, 1)),
        (bfs_by_depth_perm, ["RDLU", "RDUL", "DRUL", "DRLU", "LURD","LUDR","ULRD", "ULDR"], "BFS - permutacje", (1, 0)),
        (dfs_by_depth_perm, ["RDLU", "RDUL", "DRUL", "DRLU", "LURD","LUDR","ULRD", "ULDR"], "DFS - permutacje", (1, 1)),
    ],
    metric_name="searchTime",
    title="Czas wyszukiwania według głębokości i wariantu",
    ylabel="Czas [s]",
    filename="plots/searchTimePlot.png"
)

plot_grouped_bars(
    grouped_data=[
        (
            {i: {"bfs": bfs_by_depth[i], "dfs": dfs_by_depth[i], "astr": astr_by_depth[i]} for i in range(1, 8)},
            ["bfs", "dfs", "astr"],
            "Porównanie strategii",
            (0, 0)
        ),
        (astr_by_depth_heur, ["manh", "hamm"], "A* - heurystyki", (0, 1)),
        (bfs_by_depth_perm, ["RDLU", "RDUL", "DRUL", "DRLU", "LURD", "LUDR", "ULRD", "ULDR"], "BFS - permutacje",
         (1, 0)),
        (dfs_by_depth_perm, ["RDLU", "RDUL", "DRUL", "DRLU", "LURD", "LUDR", "ULRD", "ULDR"], "DFS - permutacje",
         (1, 1)),
    ],
    metric_name="maxDepthRecursion",
    title="Czas wyszukiwania według głębokości i wariantu",
    ylabel="Czas [s]",
    filename="plots/maxDepthRecursionPlot.png"
)

plot_grouped_bars(
    grouped_data=[
        (
            {i: {"bfs": bfs_by_depth[i], "dfs": dfs_by_depth[i], "astr": astr_by_depth[i]} for i in range(1, 8)},
            ["bfs", "dfs", "astr"],
            "Porównanie strategii",
            (0, 0)
        ),
        (astr_by_depth_heur, ["manh", "hamm"], "A* - heurystyki", (0, 1)),
        (bfs_by_depth_perm, ["RDLU", "RDUL", "DRUL", "DRLU", "LURD", "LUDR", "ULRD", "ULDR"], "BFS - permutacje",
         (1, 0)),
        (dfs_by_depth_perm, ["RDLU", "RDUL", "DRUL", "DRLU", "LURD", "LUDR", "ULRD", "ULDR"], "DFS - permutacje",
         (1, 1)),
    ],
    metric_name="processedStates",
    title="Czas wyszukiwania według głębokości i wariantu",
    ylabel="Czas [s]",
    filename="plots/processedStatesPlot.png"
)

plot_grouped_bars(
    grouped_data=[
        (
            {i: {"bfs": bfs_by_depth[i], "dfs": dfs_by_depth[i], "astr": astr_by_depth[i]} for i in range(1, 8)},
            ["bfs", "dfs", "astr"],
            "Porównanie strategii",
            (0, 0)
        ),
        (astr_by_depth_heur, ["manh", "hamm"], "A* - heurystyki", (0, 1)),
        (bfs_by_depth_perm, ["RDLU", "RDUL", "DRUL", "DRLU", "LURD", "LUDR", "ULRD", "ULDR"], "BFS - permutacje",
         (1, 0)),
        (dfs_by_depth_perm, ["RDLU", "RDUL", "DRUL", "DRLU", "LURD", "LUDR", "ULRD", "ULDR"], "DFS - permutacje",
         (1, 1)),
    ],
    metric_name="visitedStates",
    title="Czas wyszukiwania według głębokości i wariantu",
    ylabel="Czas [s]",
    filename="plots/visitedStatesPlot.png"
)

plot_grouped_bars(
    grouped_data=[
        (
            {i: {"bfs": bfs_by_depth[i], "dfs": dfs_by_depth[i], "astr": astr_by_depth[i]} for i in range(1, 8)},
            ["bfs", "dfs", "astr"],
            "Porównanie strategii",
            (0, 0)
        ),
        (astr_by_depth_heur, ["manh", "hamm"], "A* - heurystyki", (0, 1)),
        (bfs_by_depth_perm, ["RDLU", "RDUL", "DRUL", "DRLU", "LURD", "LUDR", "ULRD", "ULDR"], "BFS - permutacje",
         (1, 0)),
        (dfs_by_depth_perm, ["RDLU", "RDUL", "DRUL", "DRLU", "LURD", "LUDR", "ULRD", "ULDR"], "DFS - permutacje",
         (1, 1)),
    ],
    metric_name="solutionLength",
    title="Czas wyszukiwania według głębokości i wariantu",
    ylabel="Czas [s]",
    filename="plots/solutionLengthPlot.png"
)