from pydantic import BaseModel
from models.product import Product
from models.product_analysis import ProductAnalysis

class ProductResponse(BaseModel):
    product: Product
    analysis: ProductAnalysis

    class Config:
        json_schema_extra = {
            "example": {
                "product": {
                    "barcode": "3017620422003",
                    "brand": "Tropicana",
                    "category": "Fruit juices",
                    "country": "United States",
                    "creator": "openfoodfacts-contributors",
                    "image": "https://static.openfoodfacts.org/images/products/301/762/042/2003/front_en.50.400.jpg",
                    "image_ingredients": "https://static.openfoodfacts.org/images/products/301/762/042/2003/ingredients_en.400.jpg",
                    "image_nutritions": "https://static.openfoodfacts.org/images/products/301/762/042/2003/nutrition_en.400.jpg",
                    "ingredients": "orange juice"
                },
                "analysis": {
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
                    "health_rating": "moderate",
                    "environmental_rating": "poor"
                }
            }
        } 