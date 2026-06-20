"""Дополнительное задание: сравнение времени решения СЛАУ."""

import argparse
import time

import matplotlib.pyplot as plt
import numpy as np


def gaussian_elimination(matrix: np.ndarray, vector: np.ndarray) -> np.ndarray:
    """Решить СЛАУ методом Гаусса с выбором главного элемента."""
    augmented = np.column_stack((matrix, vector)).astype(float).tolist()
    size = len(augmented)

    for pivot_column in range(size):
        pivot_row = max(
            range(pivot_column, size),
            key=lambda row: abs(augmented[row][pivot_column]),
        )
        if abs(augmented[pivot_row][pivot_column]) < 1e-12:
            raise ValueError("Матрица вырождена")
        augmented[pivot_column], augmented[pivot_row] = (
            augmented[pivot_row],
            augmented[pivot_column],
        )

        pivot = augmented[pivot_column]
        for row_index in range(pivot_column + 1, size):
            row = augmented[row_index]
            factor = row[pivot_column] / pivot[pivot_column]
            row[pivot_column] = 0.0
            for column in range(pivot_column + 1, size + 1):
                row[column] -= factor * pivot[column]

    solution = [0.0] * size
    for row_index in range(size - 1, -1, -1):
        row = augmented[row_index]
        known = sum(
            row[column] * solution[column] for column in range(row_index + 1, size)
        )
        solution[row_index] = (row[-1] - known) / row[row_index]
    return np.array(solution)


def build_system(size: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    matrix = rng.uniform(-1, 1, (size, size))
    matrix += np.eye(size) * size
    expected = rng.uniform(-10, 10, size)
    return matrix, matrix @ expected


def measure(size: int) -> tuple[float, float]:
    matrix, vector = build_system(size, seed=size)

    started = time.perf_counter()
    numpy_solution = np.linalg.solve(matrix, vector)
    numpy_time = time.perf_counter() - started

    started = time.perf_counter()
    custom_solution = gaussian_elimination(matrix, vector)
    custom_time = time.perf_counter() - started

    if not np.allclose(custom_solution, numpy_solution, rtol=1e-7, atol=1e-7):
        raise RuntimeError("Собственный метод Гаусса дал неверный результат")
    return numpy_time, custom_time


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", nargs="+", type=int, default=[50, 100, 150, 200])
    parser.add_argument("--output", default="gaussian_timing.png")
    args = parser.parse_args()

    numpy_times = []
    custom_times = []
    for size in args.sizes:
        numpy_time, custom_time = measure(size)
        numpy_times.append(numpy_time)
        custom_times.append(custom_time)
        print(f"n={size:4d}: NumPy={numpy_time:.6f} с, свой метод={custom_time:.6f} с")

    plt.plot(args.sizes, numpy_times, marker="o", label="NumPy")
    plt.plot(args.sizes, custom_times, marker="o", label="Свой метод Гаусса")
    plt.xlabel("Количество неизвестных")
    plt.ylabel("Время, секунд")
    plt.title("Время решения заполненной СЛАУ")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.output, dpi=160)
    print(f"График сохранён: {args.output}")


if __name__ == "__main__":
    main()
