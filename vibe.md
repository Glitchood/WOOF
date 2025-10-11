### `[2025-10-10 10:20AM]`
**Prompt:**
> "Can you optimize and improve this draft api specification - keep it simple yet relevant. we can include a wide variety of vulnerabilities."

**Model:** `Gemini 2.5 Pro`

**Platform:** `Google AI Studio`

---
### `[2025-10-10 2:45PM]
**Prompt:**
> "can we make a fastapi python with sqlmodel and jwt tokens (the lock icons means it will require authentication) do not worry about the WAF/WOOF. That will be implmented later. only worry about the vulnerability."

**Model:** `Claude Sonnet 3.5`

**Platform:** `VSCode`

---
### `[2025-10-10 5:44PM]
**Prompt:**
> "(models.Transaction.to_user_name == user_id) I found this. How do I get the username of the person with the user_id instead?"

**Model:** `GPT-5`

**Platform:** `ChatGPT web`

---
### `[2025-10-10 9:02PM]
**Prompt:**
> "I have a dataset of SQL injections and non SQL phrases and sentences. How can I use this to create a model that classifies whether text could be an SQL injection or not?"

**Model:** `GPT-5`

**Platform:** `ChatGPT web`

---
### `[2025-10-10 10:16 PM]
**Prompt:**
> "--------------------------------------------------------------------------- UnicodeDecodeError Traceback (most recent call last) /tmp/ipython-input-597913002.py in <cell line: 0>() 1 count = 0 2 with open('rockyou.txt', 'r') as f: ----> 3 passwords = f.read() 4 passwords = np.array(passwords.split('\n')) /usr/lib/python3.12/codecs.py in decode(self, input, final) UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf1 in position 5079963: invalid continuation byte I'm getting this error when reading rockyou.txt. How can I get around this?"

**Model:** `GPT-4o mini`

**Platform:** `ChatGPT web`

---
### `[2025-10-10 7:56 PM]
**Prompt:**
> "change the following code such that ORM is replaces with raw SQL

"""



from sqlmodel import Session
from sqlalchemy import text

from . import models, schemas


def get_user_by_username(db: Session, username: str):
    query = text("SELECT * FROM user WHERE username = :username")
    result = db.execute(query, {"username": username})
    return result.first()


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    query = text("""
        INSERT INTO user (username, hashed_password, balance) 
        VALUES (:username, :hashed_password, 1000.0)
    """)
    db.execute(query, {
        "username": user.username, 
        "hashed_password": hashed_password
    })
    db.commit()
    
    # Retrieve the created user
    get_query = text("SELECT * FROM user WHERE username = :username")
    result = db.execute(get_query, {"username": user.username})
    return result.first()


def get_user(db: Session, user_id: int):
    query = text("SELECT * FROM user WHERE id = :user_id")
    result = db.execute(query, {"user_id": user_id})
    return result.first()


def create_transaction(db: Session, from_user_id: int, transaction: schemas.TransactionCreate):
    # Get from_user
    from_user_query = text("SELECT * FROM user WHERE id = :from_user_id")
    from_user = db.execute(from_user_query, {"from_user_id": from_user_id}).first()
    
    # Get to_user
    to_user_query = text("SELECT * FROM user WHERE username = :username")
    to_user = db.execute(to_user_query, {"username": transaction.to_user_name}).first()

    if not from_user or not to_user:
        return None

    if from_user.balance < transaction.amount:
        return None

    # Update from_user balance
    update_from_query = text("""
        UPDATE user SET balance = balance - :amount 
        WHERE id = :from_user_id
    """)
    db.execute(update_from_query, {
        "amount": transaction.amount, 
        "from_user_id": from_user_id
    })
    
    # Update to_user balance
    update_to_query = text("""
        UPDATE user SET balance = balance + :amount 
        WHERE username = :username
    """)
    db.execute(update_to_query, {
        "amount": transaction.amount, 
        "username": transaction.to_user_name
    })

    # Create transaction record
    insert_query = text("""
        INSERT INTO transaction (from_user_id, to_user_name, amount, description) 
        VALUES (:from_user_id, :to_user_name, :amount, :description)
    """)
    db.execute(insert_query, {
        "from_user_id": from_user_id,
        "to_user_name": transaction.to_user_name,
        "amount": transaction.amount,
        "description": transaction.description
    })
    db.commit()
    
    # Get the last inserted transaction
    get_query = text("SELECT * FROM transaction ORDER BY id DESC LIMIT 1")
    result = db.execute(get_query)
    return result.first()


def get_transactions_for_user(db: Session, user_id: int):
    # First get the username for the user_id
    user_query = text("SELECT username FROM user WHERE id = :user_id")
    user_result = db.execute(user_query, {"user_id": user_id})
    username = user_result.scalar()
    
    if not username:
        return []
    
    # Get transactions where user is sender or receiver
    query = text("""
        SELECT * FROM transaction 
        WHERE from_user_id = :user_id 
        OR to_user_name = :username
    """)
    result = db.execute(query, {
        "user_id": user_id, 
        "username": username
    })
    return result.all()"

"""
"

**Model:** `Deepseek 3.1`

**Platform:** `Deepseek web`
