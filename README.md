# DataForge CLI: Production-Ready Crypto ETL Pipeline

An enterprise-grade, decoupled **Extract, Transform, Load (ETL) Command-Line Interface (CLI)** tool built natively for Linux environments. This system securely ingests real-time cryptocurrency metrics from external APIs, sanitizes data structures, injects operational business layers, and persists records using a robust ORM pattern.

This repository serves as a showcase of core engineering practices: **SOLID design patterns**, **automated Linux shell scripting**, **relational schema design**, **Unit Testing**, and **CI/CD pipeline automation**.

---

## 🏗️ System Architecture & SOLID Enforcement

Rather than a monolithic script, the core execution engine is split into single-responsibility boundary zones to prevent architectural drift and allow decoupled component testing:
*   **Single Responsibility (S):** `CryptoProvider` only handles networking; `DataTransformer` handles data structural calculations; `DataSaver` isolates transaction management.
*   **Open/Closed (O) & Dependency Inversion (D):** Data pipelines are structurally mapped out via abstractions. Changing downstream targets or updating ingress API schemas requires zero structural changes to the orchestration layer.
*   **Interface Segregation (I):** Model boundaries decouple transaction contexts from persistence instances cleanly.

---

## 🛠️ Tech Stack & Skills Highlighted

*   **Language:** Python (OOP, Advanced Type Hinting, Data Classes)
*   **Linux & Shell Scripting:** POSIX-compliant Bash scripting for environments orchestration, execution permissions (`chmod +x`), and automated CLI parameter routing (`argparse`).
*   **Database & ORM:** SQLAlchemy ORM coupled with raw-equivalent data mapping, relational database transactional state safety (`session.rollback()`), and automated table creation.
*   **Testing & CI/CD:** Enterprise regression verification via `pytest`. Continuous Integration powered by GitHub Actions executing workflows on native `ubuntu-latest` instances.
*   **Git Lifecycle:** Enforced structural history through atomic updates using the *Conventional Commits* standard.

---

## 📂 Repository Structure

```text
├── .github/workflows/      # Continuous Integration Pipelines (GitHub Actions)
├── core/
│   ├── providers/          # Ingress Layer: API consumers (Network isolated)
│   ├── transformers/       # Business Logic Layer: Data validation and metrics (Pure code)
│   └── data_saver.py       # Persistence Layer: Translates items into ORM operations
├── database/
│   ├── connection.py       # SQLite engine assembly and safe transactional context sessions
│   └── models.py           # SQLAlchemy declarative schema configurations
├── docs/
│   ├── pseudocode.md       # Pre-implementation architectural planning layout
│   └── architecture_blueprint.md
├── scripts/
│   └── setup.sh            # Automated shell installer (Enviroment instantiation & dependencies)
├── tests/                  # Automated component regression test suites
├── main.py                 # Core CLI entry point routing native Linux flags
└── requirements.txt        # Pinned production dependency manifest
```

---

## 🚀 Getting Started (Linux / macOS)

### 1. Automated Setup
Configure your virtual environment, update system package managers, and compile the dependencies automatically with a single command:
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 2. Manual Installation (Alternative)
If you prefer setting up the components manually:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 💻 Usage

Run the data pipeline directly from the root of your workspace using native terminal flag configurations:

### Standard Run
```bash
source .venv/bin/activate
python main.py
```

### Debug Run (Verbose Logs)
Displays real-time logs tracing extraction checkpoints, object structural sizes, and persistence lifecycle transactions:
```bash
python main.py --debug
```

---

## 🧪 Automated Testing Suite

The transformation engine is fully decoupled from external connections, enabling instant mock verification through the test pipeline.

Execute the testing harness locally:
```bash
pytest tests/ -v
```

---

## 🤖 Continuous Integration Pipeline

Every single `push` or `pull_request` targeted at the `main` or `develop` branches automatically spawns a GitHub runner that performs the following quality checks:
1. Validates structural syntax integrity.
2. Runs the POSIX `./scripts/setup.sh` to ensure cross-environment deployability.
3. Triggers the complete `pytest` unit test array.

This guarantees that master environments are persistently deployable and structurally sound.