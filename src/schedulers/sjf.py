"""SJF 短作业优先调度"""
from typing import List, Optional
from .base import SchedulerBase
from ..process import Process


class SJFScheduler(SchedulerBase):
    def __init__(self, preemptive: bool = False):
        self.preemptive = preemptive
        self.ready_queue = []
        self.all_processes = []
        self.current_process = None

    def add_process(self, process: Process) -> None:
        self.all_processes.append(process)

    def next_process(self, current_time: int) -> Optional[Process]:
        # 将到达的进程加入就绪队列
        for p in self.all_processes[:]:
            if p.arrive_time <= current_time and p.remaining_time > 0:
                if p not in self.ready_queue and p != self.current_process:
                    self.ready_queue.append(p)
                if p in self.all_processes:
                    self.all_processes.remove(p)

        # 按剩余时间排序（SJF核心）
        self.ready_queue.sort(key=lambda p: p.remaining_time)

        # 抢占逻辑
        if self.preemptive and self.current_process:
            if (self.ready_queue and
                    self.ready_queue[0].remaining_time < self.current_process.remaining_time):
                # 抢占：当前进程放回队列
                self.ready_queue.insert(0, self.current_process)
                self.current_process = None

        # 选择新进程
        if not self.current_process and self.ready_queue:
            self.current_process = self.ready_queue.pop(0)
            if self.current_process.start_time is None:
                self.current_process.start_time = current_time
            return self.current_process

        return self.current_process

    def is_preemptive(self) -> bool:
        return self.preemptive

    def reset(self) -> None:
        self.ready_queue.clear()
        self.current_process = None