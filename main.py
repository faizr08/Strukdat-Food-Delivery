from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db, get_current_user # Dependency database & auth

app = FastAPI()

@app.post("/api/m2/create", response_model=schemas.M2Response, status_code=status.HTTP_201_CREATED)
def create_m2_data(
    payload: schemas.M2CreateRequest, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Buat instance model database baru
    new_data = models.M2Feature(
        title=payload.title,
        description=payload.description,
        user_id=current_user["id"]
    )
    
    # Simpan ke database
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    
    return new_data