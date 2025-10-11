from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlmodel import Session

from . import auth, crud, models, schemas
from .config import settings
from .database import get_session, init_db

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
            algorithms=[settings.ALGORITHM]
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

def authenticate_user(db: Session, username: str, password: str):
    # VULNERABLE: Direct string concatenation
    query = f"SELECT * FROM user WHERE username = '{username}' AND hashed_password = '{password}'"
    result = db.execute(sqlalchemy.text(query))
    print("has been ran")
    return result.first()
    
@app.post('/login')
def login(credentials: schemas.UserLogin, db: Session = Depends(get_session)):
    user = authenticate_user(db, credentials.username, credentials.password)
    if user:
        return {"message": "Login successful", "user": user}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/api/me", response_model=schemas.UserPublic)
async def read_users_me(
    current_user: Annotated[models.User, Depends(get_current_user)]
) -> schemas.UserPublic:
    return schemas.UserPublic(
        id=current_user.id,
        username=current_user.username,
        balance=current_user.balance
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
