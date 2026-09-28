'''[ Incoming Request ]  ---> [ Input Schema ]   ---> [ CRUD Function ] ---> [ Database ]
 (Admin / User)             (Validation)           (Executes SQL)         (Storage)
                                                                             |
[ Outgoing Response ] <--- [ Output Schema ]  <--- [ CRUD Function ] <-------+
 (JSON Output)              (Formatting)           (Fetches Data)
'''

"""
Rules that guide what is request is coming  in into the crud and what output is coming out of the crud 

"""


from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class FlagCreate(BaseModel):
    """What a client sends to create a new flag."""
    key: str = Field(..., min_length=1, description="Unique identifier, e.g. 'new-checkout-button'")
    description: str = ""
    enabled: bool = False
    rollout_percentage: int = Field(0, ge=0, le=100)

class FlagUpdate(BaseModel):
    """
    What a client sends to update a flag. Every field is optional —
    a client might only want to flip `enabled`, without resending
    everything else.
    """
    description: Optional[str] = None
    enabled: Optional[bool] = None
    rollout_percentage: Optional[int] = Field(None, ge=0, le=100)


class FlagResponse(BaseModel):
    """What the API sends back — includes the fields the database owns."""
    id: int
    key: str
    description: str
    enabled: bool
    rollout_percentage: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True