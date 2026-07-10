from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models, schemas, auth, auth_utils

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CuroME API")

# --- Registration Endpoint ---
@app.post("/auth/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Check if email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Hash the password
    hashed_pw = auth.hash_password(user.password)
    
    # 3. Create user object
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role,
        name=user.name,
        age=user.age,
        gender=user.gender,
        phone=user.phone,
        # Generate patient_id if role is patient
        patient_id=f"PAT-{user.name[:3].upper()}{user.age or 0}" if user.role == "patient" else None
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- Login Endpoint ---
@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Find the user
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # 2. Verify credentials
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )
    
    # 3. Generate JWT Token
    access_token = auth_utils.create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"message": "CuroME API is running!"}