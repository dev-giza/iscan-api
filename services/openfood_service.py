import httpx
from fastapi import HTTPException
from config import get_settings

settings = get_settings()

class OpenFoodService:
    @staticmethod
    async def get_product(barcode: str) -> dict:
        """
        Fetch product information from OpenFood API
        
        Args:
            barcode (str): Product barcode
            
        Returns:
            dict: Product information
            
        Raises:
            HTTPException: If product is not found or API request fails
        """
        url = settings.OPENFOOD_API_URL.format(barcode=barcode)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") != 1:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Product with barcode {barcode} not found"
                    )
                
                return data
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Network error occurred: {str(e)}"
                )
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"OpenFood API error: {str(e)}"
                ) 