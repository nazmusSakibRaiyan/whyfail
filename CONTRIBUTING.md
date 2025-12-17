# Contributing to whyfail

Thanks for your interest in contributing! This project aims to make Python errors understandable by humans. Contributions of all kinds are welcome — bug fixes, explainers for new exceptions, docs, tests, and examples.

## Getting Started

### Prerequisites
- Python 3.8 or newer
- Git

### Setup
```bash
# Clone
git clone https://github.com/nazmusSakibRaiyan/whyfail.git
cd whyfail

# Virtual environment
python -m venv .venv
# Windows
. .venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

# Install in dev mode (includes tests/linting tools)
pip install -e ".[dev]"

# Run tests
pytest -v --cov=whyfail
```

## Development Workflow

1. **Create a branch**
   - `feature/your-feature` or `fix/your-fix`
2. **Write code + tests**
   - Keep changes small and focused
   - Add or update tests in `tests/`
3. **Run checks**
   ```bash
   black whyfail tests
   isort whyfail tests
   flake8 whyfail tests
   pytest -v
   ```
4. **Open a Pull Request**
   - Describe the change and motivation
   - Link to related issues
   - Include screenshots/output if relevant

## Adding a New Explainer

1. Implement your explainer in `whyfail/explainers.py`:
   ```python
   from whyfail import Explanation

   class MyError(Exception):
       pass

   def explain_my_error(err: MyError) -> Explanation:
       return Explanation(
           title="MyError occurred",
           reason="Explain why this typically happens",
           suggestions=["Actionable step 1", "Step 2"],
           context=str(err),
       )
   ```
2. Register it:
   ```python
   whyfail.register_explainer(MyError, explain_my_error)
   ```
3. Add tests in `tests/` that verify output contains the key parts.

## Coding Guidelines
- Keep output concise, actionable, and friendly
- Prefer simple language over jargon
- Avoid heavy runtime introspection or monkey-patching
- Maintain backward compatibility where possible

## CI & Publishing

- **CI**: GitHub Actions runs tests on push/PR to `main` (see `.github/workflows/ci.yml`).
- **Publishing**: A release or tag `v*` triggers PyPI publishing via `.github/workflows/publish.yml`.
  - Maintainers must set the secret `PYPI_API_TOKEN` in the repository settings.
  - Version is managed in `pyproject.toml` and `whyfail/__init__.py`.
  - To release:
    ```bash
    # Update version in pyproject.toml and __init__.py
    git commit -am "chore: release v0.1.1"
    git tag v0.1.1
    git push && git push --tags
    # Or create a GitHub Release; the workflow will publish to PyPI
    ```

## Issue Reporting
- Use clear, reproducible examples
- Include OS, Python version, and steps to reproduce
- Suggest expected vs actual output

## License
By contributing, you agree that your contributions are licensed under the MIT License.
