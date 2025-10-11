from sqlmodel import Session
from sqlalchemy import text

from . import models, schemas


def get_user_by_username(db: Session, username: str):
    query = text(f"SELECT * FROM user WHERE username = '{username}'")
    result = db.execute(query)
    return result.first()


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    query = text(f"""
        INSERT INTO user (username, hashed_password, balance) 
        VALUES ('{user.username}', '{hashed_password}', 1000.0)
    """)
    db.execute(query)
    db.commit()
    
    # Retrieve the created user
    get_query = text(f"SELECT * FROM user WHERE username = '{user.username}'")
    result = db.execute(get_query)
    return result.first()


def get_user(db: Session, user_id: int):
    query = text(f"SELECT * FROM user WHERE id = {user_id}")
    result = db.execute(query)
    return result.first()


def create_transaction(db: Session, from_user_id: int, transaction: schemas.TransactionCreate):
    # Get from_user
    from_user_query = text(f"SELECT * FROM user WHERE id = {from_user_id}")
    from_user = db.execute(from_user_query).first()
    
    # Get to_user
    to_user_query = text(f"SELECT * FROM user WHERE username = '{transaction.to_user_name}'")
    to_user = db.execute(to_user_query).first()

    if not from_user or not to_user:
        return None

    if from_user.balance < transaction.amount:
        return None

    # Update from_user balance
    update_from_query = text(f"""
        UPDATE user SET balance = balance - {transaction.amount} 
        WHERE id = {from_user_id}
    """)
    db.execute(update_from_query)
    
    # Update to_user balance
    update_to_query = text(f"""
        UPDATE user SET balance = balance + {transaction.amount} 
        WHERE username = '{transaction.to_user_name}'
    """)
    db.execute(update_to_query)

    # Create transaction record
    insert_query = text(f"""
        INSERT INTO transaction (from_user_id, to_user_name, amount, description) 
        VALUES ({from_user_id}, '{transaction.to_user_name}', {transaction.amount}, '{transaction.description}')
    """)
    db.execute(insert_query)
    db.commit()
    
    # Get the last inserted transaction
    get_query = text("SELECT * FROM transaction ORDER BY id DESC LIMIT 1")
    result = db.execute(get_query)
    return result.first()


def get_transactions_for_user(db: Session, user_id: int):
    # First get the username for the user_id
    user_query = text(f"SELECT username FROM user WHERE id = {user_id}")
    user_result = db.execute(user_query)
    username = user_result.scalar()
    
    if not username:
        return []
    
    # Get transactions where user is sender or receiver
    query = text(f"""
        SELECT * FROM transaction 
        WHERE from_user_id = {user_id} 
        OR to_user_name = '{username}'
    """)
    result = db.execute(query)
    return result.all()
