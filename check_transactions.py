from app import app, db, Transaction

print("--- CHECKING TRANSACTIONS ---")
with app.app_context():
    txs = Transaction.query.all()
    print(f"Total Transactions: {len(txs)}")
    for t in txs:
        print(f"ID: {t.id} | User: {t.user_id} | Book: {t.book_id} | Status: '{t.status}' | Due: {t.due_date}")

print("--- END ---")
