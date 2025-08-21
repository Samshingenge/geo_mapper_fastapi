from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship
from typing import Optional
import enum
from shapely.geometry import shape

from app.db.base import Base

class FiberStatus(str, enum.Enum):
    ACTIVE = "Active"
    PLANNED = "Planned"
    UNAVAILABLE = "Unavailable"

class Region(Base):
    """
    Model representing a region in Namibia with its fiber coverage status.
    """
    __tablename__ = "regions"
    # __table_args__ = {"extend_existing": True}  # Add this to allow table redefinition
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    geometry = Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=False)
    fiber_status = Column(Enum(FiberStatus), nullable=False, default=FiberStatus.UNAVAILABLE)
    properties = Column(JSONB, default={})
    
    def __repr__(self):
        return f"<Region(name='{self.name}', fiber_status='{self.fiber_status}')>"
    
    def to_dict(self):
        """Convert the region to a dictionary with proper geometry serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "fiber_status": self.fiber_status,
            "geometry": self.geometry,
            "properties": self.properties
        }
    
    def to_geojson(self):
        """Convert the region to a GeoJSON feature."""
        from geoalchemy2.shape import to_shape
        from shapely.geometry import mapping
        
        geometry = to_shape(self.geometry)
        return {
            "type": "Feature",
            "geometry": mapping(geometry) if geometry else None,
            "properties": {
                "id": self.id,
                "name": self.name,
                "fiber_status": self.fiber_status.value,
                **self.properties
            }
        }
    
    @classmethod
    def from_geojson_feature(cls, feature: dict):
        """
        Create a Region instance from a GeoJSON feature.
        """
        if 'geometry' not in feature or 'properties' not in feature:
            raise ValueError("Invalid GeoJSON feature: missing 'geometry' or 'properties'")
            
        properties = feature['properties']
        if 'name' not in properties:
            raise ValueError("GeoJSON feature properties must contain a 'name' field")
            
        # Convert GeoJSON geometry dict to a shapely object, then to WKT with SRID
        geom = shape(feature['geometry'])
        wkt = f"SRID=4326;{geom.wkt}"
            
        return cls(
            name=properties['name'],
            geometry=wkt,
            fiber_status=properties.get('fiber_status', FiberStatus.UNAVAILABLE),
            properties={
                k: v for k, v in properties.items() 
                if k not in ['name', 'fiber_status']  # Exclude fields already mapped to columns
            }
        )
