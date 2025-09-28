"""
Risk Predictor Module  
Machine Learning-based project risk assessment
"""

import logging
from datetime import datetime
import json
import random

# Try to import ML libraries
try:
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("Warning: ML libraries not available. Using rule-based risk assessment.")

logger = logging.getLogger(__name__)

class RiskPredictor:
    def __init__(self):
        self.risk_categories = [
            'Budget Overrun Risk',
            'Timeline Delay Risk', 
            'Technical Implementation Risk',
            'Compliance Risk',
            'Resource Availability Risk'
        ]
        
        self.risk_factors = {
            'Budget Overrun Risk': {
                'indicators': ['budget', 'cost', 'financial', 'estimation', 'market'],
                'weight': 0.25
            },
            'Timeline Delay Risk': {
                'indicators': ['timeline', 'schedule', 'duration', 'phase', 'milestone'],
                'weight': 0.20
            },
            'Technical Implementation Risk': {
                'indicators': ['technical', 'technology', 'implementation', 'complexity', 'integration'],
                'weight': 0.25
            },
            'Compliance Risk': {
                'indicators': ['compliance', 'regulatory', 'approval', 'legal', 'clearance'],
                'weight': 0.15
            },
            'Resource Availability Risk': {
                'indicators': ['resource', 'manpower', 'skill', 'availability', 'procurement'],
                'weight': 0.15
            }
        }
        
        if ML_AVAILABLE:
            self.models = self._train_risk_models()
        else:
            self.models = None
            
        logger.info("Risk Predictor initialized")

    def predict_risks(self, analysis_result):
        """Predict project risks based on DPR analysis"""
        logger.info("Starting risk prediction analysis")
        
        try:
            if ML_AVAILABLE and self.models:
                risk_predictions = self._predict_with_ml(analysis_result)
            else:
                risk_predictions = self._predict_with_rules(analysis_result)
            
            # Calculate overall risk
            overall_risk = self._calculate_overall_risk(risk_predictions)
            
            # Generate risk summary
            risk_summary = self._generate_risk_summary(risk_predictions, overall_risk)
            
            result = {
                'overall_risk': overall_risk,
                'risk_predictions': risk_predictions,
                'risk_summary': risk_summary,
                'generated_at': datetime.now().isoformat()
            }
            
            logger.info(f"Risk prediction completed. Overall risk: {overall_risk['level']}")
            return result
            
        except Exception as e:
            logger.error(f"Error in risk prediction: {str(e)}")
            return self._generate_fallback_risks()

    def _predict_with_ml(self, analysis_result):
        """Use ML models for risk prediction"""
        risk_predictions = {}
        
        # Extract features from analysis
        features = self._extract_features(analysis_result)
        
        for risk_category in self.risk_categories:
            model = self.models.get(risk_category)
            if model:
                try:
                    # Predict probability
                    probability = model.predict_proba([features])[0][1] * 100
                    
                    # Determine risk level
                    if probability >= 60:
                        level = 'High'
                        severity = 'High'
                    elif probability >= 40:
                        level = 'Medium' 
                        severity = 'Medium'
                    else:
                        level = 'Low'
                        severity = 'Low'
                    
                    risk_predictions[risk_category] = {
                        'probability': round(probability, 1),
                        'level': level,
                        'severity': severity,
                        'primary_factors': self._identify_risk_factors(risk_category, analysis_result),
                        'mitigation_suggestions': self._get_mitigation_suggestions(risk_category)
                    }
                    
                except Exception as e:
                    logger.warning(f"ML prediction failed for {risk_category}: {e}")
                    risk_predictions[risk_category] = self._rule_based_risk(risk_category, analysis_result)
            else:
                risk_predictions[risk_category] = self._rule_based_risk(risk_category, analysis_result)
        
        return risk_predictions

    def _predict_with_rules(self, analysis_result):
        """Use rule-based approach for risk prediction"""
        risk_predictions = {}
        
        for risk_category in self.risk_categories:
            risk_predictions[risk_category] = self._rule_based_risk(risk_category, analysis_result)
        
        return risk_predictions

    def _rule_based_risk(self, risk_category, analysis_result):
        """Calculate risk using rule-based approach"""
        section_analyses = analysis_result.get('section_analyses', {})
        overall_score = analysis_result.get('overall_score', 75)
        
        # Base probability calculation
        base_probability = max(0, 100 - overall_score)
        
        # Risk-specific adjustments
        if risk_category == 'Budget Overrun Risk':
            finance_score = section_analyses.get('Means of Finance', {}).get('score', 70)
            probability = base_probability + (100 - finance_score) * 0.5
            
        elif risk_category == 'Timeline Delay Risk':
            timeline_score = section_analyses.get('Time Frame', {}).get('score', 70)
            probability = base_probability + (100 - timeline_score) * 0.6
            
        elif risk_category == 'Technical Implementation Risk':
            tech_score = section_analyses.get('Technology Issues', {}).get('score', 70)
            probability = base_probability + (100 - tech_score) * 0.7
            
        elif risk_category == 'Compliance Risk':
            legal_score = section_analyses.get('Legal Framework', {}).get('score', 80)
            probability = base_probability + (100 - legal_score) * 0.4
            
        elif risk_category == 'Resource Availability Risk':
            mgmt_score = section_analyses.get('Management Arrangements', {}).get('score', 75)
            probability = base_probability + (100 - mgmt_score) * 0.5
        
        else:
            probability = base_probability
        
        # Normalize probability
        probability = min(85, max(15, probability))
        
        # Determine risk level
        if probability >= 60:
            level = 'High'
            severity = 'High'
        elif probability >= 40:
            level = 'Medium'
            severity = 'Medium'
        else:
            level = 'Low'
            severity = 'Low'
        
        return {
            'probability': round(probability, 1),
            'level': level,
            'severity': severity,
            'primary_factors': self._identify_risk_factors(risk_category, analysis_result),
            'mitigation_suggestions': self._get_mitigation_suggestions(risk_category)
        }

    def _extract_features(self, analysis_result):
        """Extract features for ML models"""
        section_analyses = analysis_result.get('section_analyses', {})
        quality_scores = analysis_result.get('quality_scores', {})
        
        features = [
            analysis_result.get('overall_score', 75) / 100,
            analysis_result.get('completeness_percentage', 80) / 100,
        ]
        
        # Add section scores as features
        for section_name in ['Context/Background', 'Problems Addressed', 'Project Objectives',
                           'Technology Issues', 'Management Arrangements', 'Means of Finance',
                           'Time Frame', 'Target Beneficiaries', 'Legal Framework', 'Risk Analysis']:
            score = section_analyses.get(section_name, {}).get('score', 70)
            features.append(score / 100)
        
        # Add quality scores
        for quality_name in ['data_accuracy', 'completeness', 'technical_viability', 
                           'compliance', 'budget_realism']:
            score = quality_scores.get(quality_name, 70)
            features.append(score / 100)
        
        return features

    def _identify_risk_factors(self, risk_category, analysis_result):
        """Identify primary risk factors"""
        section_analyses = analysis_result.get('section_analyses', {})
        
        risk_factors = {
            'Budget Overrun Risk': [
                'Inadequate cost estimation methodology',
                'Missing market rate analysis', 
                'No contingency planning',
                'Unrealistic budget assumptions'
            ],
            'Timeline Delay Risk': [
                'Aggressive project timeline',
                'Insufficient buffer time allocation',
                'Complex dependency management',
                'Approval process delays'
            ],
            'Technical Implementation Risk': [
                'Unproven technology selection',
                'High technical complexity',
                'Integration challenges',
                'Skill gap in implementation team'
            ],
            'Compliance Risk': [
                'Missing regulatory approvals',
                'Incomplete compliance framework',
                'Environmental clearance gaps',
                'Legal framework uncertainties'
            ],
            'Resource Availability Risk': [
                'Skilled manpower shortage',
                'Equipment procurement delays',
                'Vendor reliability issues',
                'Resource allocation conflicts'
            ]
        }
        
        # Return 2-3 most relevant factors
        factors = risk_factors.get(risk_category, ['General project risks'])
        return factors[:3]

    def _get_mitigation_suggestions(self, risk_category):
        """Get mitigation suggestions for each risk category"""
        mitigation_strategies = {
            'Budget Overrun Risk': [
                'Conduct detailed market survey for cost estimation',
                'Include 10-15% contingency in budget',
                'Implement regular cost monitoring and control',
                'Establish cost escalation mechanisms'
            ],
            'Timeline Delay Risk': [
                'Develop realistic project schedule with buffers',
                'Implement critical path method (CPM)',
                'Establish fast-track approval processes', 
                'Create parallel execution streams'
            ],
            'Technical Implementation Risk': [
                'Conduct proof of concept studies',
                'Engage technical experts and consultants',
                'Implement phased rollout approach',
                'Establish technical support agreements'
            ],
            'Compliance Risk': [
                'Engage early with regulatory authorities',
                'Conduct comprehensive legal review',
                'Establish compliance monitoring framework',
                'Maintain regulatory relationship management'
            ],
            'Resource Availability Risk': [
                'Develop comprehensive resource plan',
                'Establish vendor partnerships and agreements',
                'Implement skill development programs',
                'Create resource backup strategies'
            ]
        }
        
        suggestions = mitigation_strategies.get(risk_category, ['Develop risk-specific mitigation plan'])
        return suggestions[:3]

    def _calculate_overall_risk(self, risk_predictions):
        """Calculate overall project risk"""
        risk_levels = {'Low': 1, 'Medium': 2, 'High': 3}
        
        # Count risks by level
        high_risk_count = sum(1 for risk in risk_predictions.values() if risk['level'] == 'High')
        medium_risk_count = sum(1 for risk in risk_predictions.values() if risk['level'] == 'Medium')
        low_risk_count = sum(1 for risk in risk_predictions.values() if risk['level'] == 'Low')
        
        # Calculate weighted average
        total_risks = len(risk_predictions)
        if total_risks == 0:
            return {'level': 'Medium', 'score': 50.0}
        
        weighted_score = (high_risk_count * 3 + medium_risk_count * 2 + low_risk_count * 1) / total_risks
        
        # Determine overall level
        if weighted_score >= 2.5:
            overall_level = 'High'
        elif weighted_score >= 1.5:
            overall_level = 'Medium'
        else:
            overall_level = 'Low'
        
        # Convert to percentage score
        overall_score = round((weighted_score / 3) * 100, 1)
        
        return {
            'level': overall_level,
            'score': overall_score,
            'high_risk_count': high_risk_count,
            'medium_risk_count': medium_risk_count,
            'low_risk_count': low_risk_count
        }

    def _generate_risk_summary(self, risk_predictions, overall_risk):
        """Generate risk summary text"""
        high_risks = [name for name, data in risk_predictions.items() if data['level'] == 'High']
        
        if high_risks:
            summary = f"High priority risks identified in {', '.join(high_risks)}. "
            summary += "Immediate attention and mitigation planning required."
        elif overall_risk['level'] == 'Medium':
            summary = "Medium priority risks identified. Enhanced monitoring and mitigation planning recommended."
        else:
            summary = "Low risk project profile. Standard risk management practices sufficient."
        
        return summary

    def _train_risk_models(self):
        """Train ML models for risk prediction"""
        if not ML_AVAILABLE:
            return None
        
        try:
            # Generate synthetic training data
            training_data = self._generate_training_data()
            
            models = {}
            for risk_category in self.risk_categories:
                # Prepare data for this risk category
                X = training_data['features']
                y = training_data[f'{risk_category}_target']
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                # Scale features
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                
                # Train model
                model = GradientBoostingClassifier(
                    n_estimators=100,
                    learning_rate=0.1,
                    max_depth=3,
                    random_state=42
                )
                model.fit(X_train_scaled, y_train)
                
                # Store model with scaler
                models[risk_category] = {
                    'model': model,
                    'scaler': scaler
                }
            
            logger.info("ML models trained successfully")
            return models
            
        except Exception as e:
            logger.error(f"Error training ML models: {str(e)}")
            return None

    def _generate_training_data(self):
        """Generate synthetic training data for ML models"""
        np.random.seed(42)
        n_samples = 1000
        
        # Generate features (similar to _extract_features)
        features = []
        for _ in range(n_samples):
            sample = [
                np.random.normal(0.75, 0.15),  # overall_score
                np.random.normal(0.8, 0.1),   # completeness_percentage
            ]
            
            # Section scores
            for _ in range(10):
                sample.append(np.random.normal(0.75, 0.12))
            
            # Quality scores  
            for _ in range(5):
                sample.append(np.random.normal(0.75, 0.1))
            
            # Clip to valid range
            sample = [max(0, min(1, x)) for x in sample]
            features.append(sample)
        
        training_data = {'features': np.array(features)}
        
        # Generate targets for each risk category
        for risk_category in self.risk_categories:
            targets = []
            for feature_row in features:
                # Simple logic to generate targets based on features
                overall_score = feature_row[0]
                relevant_score = feature_row[2 + hash(risk_category) % 10]  # Use hash for consistency
                
                risk_prob = 1 - (overall_score * 0.7 + relevant_score * 0.3)
                target = 1 if risk_prob > 0.4 else 0
                targets.append(target)
            
            training_data[f'{risk_category}_target'] = np.array(targets)
        
        return training_data

    def _generate_fallback_risks(self):
        """Generate fallback risk assessment"""
        risk_predictions = {}
        
        for risk_category in self.risk_categories:
            probability = random.uniform(25, 75)
            
            if probability >= 60:
                level = 'High'
            elif probability >= 40:
                level = 'Medium'
            else:
                level = 'Low'
            
            risk_predictions[risk_category] = {
                'probability': round(probability, 1),
                'level': level,
                'severity': level,
                'primary_factors': ['Analysis module error - using fallback assessment'],
                'mitigation_suggestions': ['Conduct detailed risk assessment manually']
            }
        
        overall_risk = {
            'level': 'Medium',
            'score': 50.0,
            'high_risk_count': 1,
            'medium_risk_count': 3,
            'low_risk_count': 1
        }
        
        return {
            'overall_risk': overall_risk,
            'risk_predictions': risk_predictions,
            'risk_summary': 'Fallback risk assessment - manual review recommended',
            'generated_at': datetime.now().isoformat()
        }
