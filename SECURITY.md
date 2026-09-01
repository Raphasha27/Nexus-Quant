# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| v1.0.0+ | :white_check_mark: Active |
| < v1.0.0 | :x: No |

Always use the latest version to receive security patches and improvements.

---

## Reporting a Vulnerability

The Nexus Quant team takes security seriously. We appreciate your efforts to responsibly disclose any security concerns.

**Please do NOT report security vulnerabilities through public GitHub issues.**

### Step-by-Step Reporting Process

1. **Identify the vulnerability** — Document the issue with clear reproduction steps.
2. **Email the security team** at **402106633@my.richfield.ac.za** with the following:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
   - Suggested fix (if any)
3. **Wait for acknowledgment** — You will receive a response within **48 hours**.
4. **Collaborate on the fix** — We may reach out for additional details.
5. **Disclosure** — We will coordinate a public disclosure timeline with you.

### What to Include

- Type of vulnerability (e.g., data leakage, API abuse, calculation manipulation)
- Affected component and version
- Attack vector and prerequisites
- Proof of concept (if available)
- Your suggested remediation

---

## Security Response Timeline

| Phase | Timeframe |
|-------|-----------|
| Initial acknowledgment | 48 hours |
| Severity assessment | 5 business days |
| Patch development | 10–15 business days |
| Coordinated disclosure | 30 days after fix |

---

## Intended Use

This project is designed for:

- **Quantitative Analysis** — Technical indicator calculation and backtesting
- **Research** — Academic and industry financial research
- **Education** — Learning quantitative trading methodologies
- **Strategy Development** — Building and testing trading strategies
- **Paper Trading** — Simulated trading only — not for live financial transactions

## Prohibited Use

- **Live Trading** — This is not a production trading system
- **Financial Advice** — Output is for informational purposes only
- **Unauthorized Access** — Accessing systems without permission
- **Data Manipulation** — Altering market data or indicators
- **Any illegal activity** — Any use violating applicable laws

---

## Security Design

This project implements the following security measures:

- **Environment Variables** — No hardcoded secrets or API keys
- **Input Validation** — Pydantic models validate all API inputs
- **Rate Limiting** — Protection against API abuse
- **CORS Configuration** — Restricted to trusted origins
- **Dependency Scanning** — Automated vulnerability checks in CI
- **Synthetic Data** — No real market data in codebase
- **No Persistence** — Analysis data is ephemeral by default

---

## Security Best Practices for Users

When deploying or developing with Nexus Quant:

### Configuration
- Always use **environment variables** for API keys
- Never commit `.env` files or secrets to version control
- Restrict API access to trusted networks
- Use Docker for isolated deployments

### Data Protection
- Financial data may be sensitive — ensure proper access controls
- Encrypt data at rest and in transit for production deployments
- Audit access to trading signals and portfolio data
- Consider classifying data by sensitivity level

### Network
- Deploy behind a reverse proxy with TLS termination
- Enable CORS only for trusted frontend origins
- Use HTTPS for all API communications

### Dependencies
- Run `pip audit` for Python dependency vulnerabilities
- Enable Dependabot alerts for automatic vulnerability notifications
- Review dependency updates before merging

### Disclaimer
- This is an educational/research tool — not a production trading system
- Past performance of backtested strategies does not guarantee future results
- Always paper trade before live trading
- Consult a financial advisor before making investment decisions

---

## Dependency Management

### Python Dependencies

```bash
# Check for known vulnerabilities
pip install pip-audit
pip-audit

# Update dependencies
pip install --upgrade -r requirements.txt
```

### Automated Scanning

- **Dependabot** is enabled for automatic dependency update PRs.
- **CI pipeline** runs `pip-audit` on every PR.
- Review and merge Dependabot PRs promptly.

---

## Responsible Disclosure

We follow [coordinated disclosure](https://en.wikipedia.org/wiki/Coordinated_vulnerability_disclosure) principles:

- Report vulnerabilities privately before public disclosure.
- We will credit reporters in release notes (unless anonymity is preferred).
- We ask that you do not exploit the vulnerability beyond what is necessary to demonstrate it.
- We will not pursue legal action against researchers who follow this policy.

---

## Contact

- **Email**: 402106633@my.richfield.ac.za
- **General Issues**: [GitHub Issues](../../issues)

Thank you for helping keep Nexus Quant and its users safe.
