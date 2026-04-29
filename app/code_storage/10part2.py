"""Практическая работа 10, часть 2: машинная проверка расчётов."""

import matplotlib.pyplot as plt
import numpy as np


S = 9
G = 32
K = 1


def build_main_matrix(s: int, g: int) -> np.ndarray:
    p = 2 * g + 2 * s
    m = -s - 2 * g
    return np.array(
        [
            [p / 6, m / 6, 2 * s / 6],
            [m / 6, (2 * p + s) / 6, m / 6],
            [2 * s / 6, m / 6, p / 6],
        ],
        dtype=float,
    )


def build_extra_system(s: int, g: int, k: int) -> tuple[np.ndarray, np.ndarray]:
    matrix = np.array(
        [
            [4, -1, 1, -1, 0, 0],
            [1, 5, 1, 0, -1, 0],
            [s, g, 2 * (s + g + k), 0, 0, -1],
            [-1, 0, 0, 4, -1, 0],
            [0, -1, 0, -1, 4, -1],
            [0, 0, -1, 0, -1, 4],
        ],
        dtype=float,
    )

    vector = np.array(
        [
            s - g + 4 * k,
            s - g + k + 9,
            2 * (s - g) * (s + g + k) + k * s,
            -10,
            4 - 2 * g,
            9 * g - s - 1,
        ],
        dtype=float,
    )
    return matrix, vector


def normalize_first_component(vector: np.ndarray) -> np.ndarray:
    return vector / vector[0]


def print_report(
    matrix: np.ndarray,
    eigenvalues: np.ndarray,
    eigenvectors: np.ndarray,
    lambda_max: float,
    vector_max: np.ndarray,
    row_sums: np.ndarray,
    extra_solution: np.ndarray,
) -> None:
    print("Практическая работа 10, часть 2")
    print("=" * 36)

    print("\nПараметры варианта:")
    print(f"S = {S}, G = {G}, K = {K}")

    print("\nМатрица A:")
    print(matrix)

    print("\nСобственные числа:")
    print(eigenvalues)

    print("\nСобственные векторы:")
    print(eigenvectors)

    print("\nМаксимальное собственное число:")
    print(lambda_max)

    print("\nСоответствующий вектор после нормировки:")
    print(vector_max)

    print("\nСуммы элементов по строкам:")
    print(row_sums)

    print("\nКороткое замечание:")
    print(
        "Суммы строк не обязаны совпадать с собственными числами. "
        "Такое совпадение было бы ожидаемо только в специальных случаях, "
        "например если вектор (1, 1, 1) сам является собственным."
    )

    print("\nПроверка равенства A @ v и λ * v:")
    print("A @ v =")
    print(matrix @ normalize_first_component(vector_max))
    print("λ * v =")
    print(lambda_max * normalize_first_component(vector_max))

    print("\nРешение дополнительной системы:")
    print(extra_solution)


def plot_spectrum(eigenvalues: np.ndarray) -> None:
    x = np.arange(len(eigenvalues))

    plt.figure(figsize=(8, 5))
    plt.bar(x, eigenvalues, width=0.45)
    plt.xticks(x, [f"λ{i + 1}" for i in range(len(eigenvalues))])
    plt.title("Спектр матрицы A")
    plt.xlabel("Номер собственного числа")
    plt.ylabel("Значение")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()


def main() -> None:
    matrix = build_main_matrix(S, G)
    eigenvalues, eigenvectors = np.linalg.eig(matrix)

    max_index = int(np.argmax(eigenvalues))
    lambda_max = float(eigenvalues[max_index])
    vector_max = normalize_first_component(eigenvectors[:, max_index])
    row_sums = matrix.sum(axis=1)

    extra_matrix, extra_vector = build_extra_system(S, G, K)
    extra_solution = np.linalg.solve(extra_matrix, extra_vector)

    print_report(
        matrix,
        eigenvalues,
        eigenvectors,
        lambda_max,
        vector_max,
        row_sums,
        extra_solution,
    )
    plot_spectrum(eigenvalues)


if __name__ == "__main__":
    main()
