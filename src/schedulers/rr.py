"""RR 时间片轮转调度"""
from typing import List, Optional
from collections import deque
from .base import SchedulerBase
from ..process import Process


class RRScheduler(SchedulerBase):
    def __init__(self, time_quantum: int = 4):
        self.time_quantum = time_quantum
        self.queue = deque()
        self.all_processes = []
        self.current_process = None
        self.current_time_slice = 0

    def add_process(self, process: Process) -> None:
        self.all_processes.append(process)

    def next_process(self, current_time: int) -> Optional[Process]:
        # 将到达的进程加入队列尾部
        for p in self.all_processes[:]:
            if p.arrive_time <= current_time and p.remaining_time > 0:
                if p not in self.queue and p != self.current_process:
                    self.queue.append(p)
                if p in self.all_processes:
                    self.all_processes.remove(p)

        # 时间片用完，当前进程放回队尾
        if self.current_process and self.current_time_slice >= self.time_quantum:
            if self.current_process.remaining_time > 0:
                self.queue.append(self.current_process)
            self.current_process = None
            self.current_time_slice = 0

        # 选择新进程
        if not self.current_process and self.queue:
            self.current_process = self.queue.popleft()
            if self.current_process.start_time is None:
                self.current_process.start_time = current_time
            self.current_time_slice = 0
            return self.current_process

        return self.current_process

    def on_tick(self, current_time: int) -> None:
        if self.current_process:
            self.current_time_slice += 1

    def is_preemptive(self) -> bool:
        return True

    def reset(self) -> None:
        self.queue.clear()
        self.current_process = None
        self.current_time_slice = 0