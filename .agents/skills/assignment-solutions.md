# Assignment solutions skill

Use this file for work under `app/code_storage` and numerical-solution tests.

## File conventions

- Name published files `<work>part<part>.<extension>`, for example
  `9part2.py` or `10part1.md`.
- Use Markdown for manual calculations and explanations.
- Use Python for executable machine calculations.
- Keep executable code behind `if __name__ == "__main__":` and expose reusable,
  testable functions.

## Numerical correctness

- Keep variant parameters consistent with `.agents/project.md`.
- Independently verify manual arithmetic before copying results into tables.
- Compare custom algorithms with NumPy when applicable.
- Use `numpy.allclose` or explicit tolerances for floating-point comparisons.
- For iterative methods, include a tolerance, iteration limit, convergence
  result, and residual. Raise a clear error when convergence fails.
- For Gaussian elimination, handle singular matrices and use pivoting.
- Do not use timings from one algorithm run to assert performance correctness;
  timings are demonstrations and vary by machine.

## Plotting and images

- Plotting scripts must work under `MPLBACKEND=Agg` in CI.
- Accept input and output paths through command-line arguments rather than
  relying on machine-specific files.
- Do not commit generated plots or copied input images unless explicitly asked.
- Validate that slow educational and vectorized implementations produce the
  same numerical result.

## Dependencies

- NumPy and Matplotlib belong in `requirements-solutions.txt`.
- Do not move them into `requirements.txt`; the website displays solutions but
  does not execute them in production.
