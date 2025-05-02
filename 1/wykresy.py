import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import LogLocator

results_dir = "analysis_results"


def plot_grouped_bars(grouped_data, metric_name, title, ylabel, filename):
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(title)

    for i, (data_dict, variants, plot_title, subplot_idx) in enumerate(grouped_data):
        ax = axs[subplot_idx[0]][subplot_idx[1]]
        depths = sorted(data_dict.keys())
        width = 0.1
        x = np.arange(len(depths))
        max_values = []

        for j, variant in enumerate(variants):
            means = []
            for depth in depths:
                values = [entry[metric_name] for entry in data_dict[depth][variant] if metric_name in entry]
                mean = sum(values) / len(values) if values else 0
                means.append(mean)
                max_values.extend(values)
            ax.bar(x + j * width, means, width, label=variant.upper())

        ax.set_title(plot_title)
        ax.set_xlabel("Głębokość")
        ax.set_ylabel(ylabel)
        ax.set_xticks(x + width * (len(variants) - 1) / 2)
        ax.set_xticklabels(depths)
        ax.legend()

        if subplot_idx == (0, 0) and metric_name == "max_depth_recursion":
            ax.set_yticks(np.arange(0, 25, 5))
        elif subplot_idx == (0, 0) and metric_name == "search_time":
            ax.set_yscale('log')
            ax.yaxis.set_major_locator(LogLocator(base=10.0, subs=(10.0,), numticks=6))
        elif subplot_idx == (0, 0) and metric_name == "processed_states":
            ax.set_yscale('log')
            ax.yaxis.set_major_locator(LogLocator(base=10.0, subs=(10.0,), numticks=6))
        elif subplot_idx == (0, 0) and metric_name == "visited_states":
            ax.set_yscale('log')
            ax.yaxis.set_major_locator(LogLocator(base=10.0, subs=(10.0,), numticks=6))

    plt.tight_layout(rect=(0, 0, 1, 0.96))
    os.makedirs("plots", exist_ok=True)
    plt.savefig(filename)
    plt.close()


data = []

bfs = []
dfs = []
astr = []

permutations = ["RDLU", "RDUL", "DRUL", "DRLU", "LURD", "LUDR", "ULRD", "ULDR"]
heuristics = ["manh", "hamm"]

bfs_by_depth_perm = {i: {perm: [] for perm in permutations} for i in range(1, 8)}
dfs_by_depth_perm = {i: {perm: [] for perm in permutations} for i in range(1, 8)}
astr_by_depth_heur = {i: {heur: [] for heur in heuristics} for i in range(1, 8)}

bfs_by_depth = {i: [] for i in range(1, 8)}
dfs_by_depth = {i: [] for i in range(1, 8)}
astr_by_depth = {i: [] for i in range(1, 8)}

for filename in os.listdir(results_dir):
    if not filename.endswith("_stats.txt"):
        continue

    parts = filename.split("_")
    depth = int(parts[1])
    alg = parts[3]
    variant = parts[4].split(".")[0]

    with open(os.path.join(results_dir, filename)) as f:
        lines = f.read().strip().split("\n")
        if len(lines) != 5:
            continue

        result = {
            "depth": depth,
            "alg": alg,
            "variant": variant,
            "filename": filename,
            "solution_length": int(lines[0]),
            "visited_states": int(lines[1]),
            "processed_states": int(lines[2]),
            "max_depth_recursion": int(lines[3]),
            "search_time": float(lines[4])
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




def plot_all_metrics():
    metrics = [
        ("search_time", "Czas wyszukiwania według głębokości i wariantu", "Czas [ms]", "search_time_plot.png"),
        ("max_depth_recursion", "Maksymalna osiągnięta głębokość według głębokości i wariantu", "maksymalna głębokość", "max_depth_recursion_plot.png"),
        ("processed_states", "Przetworzone stany według głębokości i wariantu", "przetworzone stany", "processed_states_plot.png"),
        ("visited_states", "Odwiedzone stany według głębokości i wariantu", "odwiedzone stany", "visited_states_plot.png"),
        ("solution_length", "Długość rozwiązania według głębokości", "długość rozwiązania", "solution_length_plot.png"),
    ]

    for metric_name, title, ylabel, filename in metrics:
        plot_grouped_bars(
            grouped_data=[
                (
                    {i: {"bfs": bfs_by_depth[i], "dfs": dfs_by_depth[i], "astr": astr_by_depth[i]} for i in range(1, 8)},
                    ["bfs", "dfs", "astr"],
                    "Porównanie strategii",
                    (0, 0)
                ),
                (astr_by_depth_heur, heuristics, "A* - heurystyki", (0, 1)),
                (bfs_by_depth_perm, permutations, "BFS - permutacje", (1, 0)),
                (dfs_by_depth_perm, permutations, "DFS - permutacje", (1, 1)),
            ],
            metric_name=metric_name,
            title=title,
            ylabel=ylabel,
            filename=f"plots/{filename}"
        )


plot_all_metrics()
