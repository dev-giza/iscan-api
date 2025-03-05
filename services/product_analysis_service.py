from typing import List, Dict, Tuple
from models.product_analysis import ProductAnalysis

class ProductAnalysisService:
    @staticmethod
    def analyze_product(product_data: dict) -> ProductAnalysis:
        """
        Analyze product data and determine health and environmental ratings
        
        Args:
            product_data (dict): Raw product data from OpenFood API
            
        Returns:
            ProductAnalysis: Analyzed product data with ratings
        """
        # Extract basic information
        product = product_data.get("product", {})
        
        # Extract nutritional values
        nutriments = product.get("nutriments", {})
        
        # Determine health rating based on Nutri-Score and NOVA
        nutri_score = product.get("nutriscore_grade", "e").lower()
        nutri_score_points = product.get("nutriscore_score", 0)
        nova_group = int(product.get("nova_group", 4))
        
        # Determine health rating
        health_rating = ProductAnalysisService._determine_health_rating(
            nutri_score, nutri_score_points, nova_group
        )
        
        # Determine environmental rating
        eco_score = product.get("ecoscore_grade", "e").lower()
        eco_score_points = product.get("ecoscore_score", 0)
        environmental_rating = ProductAnalysisService._determine_environmental_rating(
            eco_score, eco_score_points
        )
        
        # Extract allergens and additives
        allergens = [tag for tag in product.get("allergens_tags", [])]
        additives = [tag for tag in product.get("additives_tags", [])]
        
        # Extract labels
        labels = [tag.replace("en:", "") for tag in product.get("labels_tags", [])]
        
        # Calculate product rating
        rating_score, rating_details, rating_description = ProductAnalysisService._calculate_product_rating(
            nutri_score=nutri_score,
            additives=additives,
            nova_group=nova_group,
            eco_score=eco_score,
            product_name=product.get("product_name", "")
        )
        
        return ProductAnalysis(
            barcode=product.get("_id", ""),
            name=product.get("product_name", ""),
            brand=product.get("brands", ""),
            nutri_score=nutri_score,
            nutri_score_points=nutri_score_points,
            nova_group=nova_group,
            energy_kcal=nutriments.get("energy-kcal_100g", 0),
            proteins=nutriments.get("proteins_100g", 0),
            carbohydrates=nutriments.get("carbohydrates_100g", 0),
            sugars=nutriments.get("sugars_100g", 0),
            fat=nutriments.get("fat_100g", 0),
            saturated_fat=nutriments.get("saturated-fat_100g", 0),
            salt=nutriments.get("salt_100g", 0),
            allergens=allergens,
            additives=additives,
            eco_score=eco_score,
            eco_score_points=eco_score_points,
            labels=labels,
            rating_score=rating_score,
            rating_description=rating_description,
            rating_details=rating_details,
            health_rating=health_rating,
            environmental_rating=environmental_rating
        )
    
    @staticmethod
    def _calculate_product_rating(
        nutri_score: str,
        additives: List[str],
        nova_group: int,
        eco_score: str,
        product_name: str
    ) -> Tuple[int, Dict, str]:
        """
        Calculate product rating based on various factors
        
        Returns:
            Tuple[int, Dict, str]: (total_score, score_details, description)
        """
        # 1. Nutri-Score points (0-60)
        nutri_weights = {
            "a": 60,
            "b": 45,
            "c": 35,
            "d": 20,
            "e": 10
        }
        nutri_points = nutri_weights.get(nutri_score.lower(), 0)
        
        # 2. Additives bonus (+10 if no additives)
        additives_bonus = 10 if not additives else 0
        
        # 3. NOVA bonus (0-10)
        nova_bonus = {
            1: 10,  # Unprocessed
            2: 5,   # Processed ingredients
            3: 0,   # Processed foods
            4: -10  # Ultra-processed
        }.get(nova_group, 0)
        
        # 4. Eco-Score penalty (-10 to 0)
        eco_penalty = {
            "a": 0,
            "b": -5,
            "c": -7,
            "d": -10,
            "e": -15
        }.get(eco_score.lower(), -10)
        
        # Calculate total score
        total_score = max(0, min(100, 
            nutri_points + 
            additives_bonus + 
            nova_bonus + 
            eco_penalty
        ))
        
        # Prepare detailed breakdown
        details = {
            "nutri_score_points": nutri_points,
            "additives_bonus": additives_bonus,
            "nova_bonus": nova_bonus,
            "eco_penalty": eco_penalty
        }
        
        # Generate description
        description = ProductAnalysisService._generate_rating_description(
            product_name=product_name,
            total_score=total_score,
            nutri_score=nutri_score,
            additives=additives,
            nova_group=nova_group,
            eco_score=eco_score
        )
        
        return total_score, details, description
    
    @staticmethod
    def _generate_rating_description(
        product_name: str,
        total_score: int,
        nutri_score: str,
        additives: List[str],
        nova_group: int,
        eco_score: str
    ) -> str:
        """Generate a human-readable description of the product rating"""
        # Determine rating level
        if total_score >= 70:
            rating_level = "высокую"
        elif total_score >= 40:
            rating_level = "среднюю"
        else:
            rating_level = "низкую"
        
        # Build description
        description = f"Продукт '{product_name}' получил {rating_level} оценку {total_score}/100.\n"
        
        # Add pros
        pros = []
        if nutri_score in ["a", "b"]:
            pros.append(f"хороший Nutri-Score ({nutri_score.upper()})")
        if not additives:
            pros.append("отсутствие добавок")
        if nova_group == 1:
            pros.append("минимальная обработка (NOVA 1)")
        if eco_score in ["a", "b"]:
            pros.append(f"хороший экологический рейтинг ({eco_score.upper()})")
        
        if pros:
            description += f"Основные плюсы: {', '.join(pros)}.\n"
        
        # Add cons
        cons = []
        if nutri_score in ["d", "e"]:
            cons.append(f"низкий Nutri-Score ({nutri_score.upper()})")
        if additives:
            cons.append(f"наличие добавок ({len(additives)} шт.)")
        if nova_group == 4:
            cons.append("высокая степень обработки (NOVA 4)")
        if eco_score in ["d", "e"]:
            cons.append(f"низкий экологический рейтинг ({eco_score.upper()})")
        
        if cons:
            description += f"Основные минусы: {', '.join(cons)}."
        
        return description
    
    @staticmethod
    def _determine_health_rating(nutri_score: str, nutri_points: int, nova_group: int) -> str:
        """Determine overall health rating based on Nutri-Score and NOVA classification"""
        # Nutri-Score weights
        nutri_weights = {
            "a": 3,
            "b": 2,
            "c": 1,
            "d": 0,
            "e": -1
        }
        
        # NOVA weights (lower is better)
        nova_weights = {
            1: 2,  # Unprocessed or minimally processed foods
            2: 1,  # Processed culinary ingredients
            3: 0,  # Processed foods
            4: -1  # Ultra-processed foods
        }
        
        # Calculate weighted score
        score = nutri_weights.get(nutri_score, 0) + nova_weights.get(nova_group, 0)
        
        if score >= 4:
            return "good"
        elif score >= 1:
            return "moderate"
        else:
            return "poor"
    
    @staticmethod
    def _determine_environmental_rating(eco_score: str, eco_points: int) -> str:
        """Determine environmental rating based on Eco-Score"""
        # Eco-Score weights
        eco_weights = {
            "a": 3,
            "b": 2,
            "c": 1,
            "d": 0,
            "e": -1
        }
        
        score = eco_weights.get(eco_score, 0)
        
        if score >= 2:
            return "good"
        elif score >= 0:
            return "moderate"
        else:
            return "poor" 