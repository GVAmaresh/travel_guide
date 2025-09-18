
import os
import json
from datetime import datetime, timedelta
from typing import Dict

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from src.core.user_creation import get_user, verify_password
from fastapi import Depends, HTTPException, status
from firebase_admin import firestore
from src.core.config import settings
from src.core.user_creation import create_user as create_new_user
from src.core.session_manager import create_session, get_session, update_session
from src.agents.logic import run_root_agent, run_summary_agent, generate_final_prompt
from .models import PlanTripRequest, GenerateSummaryRequest, UpdateSummaryRequest

class UserCreate(BaseModel):
    username: str
    password: str
    


SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

class ChatRequest(BaseModel):
    message: str

class Token(BaseModel):
    access_token: str
    token_type: str

app = FastAPI(
    title="TravelHues AI Agent API",
    description="API to interact with the TravelHues planning agent."
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("token = ",token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id

@app.post("/register", status_code=status.HTTP_201_CREATED, tags=["Authentication"])
async def register_new_user(user_data: UserCreate):
    db = firestore.client()

    if get_user(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    create_new_user(db, user_data.username, user_data.password)
    return {"message": f"User '{user_data.username}' created successfully"}


@app.post("/token", response_model=Token, tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = firestore.client()
    user = get_user(db, form_data.username)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise credentials_exception
    
    user_id = user["username"]
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/plan-trip", status_code=status.HTTP_201_CREATED, tags=["Planning"])
async def plan_trip(
    request: PlanTripRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    analysis = run_root_agent(request.destination)
    initial_data = {
        "origin": request.origin,
        "destination": request.destination,
        "dates": request.dates.model_dump(),
        "is_flexible": request.is_flexible,
        "analysis": analysis
    }
    session = create_session(user_id=current_user_id, initial_data=initial_data)
    
    return {
        "session_id": session["session_id"],
        "status": "success",
        "analysis": analysis
    }

@app.post("/generate-summary", tags=["Planning"])
async def generate_summary(
    request: GenerateSummaryRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    session = get_session(request.session_id)
    if not session or session.get("user_uid") != current_user_id:
        raise HTTPException(status_code=404, detail="Session not found or access denied")

    summary_text = run_summary_agent(
        session_data=session, 
        preferences=request.preferences.model_dump(), 
        details=request.additional_details
    )
    
    update_data = {
        "preferences": request.preferences.model_dump(),
        "additional_details": request.additional_details,
        "summary": summary_text,
        "status": "summary_generated"
    }
    update_session(request.session_id, update_data)
    
    return {
        "session_id": request.session_id,
        "status": "summary_generated",
        "summary": summary_text,
        "user_actions": ["confirm", "edit"]
    }

@app.post("/update-summary", tags=["Planning"])
async def update_summary(
    request: UpdateSummaryRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    session = get_session(request.session_id)
    if not session or session.get("user_uid") != current_user_id:
        raise HTTPException(status_code=404, detail="Session not found or access denied")

    summary_to_use = ""
    if request.action == "edit":
        if not request.edited_summary_text:
            raise HTTPException(status_code=400, detail="edited_summary_text is required for edit action")
        summary_to_use = request.edited_summary_text
        update_session(request.session_id, {"summary": summary_to_use})
    else: # confirm
        summary_to_use = session.get("summary")

    final_prompt = generate_final_prompt(summary_to_use)
    
    update_session(request.session_id, {
        "final_prompt_for_itinerary_agent": final_prompt,
        "status": "prompt_generated"
    })

    return {
        "session_id": request.session_id,
        "status": "prompt_generated",
        "message": "Summary confirmed. Generating itinerary now.",
        "final_prompt_for_itinerary_agent": final_prompt
    }











