# 🚀 SignalMatrix Repo

**SignalMatrix Repo** is a premium GitHub Portfolio Analyzer designed for technical recruiters and engineering managers. It provides a deep, multi-layered evaluation of a developer's engineering profile by combining deterministic scoring with AI-driven qualitative reasoning.

---

## ✨ Key Features

- **🏆 Deterministic Scoring (0-50)**: A rigorous evaluation based on 5 core metrics:
  - **Consistency**: Analysis of commit patterns over time.
  - **Engineering Depth**: Modular structure, documentation density, and repo complexity.
  - **Clarity**: Evaluation of READMEs and project organization.
  - **Focus**: Language specialization vs. "jack-of-all-trades" dispersion.
  - **Production Readiness**: Presence of CI/CD, unit tests, and releases.
- **🤝 Collaboration Score**: Quantifies contributions to shared or public repositories.
- **📈 Maturity Trend**: Analyzes the evolution of project complexity over time.
- **🚩 Red Flag Detection**: Identifies issues like fork-heavy profiles or repetitive commits.
- **🤖 AI Reasoning Engine**: Generates a professional Executive Summary and a 30-Day Improvement Roadmap.
- **💎 Premium UI**: A glassmorphic, dark-mode dashboard with smooth animations.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **Frontend**: Vanilla HTML/CSS/JS (Modern Glassmorphism)
- **API Integration**: GitHub REST API, OpenAI API (GPT-4o-mini)
- **Architecture**: 6-Layer Modular System

---

## � Quick Start

### 1. Prerequisites
- Python 3.10+
- GitHub Personal Access Token
- OpenAI API Key

### 2. Setup
```powershell
# Clone the repository
git clone https://github.com/yourusername/signalmatrix-repo.git
cd signalmatrix-repo

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
copy .env.example .env
```

### 3. Configuration
Open the `.env` file and add your credentials. The application uses **Pydantic Settings** to validate these variables on startup.

```env
GITHUB_TOKEN=ghp_...
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

> [!IMPORTANT]
> **Security Note:** Never commit your `.env` file. It is included in `.gitignore` by default. For production deployment, ensure these are set as environment variables in your hosting environment.

#### Input Validation
The API includes built-in validation for GitHub usernames to prevent malformed requests (alphanumeric and single hyphens, 1-39 characters).

### 4. Run Application
```powershell
python -m uvicorn app.main:app --reload --reload-dir app
```
Visit `http://127.0.0.1:8000` to start analyzing.

---

## 🏗️ 6-Layer Architecture

1. **GitHub Collector**: High-performance data retrieval with rate-limit handling.
2. **Signal Extraction**: Translating raw API data into engineering signals.
3. **Scoring Engine**: Mathematical weighting of signals into a unified metric.
4. **AI Reasoning**: Qualitative synthesis of results using GPT-4o-mini.
5. **Report Generator**: Consolidating data into a structured JSON report.
6. **Frontend Renderer**: Dynamic dashboard for recruiter-style presentation.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
