"""优先级调度"""
from typing import List, Optional
from .base import SchedulerBase
from ..process import Process


class PriorityScheduler(SchedulerBase):
    def __init__(self, dynamic: bool = False):
        self.dynamic = dynamic
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

        # 动态优先级：等待时间越长优先级越高（老化）
        if self.dynamic:
            for p in self.ready_queue:
                # 等待时间增加，优先级数字减小（更高优先级）
                p.priority = max(1, p.priority - (current_time - p.arrive_time) // 10)

        # 按优先级排序（数字越小优先级越高）
        self.ready_queue.sort(key=lambda p: p.priority)

        # 抢占逻辑
        if self.current_process:
            if self.ready_queue and self.ready_queue[0].priority < self.current_process.priority:
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
        return True

    def reset(self) -> None:
        self.ready_queue.clear()
        self.current_process = None