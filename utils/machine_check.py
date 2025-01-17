import random


def check_machine_status(machine_id):
    """
    Емуляція перевірки підключення кавомашини.
    Для реального проєкту замінити цей код на читання сигналу датчика.
    """
    # Емуляція: кавомашина активна в 80% випадків
    return random.choice([True, True, True, False])
