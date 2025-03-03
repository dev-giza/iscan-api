import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
OPENFOOD_API_URL = "https://world.openfoodfacts.org/api/v2/product/{barcode}.json"

async def get_product_from_openfood(barcode: str):
    url = OPENFOOD_API_URL.format(barcode=barcode)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            if "product" not in data:
                return None
            return data["product"]
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail="Network error occurred")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=404, detail="Product not found")


class Product(BaseModel):
    barcode: str
    brand: str
    category: str
    country: str
    creator: str
    image: str 
    image_ingredients: str  
    image_nutritions: str  
    ingredients: str

@app.get("/products/{barcode}")
async def read_product(barcode: str):
    openfood_data = await get_product_from_openfood(barcode)
    if openfood_data is None:
        raise HTTPException(status_code=404, detail="Product not found")

    product = Product(
        barcode=openfood_data.get("_id", "Unknown"),
        brand=openfood_data.get("brands", "Unknown"),
        category=openfood_data.get("categories", "Unknown"),
        country=openfood_data.get("countries", "Unknown"),
        creator=openfood_data.get("creator", "Unknown"),
        image=openfood_data.get("image_url", "Unknown"),
        image_ingredients=openfood_data.get("image_ingredients_url", "Unknown"),
        image_nutritions=openfood_data.get("image_nutrition_url", "Unknown"),
        ingredients=openfood_data.get("ingredients_text", "Unknown"),
    )

    return product


# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)