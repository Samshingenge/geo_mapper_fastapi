from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping

from app import models, schemas
from app.db.base import get_db

router = APIRouter()

def to_geojson(region):
    """Convert a region to GeoJSON format."""
    geometry = to_shape(region.geometry)
    
    return {
        "type": "Feature",
        "geometry": mapping(geometry) if geometry else None,
        "properties": {
            "id": region.id,
            "name": region.name,
            "fiber_status": region.fiber_status.value,
            **region.properties
        }
    }

@router.get("/", response_model=schemas.GeoJSONFeatureCollection)
def read_regions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
):
    """
    Retrieve regions with optional filtering by status.
    Returns a GeoJSON FeatureCollection.
    """
    query = db.query(models.Region)
    
    if status:
        query = query.filter(models.Region.fiber_status == status)
    
    regions = query.offset(skip).limit(limit).all()
    
    return {
        "type": "FeatureCollection",
        "features": [to_geojson(region) for region in regions]
    }

@router.get("/geojson", response_model=dict)
def read_regions_geojson(
    db: Session = Depends(get_db),
    status: Optional[str] = None
):
    """
    Retrieve regions in GeoJSON format.
    """
    query = db.query(models.Region)
    
    if status:
        query = query.filter(models.Region.fiber_status == status)
    
    regions = query.all()
    
    features = [to_geojson(region) for region in regions]
    
    return {
        "type": "FeatureCollection",
        "features": features
    }

@router.get("/{region_id}", response_model=schemas.RegionOut)
def read_region(region_id: int, db: Session = Depends(get_db)):
    """
    Get a specific region by ID.
    """
    region = db.query(models.Region).filter(models.Region.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    return to_geojson(region)

@router.get("/name/{region_name}", response_model=schemas.RegionOut)
def read_region_by_name(region_name: str, db: Session = Depends(get_db)):
    """
    Get a specific region by name.
    """
    region = db.query(models.Region).filter(models.Region.name.ilike(f"%{region_name}%")).first()
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    return to_geojson(region)

@router.get("/{region_id}/geojson", response_model=dict)
def read_region_geojson(region_id: int, db: Session = Depends(get_db)):
    """
    Get a specific region by ID in GeoJSON format.
    """
    region = db.query(models.Region).filter(models.Region.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    
    return to_geojson(region)

@router.get("/coverage/{region_name}")
def get_coverage(region_name: str, db: Session = Depends(get_db)):
    """
    Get the fiber coverage status for a specific region by name.
    """
    region = db.query(models.Region).filter(models.Region.name.ilike(f"%{region_name}%")).first()
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    
    return {
        "region": region.name,
        "status": region.fiber_status.value,
        "details": region.properties
    }
