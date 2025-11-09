from pydantic import BaseModel
from datetime import date
from typing import Dict, List, Optional

class WheelSpecFields(BaseModel):
    treadDiameterNew: Optional[str]
    lastShopIssueSize: Optional[str]
    condemningDia: Optional[str]
    wheelGauge: Optional[str]
    # Add remaining fields as needed...

class WheelSpecCreate(BaseModel):
    formNumber: str
    submittedBy: str
    submittedDate: date
    fields: Dict[str, str]

class WheelSpecResponse(BaseModel):
    success: bool
    message: str
    data: Dict
