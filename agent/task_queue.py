from enum import Enum
class TaskPriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
class _Queue:
    def submit(self, goal="", priority=None, speak=None):
        return "stub-task-id"
_q = _Queue()
def get_queue(): return _q
