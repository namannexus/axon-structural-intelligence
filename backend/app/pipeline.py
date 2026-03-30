import os
import json
from app.vision.floorplan_parser import FloorPlanParser
from app.geometry.reconstruction import GeometryReconstructor
from app.materials.analyzer import MaterialAnalyzer
from app.explainability.llm_engine import ExplainabilityEngine

class StructuralIntelligencePipeline:
    def __init__(self, upload_dir: str = "temp_uploads"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    def execute(self, image_path: str):
        # 1. Parse Image (Module 1)
        parser = FloorPlanParser(image_path)
        parsed_json = parser.parse()
        
        # 2. Reconstruct Geometry (Module 2)
        reconstructor = GeometryReconstructor(parsed_json)
        graph_json = reconstructor.reconstruct()
        
        # Save temp files for the analyzer and LLM
        graph_path = os.path.join(self.upload_dir, "graph.json")
        with open(graph_path, "w") as f:
            f.write(graph_json)
            
        # 3. Material Analysis (Module 4)
        analyzer = MaterialAnalyzer(graph_json)
        materials_json = analyzer.analyze()
        
        materials_path = os.path.join(self.upload_dir, "materials.json")
        with open(materials_path, "w") as f:
            f.write(materials_json)
            
        # 4. AI Explanation (Module 5)
        # Note: We pass the paths we just saved
        llm_engine = ExplainabilityEngine(graph_path, materials_path)
        explanation_json = llm_engine.generate_explanation()
        
        # Return everything as a unified Python dictionary
        return {
            "graph": json.loads(graph_json),
            "materials": json.loads(materials_json),
            "explanation": json.loads(explanation_json)
        }