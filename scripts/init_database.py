"""
Database initialization and migration script.
Run this to set up the database schema.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_db
from database.services import ProjectService
from database.models import ModelType
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_database():
    """Initialize database with schema"""
    try:
        logger.info("Creating database tables...")
        init_db()
        logger.info("✅ Database initialized successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        return False


def seed_sample_data():
    """Add sample projects for testing (optional)"""
    try:
        logger.info("Adding sample projects...")
        
        # Sample Decision Tree Project
        ProjectService.create_project(
            name="COVID-19 Treatment Comparison",
            model_type="decision_tree",
            description="Comparing standard care vs. antiviral treatment for COVID-19 patients",
            tags=["infectious-disease", "decision-tree", "covid-19"]
        )
        
        # Sample Markov Model Project
        ProjectService.create_project(
            name="Diabetes Progression Model",
            model_type="markov",
            description="Markov model tracking diabetes progression over 20 years",
            tags=["chronic-disease", "markov", "diabetes"]
        )
        
        # Sample PSM Project
        ProjectService.create_project(
            name="Cancer Immunotherapy PSM",
            model_type="psm",
            description="Partitioned survival model for novel immunotherapy vs. chemotherapy",
            tags=["oncology", "psm", "immunotherapy"]
        )
        
        logger.info("✅ Sample projects added!")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to seed data: {e}")
        return False


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Health Economic Modeling Hub - Database Setup")
    logger.info("=" * 60)
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    # Ask if user wants sample data
    response = input("\n📊 Add sample projects for testing? (y/n): ").strip().lower()
    if response == 'y':
        seed_sample_data()
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ Database setup complete!")
    logger.info("=" * 60)
    logger.info("\nYou can now run the application with: python app.py")
