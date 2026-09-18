from typing import Optional, List
from pydantic import BaseModel, Field

class SoilMetrics(BaseModel):
    ph: Optional[float] = Field(None, ge=0.0, le=14.0, description="Soil pH level")
    organic_carbon_pct: Optional[float] = Field(None, ge=0.0, le=20.0, description="Soil organic carbon percentage (SOC %)")
    moisture_pct: Optional[float] = Field(None, ge=0.0, le=100.0, description="Soil volumetric moisture percentage")
    soil_texture: Optional[str] = Field(None, description="e.g., Sandy Loam, Clay, Silt")

class ClimateMetrics(BaseModel):
    annual_rainfall_mm: Optional[float] = Field(None, ge=0.0, description="Annual precipitation in mm")
    mean_temperature_c: Optional[float] = Field(None, description="Mean temperature in Celsius")
    aridity_index: Optional[float] = Field(None, description="Precipitation / Potential Evapotranspiration")

class LandUseMetrics(BaseModel):
    land_cover_type: Optional[str] = Field(None, description="e.g., Monoculture cropland, Degraded pasture, Agroforestry")
    canopy_cover_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    fragmentation_index: Optional[float] = Field(None, ge=0.0, le=1.0, description="0 is contiguous, 1 is highly fragmented")

class SpatialContext(BaseModel):
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    region_name: Optional[str] = None
    biome: Optional[str] = None

class EcosystemQueryPayload(BaseModel):
    query_text: str = Field(..., description="User query or ecosystem problem description")
    soil: Optional[SoilMetrics] = Field(default_factory=SoilMetrics)
    climate: Optional[ClimateMetrics] = Field(default_factory=ClimateMetrics)
    land_use: Optional[LandUseMetrics] = Field(default_factory=LandUseMetrics)
    spatial: Optional[SpatialContext] = Field(default_factory=SpatialContext)
    thread_id: Optional[str] = Field("session_default", description="Conversation thread session identifier")
