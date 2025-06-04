def main(psi, debug=False):
    # 1. Вычисляем множество E
    E = set()
    for psi_val in psi:
        condition = (psi_val <= 88) ^ (psi_val >= -53)
        if condition:
            e = psi_val - (psi_val % 2)
            E.add(e)
            if debug:
                print(f"ψ={psi_val:4d} → e={e:4d} (XOR условие)")
        elif debug:
            print(f"ψ={psi_val:4d} → не в E")

    if debug:
        print(f"\nМножество E: {sorted(E)}")

    # 2. Вычисляем множество N
    N = {psi_val for psi_val in psi if -42 <= psi_val < 78}
    if debug:
        print(f"Множество N: {sorted(N)}")

    # 3. Вычисляем множество Θ
    Theta = {nu * epsilon for nu in N for epsilon in E if nu > epsilon}
    if debug:
        print(f"\nМножество Θ: {sorted(Theta)}")
        print(f"Количество элементов в Θ: {len(Theta)}")

    # 4. Вычисляем δ
    # Первая сумма: сумма модулей элементов E
    sum_abs_E = sum(abs(e) for e in E)

    # Вторая сумма: сумма (ε³ + θ) для всех ε ∈ E и θ ∈ Θ
    sum_pairs = 0
    for epsilon in E:
        for theta in Theta:
            sum_pairs += epsilon ** 3 + theta

    delta = sum_abs_E + sum_pairs

    if debug:
        print(f"\nСумма |E|: {sum_abs_E}")
        print(f"Сумма (ε³+θ): {sum_pairs}")
        print(f"Итого δ: {delta}")

    return delta


# Тесты
print("=== Тест 1 ===")
test1 = {32, 36, 69, -56, 45, -82, 79, -74, -8, -7}
res1 = main(test1, debug=True)
print(f"\nОжидается: -28485744 | Получено: {res1}")

print("\n=== Тест 2 ===")
test2 = {32, 1, -94, 40, 74, -29, 77, 15, 16, 90}
res2 = main(test2, debug=True)
print(f"\nОжидается: -856668 | Получено: {res2}")
