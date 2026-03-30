import json
from typing import List
from app.core.models import GeometryGraphData, MaterialAnalysisOutput, ElementRecommendation, MaterialScore

# Hackathon Material Dataset
# Cost is represented as relative price per sq. meter.
# Strength is relative load-bearing capacity (MPa).
MATERIAL_DB = {
    "load-bearing": [
        {"name": "RCC (Reinforced Concrete)", "cost": 120, "strength": 40},
        {"name": "High-Strength Steel", "cost": 200, "strength": 250},
        {"name": "Red Brick (Solid)", "cost": 60, "strength": 10},
        {"name": "Fly Ash Bricks", "cost": 50, "strength": 12}
    ],
    "partition": [
        {"name": "AAC Blocks", "cost": 80, "strength": 4},
        {"name": "Drywall / Gypsum", "cost": 30, "strength": 1},
        {"name": "Hollow Concrete Blocks", "cost": 55, "strength": 5},
        {"name": "Glass Panel", "cost": 150, "strength": 2}
    ]
}

class MaterialAnalyzer:
    def __init__(self, structural_graph_json: str):
        # Parse the JSON from Module 2
        self.graph_data = GeometryGraphData.model_validate_json(structural_graph_json)
        
        # Adjustable weights for tradeoff formula
        self.weight_cost = 0.5
        self.weight_strength = 0.5

    def _calculate_score(self, material: dict, category: str) -> float:
        """
        Computes the tradeoff score.
        Formula: (weight_strength * normalized_strength) + (weight_cost * normalized_cost_efficiency)
        """
        # Get max values for normalization to keep scores between 0 and 1
        max_strength = max([m["strength"] for m in MATERIAL_DB[category]])
        max_cost = max([m["cost"] for m in MATERIAL_DB[category]])
        
        normalized_strength = material["strength"] / max_strength
        # For cost, lower is better, so we invert the normalization
        cost_efficiency = 1.0 - (material["cost"] / max_cost)
        
        # Hackathon Note: Prevent cost_efficiency from being literally 0 for the most expensive item
        cost_efficiency = max(cost_efficiency, 0.1) 
        
        score = (self.weight_cost * cost_efficiency) + (self.weight_strength * normalized_strength)
        return round(score * 100, 2) # Return as a percentage score out of 100

    def analyze(self) -> str:
        """Processes each wall element and assigns material recommendations."""
        recommendations_list: List[ElementRecommendation] = []
        
        # Iterate through the walls/edges defined in the structural graph
        for edge in self.graph_data.edges:
            wall_type = self.graph_data.wall_types.get(edge.wall_id, "partition")
            
            # Fetch the valid materials for this wall type
            available_materials = MATERIAL_DB.get(wall_type, MATERIAL_DB["partition"])
            
            scored_materials = []
            for mat in available_materials:
                score = self._calculate_score(mat, wall_type)
                scored_materials.append(MaterialScore(material=mat["name"], score=score))
            
            # Sort by highest score first
            scored_materials.sort(key=lambda x: x.score, reverse=True)
            
            recommendations_list.append(ElementRecommendation(
                element=edge.wall_id,
                recommended_materials=scored_materials
            ))

        output = MaterialAnalysisOutput(recommendations=recommendations_list)
        return output.model_dump_json(indent=2)