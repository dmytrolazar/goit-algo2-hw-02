from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк (словники з ключами id, volume, priority, print_time)
        constraints: Обмеження принтера (словник з ключами max_volume та max_items)

    Returns:
        Dict: словник з оптимальним порядком друку (print_order) та загальним часом друку (total_time)
    """
    # Перетворення вхідних даних у відповідні dataclass об’єкти
    jobs = [PrintJob(**job) for job in print_jobs]
    printer = PrinterConstraints(**constraints)

    # Сортуємо завдання за пріоритетом (чим менше значення, тим вищий пріоритет)
    # При однакових пріоритетах зберігається початковий порядок
    jobs.sort(key=lambda job: job.priority)

    print_order = []  # список для збереження порядку друку (ідентифікатори завдань)
    total_time = 0  # загальний час друку в хвилинах

    current_group = []  # поточна група завдань для одночасного друку
    current_group_volume = 0  # сумарний об'єм поточної групи

    for job in jobs:
        # Перевірка чи можна додати завдання до поточної групи:
        # 1. Чи не перевищено максимальну кількість завдань у групі?
        # 2. Чи не перевищується при додаванні завдання максимальний допустимий об'єм?
        if (len(current_group) < printer.max_items and
                current_group_volume + job.volume <= printer.max_volume):
            current_group.append(job)
            current_group_volume += job.volume
        else:
            # Якщо завдання не може бути додано в поточну групу,
            # «друкуємо» поточну групу:
            # Час друку групи = максимальний час серед завдань у групі
            group_time = max(j.print_time for j in current_group)
            total_time += group_time
            # Записуємо порядок виконання завдань з поточної групи
            print_order.extend([j.id for j in current_group])
            # Починаємо нову групу із завдання, яке не помістилося
            current_group = [job]
            current_group_volume = job.volume

    # Якщо після обходу залишилися завдання у групі, обробляємо їх
    if current_group:
        group_time = max(j.print_time for j in current_group)
        total_time += group_time
        print_order.extend([j.id for j in current_group])

    return {
        "print_order": print_order,
        "total_time": total_time
    }


# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму (неможливість групування завдань)
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
