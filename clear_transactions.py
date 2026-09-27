from app import app, db, Transaction, Book

print("--- CLEARING TRANSACTIONS & RESETTING STOCK ---")
with app.app_context():
    # 1. Delete all transactions
    num_deleted = db.session.query(Transaction).delete()
    print(f"Deleted {num_deleted} transactions.")
    
    # 2. Reset Book Availability
    books = Book.query.all()
    count = 0
    for book in books:
        book.available = book.quantity
        count += 1
    
    db.session.commit()
    print(f"Reset stock for {count} books.")

print("--- END ---")
