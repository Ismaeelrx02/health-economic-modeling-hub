"""SQLAlchemy database models for Health Economic Modeling Hub"""
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Text, 
    ForeignKey, JSON, Enum as SQLEnum, Boolean
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class ModelType(str, enum.Enum):
    """Types of health economic models"""
    DECISION_TREE = "decision_tree"
    MARKOV = "markov"
    PSM = "psm"


class Project(Base):
    """Main project container"""
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    model_type = Column(SQLEnum(ModelType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    owner = Column(String(100))  # User identifier
    tags = Column(JSON)  # List of tags
    is_archived = Column(Boolean, default=False)
    
    # Relationships
    scenarios = relationship("Scenario", back_populates="project", cascade="all, delete-orphan")
    parameters = relationship("Parameter", back_populates="project", cascade="all, delete-orphan")
    results = relationship("Result", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', type='{self.model_type}')>"


class Scenario(Base):
    """Scenarios/strategies within a project"""
    __tablename__ = 'scenarios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    is_baseline = Column(Boolean, default=False)
    
    # Model structure stored as JSON
    model_structure = Column(JSON)  # Tree nodes, states, survival curves
    
    # Cost and effectiveness data
    costs = Column(JSON)  # Annual costs, one-time costs
    effectiveness = Column(JSON)  # QALYs, LYs, outcomes
    
    # Probabilities and transitions
    probabilities = Column(JSON)  # Transition probabilities, event rates
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="scenarios")
    
    def __repr__(self):
        return f"<Scenario(id={self.id}, name='{self.name}', project_id={self.project_id})>"


class Parameter(Base):
    """Parameters for sensitivity analysis"""
    __tablename__ = 'parameters'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(100))  # 'cost', 'effectiveness', 'probability', 'utility'
    base_value = Column(Float, nullable=False)
    min_value = Column(Float)
    max_value = Column(Float)
    distribution = Column(String(50))  # 'uniform', 'normal', 'beta', 'gamma'
    distribution_params = Column(JSON)  # Parameters for the distribution
    unit = Column(String(50))  # '$', '%', 'years', etc.
    description = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="parameters")
    
    def __repr__(self):
        return f"<Parameter(id={self.id}, name='{self.name}', value={self.base_value})>"


class Result(Base):
    """Stored analysis results"""
    __tablename__ = 'results'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    analysis_type = Column(String(50), nullable=False)  # 'base_case', 'dsa', 'psa', 'comparison'
    
    # Results data stored as JSON
    results_data = Column(JSON, nullable=False)  # ICERs, NMB, costs, QALYs
    charts_data = Column(JSON)  # Pre-computed chart data
    
    # Analysis metadata
    discount_rate = Column(Float)
    time_horizon = Column(Integer)
    wtp_threshold = Column(Float)
    psa_iterations = Column(Integer)  # For PSA results
    
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="results")
    
    def __repr__(self):
        return f"<Result(id={self.id}, type='{self.analysis_type}', project_id={self.project_id})>"
