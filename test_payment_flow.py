from app import app, db, User, Book, Transaction
from datetime import datetime, timedelta
import uuid

print("--- TESTING PAYMENT FLOW ---")
with app.app_context():
    # 1. Setup Data
    user = User.query.filter_by(role='student').first()
    book = Book.query.first()
    if not user or not book:
        print("Error: No student or book found.")
        exit(1)
        
    print(f"Student: {user.username}")
    print(f"Book: {book.title}")

    # 2. Create Overdue Transaction
    # Issued 30 days ago, Due 16 days ago (14 day loan)
    issue_date = datetime.utcnow() - timedelta(days=30)
    due_date = issue_date + timedelta(days=14) # Due 16 days ago from NOW
    
    print(f"Creating Transaction... Issue: {issue_date.date()} Due: {due_date.date()}")
    
    txn = Transaction(
        user_id=user.id,
        book_id=book.id,
        issue_date=issue_date,
        due_date=due_date,
        status='issued'
    )
    db.session.add(txn)
    db.session.commit()
    print(f"Transaction ID: {txn.id} Created.")

    # 3. Simulate Return (Today)
    # Return Date = Now
    return_date = datetime.utcnow()
    txn.return_date = return_date
    txn.status = 'returned'
    db.session.commit()
    
    # 4. Check Penalty
    # Logic: (Return - Due).days * 10
    delta = return_date - due_date
    expected_fine = delta.days * 10
    print(f"Returned On: {return_date.date()}")
    print(f"Overdue by: {delta.days} days")
    print(f"Calculated Penalty (Property): {txn.penalty}")
    
    if txn.penalty != expected_fine:
        print(f"WARNING: Mismatch! Expected {expected_fine}")
    else:
        print("Penalty Calculation: CORRECT")

    # 5. Simulate Payment (Student Pay Action)
    print("Simulating Payment...")
    if txn.penalty > 0 and not txn.fine_paid:
        txn.fine_paid = True
        txn.payment_id = f"TEST-{str(uuid.uuid4())[:8]}"
        db.session.commit()
        print(f"Payment Successful! Txn ID: {txn.payment_id}")
    else:
        print("Error: No fine to pay or already paid.")

print("--- END ---")
