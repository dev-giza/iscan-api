from fastapi import APIRouter, HTTPException
from models.product import Product
from models.product_analysis import ProductAnalysis
from models.product_response import ProductResponse
from services.openfood_service import OpenFoodService
from services.product_analysis_service import ProductAnalysisService

router = APIRouter()

@router.get("/{barcode}", response_model=ProductResponse, summary="Get product information and analysis")
async def read_product(barcode: str):
    """
    Retrieve product information and analysis by barcode from OpenFood database.
    
    Args:
        barcode (str): Product barcode
        
    Returns:
        ProductResponse: Product information and analysis
        
    Raises:
        HTTPException: If product is not found or API request fails
    """
    openfood_data = await OpenFoodService.get_product(barcode)
    product_data = openfood_data.get("product", {})
    
    product = Product(
        barcode=product_data.get("_id", ""),
        brand=product_data.get("brands", ""),
        category=product_data.get("categories", ""),
        country=product_data.get("countries", ""),
        creator=product_data.get("creator", ""),
        image=product_data.get("image_url", ""),
        image_ingredients=product_data.get("image_ingredients_url", ""),
        image_nutritions=product_data.get("image_nutrition_url", ""),
        ingredients=product_data.get("ingredients_text", ""),
    )
    
    analysis = ProductAnalysisService.analyze_product(openfood_data)
    
    return ProductResponse(product=product, analysis=analysis)