"""
Database Manager Module
SQLite database operations for storing analysis results
"""

import sqlite3
import json
import logging
import os
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path='dpr_analysis.db'):
        self.db_path = db_path
        self.init_database()
        logger.info(f"Database Manager initialized with database: {db_path}")

    def init_database(self):
        """Initialize database with required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create analyses table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS analyses (
                        id TEXT PRIMARY KEY,
                        filename TEXT NOT NULL,
                        analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        overall_score REAL,
                        risk_level TEXT,
                        completeness_percentage REAL,
                        analysis_data TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create sections table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS analysis_sections (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        analysis_id TEXT,
                        section_name TEXT,
                        score INTEGER,
                        completeness INTEGER,
                        quality INTEGER,
                        issues TEXT,
                        recommendations TEXT,
                        FOREIGN KEY (analysis_id) REFERENCES analyses (id)
                    )
                ''')
                
                # Create risks table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS analysis_risks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        analysis_id TEXT,
                        risk_category TEXT,
                        probability REAL,
                        risk_level TEXT,
                        severity TEXT,
                        primary_factors TEXT,
                        mitigation_suggestions TEXT,
                        FOREIGN KEY (analysis_id) REFERENCES analyses (id)
                    )
                ''')
                
                # Create recommendations table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS analysis_recommendations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        analysis_id TEXT,
                        priority TEXT,
                        category TEXT,
                        recommendation TEXT,
                        FOREIGN KEY (analysis_id) REFERENCES analyses (id)
                    )
                ''')
                
                # Create indexes for better performance
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_analyses_date ON analyses (analyzed_at)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_analyses_score ON analyses (overall_score)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_sections_analysis ON analysis_sections (analysis_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_risks_analysis ON analysis_risks (analysis_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_recommendations_analysis ON analysis_recommendations (analysis_id)')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise

    def store_analysis(self, analysis_data):
        """Store complete analysis result in database"""
        try:
            analysis_id = str(uuid.uuid4())
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Store main analysis record
                file_info = analysis_data.get('file_info', {})
                analysis = analysis_data.get('analysis', {})
                risks = analysis_data.get('risks', {})
                
                cursor.execute('''
                    INSERT INTO analyses 
                    (id, filename, overall_score, risk_level, completeness_percentage, analysis_data)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    analysis_id,
                    file_info.get('filename', 'Unknown'),
                    analysis.get('overall_score', 0),
                    risks.get('overall_risk', {}).get('level', 'Unknown'),
                    analysis.get('completeness_percentage', 0),
                    json.dumps(analysis_data)
                ))
                
                # Store section analyses
                section_analyses = analysis.get('section_analyses', {})
                for section_name, section_data in section_analyses.items():
                    cursor.execute('''
                        INSERT INTO analysis_sections 
                        (analysis_id, section_name, score, completeness, quality, issues, recommendations)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        analysis_id,
                        section_name,
                        section_data.get('score', 0),
                        section_data.get('completeness', 0),
                        section_data.get('quality', 0),
                        json.dumps(section_data.get('issues', [])),
                        json.dumps(section_data.get('recommendations', []))
                    ))
                
                # Store risk predictions
                risk_predictions = risks.get('risk_predictions', {})
                for risk_category, risk_data in risk_predictions.items():
                    cursor.execute('''
                        INSERT INTO analysis_risks 
                        (analysis_id, risk_category, probability, risk_level, severity, 
                         primary_factors, mitigation_suggestions)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        analysis_id,
                        risk_category,
                        risk_data.get('probability', 0),
                        risk_data.get('level', 'Unknown'),
                        risk_data.get('severity', 'Unknown'),
                        json.dumps(risk_data.get('primary_factors', [])),
                        json.dumps(risk_data.get('mitigation_suggestions', []))
                    ))
                
                # Store recommendations
                recommendations = analysis_data.get('recommendations', [])
                for rec in recommendations:
                    cursor.execute('''
                        INSERT INTO analysis_recommendations 
                        (analysis_id, priority, category, recommendation)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        analysis_id,
                        rec.get('priority', 'Medium'),
                        rec.get('category', 'General'),
                        rec.get('recommendation', '')
                    ))
                
                conn.commit()
                logger.info(f"Analysis stored successfully with ID: {analysis_id}")
                return analysis_id
                
        except Exception as e:
            logger.error(f"Error storing analysis: {str(e)}")
            return None

    def get_analysis(self, analysis_id):
        """Retrieve analysis by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT analysis_data FROM analyses WHERE id = ?
                ''', (analysis_id,))
                
                result = cursor.fetchone()
                if result:
                    return json.loads(result[0])
                else:
                    return None
                    
        except Exception as e:
            logger.error(f"Error retrieving analysis {analysis_id}: {str(e)}")
            return None

    def get_analysis_history(self, limit=10, offset=0):
        """Get analysis history with pagination"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, filename, analyzed_at, overall_score, risk_level, completeness_percentage
                    FROM analyses 
                    ORDER BY analyzed_at DESC 
                    LIMIT ? OFFSET ?
                ''', (limit, offset))
                
                results = cursor.fetchall()
                
                history = []
                for row in results:
                    history.append({
                        'id': row[0],
                        'filename': row[1],
                        'analyzed_at': row[2],
                        'overall_score': row[3],
                        'risk_level': row[4],
                        'completeness_percentage': row[5]
                    })
                
                return history
                
        except Exception as e:
            logger.error(f"Error retrieving analysis history: {str(e)}")
            return []

    def get_analysis_statistics(self):
        """Get database statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total analyses count
                cursor.execute('SELECT COUNT(*) FROM analyses')
                total_analyses = cursor.fetchone()[0]
                
                # Average overall score
                cursor.execute('SELECT AVG(overall_score) FROM analyses WHERE overall_score IS NOT NULL')
                avg_score = cursor.fetchone()[0] or 0
                
                # Risk level distribution
                cursor.execute('''
                    SELECT risk_level, COUNT(*) 
                    FROM analyses 
                    WHERE risk_level IS NOT NULL 
                    GROUP BY risk_level
                ''')
                risk_distribution = dict(cursor.fetchall())
                
                # Recent analyses (last 30 days)
                cursor.execute('''
                    SELECT COUNT(*) FROM analyses 
                    WHERE analyzed_at >= datetime('now', '-30 days')
                ''')
                recent_analyses = cursor.fetchone()[0]
                
                return {
                    'total_analyses': total_analyses,
                    'average_score': round(avg_score, 2),
                    'risk_distribution': risk_distribution,
                    'recent_analyses': recent_analyses,
                    'database_size': os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
                }
                
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            return {}

    def search_analyses(self, search_term, limit=20):
        """Search analyses by filename or content"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, filename, analyzed_at, overall_score, risk_level
                    FROM analyses 
                    WHERE filename LIKE ? OR analysis_data LIKE ?
                    ORDER BY analyzed_at DESC 
                    LIMIT ?
                ''', (f'%{search_term}%', f'%{search_term}%', limit))
                
                results = cursor.fetchall()
                
                search_results = []
                for row in results:
                    search_results.append({
                        'id': row[0],
                        'filename': row[1],
                        'analyzed_at': row[2],
                        'overall_score': row[3],
                        'risk_level': row[4]
                    })
                
                return search_results
                
        except Exception as e:
            logger.error(f"Error searching analyses: {str(e)}")
            return []

    def delete_analysis(self, analysis_id):
        """Delete analysis and all related data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Delete from all related tables
                cursor.execute('DELETE FROM analysis_recommendations WHERE analysis_id = ?', (analysis_id,))
                cursor.execute('DELETE FROM analysis_risks WHERE analysis_id = ?', (analysis_id,))
                cursor.execute('DELETE FROM analysis_sections WHERE analysis_id = ?', (analysis_id,))
                cursor.execute('DELETE FROM analyses WHERE id = ?', (analysis_id,))
                
                conn.commit()
                
                deleted_count = cursor.rowcount
                logger.info(f"Deleted analysis {analysis_id} (affected rows: {deleted_count})")
                return deleted_count > 0
                
        except Exception as e:
            logger.error(f"Error deleting analysis {analysis_id}: {str(e)}")
            return False

    def cleanup_old_analyses(self, days=90):
        """Clean up analyses older than specified days"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get IDs of old analyses
                cursor.execute('''
                    SELECT id FROM analyses 
                    WHERE analyzed_at < datetime('now', '-' || ? || ' days')
                ''', (days,))
                
                old_ids = [row[0] for row in cursor.fetchall()]
                
                # Delete old analyses
                for analysis_id in old_ids:
                    self.delete_analysis(analysis_id)
                
                logger.info(f"Cleaned up {len(old_ids)} old analyses")
                return len(old_ids)
                
        except Exception as e:
            logger.error(f"Error cleaning up old analyses: {str(e)}")
            return 0

    def export_data(self, format='json'):
        """Export all data in specified format"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, filename, analyzed_at, overall_score, risk_level, 
                           completeness_percentage, analysis_data
                    FROM analyses 
                    ORDER BY analyzed_at DESC
                ''')
                
                results = cursor.fetchall()
                
                exported_data = []
                for row in results:
                    try:
                        analysis_data = json.loads(row[6]) if row[6] else {}
                    except:
                        analysis_data = {}
                    
                    exported_data.append({
                        'id': row[0],
                        'filename': row[1],
                        'analyzed_at': row[2],
                        'overall_score': row[3],
                        'risk_level': row[4],
                        'completeness_percentage': row[5],
                        'analysis_data': analysis_data
                    })
                
                if format == 'json':
                    return json.dumps(exported_data, indent=2, default=str)
                else:
                    return exported_data
                    
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            return None

    def close(self):
        """Close database connections"""
        # SQLite connections are automatically closed with context managers
        logger.info("Database manager closed")
