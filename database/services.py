"""Database service layer - CRUD operations for all entities"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import desc, func
from database.connection import get_db_session
from database.models import Project, Scenario, Parameter, Result, ModelType
import logging

logger = logging.getLogger(__name__)


class ProjectService:
    """Service for managing projects"""
    
    @staticmethod
    def create_project(name: str, model_type: str, description: str = "", 
                      owner: str = None, tags: List[str] = None) -> Dict[str, Any]:
        """Create a new project"""
        with get_db_session() as session:
            project = Project(
                name=name,
                description=description,
                model_type=ModelType(model_type),
                owner=owner,
                tags=tags or [],
                is_archived=False
            )
            session.add(project)
            session.flush()
            
            return {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'model_type': project.model_type.value,
                'created_at': project.created_at.isoformat(),
                'updated_at': project.updated_at.isoformat(),
                'owner': project.owner,
                'tags': project.tags,
                'is_archived': project.is_archived
            }
    
    @staticmethod
    def get_project(project_id: int) -> Optional[Dict[str, Any]]:
        """Get a project by ID"""
        with get_db_session() as session:
            project = session.query(Project).filter(Project.id == project_id).first()
            if not project:
                return None
            
            return {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'model_type': project.model_type.value,
                'created_at': project.created_at.isoformat(),
                'updated_at': project.updated_at.isoformat(),
                'owner': project.owner,
                'tags': project.tags,
                'is_archived': project.is_archived,
                'scenarios_count': len(project.scenarios),
                'parameters_count': len(project.parameters)
            }
    
    @staticmethod
    def list_projects(include_archived: bool = False, model_type: str = None) -> List[Dict[str, Any]]:
        """List all projects"""
        with get_db_session() as session:
            query = session.query(Project)
            
            if not include_archived:
                query = query.filter(Project.is_archived == False)
            
            if model_type:
                query = query.filter(Project.model_type == ModelType(model_type))
            
            projects = query.order_by(desc(Project.updated_at)).all()
            
            return [{
                'id': p.id,
                'name': p.name,
                'description': p.description,
                'model_type': p.model_type.value,
                'created_at': p.created_at.isoformat(),
                'updated_at': p.updated_at.isoformat(),
                'owner': p.owner,
                'tags': p.tags,
                'is_archived': p.is_archived,
                'scenarios_count': len(p.scenarios)
            } for p in projects]
    
    @staticmethod
    def update_project(project_id: int, **kwargs) -> bool:
        """Update a project"""
        with get_db_session() as session:
            project = session.query(Project).filter(Project.id == project_id).first()
            if not project:
                return False
            
            for key, value in kwargs.items():
                if hasattr(project, key):
                    setattr(project, key, value)
            
            project.updated_at = datetime.utcnow()
            return True
    
    @staticmethod
    def delete_project(project_id: int) -> bool:
        """Delete a project"""
        with get_db_session() as session:
            project = session.query(Project).filter(Project.id == project_id).first()
            if not project:
                return False
            
            session.delete(project)
            return True


class ScenarioService:
    """Service for managing scenarios"""
    
    @staticmethod
    def create_scenario(project_id: int, name: str, description: str = "",
                       is_baseline: bool = False, model_structure: Dict = None,
                       costs: Dict = None, effectiveness: Dict = None,
                       probabilities: Dict = None) -> Dict[str, Any]:
        """Create a new scenario"""
        with get_db_session() as session:
            scenario = Scenario(
                project_id=project_id,
                name=name,
                description=description,
                is_baseline=is_baseline,
                model_structure=model_structure or {},
                costs=costs or {},
                effectiveness=effectiveness or {},
                probabilities=probabilities or {}
            )
            session.add(scenario)
            session.flush()
            
            return {
                'id': scenario.id,
                'project_id': scenario.project_id,
                'name': scenario.name,
                'description': scenario.description,
                'is_baseline': scenario.is_baseline,
                'model_structure': scenario.model_structure,
                'costs': scenario.costs,
                'effectiveness': scenario.effectiveness,
                'probabilities': scenario.probabilities,
                'created_at': scenario.created_at.isoformat()
            }
    
    @staticmethod
    def get_scenario(scenario_id: int) -> Optional[Dict[str, Any]]:
        """Get a scenario by ID"""
        with get_db_session() as session:
            scenario = session.query(Scenario).filter(Scenario.id == scenario_id).first()
            if not scenario:
                return None
            
            return {
                'id': scenario.id,
                'project_id': scenario.project_id,
                'name': scenario.name,
                'description': scenario.description,
                'is_baseline': scenario.is_baseline,
                'model_structure': scenario.model_structure,
                'costs': scenario.costs,
                'effectiveness': scenario.effectiveness,
                'probabilities': scenario.probabilities,
                'created_at': scenario.created_at.isoformat(),
                'updated_at': scenario.updated_at.isoformat()
            }
    
    @staticmethod
    def list_scenarios(project_id: int) -> List[Dict[str, Any]]:
        """List all scenarios for a project"""
        with get_db_session() as session:
            scenarios = session.query(Scenario).filter(
                Scenario.project_id == project_id
            ).order_by(desc(Scenario.is_baseline), Scenario.name).all()
            
            return [{
                'id': s.id,
                'project_id': s.project_id,
                'name': s.name,
                'description': s.description,
                'is_baseline': s.is_baseline,
                'model_structure': s.model_structure,
                'costs': s.costs,
                'effectiveness': s.effectiveness,
                'probabilities': s.probabilities
            } for s in scenarios]
    
    @staticmethod
    def update_scenario(scenario_id: int, **kwargs) -> bool:
        """Update a scenario"""
        with get_db_session() as session:
            scenario = session.query(Scenario).filter(Scenario.id == scenario_id).first()
            if not scenario:
                return False
            
            for key, value in kwargs.items():
                if hasattr(scenario, key):
                    setattr(scenario, key, value)
            
            scenario.updated_at = datetime.utcnow()
            return True
    
    @staticmethod
    def delete_scenario(scenario_id: int) -> bool:
        """Delete a scenario"""
        with get_db_session() as session:
            scenario = session.query(Scenario).filter(Scenario.id == scenario_id).first()
            if not scenario:
                return False
            
            session.delete(scenario)
            return True


class ParameterService:
    """Service for managing parameters"""
    
    @staticmethod
    def create_parameter(project_id: int, name: str, base_value: float,
                        category: str = None, min_value: float = None,
                        max_value: float = None, distribution: str = None,
                        distribution_params: Dict = None, unit: str = None,
                        description: str = "") -> Dict[str, Any]:
        """Create a new parameter"""
        with get_db_session() as session:
            parameter = Parameter(
                project_id=project_id,
                name=name,
                category=category,
                base_value=base_value,
                min_value=min_value,
                max_value=max_value,
                distribution=distribution,
                distribution_params=distribution_params or {},
                unit=unit,
                description=description
            )
            session.add(parameter)
            session.flush()
            
            return {
                'id': parameter.id,
                'project_id': parameter.project_id,
                'name': parameter.name,
                'category': parameter.category,
                'base_value': parameter.base_value,
                'min_value': parameter.min_value,
                'max_value': parameter.max_value,
                'distribution': parameter.distribution,
                'distribution_params': parameter.distribution_params,
                'unit': parameter.unit,
                'description': parameter.description
            }
    
    @staticmethod
    def list_parameters(project_id: int, category: str = None) -> List[Dict[str, Any]]:
        """List all parameters for a project"""
        with get_db_session() as session:
            query = session.query(Parameter).filter(Parameter.project_id == project_id)
            
            if category:
                query = query.filter(Parameter.category == category)
            
            parameters = query.order_by(Parameter.category, Parameter.name).all()
            
            return [{
                'id': p.id,
                'project_id': p.project_id,
                'name': p.name,
                'category': p.category,
                'base_value': p.base_value,
                'min_value': p.min_value,
                'max_value': p.max_value,
                'distribution': p.distribution,
                'distribution_params': p.distribution_params,
                'unit': p.unit,
                'description': p.description
            } for p in parameters]
    
    @staticmethod
    def update_parameter(parameter_id: int, **kwargs) -> bool:
        """Update a parameter"""
        with get_db_session() as session:
            parameter = session.query(Parameter).filter(Parameter.id == parameter_id).first()
            if not parameter:
                return False
            
            for key, value in kwargs.items():
                if hasattr(parameter, key):
                    setattr(parameter, key, value)
            
            return True
    
    @staticmethod
    def delete_parameter(parameter_id: int) -> bool:
        """Delete a parameter"""
        with get_db_session() as session:
            parameter = session.query(Parameter).filter(Parameter.id == parameter_id).first()
            if not parameter:
                return False
            
            session.delete(parameter)
            return True


class ResultService:
    """Service for managing analysis results"""
    
    @staticmethod
    def save_result(project_id: int, analysis_type: str, results_data: Dict,
                   charts_data: Dict = None, discount_rate: float = None,
                   time_horizon: int = None, wtp_threshold: float = None,
                   psa_iterations: int = None, notes: str = "") -> Dict[str, Any]:
        """Save analysis results"""
        with get_db_session() as session:
            result = Result(
                project_id=project_id,
                analysis_type=analysis_type,
                results_data=results_data,
                charts_data=charts_data or {},
                discount_rate=discount_rate,
                time_horizon=time_horizon,
                wtp_threshold=wtp_threshold,
                psa_iterations=psa_iterations,
                notes=notes
            )
            session.add(result)
            session.flush()
            
            return {
                'id': result.id,
                'project_id': result.project_id,
                'analysis_type': result.analysis_type,
                'results_data': result.results_data,
                'charts_data': result.charts_data,
                'created_at': result.created_at.isoformat()
            }
    
    @staticmethod
    def get_latest_result(project_id: int, analysis_type: str = None) -> Optional[Dict[str, Any]]:
        """Get the latest result for a project"""
        with get_db_session() as session:
            query = session.query(Result).filter(Result.project_id == project_id)
            
            if analysis_type:
                query = query.filter(Result.analysis_type == analysis_type)
            
            result = query.order_by(desc(Result.created_at)).first()
            
            if not result:
                return None
            
            return {
                'id': result.id,
                'project_id': result.project_id,
                'analysis_type': result.analysis_type,
                'results_data': result.results_data,
                'charts_data': result.charts_data,
                'discount_rate': result.discount_rate,
                'time_horizon': result.time_horizon,
                'wtp_threshold': result.wtp_threshold,
                'psa_iterations': result.psa_iterations,
                'notes': result.notes,
                'created_at': result.created_at.isoformat()
            }
    
    @staticmethod
    def list_results(project_id: int) -> List[Dict[str, Any]]:
        """List all results for a project"""
        with get_db_session() as session:
            results = session.query(Result).filter(
                Result.project_id == project_id
            ).order_by(desc(Result.created_at)).all()
            
            return [{
                'id': r.id,
                'project_id': r.project_id,
                'analysis_type': r.analysis_type,
                'created_at': r.created_at.isoformat(),
                'discount_rate': r.discount_rate,
                'time_horizon': r.time_horizon,
                'notes': r.notes
            } for r in results]
    
    @staticmethod
    def delete_result(result_id: int) -> bool:
        """Delete a result"""
        with get_db_session() as session:
            result = session.query(Result).filter(Result.id == result_id).first()
            if not result:
                return False
            
            session.delete(result)
            return True
