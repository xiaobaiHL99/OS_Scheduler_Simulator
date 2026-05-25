"""输入处理模块"""
from typing import List
import random
from ..process import Process

def read_from_file(filename: str) -> List[Process]:
    """从文件读取进程信息"""
    processes = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split()
                    if len(parts) >= 3:
                        pid = int(parts[0])
                        arrive_time = int(parts[1])
                        burst_time = int(parts[2])
                        priority = int(parts[3]) if len(parts) > 3 else 0
                        processes.append(Process(pid, arrive_time, burst_time, priority))
    except FileNotFoundError:
        print(f"文件 {filename} 不存在，使用默认数据")
        return get_default_processes()
    return processes

def get_default_processes() -> List[Process]:
    """默认测试数据"""
    return [
        Process(1, 0, 5, 3),
        Process(2, 2, 3, 1),
        Process(3, 4, 2, 2),
        Process(4, 6, 4, 4),
    ]

def generate_random_processes(count: int = 5, max_arrive: int = 10, max_burst: int = 8) -> List[Process]:
    """随机生成进程"""
    processes = []
    for i in range(1, count + 1):
        arrive_time = random.randint(0, max_arrive)
        burst_time = random.randint(1, max_burst)
        priority = random.randint(1, 5)
        processes.append(Process(i, arrive_time, burst_time, priority))
    return sorted(processes, key=lambda p: p.arrive_time)