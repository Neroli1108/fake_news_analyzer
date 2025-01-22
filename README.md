# Fake News Analyzer

A simple Python project that attempts to detect whether a given piece of news or text is likely to be fake or real. This repository includes a Flask web application, a Hugging Face transformer–based detector, and (optionally) a Google Gemini–based approach.

## Requirements

- **Python 3.11** is **strongly recommended** for this project (and tested with this version).
- pip (package installer for Python)  
- (Optional) A [Google Gemini API key](https://cloud.google.com/).

## Project Features

- **Flask Web App**: Serve a simple interface for pasting text and getting a classification.  
- **Hugging Face Zero-Shot Classifier**: Detects whether text is “fake news,” “real news,” “propaganda,” or “satire.”  
- **(Optional) Google Gemini**: Integrates a generative AI model for classification if you have a valid API key.  

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fake_news_analyzer.git
cd fake_news_analyzer
```

### 2. Install Python 3.11

Ensure you have **Python 3.11** installed and available on your system. You can check this with:

```bash
python3 --version
```

If it doesn’t show `3.11.x`, download and install from [python.org](https://www.python.org/downloads/) or use a package manager (like Homebrew on macOS).

### 3. (Optional) Create a Virtual Environment

Although not required, using a virtual environment can keep your system clean and dependencies isolated:

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or venv\Scripts\activate on Windows
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> If you’re not using a virtual environment, run the above commands with the Python 3.11 interpreter:  
> ```bash
> python3.11 -m pip install --upgrade pip
> python3.11 -m pip install -r requirements.txt
> ```

### 5. Set up (Optional) Gemini API Key

If you plan to use the **Google Gemini** detector, you need an API key. Add your key either:
- as an environment variable, or
- directly in your config, or
- pass it via the web form if your app supports it.

### 6. Run the Flask Application

```bash
python app.py
```

By default, Flask runs on [http://127.0.0.1:5000](http://127.0.0.1:5000).

### 7. Using the App

1. Open your browser at `http://127.0.0.1:5000`.  
2. Paste some text or news snippet you want to analyze.  
3. Depending on your setup, choose **Hugging Face** or **Gemini** as the detection method.  
4. (If using Gemini) Enter your API key if required.  
5. Click **Analyze**. The app will:
   - Classify the text (e.g., “fake news,” “real news,” etc.).  
   - Show confidence scores and optional cross-check info.

### 8. Deactivate Environment

When you’re done, if you used a virtual environment:

```bash
deactivate
```

---

## Project Structure

```
fake_news_analyzer/
├── app.py                            # Main Flask application
├── requirements.txt                  # Dependencies
├── README.md                         # This file
└── detector/
    ├── fake_news_detector.py         # Hugging Face approach
    ├── gemini_fake_news_detector.py  # Google Gemini approach
    ├── news_analysis_service.py      # Main analysis orchestration
    └── __init__.py
```

---

## Contributing

1. Fork this repository.  
2. Create a new branch: `git checkout -b my-new-feature`.  
3. Make your changes and commit them: `git commit -m 'Add some feature'`.  
4. Push to the branch: `git push origin my-new-feature`.  
5. Create a pull request.

---

## License

[MIT License](LICENSE) – feel free to use and modify this project as you like.

---

**Enjoy using the Fake News Analyzer!** If you have any questions or run into issues, please open an [issue](https://github.com/yourusername/fake_news_analyzer/issues) on GitHub.