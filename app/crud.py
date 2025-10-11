from sqlmodel import Session, select

from . import models, schemas


def get_user_by_username(db: Session, username: str):
    return db.exec(select(models.User).where(models.User.username == username)).first()


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.get(models.User, user_id)


def create_transaction(
    db: Session, from_user_id: int, transaction: schemas.TransactionCreate
):
    from_user = db.get(models.User, from_user_id)
    to_user = db.query(models.User).filter_by(username=transaction.to_user_name).first()

    if not from_user or not to_user:
        return None  # Handle user not found

    if from_user.balance < transaction.amount:
        return None  # Handle insufficient funds

    from_user.balance -= transaction.amount
    to_user.balance += transaction.amount

    db_transaction = models.Transaction(
        from_user_id=from_user_id,
        to_user_name=transaction.to_user_name,
        amount=transaction.amount,
        description=transaction.description,
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions_for_user(db: Session, user_id: int):
    return db.exec(
        select(models.Transaction).where(
            (models.Transaction.from_user_id == user_id)
            | (models.Transaction.to_user_name == db.get(models.User, user_id).username)
        )
    ).all()
