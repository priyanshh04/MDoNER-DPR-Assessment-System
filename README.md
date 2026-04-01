# 🏛️ MDoNER DPR Assessment System

## AI-Powered Detailed Project Report Quality Assessment Platform

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

A comprehensive web-based platform designed for the **Ministry of Development of North Eastern Region (MDoNER)** to assess the quality of Detailed Project Reports (DPRs) using advanced **Natural Language Processing** and **Machine Learning** techniques.

---

## 🌟 Features

### 🔍 AI-Powered Analysis
- Advanced NLP for document text extraction and analysis  
- Machine Learning risk prediction models  
- Automated quality assessment across 10 mandatory DPR sections  
- Intelligent scoring based on MDoNER guidelines  

### 📊 Interactive Dashboard
- Real-time analysis with progress tracking  
- Professional dark theme UI matching government portals  
- Responsive design for desktop and mobile devices  
- Interactive charts using Chart.js  

### 🎯 Comprehensive Assessment
- Section-wise analysis of all 10 DPR sections  
- ML-based risk prediction (5 major categories)  
- Quality metrics: accuracy, completeness, feasibility  
- Smart recommendations with priority ranking  

### 📄 Document Processing
- Supports PDF, Word (.doc/.docx), and text files  
- Text extraction using PyPDF2, pdfplumber, python-docx  
- Handles files up to 16MB  
- Graceful fallback mechanisms  

### 📈 Reporting & Export
- PDF reports using ReportLab  
- JSON export support  
- Historical tracking using SQLite  
- Project comparison features  

---

## 🚀 Demo

### Folder Structure
```plaintext
MDoNER_DPR_Assessment_System/
├── app.js
├── app.py
├── database_manager.py
├── dpr_analysis.db
├── dpr_analyzer.py
├── dpr_validator.py
├── index.html
├── pdf_processor.py
├── report_generator.py
├── requirements.txt
├── risk_predictor.py
├── style.css
├── logs/
├── reports/
├── uploads/
├── .vscode/
│   └── launch.json
├── .venv/
└── __pycache__/
```

### Live Demo
Try the demo analysis to see the system in action without uploading any files.

## 🛠️ Technology Stack

### Backend
- **Python 3.9+** - Core programming language
- **Flask** - Web framework
- **SQLite** - Database for analysis storage
- **scikit-learn** - Machine learning models
- **NLTK & TextBlob** - Natural language processing
- **ReportLab** - PDF report generation

### Frontend
- **HTML5/CSS3** - Modern responsive design
- **Vanilla JavaScript** - Interactive functionality
- **Chart.js** - Data visualization
- **Professional Dark Theme** - Government portal styling

### Document Processing
- **PyPDF2** - PDF text extraction
- **pdfplumber** - Enhanced PDF processing
- **python-docx** - Word document processing
- **Intelligent fallbacks** - Graceful degradation when libraries unavailable

## 📋 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Modern web browser

### Quick Start

**Clone the repository**
