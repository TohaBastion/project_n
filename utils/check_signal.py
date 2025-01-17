import random


def check_signal_1_status(machine_id):
    true_or_false = [True, True, True, False]

    signal_1_dict = {
        "Machine 1": random.choice(true_or_false),
        "Machine 2": random.choice(true_or_false),
        "Machine 3": random.choice(true_or_false),
        "Machine 4": random.choice(true_or_false)
    }

    return signal_1_dict[machine_id]


def check_signal_2_status(machine_id):
    true_or_false = [True, True, True, False]

    signal_2_dict = {
        "Machine 1": random.choice(true_or_false),
        "Machine 2": random.choice(true_or_false),
        "Machine 3": random.choice(true_or_false),
        "Machine 4": random.choice(true_or_false)
    }

    return signal_2_dict[machine_id]
