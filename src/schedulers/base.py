"""调度器抽象基类"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..process import Process

class SchedulerBase(ABC):
    @abstractmethod
    def add_process(self, process: Process) -> None:
        """添加一个进程"""
        pass

    @abstractmethod
    def next_process(self, current_time: int) -> Optional[Process]:
        """选择下一个要执行的进程，返回None表示空闲"""
        pass

    @abstractmethod
    def is_preemptive(self) -> bool:
        """是否为抢占式调度"""
        pass

    def on_tick(self, current_time: int) -> None:
        """每个时间单位调用一次（可选覆盖）"""
        pass

    def reset(self) -> None:
        """重置调度器状态"""
        pass

    def get_name(self) -> str:
        return self.__class__.__name__