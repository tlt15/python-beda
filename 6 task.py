def main(psi):
    # Вычисляем E
    E = {psi_val - (psi_val % 2) for psi_val in psi
         if (psi_val <= 88) ^ (psi_val >= -53)}

    # Вычисляем N
    N = {psi_val for psi_val in psi if -42 <= psi_val < 78}

    # Вычисляем Θ
    Theta = {nu * epsilon for nu in N for epsilon in E if nu > epsilon}

    # Вычисляем δ
    sum_abs_E = sum(abs(e) for e in E)
    sum_pairs = sum(epsilon ** 3 + theta for epsilon in E for theta in Theta)

    return sum_abs_E + sum_pairs


# Проверка
print(main({32, 36, 69, -56, 45, -82, 79, -74, -8, -7}))  # -20485744
print(main({32, 1, -94, 40, 74, -29, 77, 15, 16, 90}))  # -856668
