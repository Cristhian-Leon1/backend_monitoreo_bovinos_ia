"""
Resolver referencias circulares entre modelos Pydantic
"""

def resolve_model_references():
    """
    Resuelve las referencias hacia adelante en los modelos Pydantic
    Debe ser llamado después de que todos los modelos estén definidos
    """
    try:
        from app.models.finca import FincaWithBovinos
        from app.models.bovino import BovinoWithMediciones, BovinoResponse
        from app.models.medicion import MedicionResponse
        
        # Resolver referencias en FincaWithBovinos
        FincaWithBovinos.model_rebuild()
        
        # Resolver referencias en BovinoWithMediciones
        BovinoWithMediciones.model_rebuild()
        
        print("✅ Referencias de modelos resueltas correctamente")
        
    except Exception as e:
        print(f"⚠️ Error resolviendo referencias de modelos: {e}")
