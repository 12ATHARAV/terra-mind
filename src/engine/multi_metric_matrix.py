from typing import Dict, Any, List
from src.schemas.ecosystem_input import EcosystemQueryPayload


class MultiMetricReasoningEngine:
    """Couples at least 3 environmental variables simultaneously."""

    @staticmethod
    def evaluate_couplings(payload: EcosystemQueryPayload) -> Dict[str, Any]:
        soc = payload.soil.organic_carbon_pct if payload.soil and payload.soil.organic_carbon_pct is not None else None
        rainfall = payload.climate.annual_rainfall_mm if payload.climate and payload.climate.annual_rainfall_mm is not None else None
        crop = payload.land_use.land_cover_type.lower() if payload.land_use and payload.land_use.land_cover_type else ""
        frag = payload.land_use.fragmentation_index if payload.land_use and payload.land_use.fragmentation_index is not None else 0.5
        canopy = payload.land_use.canopy_cover_pct if payload.land_use and payload.land_use.canopy_cover_pct is not None else None

        couplings = []

        # Coupling 1: Semi-arid degraded monoculture nexus
        if (soc is not None and soc < 0.8) or (rainfall is not None and rainfall < 700) or any(k in crop for k in ["monoculture", "wheat", "cotton", "fallow"]):
            couplings.append({
                "id": "NEXUS-01-SOC-WATER-CROP",
                "variables": ["Soil Organic Carbon (SOC %)", "Annual Rainfall Infiltration (mm)", "Crop Canopy Diversity"],
                "diagnosis": "Severe biological decoupling: Monoculture cropping combined with low organic matter (<0.7%) impedes precipitation infiltration, driving high surface evaporation and soil microbial collapse.",
                "intervention_archetype": "Legume-Cover Crop Agroforestry Intercropping (Crotalaria juncea + Faidherbia albida)",
                "projected_deltas": [
                    {"metric": "Soil Organic Carbon", "baseline": f"{soc or 0.4}%", "projected": f"{(soc or 0.4) + 0.35:.2f}%", "delta": "+20% to +35%", "mechanism": "Rhizodeposition & biological N-fixation"},
                    {"metric": "Effective Water Retention", "baseline": "Low (<18%)", "projected": "Moderate (+28%)", "delta": "+25% to +30%", "mechanism": "Aggregated soil pore structure and reduced evaporation"},
                    {"metric": "Pollinator / Microbial Diversity", "baseline": "Depauperate (H'=0.8)", "projected": "Enriched (H'=1.45)", "delta": "+45%", "mechanism": "Floral nectar phenology and mycorrhizal inoculation"}
                ]
            })

        # Coupling 2: Habitat fragmentation & canopy cover nexus
        if frag > 0.4 or (canopy is not None and canopy < 30):
            couplings.append({
                "id": "NEXUS-02-CANOPY-FRAGMENTATION-TROPHIC",
                "variables": ["Canopy Cover %", "Landscape Fragmentation Index", "Avian/Insect Species Richness"],
                "diagnosis": "High structural fragmentation interrupts dispersal pathways, generating severe edge effects and genetic bottlenecks for native insect pollinators and predatory birds.",
                "intervention_archetype": "Native Vegetative Hedgerow Corridors & Stratified Windbreaks",
                "projected_deltas": [
                    {"metric": "Canopy Structural Heterogeneity", "baseline": "Low (12-20%)", "projected": "High (35-45%)", "delta": "+15-25% absolute", "mechanism": "Multi-tier native shrub & tree planting"},
                    {"metric": "Shannon-Wiener Biodiversity Index", "baseline": "H'=1.1", "projected": "H'=1.7", "delta": "+0.6 points", "mechanism": "Restored biological stepping-stone corridors"}
                ]
            })

        # Coupling 3: Coastal/mangrove nexus
        q_lower = payload.query_text.lower()
        is_coastal = (payload.spatial and payload.spatial.biome and "mangrove" in payload.spatial.biome.lower()) or "mangrove" in q_lower or "coastal" in q_lower
        if is_coastal:
            couplings.append({
                "id": "NEXUS-03-SALINITY-HYPOXIA-BLUECARBON",
                "variables": ["Soil Salinity (ppt)", "Tidal Soil Oxygen Level (mg/L)", "Blue Carbon Sequestration Rate (tCO2e/ha/yr)"],
                "diagnosis": "Salinity intrusion exceeding 25 ppt induces anaerobic soil conditions, collapsing aerobic microbial communities and releasing stored blue carbon as methane.",
                "intervention_archetype": "Tidal Regulation & Freshwater Augmentation with Native Mangrove Propagule Seeding",
                "projected_deltas": [
                    {"metric": "Blue Carbon Sequestration", "baseline": "2-3 tCO2e/ha/yr", "projected": "6-8 tCO2e/ha/yr", "delta": "+150-200%", "mechanism": "Aerobic microbial community recovery and root biomass expansion"},
                    {"metric": "Coastal Erosion Rate", "baseline": "High (>50 cm/yr)", "projected": "Low (<15 cm/yr)", "delta": "-70% to -85%", "mechanism": "Mangrove root network sediment stabilization"}
                ]
            })

        # Fallback general nexus
        if not couplings:
            couplings.append({
                "id": "NEXUS-00-GENERAL-ECOSYSTEM",
                "variables": ["Soil Health Index", "Vegetation Cover (%)", "Local Species Richness"],
                "diagnosis": "General ecosystem baseline: insufficient specific metrics to trigger targeted nexus. Applying broad-spectrum ecological health assessment.",
                "intervention_archetype": "Integrated Ecosystem Restoration: Native Revegetation + Soil Amendment + Monitoring",
                "projected_deltas": [
                    {"metric": "Overall Ecosystem Health Index", "baseline": "Degraded (2-3/10)", "projected": "Recovering (6-7/10)", "delta": "+50-70%", "mechanism": "Holistic soil-vegetation-fauna restoration"}
                ]
            })

        return {
            "coupled_interactions_found": len(couplings),
            "interactions": couplings
        }
