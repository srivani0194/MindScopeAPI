from fastapi import APIRouter, Request
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import UserCreate, Token, MoodCreate, MoodOut
from app.models import User, MoodEntry
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.db import SessionLocal
from app.limiter import limiter
from sqlalchemy import func
from datetime import datetime, timedelta


router = APIRouter()


# database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

 # Root Welcome route       
@router.get("/")
def read_root():
    return {"message: Welcome to MindScope API!"}


@router.post("/token")
def fake_token():
    return {"access_token": "fake-token", "token_type": "bearer"}

# Register a new user
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hased_pw = hash_password(user.password)
    new_user = User(username=user.username, hashed_password = hased_pw)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

# Login and get JWT Token
@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session= Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username). first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    
    token = create_access_token({"sub": db_user.username})

    return {"access_token": token, "token_type": "bearer"}

# Enter the mood 
@router.post("/trackmood", response_model=MoodOut)
@limiter.limit("5/minute")
def create_mood(
    request: Request,
    entry: MoodCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    mood = MoodEntry(**entry.dict(), user_id=user.id)
    db.add(mood)
    db.commit()
    db.refresh(mood)
    return mood

# retrive the moods
@router.get("/trackmood", response_model=list[MoodOut])
def read_moods(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(MoodEntry).filter(MoodEntry.user_id == user.id).all()

# Update mood
@router.put("/trackmood/{id}", response_model=MoodOut)
def update_mood(id: int, entry: MoodCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    mood = db.query(MoodEntry).filter(MoodEntry.id == id, MoodEntry.user_id == user.id).first()
    if not mood:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    for key, value in entry.dict().items():
        setattr(mood, key, value)
    db.commit()
    db.refresh(mood)
    return mood

# Delete mood
@router.delete("/mood/{id}")
def delete_mood(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    mood = db.query(MoodEntry).filter(MoodEntry.id == id, MoodEntry.user_id == user.id).first()
    if not mood:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    db.delete(mood)
    db.commit()
    return {"message": "Mood deleted successfully"}

# summary of the mood
@router.get("/summary")
def get_mood_summary(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    today = datetime.utcnow().date()
    start_of_week = today - timedelta(days=today.weekday())

    # Query moods this week for the current user
    results = (
        db.query(MoodEntry.mood, func.count().label("count"))
        .filter(
            MoodEntry.user_id == user.id,
            MoodEntry.date >= start_of_week
        )
        .group_by(MoodEntry.mood)
        .all()
    )

    # Display the result as dictionary
    summary = {mood: count for mood, count in results}
    return {"summary": summary, "week_start": str(start_of_week), "today": str(today)}



