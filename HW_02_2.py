from typing import List, Dict
import sys


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію.

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжиною i+1

    Returns:
        Dict з максимальним прибутком, списком відрізків та кількістю розрізів.
        Формат:
        {
            "max_profit": int,
            "cuts": List[int],
            "number_of_cuts": int
        }
    """
    # Перевірка вхідних даних
    if length <= 0:
        raise ValueError("Довжина стрижня повинна бути більше нуля.")
    if not prices or len(prices) != length:
        raise ValueError("Масив цін повинен бути непорожнім і мати довжину, рівну довжині стрижня.")

    memo = {}

    def helper(n: int):
        """
        Рекурсивна функція, яка повертає кортеж:
          (максимальний прибуток для стрижня довжини n, список відрізків, що дають цей прибуток)
        """
        if n == 0:
            return (0, [])
        if n in memo:
            return memo[n]

        best_profit = -sys.maxsize
        best_cuts = []
        # Розглядаємо можливий перший розріз довжиною i (від 1 до n)
        for i in range(1, n + 1):
            # Рекурсивно знаходимо оптимальне розрізання для залишку (n-i)
            rem_profit, rem_cuts = helper(n - i)
            candidate_profit = prices[i - 1] + rem_profit
            candidate_cuts = [i] + rem_cuts
            # Оновлюємо результат:
            # - Якщо прибуток більший, то беремо цей варіант.
            # - Якщо прибуток рівний, то віддаємо перевагу рішенню з більшою кількістю відрізків.
            if candidate_profit > best_profit:
                best_profit = candidate_profit
                best_cuts = candidate_cuts
            elif candidate_profit == best_profit:
                if len(candidate_cuts) > len(best_cuts):
                    best_cuts = candidate_cuts
        memo[n] = (best_profit, best_cuts)
        return memo[n]

    profit, cuts = helper(length)
    number_of_cuts = len(cuts) - 1 if cuts else 0

    return {
        "max_profit": profit,
        "cuts": cuts,
        "number_of_cuts": number_of_cuts
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію.

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжиною i+1

    Returns:
        Dict з максимальним прибутком, списком відрізків та кількістю розрізів.
        Формат:
        {
            "max_profit": int,
            "cuts": List[int],
            "number_of_cuts": int
        }
    """
    # Перевірка вхідних даних
    if length <= 0:
        raise ValueError("Довжина стрижня повинна бути більше нуля.")
    if not prices or len(prices) != length:
        raise ValueError("Масив цін повинен бути непорожнім і мати довжину, рівну довжині стрижня.")

    # dp[j] буде кортежем (max_profit, pieces), де pieces – кількість відрізків, які дають цей прибуток
    dp = [(0, 0)] * (length + 1)
    # cut[j] зберігає оптимальну довжину першого відрізка для стрижня довжини j
    cut = [0] * (length + 1)

    dp[0] = (0, 0)  # Для стрижня довжиною 0 прибуток 0, кількість відрізків 0

    # Обчислення по зростанню довжини стрижня
    for j in range(1, length + 1):
        best_profit = -sys.maxsize
        best_pieces = 0
        best_cut = 0
        # Розглядаємо варіанти першого розрізу довжиною i (1 <= i <= j)
        for i in range(1, j + 1):
            candidate_profit = prices[i - 1] + dp[j - i][0]
            candidate_pieces = 1 + dp[j - i][1]  # додали один відрізок
            # Оновлення:
            # 1. Якщо прибуток більший, вибираємо цей варіант.
            # 2. Якщо прибуток рівний, вибираємо той, що дає більше відрізків.
            # 3. Якщо і прибуток, і кількість відрізків рівні, віддаємо перевагу більшій довжині першого відрізка.
            if candidate_profit > best_profit:
                best_profit = candidate_profit
                best_pieces = candidate_pieces
                best_cut = i
            elif candidate_profit == best_profit:
                if candidate_pieces > best_pieces:
                    best_profit = candidate_profit
                    best_pieces = candidate_pieces
                    best_cut = i
                elif candidate_pieces == best_pieces and i > best_cut:
                    best_cut = i
        dp[j] = (best_profit, best_pieces)
        cut[j] = best_cut

    # Реконструкція оптимального порядку розрізів
    cuts_list = []
    remaining = length
    while remaining > 0:
        cuts_list.append(cut[remaining])
        remaining -= cut[remaining]
    number_of_cuts = len(cuts_list) - 1 if cuts_list else 0

    return {
        "max_profit": dp[length][0],
        "cuts": cuts_list,
        "number_of_cuts": number_of_cuts
    }


def run_tests():
    """Функція для запуску тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        # Тест 2: Оптимально не різати
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        # Тест 3: Всі розрізи по 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()
