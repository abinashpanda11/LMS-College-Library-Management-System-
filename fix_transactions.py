from app import app, db, Transaction

print("--- FIXING TRANSACTIONS ---")
with app.app_context():
    # Update Null statuses to 'issued'
    txs = Transaction.query.filter(Transaction.status == None).all()
    print(f"Found {len(txs)} transactions with NULL status.")
    for t in txs:
        t.status = 'issued'
    
    db.session.commit()
    print("Fixed.")

    # Verify
    all_tx = Transaction.query.all()
    for t in all_tx:
        print(f"ID: {t.id} Status: {t.status}")

print("--- END ---")
