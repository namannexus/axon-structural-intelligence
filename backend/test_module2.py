import json
import os
from app.geometry.reconstruction import GeometryReconstructor

def run_module_2():
    print("🚀 Initializing Geometry Reconstructor...")
    
    # Ensure Module 1 output exists
    if not os.path.exists("parsed_layout.json"):
        print("❌ Error: parsed_layout.json not found. Run Module 1 first!")
        return

    # Load data from Module 1
    with open("parsed_layout.json", "r") as f:
        parsed_data = f.read()
        
    reconstructor = GeometryReconstructor(parsed_data)
    
    print("⚙️ Processing graph (Node snapping, Edge generation, Classification)...")
    json_result = reconstructor.reconstruct()
    
    print("✅ Reconstruction Complete! Graph Data:")
    # Print preview (first 500 chars to avoid flooding terminal)
    print(json_result[:500] + "\n... [Output Truncated] ...\n")
    
    # Save to file to pass to Module 3
    with open("structural_graph.json", "w") as f:
        f.write(json_result)
    print("💾 Saved graph output to 'structural_graph.json'")

if __name__ == "__main__":
    run_module_2()