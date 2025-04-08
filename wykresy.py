import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load and process data
data = []
for filename in os.listdir("analysis_results"):
    if filename.endswith("_stats.txt"):
        parts = filename.split('_')
        try:
            depth = int(parts[1][1:])
            algorithm = parts[3]
            variant = parts[4]

            with open(os.path.join("analysis_results", filename), 'r') as f:
                lines = [line.strip() for line in f.readlines()]
                if len(lines) >= 4:
                    data.append({
                        'depth': depth,
                        'algorithm': algorithm,
                        'variant': variant,
                        'max_depth': int(lines[3])
                    })
        except (IndexError, ValueError):
            continue








plt.xlabel('Głębokość rozwiązania', fontsize=12)
plt.ylabel('Średnia maks. głębokość rekursji', fontsize=12)
plt.title('Porównanie wszystkich strategii', fontsize=14, pad=20)
plt.xticks(x + bar_width, all_depths)
plt.legend(fontsize=10)
plt.grid(True, axis='y', alpha=0.3)

# Plot 2: BFS variants
plt.subplot(2, 2, 2)
variants_bfs = grouped_bfs['variant'].unique()
for i, variant in enumerate(variants_bfs):
    subset = grouped_bfs[grouped_bfs['variant'] == variant]
    if not subset.empty:
        plt.bar(x + i * bar_width, subset['max_depth'], width=bar_width, label=f'BFS ({variant})')

plt.xlabel('Głębokość rozwiązania', fontsize=12)
plt.ylabel('Średnia maks. głębokość rekursji', fontsize=12)
plt.title('BFS - różne porządki ruchów', fontsize=14, pad=20)
plt.xticks(x + (len(variants_bfs) - 1) * bar_width / 2, all_depths)
plt.legend(fontsize=10)
plt.grid(True, axis='y', alpha=0.3)

# Plot 3: DFS variants
plt.subplot(2, 2, 3)
variants_dfs = grouped_dfs['variant'].unique()
for i, variant in enumerate(variants_dfs):
    subset = grouped_dfs[grouped_dfs['variant'] == variant]
    if not subset.empty:
        plt.bar(x + i * bar_width, subset['max_depth'], width=bar_width, label=f'DFS ({variant})')

plt.xlabel('Głębokość rozwiązania', fontsize=12)
plt.ylabel('Średnia maks. głębokość rekursji', fontsize=12)
plt.title('DFS - różne porządki ruchów', fontsize=14, pad=20)
plt.xticks(x + (len(variants_dfs) - 1) * bar_width / 2, all_depths)
plt.legend(fontsize=10)
plt.grid(True, axis='y', alpha=0.3)

# Plot 4: A* heuristics
plt.subplot(2, 2, 4)
variants_astar = ['hamm', 'manh']
for i, variant in enumerate(variants_astar):
    subset = grouped_astar[grouped_astar['variant'] == variant]
    if not subset.empty:
        plt.bar(x + i * bar_width, subset['max_depth'], width=bar_width, label=f'A* ({variant})')

plt.xlabel('Głębokość rozwiązania', fontsize=12)
plt.ylabel('Średnia maks. głębokość rekursji', fontsize=12)
plt.title('A* - różne heurystyki', fontsize=14, pad=20)
plt.xticks(x + bar_width / 2, all_depths)
plt.legend(fontsize=10)
plt.grid(True, axis='y', alpha=0.3)

plt.tight_layout(pad=3.0)
plt.savefig('porownanie_rekursji_slupki.png', dpi=300, bbox_inches='tight')
plt.show()