"""Дополнительное задание: перевод цветного изображения в оттенки серого."""

import argparse

import matplotlib.pyplot as plt
import numpy as np


def grayscale_slow(image: np.ndarray) -> np.ndarray:
    """Учебная реализация с двумя циклами."""
    rgb = image[..., :3]
    result = np.empty(rgb.shape[:2], dtype=float)
    for row in range(rgb.shape[0]):
        for column in range(rgb.shape[1]):
            result[row, column] = np.mean(rgb[row, column])
    return result


def grayscale_fast(image: np.ndarray) -> np.ndarray:
    """Векторизованная реализация NumPy без циклов Python."""
    return np.mean(image[..., :3], axis=2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="Путь к исходному изображению")
    parser.add_argument("--output", default="grayscale.png")
    args = parser.parse_args()

    image = plt.imread(args.image)
    slow = grayscale_slow(image)
    fast = grayscale_fast(image)

    if not np.allclose(slow, fast):
        raise RuntimeError("Медленный и быстрый способы дали разные результаты")

    figure, axes = plt.subplots(1, 3, figsize=(13, 4))
    axes[0].imshow(image)
    axes[0].set_title("Исходное изображение")
    axes[1].imshow(slow, cmap="gray")
    axes[1].set_title("Два цикла")
    axes[2].imshow(fast, cmap="gray")
    axes[2].set_title("Векторизация NumPy")
    for axis in axes:
        axis.axis("off")
    figure.tight_layout()
    figure.savefig(args.output, dpi=160)
    print(f"Результат сохранён: {args.output}")


if __name__ == "__main__":
    main()
