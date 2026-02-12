from pydantic import BaseModel
from datetime import datetime

class BaseMetric(BaseModel):
    vm_id: str
    timestamp: datetime
