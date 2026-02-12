from pydantic import BaseModel

class RightsizingResult(BaseModel):
    vm_id: str
    current_size: str
    recommended_size: str
    reason: str
