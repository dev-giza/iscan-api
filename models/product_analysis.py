from pydantic import BaseModel, Field
from typing import List, Optional

class ProductAnalysis(BaseModel):
    barcode: str = Field(..., description="Product barcode")
    name: str = Field(..., description="Product name")
    brand: str = Field(..., description="Product brand")
    
    # Health indicators
    nutri_score: str = Field(..., description="Nutri-Score grade (a to e)")
    nutri_score_points: int = Field(..., description="Nutri-Score points")
    nova_group: int = Field(..., description="NOVA classification (1-4)")
    
    # Nutritional values per 100g
    energy_kcal: float = Field(..., description="Energy in kcal per 100g")
    proteins: float = Field(..., description="Proteins per 100g")
    carbohydrates: float = Field(..., description="Carbohydrates per 100g")
    sugars: float = Field(..., description="Sugars per 100g")
    fat: float = Field(..., description="Fat per 100g")
    saturated_fat: float = Field(..., description="Saturated fat per 100g")
    salt: float = Field(..., description="Salt per 100g")
    
    # Health warnings
    allergens: List[str] = Field(default_factory=list, description="List of allergens")
    additives: List[str] = Field(default_factory=list, description="List of additives")
    
    # Environmental impact
    eco_score: str = Field(..., description="Eco-Score grade (a to e)")
    eco_score_points: int = Field(..., description="Eco-Score points")
    
    # Labels and certifications
    labels: List[str] = Field(default_factory=list, description="Product labels and certifications")
    
    # Product rating
    rating_score: int = Field(..., description="Overall product rating (0-100)")
    rating_description: str = Field(..., description="Detailed description of the product rating")
    rating_details: dict = Field(..., description="Detailed breakdown of the rating calculation")
    
    # Overall assessment
    health_rating: str = Field(..., description="Overall health rating (good, moderate, poor)")
    environmental_rating: str = Field(..., description="Overall environmental rating (good, moderate, poor)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "barcode": "3017620422003",
                "name": "Pure Premium Orange Juice",
                "brand": "Tropicana",
                "nutri_score": "c",
                "nutri_score_points": 5,
                "nova_group": 1,
                "energy_kcal": 45.8,
                "proteins": 0.833,
                "carbohydrates": 10.8,
                "sugars": 9.17,
                "fat": 0,
                "saturated_fat": 0,
                "salt": 0,
                "allergens": [],
                "additives": [],
                "eco_score": "d",
                "eco_score_points": 43,
                "labels": ["No GMOs", "Non GMO project"],
                "rating_score": 45,
                "rating_description": "Продукт получил среднюю оценку 45/100. Основные плюсы: минимальная обработка (NOVA 1), отсутствие добавок. Основные минусы: средний Nutri-Score (C) и низкий экологический рейтинг (D).",
                "rating_details": {
                    "nutri_score_points": 35,
                    "additives_bonus": 10,
                    "nova_bonus": 10,
                    "eco_penalty": -10
                },
                "health_rating": "moderate",
                "environmental_rating": "poor"
            }
        } 