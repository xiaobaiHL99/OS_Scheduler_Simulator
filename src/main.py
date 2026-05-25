"""主程序入口 - 测试FCFS"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.schedulers.fcfs import FCFSScheduler
from src.utils.input_handler import read_from_file, get_default_processes

def main():
    print("=" * 60)
    print("操作系统课程设计 - 进程调度算法模拟器")
    print("=" * 60)

    # 读取进程数据
    processes = read_from_file("data/processes.txt")
    if not processes:
        processes = get_default_processes()

    print(f"\n共 {len(processes)} 个进程:")
    for p in processes:
        print(f"  {p}")

    # 运行 FCFS 调度
    print("\n" + "-" * 40)
    print("FCFS 调度算法结果")
    print("-" * 40)

    scheduler = FCFSScheduler()
    for p in processes:
        scheduler.add_process(p)

    time = 0
    completed = 0
    timeline = []

    while completed < len(processes):
        p = scheduler.next_process(time)
        if p:
            timeline.append((time, p.pid))
            p.remaining_time -= 1
            if p.remaining_time == 0:
                p.finish_time = time + 1
                completed += 1
        else:
            timeline.append((time, None))
        time += 1

    # 输出调度时间线
    print("调度时间线:")
    last_pid = None
    start_time = 0
    for t, pid in timeline:
        if pid != last_pid:
            if last_pid is not None:
                print(f"  P{last_pid}: [{start_time} → {t}]")
            last_pid = pid
            start_time = t
    if last_pid is not None:
        print(f"  P{last_pid}: [{start_time} → {len(timeline)}]")

    # 计算平均周转时间
    total_turnaround = 0
    for p in processes:
        turnaround = p.finish_time - p.arrive_time
        total_turnaround += turnaround
        print(f"P{p.pid}: 到达={p.arrive_time}, 完成={p.finish_time}, 周转={turnaround}")

    print(f"\n平均周转时间: {total_turnaround / len(processes):.2f}")

if __name__ == "__main__":
    main()