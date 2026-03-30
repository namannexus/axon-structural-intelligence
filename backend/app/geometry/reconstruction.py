import uuid
import networkx as nx
import numpy as np
from scipy.spatial import cKDTree
from typing import List, Dict, Tuple
from app.core.models import FloorPlanData, GeometryGraphData, GraphNode, GraphEdge

class GeometryReconstructor:
    def __init__(self, parsed_data: str):
        self.raw_data = FloorPlanData.model_validate_json(parsed_data)
        self.graph = nx.Graph()
        self.nodes_data: List[GraphNode] = []
        self.edges_data: List[GraphEdge] = []
        self.wall_types: Dict[str, str] = {}
        
        # Tolerance in pixels for snapping endpoints together (handles CV inaccuracies)
        self.SNAP_TOLERANCE = 15.0 

    def _get_distance(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def build_nodes_and_edges(self):
        """
        Extracts endpoints, merges nearby points into single junction nodes, 
        and creates graph edges.
        """
        points = []
        point_to_wall = []

        # 1. Collect all endpoints
        for wall in self.raw_data.walls:
            points.append((wall.start.x, wall.start.y))
            point_to_wall.append((wall.id, 'start'))
            points.append((wall.end.x, wall.end.y))
            point_to_wall.append((wall.id, 'end'))

        if not points:
            return

        # 2. Use cKDTree for fast spatial clustering (resolves L-corners & broken gaps)
        tree = cKDTree(points)
        processed_indices = set()
        node_mapping = {} # maps original point index to new Node ID

        for i, pt in enumerate(points):
            if i in processed_indices:
                continue
            
            # Find all points within snapping tolerance
            neighbors = tree.query_ball_point(pt, self.SNAP_TOLERANCE)
            
            # Calculate centroid of merged points to create a stable junction
            cluster_points = [points[n] for n in neighbors]
            centroid_x = sum(p[0] for p in cluster_points) / len(cluster_points)
            centroid_y = sum(p[1] for p in cluster_points) / len(cluster_points)
            
            node_id = f"node_{uuid.uuid4().hex[:8]}"
            self.nodes_data.append(GraphNode(id=node_id, x=centroid_x, y=centroid_y))
            self.graph.add_node(node_id, pos=(centroid_x, centroid_y))
            
            for n in neighbors:
                processed_indices.add(n)
                node_mapping[n] = node_id

        # 3. Build Edges
        wall_node_map = {} # wall_id -> {start: node_id, end: node_id}
        for idx, (wall_id, pos_type) in enumerate(point_to_wall):
            if wall_id not in wall_node_map:
                wall_node_map[wall_id] = {}
            wall_node_map[wall_id][pos_type] = node_mapping[idx]

        for wall in self.raw_data.walls:
            source_node = wall_node_map[wall.id]['start']
            target_node = wall_node_map[wall.id]['end']
            
            # Prevent zero-length self-loops caused by very short noise walls
            if source_node != target_node:
                edge_id = f"edge_{uuid.uuid4().hex[:8]}"
                self.edges_data.append(GraphEdge(
                    id=edge_id,
                    source=source_node,
                    target=target_node,
                    wall_id=wall.id,
                    length=wall.length
                ))
                self.graph.add_edge(source_node, target_node, id=edge_id, wall_id=wall.id, weight=wall.length)

    def classify_walls(self):
        """
        Classifies walls based on geometric heuristics.
        [DUMMY LOGIC MARKER]: In a real scenario, this requires BIM data or structural ML.
        Heuristic used: Longest connected components and exterior perimeters are likely load-bearing.
        """
        if not self.graph.edges:
            return

        # Calculate average wall length to use as a threshold
        lengths = [e.length for e in self.edges_data]
        avg_length = sum(lengths) / len(lengths)

        for edge in self.edges_data:
            # Simple Hackathon Heuristic: 
            # If a wall is significantly longer than average, assume Load-Bearing.
            # Otherwise, Partition.
            if edge.length > (avg_length * 1.2):
                self.wall_types[edge.wall_id] = "load-bearing"
            else:
                self.wall_types[edge.wall_id] = "partition"

    def reconstruct(self) -> str:
        """Executes the reconstruction pipeline."""
        try:
            self.build_nodes_and_edges()
            self.classify_walls()
            
            output = GeometryGraphData(
                nodes=self.nodes_data,
                edges=self.edges_data,
                wall_types=self.wall_types
            )
            return output.model_dump_json(indent=2)
            
        except Exception as e:
            raise RuntimeError(f"Geometry Reconstruction failed: {str(e)}")