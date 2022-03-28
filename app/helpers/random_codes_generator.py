import random


def generate_random_hash(min_len: int = 15, max_len: int = 20) -> str:
    if min_len > max_len:
        raise Exception("Incorrect values.")
    return "".join(
        [random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range((random.randint(15, 20)))]
    )


def generate_confirmation_code(code_len: int = 6) -> str:
    return "".join([str(random.randint(0, 9)) for _ in range(code_len)])
