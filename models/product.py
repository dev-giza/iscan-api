from pydantic import BaseModel, Field

class Product(BaseModel):
    barcode: str = Field(..., description="Product barcode")
    brand: str = Field(..., description="Product brand name")
    category: str = Field(..., description="Product category")
    country: str = Field(..., description="Product country of origin")
    creator: str = Field(..., description="Product creator")
    image: str = Field(..., description="URL to product image")
    image_ingredients: str = Field(..., description="URL to product ingredients image")
    image_nutritions: str = Field(..., description="URL to product nutrition facts image")
    ingredients: str = Field(..., description="Product ingredients list")

    class Config:
        json_schema_extra = {
            "example": {
                "barcode": "3017620422003",
                "brand": "Nutella",
                "category": "Spreads",
                "country": "France",
                "creator": "openfoodfacts-contributors",
                "image": "https://static.openfoodfacts.org/images/products/301/762/042/2003/front_en.50.400.jpg",
                "image_ingredients": "https://static.openfoodfacts.org/images/products/301/762/042/2003/ingredients_en.400.jpg",
                "image_nutritions": "https://static.openfoodfacts.org/images/products/301/762/042/2003/nutrition_en.400.jpg",
                "ingredients": "Sugar, Palm Oil, Hazelnuts (13%), Skimmed Milk Powder (8.7%), Fat-Reduced Cocoa (7.4%), Emulsifier: Lecithins (Soya), Vanillin"
            }
        } 