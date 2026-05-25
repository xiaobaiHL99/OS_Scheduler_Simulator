"""FCFS 先来先服务调度"""
from typing import List, Optional
from collections import deque
from .base import SchedulerBase
from ..process import Process

class FCFSScheduler(SchedulerBase):
    def __init__(self):
        self.queue = deque()
        self.all_processes = []

    def add_process(self, process: Process) -> None:
        self.all_processes.append(process)

    def next_process(self, current_time: int) -> Optional[Process]:
        # 将到达的进程加入就绪队列
        for p in self.all_processes[:]:
            if p.arrive_time <= current_time and p.remaining_time > 0:
                if p not in self.queue:
                    self.queue.append(p)
                self.all_processes.remove(p)

        # 返回队首进程
        if self.queue:
            p = self.queue.popleft()
            if p.start_time is None:
                p.start_time = current_time
            return p
        return None

    def is_preemptive(self) -> bool:
        return False

    def reset(self) -> None:
        self.queue.clear()
        self.all_processes.clear()