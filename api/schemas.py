from pydantic import BaseModel
from typing import Optional

class DetectionBase(BaseModel):
    file_name: str
    class_id: int
    x_center: float
    y_center: float
    width: float
    height: float
    confidence: Optional[float] = None

class DetectionCreate(DetectionBase):
    pass

class Detection(DetectionBase):
    id: int
    timestamp: str

    class Config:
        from_attributes = True

# NEW SCHEMA: TelegramMessage
class MessageBase(BaseModel):
    channel_name: str
    message_text: str
    media_link: Optional[str] = None
    media_type: Optional[str] = None
    timestamp_utc: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int

    class Config:
        from_attributes = True