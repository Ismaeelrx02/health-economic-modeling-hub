"""
Database Module - SQLite database for storing projects and models
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

DATABASE_PATH = "health_econ_hub.db"

def init_database():
    """Initialize database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            model_type TEXT NOT NULL,
            status TEXT DEFAULT 'draft',
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Decision Trees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS decision_trees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            tree_structure TEXT,
            parameters TEXT,
            results TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
        )
    ''')
    
    # Markov Models table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS markov_models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            states TEXT,
            transition_matrix TEXT,
            state_costs TEXT,
            state_utilities TEXT,
            time_horizon INTEGER DEFAULT 10,
            cycle_length REAL DEFAULT 1.0,
            discount_rate_cost REAL DEFAULT 0.03,
            discount_rate_outcome REAL DEFAULT 0.03,
            results TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
        )
    ''')
    
    # PSM Models table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS psm_models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            survival_curves TEXT,
            treatment_costs TEXT,
            utilities TEXT,
            time_horizon INTEGER DEFAULT 20,
            discount_rate_cost REAL DEFAULT 0.03,
            discount_rate_outcome REAL DEFAULT 0.03,
            results TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on import
init_database()

# Project Functions
def get_all_projects() -> List[Dict[str, Any]]:
    """Get all projects from database"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM projects ORDER BY updated_date DESC')
    rows = cursor.fetchall()
    
    projects = [dict(row) for row in rows]
    conn.close()
    
    return projects

def create_project(name: str, description: str, model_type: str) -> int:
    """Create a new project"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO projects (name, description, model_type, status, created_date, updated_date)
        VALUES (?, ?, ?, 'draft', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    ''', (name, description, model_type))
    
    project_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return project_id

def get_project(project_id: int) -> Optional[Dict[str, Any]]:
    """Get a single project by ID"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    row = cursor.fetchone()
    
    project = dict(row) if row else None
    conn.close()
    
    return project

def update_project(project_id: int, **kwargs) -> bool:
    """Update a project"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Build update query dynamically
    fields = []
    values = []
    for key, value in kwargs.items():
        fields.append(f"{key} = ?")
        values.append(value)
    
    fields.append("updated_date = CURRENT_TIMESTAMP")
    values.append(project_id)
    
    query = f"UPDATE projects SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, values)
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return success

def delete_project(project_id: int) -> bool:
    """Delete a project"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return success

def get_project_count() -> Dict[str, int]:
    """Get counts of projects by type"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM projects')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM decision_trees')
    decision_trees = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM markov_models')
    markov_models = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM psm_models')
    psm_models = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total': total,
        'decision_trees': decision_trees,
        'markov_models': markov_models,
        'psm_models': psm_models
    }
