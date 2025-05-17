# app/pending_transactions.py

pending_transactions = []

def add_transaction(transaction):
    pending_transactions.append(transaction)

def get_all_pending():
    return pending_transactions

def clear_transactions():
    global pending_transactions
    pending_transactions = []
