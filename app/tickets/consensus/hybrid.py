import time
import hashlib
import os
import json
from .pos import simulate_pos, reward_validator
from .poet import simulate_poet, penalize_validator
from app.pending_transactions import get_all_pending, clear_transactions

BLOCKCHAIN_FILE = "blockchain_data.json"

class Block:
    def __init__(self, index, timestamp, data, previous_hash, hash=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = hash or self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
def load_blockchain():
    if os.path.exists(BLOCKCHAIN_FILE):
        try:
            with open(BLOCKCHAIN_FILE, "r") as file:
                data = json.load(file)
                return [Block(**block) for block in data]
        except Exception as e:
            print(f"Error loading blockchain: {e}")
            return []
    return []

def save_blockchain():
    with open(BLOCKCHAIN_FILE, "w") as file:
        json.dump([block.__dict__ for block in blockchain], file, indent=4)

blockchain = load_blockchain()

def create_block(data):
    pending = get_all_pending()
    print(f"[create_block] pending: {pending}")
    if not pending:
        print("[create_block] No pending transactions, block not created.")
        return None

    index = len(blockchain)
    timestamp = time.time()
    previous_hash = blockchain[-1].hash if blockchain else "0"

    # Get current data
    pos_validators = simulate_pos()
    poet_wait_times = simulate_poet()
    
    # Compute hybrid scores
    hybrid_scores = []
    for v in pos_validators:
        name = v["name"]
        stake = v["stake"]
        wait_time = poet_wait_times.get(name, 1.0)
        score = stake / wait_time  # Higher is better
        hybrid_scores.append({
            "name": name,
            "stake": stake,
            "wait_time": wait_time,
            "score": score
        })

    # Select winner
    winner = max(hybrid_scores, key=lambda x: x["score"])
    winner_name = winner["name"]

    # Reward and penalize winner
    reward_validator(winner_name, reward=10)
    penalize_validator(winner_name, extra_delay=0.2)

    # Save block
    consensus_info = {
        "selected_validator": winner,
    }

    block_data = {
        "ticket_data": data,
        "consensus_result": consensus_info
    }

    block = Block(index, timestamp, block_data, previous_hash)
    blockchain.append(block)
    save_blockchain()
    return block

def is_chain_valid():
    for i in range(1, len(blockchain)):
        current = blockchain[i]
        previous = blockchain[i - 1]

        # Check if current hash is correct
        if current.hash != current.calculate_hash():
            return False, f"Block {i} has an invalid hash."

        # Check if previous hash is correct
        if current.previous_hash != previous.hash:
            return False, f"Block {i} has an invalid previous hash."

    return True, "Blockchain is valid."

