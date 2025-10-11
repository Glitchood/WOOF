from sqlmodel import Session
from sqlalchemy import text

from . import models, schemas


def get_user_by_username(db: Session, username: str):
    # VULNERABLE: Raw SQL with direct string concatenation
    query = f"SELECT * FROM user WHERE username = '{username}'"
    print(f"EXECUTING VULNERABLE QUERY: {query}")  # DEBUG LINE
    result = db.execute(text(query))
    user = result.first()
    print(f"QUERY RESULT: {user}")  # DEBUG LINE
    return user


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    # VULNERABLE: Raw SQL insert with string concatenation
    query = f"INSERT INTO user (username, hashed_password, balance) VALUES ('{user.username}', '{hashed_password}', 1000.0)"
    db.execute(text(query))
    db.commit()
    
    # VULNERABLE: Retrieve user with same vulnerable pattern
    get_query = f"SELECT * FROM user WHERE username = '{user.username}'"
    result = db.execute(text(get_query))
    return result.first()


def get_user(db: Session, user_id: int):
    # VULNERABLE: Direct numeric concatenation
    query = f"SELECT * FROM user WHERE id = {user_id}"
    result = db.execute(text(query))
    return result.first()


def create_transaction(
    db: Session, from_user_id: int, transaction: schemas.TransactionCreate
):
    # VULNERABLE: Get from_user with string concatenation
    from_user_query = f"SELECT * FROM user WHERE id = {from_user_id}"
    from_user = db.execute(text(from_user_query)).first()
    
    # VULNERABLE: Get to_user with string concatenation  
    to_user_query = f"SELECT * FROM user WHERE username = '{transaction.to_user_name}'"
    to_user = db.execute(text(to_user_query)).first()

    if not from_user or not to_user:
        return None

    if from_user.balance < transaction.amount:
        return None

    # VULNERABLE: Update balances with direct value insertion
    update_from_query = f"UPDATE user SET balance = balance - {transaction.amount} WHERE id = {from_user_id}"
    db.execute(text(update_from_query))
    
    update_to_query = f"UPDATE user SET balance = balance + {transaction.amount} WHERE username = '{transaction.to_user_name}'"
    db.execute(text(update_to_query))

    # VULNERABLE: Insert transaction with string concatenation
    insert_query = f"INSERT INTO transaction (from_user_id, to_user_name, amount, description) VALUES ({from_user_id}, '{transaction.to_user_name}', {transaction.amount}, '{transaction.description}')"
    db.execute(text(insert_query))
    db.commit()
    
    # VULNERABLE: Get last transaction
    get_query = "SELECT * FROM transaction ORDER BY id DESC LIMIT 1"
    result = db.execute(text(get_query))
    return result.first()


def get_transactions_for_user(db: Session, user_id: int):
    # VULNERABLE: Get username with numeric injection
    user_query = f"SELECT username FROM user WHERE id = {user_id}"
    user_result = db.execute(text(user_query))
    username = user_result.scalar()
    
    if not username:
        return []
    
    # VULNERABLE: Main query with multiple injection points
    query = f"SELECT * FROM transaction WHERE from_user_id = {user_id} OR to_user_name = '{username}'"
    result = db.execute(text(query))
    return result.all()
