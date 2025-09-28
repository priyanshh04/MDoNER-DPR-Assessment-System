# 🏛️ MDoNER DPR Assessment System

## AI-Powered Detailed Project Report Quality Assessment Platform

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

A comprehensive web-based platform designed for the **Ministry of Development of North Eastern Region (MDoNER)** to assess the quality of Detailed Project Reports (DPRs) using advanced **Natural Language Processing** and **Machine Learning** techniques.

## 🌟 Features

### 🔍 AI-Powered Analysis
- **Advanced NLP** for document text extraction and analysis
- **Machine Learning** risk prediction models
- **Automated quality assessment** across 10 mandatory DPR sections
- **Intelligent scoring** based on MDoNER guidelines

### 📊 Interactive Dashboard
- **Real-time analysis** with progress tracking
- **Professional dark theme** UI matching government portals
- **Responsive design** for desktop and mobile devices
- **Interactive charts** using Chart.js for data visualization

### 🎯 Comprehensive Assessment
- **Section-wise Analysis**: Detailed evaluation of all 10 DPR sections
- **Risk Assessment**: ML-based prediction of 5 major risk categories
- **Quality Metrics**: Data accuracy, completeness, technical viability assessment
- **Smart Recommendations**: Priority-based improvement suggestions

### 📄 Document Processing
- **Multi-format Support**: PDF, Word documents (.docx/.doc), and text files
- **Intelligent Text Extraction**: Using PyPDF2, pdfplumber, and python-docx
- **Large File Handling**: Support for documents up to 16MB
- **Fallback Processing**: Graceful handling when libraries are unavailable

### 📈 Reporting & Export
- **PDF Report Generation**: Comprehensive analysis reports using ReportLab
- **Data Export**: JSON format for further analysis
- **Historical Tracking**: SQLite database for analysis history
- **Comparison Features**: Benchmarking against similar projects

## 🚀 Demo

### Screenshots

**Upload Interface**
![Upload Interface](assets/upload-interface.png)

**Analysis Dashboard**
![Analysis Dashboard](assets/dashboard.png)

**Detailed Results**
![Detailed Results](assets/detailed-analysis.png)

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

1. **Clone the repository**
