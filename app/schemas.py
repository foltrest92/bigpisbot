from datetime import datetime
from pydantic import BaseModel


class SSize(BaseModel):
    chat_id: int
    user_id: int
    size: int
    last_update: datetime
    isUpdated: bool