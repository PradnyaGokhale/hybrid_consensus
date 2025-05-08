import random
import time

participants = ["Alice", "Bob", "Charlie", "Denice", "Emma", "Frank", "Gia", "Hans", "Iris", "Jack"]
penalties = {}

def simulate_poet():
    wait_times = {
        participant: random.uniform(0.1, 1.0) + penalties.get(participant, 0)
        for participant in participants
    }
    return wait_times

def penalize_validator(name, extra_delay=0.2):
    penalties[name] = penalties.get(name, 0) + extra_delay
