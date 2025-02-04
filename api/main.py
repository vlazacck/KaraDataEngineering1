from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import get_db, engine, Base
from api.models import ObjectDetection, TelegramMessage  # Add TelegramMessage model
from api.schemas import Detection, DetectionCreate, Message, MessageCreate  # Add Message schema
from api.crud import (
    get_detections,
    create_detection,
    update_detection,
    delete_detection,
    get_detection_by_id,
    get_messages  # Add CRUD function for messages
)

app = FastAPI()

# Create tables (if they don't exist)
Base.metadata.create_all(bind=engine)

@app.get("/detections/", response_model=list[Detection])
def read_detections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    detections = get_detections(db, skip=skip, limit=limit)
    return detections

@app.get("/detections/{detection_id}", response_model=Detection)
def read_detection(detection_id: int, db: Session = Depends(get_db)):
    db_detection = get_detection_by_id(db, detection_id=detection_id)
    if db_detection is None:
        raise HTTPException(status_code=404, detail=f"Detection with ID {detection_id} not found")
    return db_detection

@app.post("/detections/", response_model=Detection)
def create_detection_endpoint(detection: DetectionCreate, db: Session = Depends(get_db)):
    return create_detection(db=db, detection=detection)

@app.put("/detections/{detection_id}", response_model=Detection)
def update_detection_endpoint(detection_id: int, detection: DetectionCreate, db: Session = Depends(get_db)):
    updated_detection = update_detection(db=db, detection_id=detection_id, detection=detection)
    if updated_detection is None:
        raise HTTPException(status_code=404, detail=f"Detection with ID {detection_id} not found")
    return updated_detection

@app.delete("/detections/{detection_id}")
def delete_detection_endpoint(detection_id: int, db: Session = Depends(get_db)):
    delete_detection(db=db, detection_id=detection_id)
    return {"detail": "Detection deleted"}

# NEW ENDPOINT: Fetch Telegram messages
@app.get("/messages/", response_model=list[Message])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = get_messages(db, skip=skip, limit=limit)
    return messages