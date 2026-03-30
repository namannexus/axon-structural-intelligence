from app.vision.floorplan_parser import FloorPlanParser
import json

def run_module_1(test_image_path: str):
    print("🚀 Initializing Floor Plan Parser...")
    parser = FloorPlanParser(test_image_path)
    
    print("⚙️ Processing image (Preprocessing, Walls, Rooms, Openings)...")
    json_result = parser.parse()
    
    print("✅ Parsing Complete! Output Data:")
    print(json_result)
    
    # Save to file to pass to Module 2
    with open("parsed_layout.json", "w") as f:
        f.write(json_result)
    print("💾 Saved output to 'parsed_layout.json'")

if __name__ == "__main__":
    # Make sure 'sample_floorplan.jpg' is in your backend folder
    run_module_1("floor_plan_A_Prompt_A_Thon.jpg")