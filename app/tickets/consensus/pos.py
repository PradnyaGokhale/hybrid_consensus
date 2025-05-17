validators = {
    "Alice": 50,
    "Bob": 30,
    "Charlie": 20,
    "Denice" : 60,
    "Emma" : 80,
    "Frank" : 50,
    "Gia" : 15,
    "Hans" : 20,
    "Iris" : 30,
    "Jack" : 80
}

def simulate_pos():
    return [{"name": name, "stake": stake} for name, stake in validators.items()]

def reward_validator(name, reward=10):
    if name in validators:
        validators[name] += reward
    else:
        validators[name] = reward
