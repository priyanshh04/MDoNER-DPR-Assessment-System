from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime
import json

# Import our modules
try:
    from dpr_analyzer import DPRAnalyzer
    from risk_predictor import RiskPredictor
    from pdf_processor import PDFProcessor
    from report_generator import ReportGenerator
    from database_manager import DatabaseManager
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some modules not available: {e}")
    MODULES_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('reports', exist_ok=True)
os.makedirs('logs', exist_ok=True)

# Initialize components if available
if MODULES_AVAILABLE:
    try:
        dpr_analyzer = DPRAnalyzer()
        risk_predictor = RiskPredictor()
        pdf_processor = PDFProcessor()
        report_generator = ReportGenerator()
        db_manager = DatabaseManager()
        logger.info("All modules loaded successfully")
    except Exception as e:
        logger.error(f"Error initializing modules: {e}")
        MODULES_AVAILABLE = False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main HTML file"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head><title>MDoNER DPR System</title></head>
        <body>
            <h1>MDoNER DPR Assessment System</h1>
            <p>index.html file not found. Please create the HTML file.</p>
        </body>
        </html>
        """)

@app.route('/style.css')
def serve_css():
    return send_from_directory('.', 'style.css')

@app.route('/app.js')
def serve_js():
    return send_from_directory('.', 'app.js')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'modules_loaded': MODULES_AVAILABLE
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"File uploaded: {filename}")
        
        # Perform analysis
        if MODULES_AVAILABLE:
            text_content = pdf_processor.extract_text(filepath)
            analysis_result = dpr_analyzer.analyze_dpr(text_content, filename)
            risk_analysis = risk_predictor.predict_risks(analysis_result)
            
            result = {
                'analysis_id': timestamp,
                'file_info': {
                    'filename': file.filename,
                    'uploaded_at': datetime.now().isoformat(),
                    'file_size': os.path.getsize(filepath)
                },
                'analysis': analysis_result,
                'risks': risk_analysis,
                'recommendations': dpr_analyzer.generate_recommendations(analysis_result)
            }
            
            # Store in database
            db_manager.store_analysis(result)
            
        else:
            # Fallback demo data
            result = generate_demo_data(file.filename)
        
        # Clean up
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/demo', methods=['GET'])
def demo_analysis():
    """Generate demo analysis"""
    return jsonify(generate_demo_data("Demo_DPR_Infrastructure_Project.pdf"))

@app.route('/api/report/<analysis_id>', methods=['GET'])
def generate_report_endpoint(analysis_id):
    """Generate analysis report"""
    try:
        if MODULES_AVAILABLE:
            analysis_data = db_manager.get_analysis(analysis_id)
            if not analysis_data:
                return jsonify({'error': 'Analysis not found'}), 404
            
            pdf_buffer = report_generator.generate_pdf_report(analysis_data)
            return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, 
                           download_name=f'DPR_Report_{analysis_id}.pdf')
        else:
            # Generate text report
            report_text = generate_text_report(analysis_id)
            return report_text, 200, {'Content-Type': 'text/plain'}
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_demo_data(filename="Demo_Project.pdf"):
    """Generate realistic demo data"""
    return {
        'analysis_id': 'demo_' + datetime.now().strftime('%Y%m%d_%H%M%S'),
        'file_info': {
            'filename': filename,
            'uploaded_at': datetime.now().isoformat(),
            'file_size': 1024000
        },
        'analysis': {
            'filename': filename,
            'overall_score': 78,
            'completeness_percentage': 80,
            'section_analyses': {
                'Context/Background': {'score': 85, 'completeness': 90, 'quality': 80},
                'Problems Addressed': {'score': 90, 'completeness': 95, 'quality': 85},
                'Project Objectives': {'score': 75, 'completeness': 80, 'quality': 70},
                'Technology Issues': {'score': 70, 'completeness': 75, 'quality': 65},
                'Management Arrangements': {'score': 80, 'completeness': 85, 'quality': 75},
                'Means of Finance': {'score': 75, 'completeness': 80, 'quality': 70},
                'Time Frame': {'score': 65, 'completeness': 70, 'quality': 60},
                'Target Beneficiaries': {'score': 85, 'completeness': 90, 'quality': 80},
                'Legal Framework': {'score': 80, 'completeness': 85, 'quality': 75},
                'Risk Analysis': {'score': 60, 'completeness': 65, 'quality': 55}
            },
            'quality_scores': {
                'data_accuracy': 82,
                'completeness': 78,
                'technical_viability': 74,
                'compliance': 85,
                'budget_realism': 70
            }
        },
        'risks': {
            'overall_risk': {'level': 'Medium', 'score': 55.0},
            'risk_predictions': {
                'Budget Overrun Risk': {'probability': 70, 'level': 'High', 'severity': 'Medium'},
                'Timeline Delay Risk': {'probability': 55, 'level': 'Medium', 'severity': 'Low'},
                'Technical Implementation Risk': {'probability': 65, 'level': 'High', 'severity': 'High'},
                'Compliance Risk': {'probability': 25, 'level': 'Low', 'severity': 'Low'},
                'Resource Availability Risk': {'probability': 45, 'level': 'Medium', 'severity': 'Medium'}
            }
        },
        'recommendations': [
            {'priority': 'High', 'category': 'Risk Analysis', 'recommendation': 'Enhance risk analysis section with detailed mitigation strategies'},
            {'priority': 'Medium', 'category': 'Timeline', 'recommendation': 'Provide more realistic timeline with buffer periods'},
            {'priority': 'Medium', 'category': 'Budget', 'recommendation': 'Include detailed cost breakdown with market analysis'},
            {'priority': 'Low', 'category': 'Technical', 'recommendation': 'Add technical feasibility validation studies'}
        ]
    }

def generate_text_report(analysis_id):
    """Generate simple text report"""
    return f"""
MDoNER DPR QUALITY ASSESSMENT REPORT
===================================

Analysis ID: {analysis_id}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
----------------
Overall Quality Score: 78/100
Risk Level: Medium
Completeness: 80%

SECTION ANALYSIS
---------------
Context/Background: 85/100
Problems Addressed: 90/100
Project Objectives: 75/100
Technology Issues: 70/100
Management Arrangements: 80/100
Means of Finance: 75/100
Time Frame: 65/100
Target Beneficiaries: 85/100
Legal Framework: 80/100
Risk Analysis: 60/100

RECOMMENDATIONS
--------------
1. [High] Enhance risk analysis section
2. [Medium] Improve timeline realism
3. [Medium] Strengthen budget analysis
4. [Low] Add technical validation

Generated by MDoNER DPR Assessment System
    """

if __name__ == '__main__':
    print("🚀 Starting MDoNER DPR Assessment System...")
    print("📁 Upload folder:", os.path.abspath(UPLOAD_FOLDER))
    print("🌐 Server starting at: http://localhost:5000")
    print("💡 Open your browser and navigate to the URL above")
    print("")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
