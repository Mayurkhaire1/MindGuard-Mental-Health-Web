# MindGuard 🛡️ - Advanced AI Mental Health Analysis System

MindGuard is a professional-grade Flask application designed for depression prediction and mental health screening. It utilizes advanced Natural Language Processing (NLP), emotion detection, and multi-modal assessment techniques (Text, Voice, Facial, and Wellness Journey) to identify potential mental health indicators and provide immediate crisis intervention resources.

> [!IMPORTANT]
> **Medical Disclaimer:** This system is for educational and self-awareness purposes only. It is **NOT** a substitute for professional clinical diagnosis or medical advice. If you or someone you know is in immediate danger, please contact emergency services or the helplines provided within the application.

---

## 🚀 Quick Setup Guide

### 📋 Prerequisites
- **Python:** version 3.11 or higher (Check with `python --version`)
- **Web Browser:** Google Chrome or Microsoft Edge (recommended for Web Speech API support)

---

## 💻 Installation (Windows)

1. **Clone/Download the repository** to your local machine.
2. **Open PowerShell/Command Prompt** and navigate to the project directory:
   ```powershell
   cd "path/to/MindGuard"
   ```
3. **Create a Virtual Environment:**
   ```powershell
   python -m venv .venv
   ```
4. **Activate the Environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   *(If you get a script execution error, run: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` and try again.)*
5. **Install Dependencies:**
   ```powershell
   python -m pip install --upgrade pip
   pip install -e .
   ```
6. **Set Environment Variables:**
   ```powershell
   $env:SESSION_SECRET="your_secret_key_here"
   $env:DATABASE_URL="sqlite:///mindguard.db"
   ```
7. **Run the Application:**
   ```powershell
   python main.py
   ```

---

## 🍎 Installation (macOS & Linux)

1. **Open Terminal** and navigate to the project directory:
   ```bash
   cd "path/to/MindGuard"
   ```
2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv .venv
   ```
3. **Activate the Environment:**
   ```bash
   source .venv/bin/activate
   ```
4. **Install Dependencies:**
   ```bash
   python3 -m pip install --upgrade pip
   pip install -e .
   ```
5. **Set Environment Variables:**
   ```bash
   export SESSION_SECRET="your_secret_key_here"
   export DATABASE_URL="sqlite:///mindguard.db"
   ```
6. **Run the Application:**
   ```bash
   python3 main.py
   ```

---

## 🛠️ Feature Overview

- **Core Text Analysis**: Submit written text to detect emotional valence and depressive markers.
- **Wellness Journey**: A 5-step comprehensive assessment covering stress, symptoms, safety, and personal reflection.
- **Multi-Modal Simulation**:
  - **Voice Analysis**: Speech-to-text transcript analysis for vocal markers.
  - **Facial Analysis**: Camera-assisted mood introspection.
  - **Heart Rate Analysis**: Physiological symptom questionnaire.
- **Reporting System**: Generates detailed PDF reports using `ReportLab` and `WeasyPrint`.
- **Dynamic Dashboard**: Real-time visualization of risk trends and emotion statistics.
- **Crisis Intervention**: Immediate redirection and resource access for high-risk flags.

---

## ❓ Troubleshooting

### 1. Missing NLTK Data
If you encounter an error regarding `punkt` or `stopwords`, run this in your terminal (with venv active):
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### 2. PDF Generation Errors
If PDF reports fail to download, ensure you have the required fonts or that `weasyprint` dependencies (like Gtk+ for Windows) are installed correctly. ReportLab should work out of the box for standard layouts.

### 3. Microphone/Camera Access
Most browsers require a **Secure Connection (HTTPS)** or **Localhost** to allow camera/mic access. If running on a local IP/network, ensure your browser permissions are set to allow the site.

---

## ⚙️ Project Structure
- `app.py`: Database and Flask app configuration.
- `routes.py`: Core routing and business logic.
- `depression_predictor.py`: The heart of the NLP analysis system.
- `static/`: Contains CSS (Tailwind/Custom), JS (Charts.js), and assets.
- `templates/`: HTML files for various assessment modules.
- `models.py`: Database schemas for sessions and metrics.

---

## 📄 License
This project is proprietary and intended for developmental use. Please refer to the author for licensing inquiries.
