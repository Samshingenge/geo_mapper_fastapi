from typing import List,Dict, Any, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum
from shapely import wkb
from shapely.geometry import mapping


class GeoJSONGeometry(BaseModel):
    type: str
    coordinates: Any

class GeoJSONProperties(BaseModel):
    id: int
    name: str
    fiber_status: str
    area_km2: Optional[float] = None
    population: Optional[int] = None

class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    id: int  # Required field at root level
    name: str  # Required field at root level
    geometry: GeoJSONGeometry
    properties: Dict[str, Any]  # Allow any additional properties
    
    class Config:
        from_attributes = True
        extra = "ignore"
        json_encoders = {
            # Add any custom JSON encoders if needed
        }

class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List['GeoJSONFeature']
    
    class Config:
        from_attributes = True

class FiberStatus(str, Enum):
    ACTIVE = "Active"
    PLANNED = "Planned"
    UNAVAILABLE = "Unavailable"

# Shared properties
class RegionBase(BaseModel):
    name: str = Field(..., description="Name of the region")
    fiber_status: FiberStatus = Field(default=FiberStatus.UNAVAILABLE, description="Fiber coverage status")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Additional properties of the region")

# Properties to receive on region creation
class RegionCreate(RegionBase):
    geometry: Dict[str, Any] = Field(..., description="GeoJSON geometry object")

# Properties to receive on region update
class RegionUpdate(RegionBase):
    name: Optional[str] = None
    fiber_status: Optional[FiberStatus] = None
    geometry: Optional[Dict[str, Any]] = None
    properties: Optional[Dict[str, Any]] = None

# Properties shared by models stored in DB
class RegionInDBBase(RegionBase):
    id: int
    
    class Config:
        from_attributes = True

# Properties to return to client
class Region(RegionInDBBase):
    pass

# Properties stored in DB
class RegionInDB(RegionInDBBase):
    pass

# Response model for region with GeoJSON
class RegionOut(RegionInDBBase):
    geometry: Dict[str, Any] = Field(..., description="GeoJSON geometry object")
    
    class Config:
        from_attributes = True
        json_encoders = {
            "geometry": lambda v: mapping(to_shape(v)) if v else None
        }
        
    @validator('geometry', pre=True)
    def convert_wkb_to_geojson(cls, v):
        if v and hasattr(v, 'desc'):  # If it's a WKB element
            return mapping(to_shape(v))
        return v

# Response model for coverage check
class CoverageResponse(BaseModel):
    region: str
    status: str
    details: Dict[str, Any] = {}
    
    class Config:
        from_attributes = True
