from .base import BaseMetric

class UsageMetric(BaseMetric):
    cpu_percent: float
    memory_percent: float
