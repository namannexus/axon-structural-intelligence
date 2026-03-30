import cv2
import numpy as np
import uuid
import math
from app.core.models import FloorPlanData, Wall, Room, Opening, Coordinate

class FloorPlanParser:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.original_img = cv2.imread(image_path)
        if self.original_img is None:
            raise FileNotFoundError(f"Could not load image at {image_path}")
        
        self.gray_img = None
        self.binary_img = None
        self.walls_data = []
        self.rooms_data = []
        self.openings_data = []

    def preprocess(self):
        """Grayscale, adaptive thresholding, and noise removal."""
        # Convert to grayscale
        self.gray_img = cv2.cvtColor(self.original_img, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian Blur to reduce noise
        blurred = cv2.GaussianBlur(self.gray_img, (5, 5), 0)
        
        # Adaptive thresholding to handle varying lighting/scans
        self.binary_img = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Morphological operations to close small gaps in broken walls
        kernel = np.ones((3, 3), np.uint8)
        self.binary_img = cv2.morphologyEx(self.binary_img, cv2.MORPH_CLOSE, kernel, iterations=2)

    def extract_walls(self):
        """Detects walls using Probabilistic Hough Transform and Contours."""
        # Use Probabilistic Hough Transform to find line segments
        lines = cv2.HoughLinesP(
            self.binary_img, 
            rho=1, 
            theta=np.pi/180, 
            threshold=50, 
            minLineLength=30, 
            maxLineGap=10  # Bridges slight coordinate misalignments
        )
        
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                length = math.hypot(x2 - x1, y2 - y1)
                
                # Filter out extremely small noise lines
                if length > 20:
                    self.walls_data.append(Wall(
                        id=f"wall_{uuid.uuid4().hex[:8]}",
                        start=Coordinate(x=x1, y=y1),
                        end=Coordinate(x=x2, y=y2),
                        length=round(length, 2),
                        thickness=5.0 # Heuristic default, refined later in 3D module
                    ))

    def extract_rooms(self):
        """Detects closed contours (rooms) using background analysis."""
        # Dilate walls slightly to ensure rooms are fully enclosed
        kernel = np.ones((5, 5), np.uint8)
        dilated_walls = cv2.dilate(self.binary_img, kernel, iterations=2)
        
        # Invert to find empty spaces (rooms)
        rooms_mask = cv2.bitwise_not(dilated_walls)
        
        # Find contours of the empty spaces
        contours, _ = cv2.findContours(rooms_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # Filter out tiny artifacts and the massive outer boundary
            if 500 < area < (self.original_img.shape[0] * self.original_img.shape[1] * 0.9):
                # Approximate polygon to handle non-orthogonal layouts smoothly
                epsilon = 0.02 * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)
                
                # Calculate center
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                else:
                    cx, cy = 0, 0
                
                contour_coords = [Coordinate(x=pt[0][0], y=pt[0][1]) for pt in approx]
                
                self.rooms_data.append(Room(
                    id=f"room_{uuid.uuid4().hex[:8]}",
                    contour=contour_coords,
                    area=round(area, 2),
                    center=Coordinate(x=cx, y=cy)
                ))

    def extract_openings(self):
        """
        Detects doors/windows. 
        Note: True opening detection requires complex template matching or ML. 
        Here, we use a heuristic based on gaps between collinear wall segments.
        """
        # [Heuristic Logic] Detect bounding boxes of contours that aren't quite walls or rooms
        # For hackathon robustness, we simulate finding gaps in the wall contour map.
        contours, _ = cv2.findContours(self.binary_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w)/h if h != 0 else 0
            
            # Doors/Windows on a 2D plan are often small rectangles or arcs
            if 100 < w*h < 1000 and (aspect_ratio > 3 or aspect_ratio < 0.3):
                self.openings_data.append(Opening(
                    id=f"opening_{uuid.uuid4().hex[:8]}",
                    start=Coordinate(x=x, y=y),
                    end=Coordinate(x=x+w, y=y+h)
                ))

    def parse(self) -> str:
        """Executes the pipeline and returns structured JSON."""
        try:
            self.preprocess()
            self.extract_walls()
            self.extract_rooms()
            self.extract_openings()
            
            output = FloorPlanData(
                walls=self.walls_data,
                rooms=self.rooms_data,
                openings=self.openings_data
            )
            return output.model_dump_json(indent=2)
            
        except Exception as e:
            # High-priority error handling
            raise RuntimeError(f"Pipeline failed during image parsing: {str(e)}")