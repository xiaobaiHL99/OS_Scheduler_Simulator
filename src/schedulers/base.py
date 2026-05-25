\"\"\"调度器抽象基类\"\"\"
from abc import ABC, abstractmethod
from typing import List, Optional
from ..process import Process

class SchedulerBase(ABC):
    @abstractmethod
        \"\"\"添加一个进程\"\"\"
        pass

    @abstractmethod
        \"\"\"选择下一个要执行的进程，返回None表示空闲\"\"\"
        pass

    @abstractmethod
        \"\"\"是否为抢占式调度\"\"\"
        pass

        \"\"\"每个时间单位调用一次（可选覆盖）\"\"\"
        pass

        \"\"\"重置调度器状态\"\"\"
        pass

        return self.__class__.__name__
