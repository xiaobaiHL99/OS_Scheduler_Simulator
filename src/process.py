"""进程类定义"""
from typing import List, Optional


class Process:
    def __init__(self, pid: int, arrive_time: int, burst_time: int, priority: int = 0):
        self.pid = pid
        self.arrive_time = arrive_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.original_priority = priority  # 用于动态优先级
        self.start_time = None
        self.finish_time = None
        self.waiting_time = 0

    def __repr__(self):
        return f"P{self.pid}"

    def __str__(self):
        return f"进程{self.pid}: 到达={self.arrive_time}, 运行={self.burst_time}, 优先级={self.priority}"

    def reset(self):
        """重置进程状态"""
        self.remaining_time = self.burst_time
        self.start_time = None
        self.finish_time = None
        self.waiting_time = 0
        self.priority = self.original_priority