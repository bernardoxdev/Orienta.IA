user_states = {}

def set_state(user_id: str, state: str):
    user_states[user_id] = state

def get_state(user_id: str):
    return user_states.get(user_id)

def clear_state(user_id: str):
    user_states.pop(user_id, None)

if __name__ == '__main__':
    pass