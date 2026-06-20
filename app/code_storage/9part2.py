"""Практическая работа 9: методы Якоби и Зейделя."""

import numpy as np


A = np.array(
    [
        [4, -1, 1],
        [1, 5, 1],
        [9, 32, 84],
    ],
    dtype=float,
)
B = np.array([-21, -12, -1859], dtype=float)


def jacobi(
    matrix: np.ndarray,
    vector: np.ndarray,
    tolerance: float = 1e-10,
    max_iterations: int = 10_000,
) -> tuple[np.ndarray, list[np.ndarray]]:
    diagonal = np.diag(matrix)
    remainder = matrix - np.diagflat(diagonal)
    current = np.zeros_like(vector)
    history = [current.copy()]

    for _ in range(max_iterations):
        updated = (vector - remainder @ current) / diagonal
        history.append(updated.copy())
        if np.linalg.norm(updated - current, ord=np.inf) < tolerance:
            return updated, history
        current = updated

    raise RuntimeError("Метод Якоби не сошёлся за заданное число итераций")


def gauss_seidel(
    matrix: np.ndarray,
    vector: np.ndarray,
    tolerance: float = 1e-10,
    max_iterations: int = 10_000,
) -> tuple[np.ndarray, list[np.ndarray]]:
    current = np.zeros_like(vector)
    history = [current.copy()]

    for _ in range(max_iterations):
        previous = current.copy()
        for row in range(len(vector)):
            before = matrix[row, :row] @ current[:row]
            after = matrix[row, row + 1 :] @ previous[row + 1 :]
            current[row] = (vector[row] - before - after) / matrix[row, row]
        history.append(current.copy())
        if np.linalg.norm(current - previous, ord=np.inf) < tolerance:
            return current, history

    raise RuntimeError("Метод Зейделя не сошёлся за заданное число итераций")


def print_result(name: str, solution: np.ndarray, history: list[np.ndarray]) -> None:
    print(f"\n{name}")
    for number, values in enumerate(history[1:4], start=1):
        print(f"Итерация {number}: {values}")
    print(f"Сошёлся за {len(history) - 1} итераций: {solution}")
    print(f"Невязка ||Ax-b||∞ = {np.linalg.norm(A @ solution - B, ord=np.inf):.3e}")


def main() -> None:
    exact = np.linalg.solve(A, B)
    jacobi_solution, jacobi_history = jacobi(A, B)
    seidel_solution, seidel_history = gauss_seidel(A, B)

    print(f"Точное решение NumPy: {exact}")
    print_result("Метод Якоби", jacobi_solution, jacobi_history)
    print_result("Метод Зейделя", seidel_solution, seidel_history)


if __name__ == "__main__":
    main()
