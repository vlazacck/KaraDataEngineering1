from sqlalchemy.orm import Session
from api.schemas import DetectionCreate

from api.models import ObjectDetection, TelegramMessage  # Add TelegramMessage model

def get_detections(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ObjectDetection).offset(skip).limit(limit).all()

def get_detection_by_id(db: Session, detection_id: int):
    return db.query(ObjectDetection).filter(ObjectDetection.id == detection_id).first()

def create_detection(db: Session, detection: DetectionCreate):
    db_detection = ObjectDetection(**detection.dict())
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    return db_detection

def update_detection(db: Session, detection_id: int, detection: DetectionCreate):
    db_detection = get_detection_by_id(db, detection_id)
    if db_detection:
        for key, value in detection.dict().items():
            setattr(db_detection, key, value)
        db.commit()
        db.refresh(db_detection)
    return db_detection

def delete_detection(db: Session, detection_id: int):
    db.query(ObjectDetection).filter(ObjectDetection.id == detection_id).delete()
    db.commit()

# NEW FUNCTION: Get Telegram messages
def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TelegramMessage).offset(skip).limit(limit).all()