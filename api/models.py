from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from api.database import Base
from datetime import datetime
class ObjectDetection(Base):
    __tablename__ = "object_detections"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    class_id = Column(Integer, nullable=False)
    x_center = Column(Float, nullable=False)
    y_center = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    confidence = Column(Float)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

# NEW MODEL: TelegramMessage
class TelegramMessage(Base):
    __tablename__ = "cleaned_telegram_data"  # Use the appropriate table name

    id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String, nullable=False)
    message_text = Column(String, nullable=False)
    media_link = Column(String)
    media_type = Column(String)
    timestamp_utc = Column(TIMESTAMP, nullable=False)