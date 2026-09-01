# Contributing to Nexus Quant

Welcome and thank you for your interest in contributing to **Nexus Quant**! Every contribution helps make quantitative trading analytics better for everyone.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Architecture Reference](#architecture-reference)
- [Release Process](#release-process)

---

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code. Please report unacceptable behavior to **raphasha27@github.com**.

---

## Development Setup

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Runtime |
| pip | Latest | Dependency management |
| Docker | 24.x+ | Optional containerized development |

### Step-by-Step Setup

1. **Fork and clone** the repository:
   ```bash
   git clone https://github.com/<your-username>/Nexus-Quant.git
   cd Nexus-Quant
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the development server**:
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

6. **Verify the API**:
   - Swagger UI: `http://localhost:8000/docs`

7. **Run linter locally** (optional):
   ```bash
   ruff check .
   ruff format .
   ```

---

## Code Style Guidelines

### Python (FastAPI)

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide.
- Use **Ruff** for linting and formatting — CI enforces this.
- Maximum line length: **88 characters**.
- Use type hints on all function signatures.
- Prefer async/await for I/O-bound operations.

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Functions | `snake_case` | `calculate_rsi` |
| Classes | `PascalCase` | `SignalGenerator` |
| Constants | `UPPER_SNAKE_CASE` | `DEFAULT_LOOKBACK` |
| API routes | `kebab-case` | `/api/v1/signals` |
| Database columns | `snake_case` | `created_at` |

### Quantitative-Specific Guidelines

- Document mathematical formulas in comments.
- Use numpy/pandas vectorized operations over loops.
- Validate input data ranges for financial indicators.
- Log calculation parameters for reproducibility.
- Use synthetic data for testing — never real trading data in tests.

### General

- Write meaningful variable and function names.
- Add docstrings for all public functions and classes.
- Keep functions focused and under 40 lines.
- No hardcoded secrets — use environment variables.

---

## Testing Requirements

| Type | Framework | Coverage Target |
|------|-----------|-----------------|
| Unit tests | pytest | 85%+ |
| Indicator tests | pytest | All 15+ indicators |
| API tests | FastAPI TestClient | All endpoints |

- Every new feature **must** include tests.
- Bug fixes **must** include a regression test.
- Run the full test suite before pushing:
  ```bash
  pytest tests/ -v --cov=api --cov-report=term-missing
  ```
- Tests must pass with zero warnings.

---

## Pull Request Process

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines above.

3. **Write or update tests** to cover your changes.

4. **Commit with a conventional message**:
   ```
   feat: add VWAP indicator calculation
   fix: correct Bollinger Bands standard deviation
   docs: update technical indicator documentation
   test: add tests for MACD signal line
   chore: update FastAPI dependencies
   ```

5. **Push and open a PR** against `main`.

6. **PR checklist** (all must pass before merge):
   - [ ] CI pipeline passes (linting, tests)
   - [ ] Code reviewed by at least one maintainer
   - [ ] No merge conflicts with `main`
   - [ ] Documentation updated (if applicable)
   - [ ] Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)

---

## Issue Guidelines

### Bug Reports

- Check [existing issues](../../issues) first to avoid duplicates.
- Include a clear, descriptive title.
- Provide steps to reproduce, expected vs. actual behavior.
- Include environment details: Python version, OS.
- Attach error logs if relevant.

### Feature Requests

- Describe the feature and its motivation.
- Explain the use case for trading analytics.
- Propose an implementation approach if possible.

### Labels

| Label | Description |
|-------|-------------|
| `bug` | Something is broken |
| `enhancement` | New feature or improvement |
| `good-first-issue` | Ideal for first-time contributors |
| `security` | Security-related concern |
| `help-wanted` | Community help appreciated |

---

## Architecture Reference

For detailed system design, data flow diagrams, and component interactions, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Key components to understand:
- **Technical Indicators** — 15+ indicators (SMA, EMA, RSI, MACD, Bollinger Bands, etc.)
- **Signal Generator** — Momentum-based trading signal engine
- **Anomaly Detector** — ML-powered volume-based z-score analysis
- **Portfolio Optimizer** — Mean-variance optimization with Sharpe ratio
- **FastAPI Server** — REST API with OpenAPI documentation

---

## Release Process

1. All changes merge to `main` via PR with passing CI.
2. Semantic versioning is used: `MAJOR.MINOR.PATCH`.
3. Tags are created for each release: `git tag v1.x.x`.
4. Docker images are built and published automatically via CI.
5. Release notes are generated from conventional commit messages.

---

## Questions?

Open a [discussion](../../discussions) or reach out to **raphasha27@github.com**.

Thank you for contributing to Nexus Quant!
