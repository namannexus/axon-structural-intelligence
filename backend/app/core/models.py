from pydantic import BaseModel, Field
from typing import List, Tuple

class Coordinate(BaseModel):
    x: int
    y: int

class Wall(BaseModel):
    id: str
    start: Coordinate
    end: Coordinate
    thickness: float = Field(default=0.0, description="Estimated thickness of the wall")
    length: float = Field(default=0.0, description="Length in pixels")

class Room(BaseModel):
    id: str
    contour: List[Coordinate] = Field(description="List of coordinates forming the room polygon")
    area: float = Field(description="Area in square pixels")
    center: Coordinate

class Opening(BaseModel):
    id: str
    start: Coordinate
    end: Coordinate
    type: str = Field(default="door/window", description="Type of opening")

class FloorPlanData(BaseModel):
    walls: List[Wall]
    rooms: List[Room]
    openings: List[Opening]
    
# ... (Keep existing Module 1 models)

class GraphNode(BaseModel):
    id: str
    x: float
    y: float

class GraphEdge(BaseModel):
    id: str
    source: str      # Node ID
    target: str      # Node ID
    wall_id: str
    length: float

class GeometryGraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    wall_types: dict # e.g., {"wall_1": "load-bearing", "wall_2": "partition"}
    
# ... (Keep existing Module 1 and 2 models)

class MaterialScore(BaseModel):
    material: str
    score: float

class ElementRecommendation(BaseModel):
    element: str # e.g., wall_id
    recommended_materials: List[MaterialScore]

class MaterialAnalysisOutput(BaseModel):
    recommendations: List[ElementRecommendation]
    
# ... (Keep existing models)

class ExplanationReport(BaseModel):
    summary: str
    material_reasoning: str
    structural_risks: str