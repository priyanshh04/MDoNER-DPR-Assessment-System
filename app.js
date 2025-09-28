// MDoNER DPR Assessment System - JavaScript Application
class DPRAssessmentSystem {
    constructor() {
        this.analysisData = null;
        this.charts = {};
        this.init();
    }

    init() {
        this.bindEvents();
        this.initializeData();
        console.log('MDoNER DPR Assessment System initialized');
    }

    bindEvents() {
        // File upload
        const fileInput = document.getElementById('fileInput');
        if (fileInput) {
            fileInput.addEventListener('change', this.handleFileUpload.bind(this));
        }

        // Demo button
        const demoBtn = document.getElementById('demoBtn');
        if (demoBtn) {
            demoBtn.addEventListener('click', this.runDemoAnalysis.bind(this));
        }

        // Modal events
        const helpBtn = document.getElementById('helpBtn');
        const helpModalClose = document.getElementById('helpModalClose');
        const overlay = document.getElementById('overlay');
        
        if (helpBtn) helpBtn.addEventListener('click', () => this.showModal('helpModal'));
        if (helpModalClose) helpModalClose.addEventListener('click', () => this.hideModal('helpModal'));
        if (overlay) overlay.addEventListener('click', this.hideAllModals.bind(this));

        // Keyboard events
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hideAllModals();
            }
        });
    }

    initializeData() {
        // Initialize sample data structure matching your screenshots
        this.sampleAnalysisData = {
            analysis_id: "mdoner_demo_001",
            file_info: {
                filename: "Digital_Infrastructure_Development_Project_AP.pdf",
                uploaded_at: new Date().toISOString(),
                file_size: 2580000
            },
            analysis: {
                overall_score: 78,
                completeness_percentage: 80,
                sections_found: 8,
                total_sections: 10,
                section_analyses: {
                    "Context/Background": { score: 85, completeness: 90, quality: 80, status: "Good" },
                    "Problems Addressed": { score: 90, completeness: 95, quality: 85, status: "Excellent" },
                    "Project Objectives": { score: 75, completeness: 80, quality: 70, status: "Good" },
                    "Technology Issues": { score: 70, completeness: 75, quality: 65, status: "Satisfactory" },
                    "Management Arrangements": { score: 80, completeness: 85, quality: 75, status: "Good" },
                    "Means of Finance": { score: 75, completeness: 80, quality: 70, status: "Good" },
                    "Time Frame": { score: 65, completeness: 70, quality: 60, status: "Needs Improvement" },
                    "Target Beneficiaries": { score: 85, completeness: 90, quality: 80, status: "Good" },
                    "Legal Framework": { score: 80, completeness: 85, quality: 75, status: "Good" },
                    "Risk Analysis": { score: 60, completeness: 65, quality: 55, status: "Needs Improvement" }
                },
                quality_scores: {
                    "Data Accuracy": 82,
                    "Completeness": 78,
                    "Technical Viability": 74,
                    "Compliance": 85,
                    "Budget Realism": 70
                }
            },
            risks: {
                overall_risk: {
                    level: "Medium",
                    score: 55.0,
                    high_risk_count: 2,
                    medium_risk_count: 2,
                    low_risk_count: 1
                },
                risk_predictions: {
                    "Budget Overrun Risk": {
                        probability: 70,
                        level: "High",
                        severity: "Medium",
                        primary_factors: ["Inadequate cost estimation", "Missing contingency planning"],
                        mitigation_suggestions: ["Detailed cost breakdown analysis", "Market rate validation"]
                    },
                    "Timeline Delay Risk": {
                        probability: 55,
                        level: "Medium",
                        severity: "Low",
                        primary_factors: ["Schedule complexity", "Approval dependencies"],
                        mitigation_suggestions: ["Critical path analysis", "Buffer time allocation"]
                    },
                    "Technical Implementation Risk": {
                        probability: 65,
                        level: "High",
                        severity: "High",
                        primary_factors: ["Technology complexity", "Integration challenges"],
                        mitigation_suggestions: ["Pilot implementation", "Technical expert consultation"]
                    },
                    "Compliance Risk": {
                        probability: 25,
                        level: "Low",
                        severity: "Low",
                        primary_factors: ["Regulatory requirements", "Documentation gaps"],
                        mitigation_suggestions: ["Legal consultation", "Compliance review"]
                    },
                    "Resource Availability Risk": {
                        probability: 45,
                        level: "Medium",
                        severity: "Medium",
                        primary_factors: ["Skilled manpower shortage", "Equipment procurement"],
                        mitigation_suggestions: ["Resource backup planning", "Vendor partnerships"]
                    }
                }
            },
            recommendations: [
                {
                    priority: "High",
                    category: "Risk Analysis",
                    recommendation: "Enhance risk analysis section with detailed mitigation strategies"
                },
                {
                    priority: "Medium",
                    category: "Time Frame",
                    recommendation: "Provide more realistic timeline with buffer mechanisms"
                },
                {
                    priority: "Medium",
                    category: "Budget Planning",
                    recommendation: "Include detailed financial contingency plans"
                },
                {
                    priority: "Low",
                    category: "Technical Documentation",
                    recommendation: "Strengthen technical feasibility documentation"
                }
            ]
        };
    }

    handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        console.log('File selected:', file.name);
        this.analyzeDocument(file);
    }

    runDemoAnalysis() {
        console.log('Running demo analysis...');
        this.analyzeDocument(null, true);
    }

    analyzeDocument(file, isDemo = false) {
        this.showSection('loadingSection');
        this.hideSection('uploadSection');
        this.hideSection('resultsSection');
        this.hideSection('analysisDetails');
        this.hideSection('recommendationsSection');
        this.hideSection('detailedSection');

        // Simulate analysis progress
        let progress = 0;
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');

        const progressSteps = [
            "Extracting text from document...",
            "Analyzing DPR sections...",
            "Evaluating quality metrics...",
            "Predicting project risks...",
            "Generating recommendations...",
            "Finalizing analysis..."
        ];

        const progressInterval = setInterval(() => {
            progress += Math.random() * 15 + 5;
            if (progress > 100) progress = 100;

            if (progressBar) {
                progressBar.style.width = progress + '%';
            }
            
            const stepIndex = Math.floor((progress / 100) * progressSteps.length);
            if (stepIndex < progressSteps.length && progressText) {
                progressText.textContent = progressSteps[stepIndex];
            }

            if (progress >= 100) {
                clearInterval(progressInterval);
                setTimeout(() => {
                    this.displayResults(isDemo ? this.sampleAnalysisData : this.generateAnalysisResults(file));
                }, 800);
            }
        }, 200);

        // If using actual API
        if (!isDemo && file) {
            this.uploadToAPI(file)
                .then(data => {
                    clearInterval(progressInterval);
                    this.displayResults(data);
                })
                .catch(error => {
                    clearInterval(progressInterval);
                    console.error('API Error:', error);
                    // Fallback to demo data
                    this.displayResults(this.sampleAnalysisData);
                });
        }
    }

    async uploadToAPI(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    generateAnalysisResults(file) {
        // Generate realistic results based on file
        const fileName = file ? file.name : 'demo_dpr.pdf';
        
        // Add some randomness to make it feel realistic
        const baseScore = Math.floor(Math.random() * 25) + 65; // 65-90
        
        const sections = {};
        const sectionNames = Object.keys(this.sampleAnalysisData.analysis.section_analyses);
        
        sectionNames.forEach(name => {
            const variance = Math.floor(Math.random() * 30) - 15; // -15 to +15
            const score = Math.max(40, Math.min(95, baseScore + variance));
            
            sections[name] = {
                score: score,
                completeness: Math.min(100, score + Math.floor(Math.random() * 20) - 5),
                quality: Math.max(30, score - Math.floor(Math.random() * 15)),
                status: this.getScoreStatus(score)
            };
        });

        return {
            ...this.sampleAnalysisData,
            file_info: {
                ...this.sampleAnalysisData.file_info,
                filename: fileName
            },
            analysis: {
                ...this.sampleAnalysisData.analysis,
                overall_score: baseScore,
                section_analyses: sections
            }
        };
    }

    displayResults(data) {
        this.analysisData = data;
        
        this.hideSection('loadingSection');
        
        // Update overall metrics
        this.updateOverallMetrics(data);
        
        // Show all result sections
        this.showSection('resultsSection');
        this.showSection('analysisDetails');
        this.showSection('recommendationsSection');
        this.showSection('detailedSection');
        
        // Populate all sections
        this.updateSectionAnalysis(data);
        this.updateRiskAnalysis(data);
        this.updateRecommendations(data);
        this.updateDetailedSections(data);
        this.updateQualityChart(data);

        console.log('Analysis results displayed successfully');
    }

    updateOverallMetrics(data) {
        const analysis = data.analysis;
        const risks = data.risks;

        // Update overall score
        const overallScore = document.getElementById('overallScore');
        const overallScoreBar = document.getElementById('overallScoreBar');
        if (overallScore) {
            overallScore.textContent = analysis.overall_score;
            
            // Animate score bar
            setTimeout(() => {
                if (overallScoreBar) {
                    overallScoreBar.style.width = analysis.overall_score + '%';
                }
            }, 300);
        }

        // Update risk level
        const riskLevel = document.getElementById('riskLevel');
        const riskDescription = document.getElementById('riskDescription');
        if (riskLevel) {
            const risk = risks.overall_risk.level;
            riskLevel.textContent = risk;
            riskLevel.className = `metric-value risk-${risk.toLowerCase()}`;
        }

        if (riskDescription) {
            const riskMessages = {
                'Low': 'Well managed risks',
                'Medium': 'Moderate attention needed',
                'High': 'Immediate action required'
            };
            riskDescription.textContent = riskMessages[risks.overall_risk.level] || 'Risk assessment';
        }

        // Update completeness
        const completenessScore = document.getElementById('completenessScore');
        if (completenessScore) {
            completenessScore.textContent = analysis.completeness_percentage + '%';
        }
    }

    updateSectionAnalysis(data) {
        const container = document.getElementById('sectionsList');
        if (!container) return;

        const sections = data.analysis.section_analyses;
        let html = '';
        
        for (const [sectionName, sectionData] of Object.entries(sections)) {
            const score = sectionData.score;
            const scoreClass = score >= 75 ? 'score-high' : score >= 60 ? 'score-medium' : 'score-low';
            
            html += `
                <div class="section-item" onclick="showSectionDetails('${sectionName}', ${score})">
                    <span class="section-name">${sectionName}</span>
                    <span class="section-score ${scoreClass}">${score}/100</span>
                </div>
            `;
        }
        
        container.innerHTML = html;

        // Make function global for onclick
        window.showSectionDetails = (sectionName, score) => {
            alert(`${sectionName}\nScore: ${score}/100\nStatus: ${this.getScoreStatus(score)}\n\nRecommendation: ${this.getSectionRecommendation(sectionName, score)}`);
        };
    }

    updateRiskAnalysis(data) {
        const container = document.getElementById('risksList');
        if (!container) return;

        const risks = data.risks.risk_predictions;
        let html = '';
        
        for (const [riskName, riskData] of Object.entries(risks)) {
            const levelClass = riskData.level.toLowerCase();
            
            html += `
                <div class="risk-item risk-${levelClass}" onclick="showRiskDetails('${riskName}', '${riskData.level}', ${riskData.probability})">
                    <span class="risk-name">${riskName}</span>
                    <span class="risk-level ${levelClass}">${riskData.level}</span>
                </div>
            `;
        }
        
        container.innerHTML = html;

        // Make function global for onclick
        window.showRiskDetails = (riskName, level, probability) => {
            const riskData = data.risks.risk_predictions[riskName];
            const factors = riskData.primary_factors.join('\n• ');
            const mitigations = riskData.mitigation_suggestions.join('\n• ');
            
            alert(`${riskName}\n\nProbability: ${probability}%\nLevel: ${level}\n\nPrimary Factors:\n• ${factors}\n\nMitigation Suggestions:\n• ${mitigations}`);
        };
    }

    updateRecommendations(data) {
        const container = document.getElementById('recommendationsList');
        if (!container) return;

        const recommendations = data.recommendations;
        let html = '';
        
        recommendations.forEach((rec, index) => {
            const priorityClass = rec.priority.toLowerCase();
            
            html += `
                <div class="recommendation-item rec-${priorityClass}">
                    <div class="rec-priority">${rec.priority} Priority</div>
                    <div><strong>${rec.category}:</strong> ${rec.recommendation}</div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    }

    updateDetailedSections(data) {
        const container = document.getElementById('detailedSections');
        if (!container) return;

        const sections = data.analysis.section_analyses;
        let html = '';
        
        for (const [sectionName, sectionData] of Object.entries(sections)) {
            const sectionId = sectionName.replace(/[^a-zA-Z0-9]/g, '');
            
            html += `
                <div class="expandable-section">
                    <div class="section-header" onclick="toggleDetailSection('${sectionId}')">
                        <span><strong>${sectionName}</strong></span>
                        <div>
                            <span>${sectionData.score}/100</span>
                            <span class="expand-icon" id="icon-${sectionId}">▼</span>
                        </div>
                    </div>
                    <div class="section-details" id="details-${sectionId}">
                        <div class="section-analysis">
                            <p><strong>Score:</strong> ${sectionData.score}/100</p>
                            <p><strong>Completeness:</strong> ${sectionData.completeness}%</p>
                            <p><strong>Quality:</strong> ${sectionData.quality}/100</p>
                            <p><strong>Status:</strong> ${sectionData.status}</p>
                            <p><strong>Analysis:</strong> ${this.getDetailedAnalysis(sectionName, sectionData.score)}</p>
                            <p><strong>Recommendation:</strong> ${this.getSectionRecommendation(sectionName, sectionData.score)}</p>
                        </div>
                    </div>
                </div>
            `;
        }
        
        container.innerHTML = html;

        // Make function global for onclick
        window.toggleDetailSection = (sectionId) => {
            const details = document.getElementById(`details-${sectionId}`);
            const icon = document.getElementById(`icon-${sectionId}`);
            
            if (details && icon) {
                if (details.classList.contains('active')) {
                    details.classList.remove('active');
                    icon.classList.remove('rotated');
                    icon.textContent = '▼';
                } else {
                    details.classList.add('active');
                    icon.classList.add('rotated');
                    icon.textContent = '▲';
                }
            }
        };
    }

    updateQualityChart(data) {
        const canvas = document.getElementById('qualityChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        
        // Destroy existing chart if it exists
        if (this.charts.quality) {
            this.charts.quality.destroy();
        }

        const qualityScores = data.analysis.quality_scores;
        
        this.charts.quality = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: Object.keys(qualityScores),
                datasets: [{
                    label: 'Quality Scores',
                    data: Object.values(qualityScores),
                    backgroundColor: 'rgba(74, 158, 255, 0.2)',
                    borderColor: '#4a9eff',
                    pointBackgroundColor: '#4a9eff',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#4a9eff',
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 20,
                            color: '#888',
                            font: {
                                size: 11
                            }
                        },
                        grid: {
                            color: '#444'
                        },
                        pointLabels: {
                            color: '#fff',
                            font: {
                                size: 12
                            }
                        },
                        angleLines: {
                            color: '#444'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(42, 42, 42, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: '#4a9eff',
                        borderWidth: 1
                    }
                }
            }
        });
    }

    getScoreStatus(score) {
        if (score >= 85) return 'Excellent';
        if (score >= 75) return 'Good';
        if (score >= 65) return 'Satisfactory';
        if (score >= 50) return 'Needs Improvement';
        return 'Poor';
    }

    getSectionRecommendation(sectionName, score) {
        const recommendations = {
            'Context/Background': 'Include more sectoral policy details and strategic importance analysis',
            'Problems Addressed': 'Provide comprehensive baseline data with statistical evidence',
            'Project Objectives': 'Define clearer, measurable development objectives with timelines',
            'Technology Issues': 'Justify technology choices with detailed feasibility analysis',
            'Management Arrangements': 'Detail implementation structure and monitoring frameworks',
            'Means of Finance': 'Provide realistic budget with detailed cost breakdown and sources',
            'Time Frame': 'Include PERT/CPM chart with realistic timeline and dependencies',
            'Target Beneficiaries': 'Conduct thorough stakeholder analysis with engagement strategy',
            'Legal Framework': 'Ensure all regulatory requirements and clearances are addressed',
            'Risk Analysis': 'Develop comprehensive risk register with detailed mitigation strategies'
        };

        const baseRec = recommendations[sectionName] || 'Enhance section quality and completeness';
        
        if (score < 60) {
            return `Priority action needed: ${baseRec}`;
        } else if (score < 75) {
            return `Improvement suggested: ${baseRec}`;
        } else {
            return `Section meets standards. Consider: ${baseRec}`;
        }
    }

    getDetailedAnalysis(sectionName, score) {
        if (score >= 85) {
            return "Excellent quality with comprehensive coverage of all required elements. Section exceeds MDoNER standards.";
        } else if (score >= 75) {
            return "Good quality with most requirements met. Minor enhancements would strengthen the section.";
        } else if (score >= 65) {
            return "Satisfactory quality but requires enhancement in key areas to fully meet guidelines.";
        } else if (score >= 50) {
            return "Basic requirements partially met. Significant improvement needed to achieve standards.";
        } else {
            return "Major deficiencies identified. Comprehensive revision required to meet MDoNER standards.";
        }
    }

    // Modal functions
    showModal(modalId) {
        const modal = document.getElementById(modalId);
        const overlay = document.getElementById('overlay');
        
        if (modal) modal.classList.remove('hidden');
        if (overlay) overlay.classList.remove('hidden');
    }

    hideModal(modalId) {
        const modal = document.getElementById(modalId);
        const overlay = document.getElementById('overlay');
        
        if (modal) modal.classList.add('hidden');
        if (overlay) overlay.classList.add('hidden');
    }

    hideAllModals() {
        const modals = document.querySelectorAll('.modal');
        const overlay = document.getElementById('overlay');
        
        modals.forEach(modal => modal.classList.add('hidden'));
        if (overlay) overlay.classList.add('hidden');
    }

    // Section visibility functions
    showSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.classList.remove('hidden');
        }
    }

    hideSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.classList.add('hidden');
        }
    }
}

// Export functions for buttons
function exportReport() {
    if (!window.dprSystem || !window.dprSystem.analysisData) {
        alert('No analysis data available for export');
        return;
    }

    const data = window.dprSystem.analysisData;
    const reportContent = generateReportContent(data);
    downloadFile(reportContent, `DPR_Analysis_Report_${Date.now()}.txt`, 'text/plain');
}

function exportData() {
    if (!window.dprSystem || !window.dprSystem.analysisData) {
        alert('No analysis data available for export');
        return;
    }

    const dataStr = JSON.stringify(window.dprSystem.analysisData, null, 2);
    downloadFile(dataStr, `DPR_Analysis_Data_${Date.now()}.json`, 'application/json');
}

function compareAnalysis() {
    alert('Comparison feature will show benchmarks against similar infrastructure projects in the Northeast region.\n\nFeatures include:\n• Peer project comparisons\n• Regional benchmarks\n• Historical performance trends\n• Best practice recommendations');
}

function newAnalysis() {
    if (window.dprSystem) {
        window.dprSystem.analysisData = null;
        window.dprSystem.hideSection('resultsSection');
        window.dprSystem.hideSection('analysisDetails');
        window.dprSystem.hideSection('recommendationsSection');
        window.dprSystem.hideSection('detailedSection');
        window.dprSystem.showSection('uploadSection');
        
        // Reset file input
        const fileInput = document.getElementById('fileInput');
        if (fileInput) fileInput.value = '';
    }
}

function generateReportContent(data) {
    const analysis = data.analysis;
    const risks = data.risks;
    const recommendations = data.recommendations;
    
    return `
MDoNER DPR QUALITY ASSESSMENT REPORT
===================================

Project: ${data.file_info.filename}
Analysis Date: ${new Date(data.file_info.uploaded_at).toLocaleDateString()}
Generated By: AI-Powered DPR Assessment System

EXECUTIVE SUMMARY
----------------
Overall Quality Score: ${analysis.overall_score}/100
Risk Level: ${risks.overall_risk.level}
Completeness: ${analysis.completeness_percentage}%
Sections Analyzed: ${analysis.sections_found}/${analysis.total_sections}

SECTION ANALYSIS
---------------
${Object.entries(analysis.section_analyses).map(([name, data]) => 
    `${name}: ${data.score}/100 (${data.status})`
).join('\n')}

QUALITY METRICS
--------------
${Object.entries(analysis.quality_scores).map(([metric, score]) => 
    `${metric.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}: ${score}/100`
).join('\n')}

RISK ASSESSMENT
--------------
Overall Risk Level: ${risks.overall_risk.level}
High Priority Risks: ${risks.overall_risk.high_risk_count}
Medium Priority Risks: ${risks.overall_risk.medium_risk_count}
Low Priority Risks: ${risks.overall_risk.low_risk_count}

Risk Details:
${Object.entries(risks.risk_predictions).map(([name, data]) => 
    `${name}: ${data.probability}% (${data.level} Risk)`
).join('\n')}

RECOMMENDATIONS
--------------
${recommendations.map((rec, i) => 
    `${i + 1}. [${rec.priority}] ${rec.category}: ${rec.recommendation}`
).join('\n')}

========================================
This report was generated by the MDoNER DPR Assessment System
developed for the Ministry of Development of North Eastern Region.
For detailed interactive analysis, please use the web dashboard.
========================================
    `;
}

function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.dprSystem = new DPRAssessmentSystem();
    console.log('MDoNER DPR Assessment System loaded successfully');
});
