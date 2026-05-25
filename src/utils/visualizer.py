"""可视化模块"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import List, Tuple, Dict


def draw_gantt(timeline: List[Tuple[int, int]], title: str, save_path: str = None):
    """
    绘制甘特图
    timeline: [(start_time, pid), ...]
    """
    fig, ax = plt.subplots(figsize=(12, 3))

    current_pid = None
    start_time = 0

    for i, (time, pid) in enumerate(timeline):
        if pid != current_pid:
            if current_pid is not None:
                ax.broken_barh([(start_time, time - start_time)], (0, 1),
                               facecolors=plt.cm.Set3(current_pid % 10))
                ax.text(start_time + (time - start_time) / 2, 0.5, f'P{current_pid}',
                        ha='center', va='center', fontsize=10)
            current_pid = pid
            start_time = time

    if current_pid is not None:
        ax.broken_barh([(start_time, len(timeline) - start_time)], (0, 1),
                       facecolors=plt.cm.Set3(current_pid % 10))
        ax.text(start_time + (len(timeline) - start_time) / 2, 0.5, f'P{current_pid}',
                ha='center', va='center', fontsize=10)

    ax.set_xlabel('时间', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.set_yticks([])
    ax.set_xlim(0, len(timeline))
    ax.grid(True, axis='x', alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    else:
        plt.show()


def compare_schedulers(results: Dict[str, dict], save_path: str = None):
    """对比多个调度算法的性能指标"""
    algorithms = list(results.keys())
    turnaround_times = [results[algo]['avg_turnaround'] for algo in algorithms]
    waiting_times = [results[algo]['avg_waiting'] for algo in algorithms]

    x = range(len(algorithms))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar([i - width / 2 for i in x], turnaround_times, width, label='平均周转时间', color='skyblue')
    bars2 = ax.bar([i + width / 2 for i in x], waiting_times, width, label='平均等待时间', color='lightcoral')

    ax.set_xlabel('调度算法', fontsize=12)
    ax.set_ylabel('时间', fontsize=12)
    ax.set_title('调度算法性能对比', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=15)
    ax.legend()
    ax.grid(True, axis='y', alpha=0.3)

    # 添加数值标签
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height, f'{height:.2f}',
                ha='center', va='bottom')
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height, f'{height:.2f}',
                ha='center', va='bottom')

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    else:
        plt.show()


def print_compare_table(results: Dict[str, dict]):
    """打印对比表格"""
    print("\n" + "=" * 80)
    print("调度算法性能对比表")
    print("=" * 80)
    print(f"{'算法':<20} {'平均周转时间':<15} {'平均等待时间':<15} {'平均响应时间':<15}")
    print("-" * 80)
    for algo, metrics in results.items():
        print(
            f"{algo:<20} {metrics['avg_turnaround']:<15.2f} {metrics['avg_waiting']:<15.2f} {metrics['avg_response']:<15.2f}")
    print("=" * 80)