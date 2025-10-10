from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlmodel import Session

from . import auth, crud, models, schemas
from .config import settings
from .database import get_session, init_db

app = FastAPI(title=settings.app_name)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/api/register", response_model=schemas.UserPublic)
async def register(user: schemas.UserCreate, db: Session = Depends(get_session)):
    try:
        print(f"Registering user: {user.username}")
        
        # Check if user exists
        db_user = crud.get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Hash password
        print("Hashing password...")
        hashed_password = auth.get_password_hash(user.password)
        print("Password hashed successfully")
        
        # Create user
        return crud.create_user(db=db, user=user, hashed_password=hashed_password)
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise


@app.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_session),
):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/me", response_model=schemas.UserPublic)
async def read_users_me(current_user: Annotated[models.User, Depends(get_current_user)]):
    return current_user


@app.get("/api/users/{user_id}", response_model=schemas.UserPublic)
def read_user(
    user_id: int,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_session),
):
    if current_user.id != user_id:  # Prevent IDOR
        raise HTTPException(status_code=403, detail="Not authorized to view this user")
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/api/transactions")
def create_transaction(
    transaction: schemas.TransactionCreate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_session),
):
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    result = crud.create_transaction(
        db=db,
        from_user_id=current_user.id,
        transaction=transaction,
    )
    
    if result is None:
        raise HTTPException(status_code=400, detail="Transaction failed")
    
    return {"status": "success", "transaction_id": result.id}


@app.get("/api/users/{user_id}/transactions")
def read_user_transactions(
    user_id: int,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_session),
):
    if current_user.id != user_id:  # Prevent IDOR
        raise HTTPException(status_code=403, detail="Not authorized to view these transactions")
    return crud.get_transactions_for_user(db, user_id=user_id)


@app.on_event("startup")
def on_startup():
    init_db()