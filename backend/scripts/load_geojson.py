import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any

# Add the backend directory to the Python path to resolve module imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session

from app.db.base import SessionLocal
from app.models.region import Region

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_geojson(file_path: str) -> Dict[str, Any]:
    """Load GeoJSON data from a file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading GeoJSON file: {e}")
        raise

def import_regions(db: Session, geojson_data: Dict[str, Any]) -> None:
    """Import regions from GeoJSON data into the database."""
    try:
        for feature in geojson_data['features']:
            # Ensure required fields exist
            if 'name' not in feature['properties']:
                logger.warning(f"Skipping feature without 'name' property: {feature}")
                continue
                
            # Check if region already exists
            existing_region = db.query(Region).filter(
                Region.name == feature['properties']['name']
            ).first()
            
            if existing_region:
                logger.info(f"Region {feature['properties']['name']} already exists, skipping...")
                continue
                
            # Create new region from GeoJSON feature
            region = Region.from_geojson_feature(feature)
            db.add(region)
            logger.info(f"Added region: {region.name} with status: {region.fiber_status}")
        
        db.commit()
        logger.info("Successfully imported all regions.")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error importing regions: {e}")
        raise

def main():
    # Path to the GeoJSON file
    current_dir = Path(__file__).parent.parent
    geojson_path = current_dir / "data" / "namibia_regions.geojson"
    
    if not geojson_path.exists():
        logger.error(f"GeoJSON file not found at {geojson_path}")
        return
    
    # Load GeoJSON data
    logger.info(f"Loading GeoJSON data from {geojson_path}")
    geojson_data = load_geojson(str(geojson_path))
    
    # Import regions into database
    db = SessionLocal()
    try:
        import_regions(db, geojson_data)
    finally:
        db.close()

if __name__ == "__main__":
    main()
