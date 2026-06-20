import importlib.util
from pathlib import Path

import numpy as np


SOLUTIONS_DIR = Path(__file__).parents[1] / "app" / "code_storage"


def load_solution(filename: str):
    path = SOLUTIONS_DIR / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_iterative_methods_find_exact_solution():
    solution = load_solution("9part2.py")
    expected = np.array([1.0, 2.0, -23.0])

    jacobi_result, _ = solution.jacobi(solution.A, solution.B)
    seidel_result, _ = solution.gauss_seidel(solution.A, solution.B)

    assert np.allclose(jacobi_result, expected)
    assert np.allclose(seidel_result, expected)


def test_custom_gaussian_elimination_matches_numpy():
    solution = load_solution("11part1.py")
    matrix, vector = solution.build_system(12, seed=7)

    actual = solution.gaussian_elimination(matrix, vector)

    assert np.allclose(actual, np.linalg.solve(matrix, vector))


def test_grayscale_implementations_match():
    solution = load_solution("11part2.py")
    image = np.random.default_rng(3).random((5, 7, 3))

    assert np.allclose(
        solution.grayscale_slow(image),
        solution.grayscale_fast(image),
    )
