from fastapi import APIRouter, HTTPException
from .models import Ticket
from .consensus.hybrid import create_block, blockchain, save_blockchain, load_blockchain, Block
from app.pending_transactions import add_transaction, get_all_pending, clear_transactions

router = APIRouter()

@router.post("/book")
def book_ticket(ticket: Ticket):
    add_transaction(ticket.dict())  # Add to pending
    
    # Commit pending transactions to blockchain
    return commit_pending()  # Calls /pending/commit logic internally

@router.get("/chain")
def get_chain():
    return blockchain

@router.get("/latest")
def get_latest_block():
    if blockchain:
        block = blockchain[-1]
        return {
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "hash": block.hash,
            "previous_hash": block.previous_hash
        }
    return {"message": "Blockchain is empty."}

@router.get("/length")
def get_chain_length():
    return {"length": len(blockchain)}

@router.delete("/reset")
def reset_blockchain():
    global blockchain
    blockchain.clear()
    save_blockchain()  # Save empty chain
    return {"message": "Blockchain has been reset."}

@router.get("/validate")
def validate_chain():
    for i in range(1, len(blockchain)):
        current = blockchain[i]
        previous = blockchain[i - 1]

        # Recalculate hash and compare
        if current.hash != current.calculate_hash():
            return {
                "valid": False,
                "error": f"Block {i} has been tampered with. Invalid hash."
            }

        # Check previous hash link
        if current.previous_hash != previous.hash:
            return {
                "valid": False,
                "error": f"Block {i} is not linked properly to Block {i - 1}."
            }

    return {"valid": True, "message": "Blockchain is valid and all blocks are intact."}

@router.post("/pending/add")
def add_to_pending(ticket: Ticket):
    add_transaction(ticket.dict())
    return {"message": "Transaction added to pending queue."}

@router.post("/pending/commit")
def commit_pending():
    # Retrieve all pending transactions
    pending = get_all_pending()
    
    if not pending:
        raise HTTPException(status_code=400, detail="No pending transactions to commit.")
    
    block = create_block(pending)  # Create a block with the pending transactions
    
    if block is None:
        raise HTTPException(status_code=500, detail="Block creation failed.")
    
    clear_transactions()  # Clear pending transactions after block creation
    
    return {
        "message": "Pending transactions committed successfully",
        "block": {
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "hash": block.hash,
            "previous_hash": block.previous_hash
        }
    }

@router.get("/pending")
def get_pending():
    return {"pending_transactions": get_all_pending()}
