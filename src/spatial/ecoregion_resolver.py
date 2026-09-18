from typing import Dict, Any

def resolve_spatial_profile(lat: float, lon: float) -> Dict[str, Any]:
    profile = {
        "latitude": lat,
        "longitude": lon,
        "koppen_climate": "BSh (Hot Semi-Arid)",
        "ecoregion": "Deccan Dry Deciduous Forests / Scrub",
        "baseline_precipitation_mm": 550.0,
        "vulnerability": "High Drought & Soil Organic Carbon Depletion"
    }
    if 21.0 <= lat <= 22.8 and 88.0 <= lon <= 90.5:
        profile["koppen_climate"] = "Aw (Tropical Wet & Dry)"
        profile["ecoregion"] = "Sundarbans Mangroves & Coastal Wetland"
        profile["baseline_precipitation_mm"] = 1800.0
        profile["vulnerability"] = "Salinity Intrusion, Tidal Soil Hypoxia, Blue Carbon Degradation"
    elif 8.0 <= lat <= 16.0 and 73.0 <= lon <= 77.5:
        profile["koppen_climate"] = "Am (Tropical Monsoon)"
        profile["ecoregion"] = "Western Ghats Montane Rain Forests"
        profile["baseline_precipitation_mm"] = 2800.0
        profile["vulnerability"] = "Canopy Fragmentation, Soil Runoff, Native Endemism Loss"
    elif 24.0 <= lat <= 30.0 and 70.0 <= lon <= 76.0:
        profile["koppen_climate"] = "BWh (Hot Desert / Semi-Arid)"
        profile["ecoregion"] = "Thar Desert / Indus Valley Desert"
        profile["baseline_precipitation_mm"] = 250.0
        profile["vulnerability"] = "Extreme Desertification, Severe Wind Erosion, Wind-driven Topsoil Loss"
    elif 24.0 <= lat <= 28.0 and 89.0 <= lon <= 97.0:
        profile["koppen_climate"] = "Cwa (Humid Subtropical Monsoon)"
        profile["ecoregion"] = "Brahmaputra Valley Semi-Evergreen Forests"
        profile["baseline_precipitation_mm"] = 2200.0
        profile["vulnerability"] = "Flood Erosion, Riparian Habitat Loss, Seasonal Waterlogging"
    return profile
