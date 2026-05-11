from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.models.calculation import Calculation
from app.models.user import User
from app.schemas.calculation import CalculationBase, CalculationResponse, CalculationUpdate
from app.schemas.token import TokenResponse
from app.schemas.user import UserCreate, UserResponse, UserLogin, UserUpdate, PasswordUpdate
from app.database import Base, get_db, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Calculations API",
    version="1.0.0",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/dashboard/view/{calc_id}", response_class=HTMLResponse)
def view_calculation_page(request: Request, calc_id: str):
    return templates.TemplateResponse("view_calculation.html", {"request": request, "calc_id": calc_id})


@app.get("/dashboard/edit/{calc_id}", response_class=HTMLResponse)
def edit_calculation_page(request: Request, calc_id: str):
    return templates.TemplateResponse("edit_calculation.html", {"request": request, "calc_id": calc_id})


@app.get("/profile-page", response_class=HTMLResponse)
def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})


@app.get("/health")
def read_health():
    return {"status": "ok"}


@app.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    user_data = user_create.dict(exclude={"confirm_password"})

    try:
        user = User.register(db, user_data)
        db.commit()
        db.refresh(user)
        return user
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/auth/login", response_model=TokenResponse)
def login_json(user_login: UserLogin, db: Session = Depends(get_db)):
    auth_result = User.authenticate(db, user_login.username, user_login.password)

    if auth_result is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = auth_result["user"]
    db.commit()

    expires_at = auth_result.get("expires_at")
    if expires_at and expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    elif not expires_at:
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)

    return TokenResponse(
        access_token=auth_result["access_token"],
        refresh_token=auth_result["refresh_token"],
        token_type="bearer",
        expires_at=expires_at,
        user_id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        is_verified=user.is_verified
    )


@app.post("/auth/token")
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    auth_result = User.authenticate(db, form_data.username, form_data.password)

    if auth_result is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": auth_result["access_token"],
        "token_type": "bearer"
    }


@app.get("/profile", response_model=UserResponse)
def get_profile(current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.put("/profile", response_model=UserResponse)
def update_profile(user_update: UserUpdate, current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.username:
        user.username = user_update.username
    if user_update.email:
        user.email = user_update.email
    if user_update.first_name:
        user.first_name = user_update.first_name
    if user_update.last_name:
        user.last_name = user_update.last_name

    db.commit()
    db.refresh(user)
    return user


@app.post("/profile/change-password")
def change_password(password_data: PasswordUpdate, current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.verify_password(password_data.current_password):
        raise HTTPException(status_code=400, detail="Current password incorrect")

    user.password = User.hash_password(password_data.new_password)
    db.commit()

    return {"message": "Password updated"}


@app.post("/calculations", response_model=CalculationResponse, status_code=201)
def create_calculation(calculation_data: CalculationBase, current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    calc = Calculation.create(
        calculation_type=calculation_data.type,
        user_id=current_user.id,
        inputs=calculation_data.inputs
    )
    calc.result = calc.get_result()

    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


@app.get("/calculations", response_model=List[CalculationResponse])
def list_calculations(current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    return db.query(Calculation).filter(Calculation.user_id == current_user.id).all()


@app.get("/calculations/{calc_id}", response_model=CalculationResponse)
def get_calculation(calc_id: str, current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(
        Calculation.id == calc_id,
        Calculation.user_id == current_user.id
    ).first()

    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    return calc


@app.put("/calculations/{calc_id}", response_model=CalculationResponse)
def update_calculation(calc_id: str, calculation_update: CalculationUpdate, current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(
        Calculation.id == calc_id,
        Calculation.user_id == current_user.id
    ).first()

    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    if calculation_update.inputs is not None:
        calc.inputs = calculation_update.inputs
        calc.result = calc.get_result()

    db.commit()
    db.refresh(calc)
    return calc


@app.delete("/calculations/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calc_id: str, current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(
        Calculation.id == calc_id,
        Calculation.user_id == current_user.id
    ).first()

    if not calc:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(calc)
    db.commit()
    return None