def find_min_and_max_element(arr):
    if not arr:
        raise ValueError("Масив не може бути порожнім")

    def find_min_max(low, high):
        # Обробляємо базові випадки:
        # 1. Залишився лише один елемент
        if low == high:
            return arr[low], arr[low]
        # 2. Залишилось два елементи
        if high == low + 1:
            if arr[low] < arr[high]:
                return arr[low], arr[high]
            else:
                return arr[high], arr[low]

        # Розділяємо масив на дві частини
        mid = (low + high) // 2
        # Обробляємо обидві половини рекурсивно
        left_min, left_max = find_min_max(low, mid)
        right_min, right_max = find_min_max(mid + 1, high)

        # Об'єднуємо результати з обох частин
        return min(left_min, right_min), max(left_max, right_max)

    return find_min_max(0, len(arr) - 1)


if __name__ == "__main__":
    data = [5, 7, 2, -3, 0, 7, 9, -1]
    min_value, max_value = find_min_and_max_element(data)
    print("Мінімум:", min_value)
    print("Максимум:", max_value)
