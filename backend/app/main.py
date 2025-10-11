from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlmodel import Session

# from . import authentication, crud, models, schemas

from .authentication import auth
from .crud import crud
from .models import models
from .schemas import schemas
from .config import settings
from .database import get_session, init_db
from .SQLClassifier import checkSQL

app = FastAPI(title=settings.app_name)
security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(get_session),
) -> models.User:
    try:
        # Verify token
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )

        # Get user from database
        user = crud.get_user_by_username(db, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@app.post("/api/register", response_model=schemas.UserPublic)
async def register(user: schemas.UserCreate, db: Session = Depends(get_session)):
    try:
        if checkSQL(user.username) or checkSQL(user.password):
            raise HTTPException(status_code=418, detail="SQL code detected")
        print(f"Registering user: {user.username}")

        # Check if user exists
        db_user = crud.get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        # Hash password
        password = user.password

        # Create user
        return crud.create_user(db=db, user=user, hashed_password=password)
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise


@app.post("/api/login", response_model=schemas.LoginResponse)
async def login(login_data: schemas.LoginRequest, db: Session = Depends(get_session)):
    if checkSQL(login_data.username) or checkSQL(login_data.password):
            raise HTTPException(status_code=418, detail="SQL code detected")
    user = crud.get_user_by_username(db, username=login_data.username)
    if not crud.verify_user(db, username=login_data.username, hashed_password=login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"token": token}


@app.get("/api/me", response_model=schemas.UserPublic)
async def read_users_me(
    current_user: Annotated[models.User, Depends(get_current_user)],
) -> schemas.UserPublic:
    return schemas.UserPublic(
        id=current_user.id, username=current_user.username, balance=current_user.balance
    )


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
    if checkSQL(transaction.to_user_name) or checkSQL(transaction.description):
            raise HTTPException(status_code=418, detail="SQL code detected")
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
        raise HTTPException(
            status_code=403, detail="Not authorized to view these transactions"
        )
    return crud.get_transactions_for_user(db, user_id=user_id)


@app.on_event("startup")
def on_startup():
    init_db()
